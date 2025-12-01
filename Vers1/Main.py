import json
import psycopg
import logging
import os
import Db_works  # Модули
import Import
import Report
from config import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME, SCHEMA, DATA_DIR

def load_stud_json(dir: DATA_DIR, file_name):
    with open(dir+file_name, encoding="utf-8") as f:
        data = json.load(f)
    return

def load_rooms_json(dir: DATA_DIR, file_name):
    with open(dir+file_name, encoding="utf-8") as f:
        data = json.load(f)
    return [
        {"students_id": int(r["id"]),  "name": r["name"], "birthday": r["birthday"], "sex": r["sex"], "room_id": int(r["room"])}
     for r in data ]

def main():
    rooms = load_json("Data/rooms.json")
    students = load_json("Data/students.json")
    print(students[1])

    loader = Import.Loader()
    loader.import_files()
    loader.import_files()

    db_conn = Db_works.PostgresConnection(DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME)

    data_base = Db_works.Database(db_conn, SCHEMA)
    data_base.create_schem()



if __name__ == "__main__":
    main()

