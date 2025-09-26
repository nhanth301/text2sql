# from src.vectordb.service import search
from src.db.service import query

def main():
    results = query("select * from customer limit 5;")
    print(results)

if __name__ == '__main__':
    main()


