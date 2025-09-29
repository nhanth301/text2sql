from qdrant_client.http import models
from src.vectordb.client import client
from src.config import config
from src.embedding.model import model
from src.schema.output_schema import SQLTableSchema


def create_collection():
    try:
        client.recreate_collection(
            collection_name= config.qdrant_collection,
            vectors_config={
                config.dense_vector_name: models.VectorParams(size=1024, distance=models.Distance.COSINE)
            },
            sparse_vectors_config={
                config.sparse_vector_name: models.SparseVectorParams()
            }
        )
    except Exception as e:
        print(e)


def search(query: str, limit: int = 5, 
           prefetch_limit: int = 10) -> list[dict[str]]:
    
    query_output = model.encode(
        [query],
        return_dense=True,
        return_sparse=True
    )
    
    query_dense_vec = query_output['dense_vecs'][0].tolist()
    
    sparse_data_dict = query_output['lexical_weights'][0]
    indices = [int(k) for k in sparse_data_dict.keys()]
    values = [float(v) for v in sparse_data_dict.values()]
    
    query_sparse_vec = models.SparseVector(
        indices=indices,
        values=values
    )

    search_result = client.query_points(
        collection_name=config.qdrant_collection,
        
        query=models.FusionQuery(
            fusion=models.Fusion.RRF
        ),
        
        prefetch=[
            models.Prefetch(
                query=query_dense_vec, 
                using=config.dense_vector_name,
                limit=prefetch_limit
            ),
            models.Prefetch(
                query=query_sparse_vec, 
                using=config.sparse_vector_name,
                limit=prefetch_limit 
            )
        ],
        limit=limit,
        with_payload=True
    )

    results = []
    for point in search_result.points:
        results.append({
            "id": point.id,
            "score": point.score,
            "payload": point.payload
        })
    return results

def se_search(tables: SQLTableSchema, k: int = 2) -> list[dict[str]]:
    result = {}
    for table in tables.create_statements:
        search_results = search(table, limit=k, prefetch_limit=5)
        for search_result in search_results:
            payload = search_result['payload']
            if payload['table'] not in result:
                result[payload['table']] = search_result
    return list(result.values())

if __name__ == "__main__":
    results = se_search(SQLTableSchema(create_statements=["CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, first_name VARCHAR(255), last_name VARCHAR(255), email VARCHAR(255), address_id INTEGER"]))
    for s in results:
        print(s)
    