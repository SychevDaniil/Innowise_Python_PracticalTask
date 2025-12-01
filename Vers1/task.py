import json
import psycopg
import logging
import os
import Db_works  # Модули
import Report
import config

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def main():
    rooms = load_json("Data/rooms.json")
    students = load_json("Data/students.json")

    with psycopg.connect(**config.DB_PARAMS) as conn:
         logging.info("Происходит загрузка данных...")
         Db_works.insert_rooms(conn, rooms)
         Db_works.insert_students(conn, students)
         logging.info("✅ Данные успешно загружены в базу.")

         logging.info("Создание репорта в json.")
         data = Db_works.Select_queries(conn, Db_works.Select_genders)
         Report.export_json(data, "Select_genders")
         logging.info("✅ Данные успешно загружены в Report.")

         logging.info("Создание репорта в xml.")
         data = Db_works.Select_queries(conn, Db_works.Select_low_5ages)
         Report.export_xml(data, "Select_low_5ages")
         logging.info("✅ Данные успешно загружены в Report.")

if __name__ == "__main__":
    main()

