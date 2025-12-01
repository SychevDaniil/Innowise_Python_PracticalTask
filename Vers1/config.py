from pathlib import Path
import logging
import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "AsSQLol")
DB_NAME = os.getenv("DB_NAME", "postgres")

SCHEMA = "Innowise"
DATA_DIR = Path("Data")
OUTPUT_DIR = Path("Reports")

QUERIES = {
    "Select_count_rooms": f"""
        SELECT r.name, COUNT(s.room_id) AS student_count
        FROM {SCHEMA}.rooms r
        LEFT JOIN {SCHEMA}.students s ON r.rooms_id = s.room_id
        GROUP BY r.name
        ORDER BY student_count DESC;
    """,
    "Select_low_5ages": f"""
        SELECT r.name, ROUND(AVG(EXTRACT(YEAR FROM age(current_date, s.birthday)))) AS avg_age
        FROM {SCHEMA}.rooms r
        INNER JOIN {SCHEMA}.students s ON r.rooms_id = s.room_id
        GROUP BY r.name
        ORDER BY avg_age ASC
        LIMIT 5;
    """,
    "Select_high_between_ages": f"""
        SELECT r.name,
               MAX(ROUND(EXTRACT(YEAR FROM age(current_date, s.birthday))))
               - MIN(ROUND(EXTRACT(YEAR FROM age(current_date, s.birthday)))) AS age_range
        FROM {SCHEMA}.rooms r
        INNER JOIN {SCHEMA}.students s ON r.rooms_id = s.room_id
        GROUP BY r.name
        ORDER BY age_range DESC
        LIMIT 5;
    """,
    "Select_genders": f"""
        SELECT r.rooms_id, r.name
        FROM {SCHEMA}.rooms r
        JOIN {SCHEMA}.students s ON s.room_id = r.rooms_id
        GROUP BY r.rooms_id, r.name
        HAVING COUNT(DISTINCT s.sex) > 1;
    """
}
logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
