import json
import psycopg
import logging
import os
import Db_works  # Модули
import Import
import Report
import config

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def main():
    rooms = load_json("Data/rooms.json")
    students = load_json("Data/students.json")

    loader = Import.Loader()
    loader.get_url()

    logging.info("✅ Данные успешно загружены в Report.")


if __name__ == "__main__":
    main()

