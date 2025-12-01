import json
import psycopg
import logging
import os
import Db_works  # Модули
import Import
import Report
from config import DATA_DIR, OUTPUT_DIR, DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME, SCHEMA, File_name_stud, File_name_rooms, QUERIES



def main():

    # загрузка json и парсинг
    loader = Import.Loader()
    """loader.import_files()
    loader.import_files()"""
    rooms = loader.load_rooms_json(DATA_DIR, File_name_rooms)
    students = loader.load_stud_json(DATA_DIR, File_name_stud)

    # загрузка соединения
    db_conn = Db_works.PostgresConnection(DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME)

    # Создание БД
    data_base = Db_works.Database(db_conn, SCHEMA)
    data_base.create_schem()
    data_base.create_stud_table()
    data_base.create_rooms_table()

    data_base.insert_stud_table(students)
    data_base.insert_rooms_table(rooms)

    sel1 = data_base.select_queries(QUERIES[1])

    rep = Report.Report()
    rep.export(sel1, "Report1", "xml")

if __name__ == "__main__":
    main()

