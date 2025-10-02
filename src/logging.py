from rich.logging import RichHandler
import logging
import os

os.makedirs("src/logs/", exist_ok=True)

file_handler = logging.FileHandler("src/logs/app.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s"))

console_handler = RichHandler(rich_tracebacks=True, markup=True)
console_handler.setLevel(logging.DEBUG)

logger = logging.getLogger("sql_agent")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False
