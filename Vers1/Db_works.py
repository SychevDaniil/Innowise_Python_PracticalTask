from config import SCHEMA
import psycopg
import logging

class PostgresConnection :
    def __init__(self, host, port, user, password, db):
        self.conn = psycopg.connect(host=host, port=port, user=user, password=password, dbname=db)

    def execute(self, sql, params=None, many=False):
        with self.conn.cursor() as cur:
            cur.execute(sql, params or ())
        return True

    def executemany(self, sql, rows):
        with self.conn.cursor() as cur:
            cur.executemany(sql, rows)

    def query(self, sql, params=None):
        with self.conn.cursor() as cur:
            cur.execute(sql, params or ())
            cols = [d.name for d in cur.description]
            return [dict(zip(cols, r)) for r in cur.fetchall()]

    def commit(self): self.conn.commit()

class Database :
    def __init__(self, db_connection: PostgresConnection, schem_name = SCHEMA):
        self.schem_name = schem_name
        self.conn = db_connection

    def create_schem(self):
        try:
            self.conn.execute(f"""CREATE SCHEMA IF NOT EXISTS {self.schem_name};""")
            logging.info(f'Схема {self.schem_name} создана успешно')
            self.conn.commit()
        except Exception as e:
            logging.warning(f'Ошибка при создании {self.schem_name}: {e}')
            return None

    def create_stud_table(self):
        try:
            self.conn.execute(f"""CREATE TABLE IF NOT EXISTS {self.schem_name}.students (
            students_id SERIAL PRIMARY KEY,
            name VARCHAR(50),
            birthday DATE,
            sex CHAR,
            room_id INT,
            CONSTRAINT fk_room
            FOREIGN KEY (room_id)
            REFERENCES {self.schem_name}.rooms(rooms_id)
            ON DELETE SET NULL );
            """)
            self.conn.commit()
        except Exception as e:
            logging.warning(f'Ошибка при создании {self.schem_name}: {e}')
            return None

    def create_rooms_table(self):
        try:
            self.conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.schem_name}.rooms (
            rooms_id SERIAL PRIMARY KEY,
            name VARCHAR(50)    );
            """)
            self.conn.commit()
        except Exception as e:
            logging.warning(f'Ошибка при создании {self.schem_name}: {e}')
            return None

    def insert_stud_table(self, students):
        try:
            sql = f"""
                INSERT INTO {self.schem_name}.students (students_id, name, sex, birthday, room_id)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (students_id) DO NOTHING;
            """
            rows = [
                (s["id"], s["name"], s["sex"], s["birthday"], s["room"])
                for s in students
            ]
            self.conn.executemany(sql, rows)
            self.conn.commit()
        except Exception as e:
            logging.warning(f'Ошибка при создании {self.schem_name}: {e}')
            return None
    def insert_rooms_table(self, rooms):
        try:
            sql = f"""
                INSERT INTO {self.schem_name}.rooms (rooms_id, name)
                VALUES (%s, %s)
                ON CONFLICT (rooms_id) DO NOTHING;
            """
            rows = [
                (room["id"], room["name"])
                for room in rooms
            ]
            self.conn.executemany(sql, rows)
            self.conn.commit()
        except Exception as e:
            logging.warning(f'Ошибка при создании {self.schem_name}: {e}')
            return None

    def select_queries(self, sel_query):
        try:
            return self.conn.query(sel_query)
        except Exception as e:
            logging.warning(f'Ошибка при выполнении {self.schem_name}: {e}')
            return None

    def create_stud_index(self, students):
         try:
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_students_id ON students(students_id);")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_students_room ON students(room_id);")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_students_birth ON students(birthday);")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_students_sex ON students(sex);")
            self.conn.commit()
         except Exception as e:
            logging.warning(f'Ошибка при создании индексов в Students: {e}')
            return None

    def create_rooms_index(self):
        try:
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_rooms_id ON rooms(rooms_id);")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_rooms_name ON rooms(name);")
            self.conn.commit()
        except Exception as e:
            logging.warning(f'Ошибка при создании индексов в Rooms: {e}')
            return None