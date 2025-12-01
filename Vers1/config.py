from pathlib import Path
import logging

DB_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "AsSQLol",
    "host": "localhost",
    "port": "5432"
}
SCHEMA = "Innowise"
OUTPUT_DIR = Path("Reports")

Select_count_romms = f"""SELECT r.name, COUNT(s.room_id) AS student_count
            FROM {SCHEMA}.rooms r
            LEFT JOIN {SCHEMA}.students s ON r.rooms_id = s.room_id
            GROUP BY r.name
            ORDER BY student_count DESC;"""
Select_low_5ages = f"""select rooms.name , round(avg(EXTRACT(year from age(current_date, birthday)))) avg_age from inowise.rooms
            inner join {SCHEMA}.students
            on rooms.rooms_id = students.room_id 
            group by rooms.name
            order by avg_age ASC
            limit 5 """
Select_higt_betwen_ages = f"""select rooms.name , MAX(round(EXTRACT(year from age(current_date, birthday))))-MIN(round(EXTRACT(year from age(current_date, birthday)))) max_age
            from {SCHEMA}.rooms
            inner join {SCHEMA}.students
            on rooms.rooms_id = students.room_id 
            group by rooms.name
            order by max_age DESC
            limit 5"""
Select_genders = f"""SELECT r.rooms_id, r.name
            FROM {SCHEMA}.rooms r
            JOIN {SCHEMA}.students s ON s.room_id = r.rooms_id
            GROUP BY r.rooms_id, r.name
            HAVING COUNT(DISTINCT s.sex) > 1"""

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")