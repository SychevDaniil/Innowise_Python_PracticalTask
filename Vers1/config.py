from pathlib import Path
import logging
DB_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "AsSQLol",
    "host": "localhost",
    "port": "5432"
}

SCHEMA = "Inowise"
OUTPUT_DIR = Path("Reports")

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")