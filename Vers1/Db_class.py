import psycopg

class PostgresConnection():
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

class Database():
    def __init__(self, db_connection: PostgresConnection):
        self.conn = db_connection

    def create_schem(self):
        self.conn.execute("""CREATE SCHEMA IF NOT EXISTS Inowise;""")
        self.conn.commit()

    def create_stud_table(self):
        self.conn.execute("""CREATE TABLE IF NOT EXISTS Inowise.students (
        students_id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        birthday DATE,
        sex CHAR,
        room_id INT,
        CONSTRAINT fk_room
        FOREIGN KEY (room_id)
        REFERENCES Inowise.rooms(rooms_id)
        ON DELETE SET NULL );
        """)
        self.conn.commit()

    def create_rooms_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS Inowise.rooms (
        rooms_id SERIAL PRIMARY KEY,
        name VARCHAR(50)    );
        """)
        self.conn.commit()

    def insert_stud_table(self, students):
        sql = """
            INSERT INTO Inowise.students (students_id, name, sex, birthday, room_id)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (students_id) DO NOTHING;
        """
        rows = [
            (s["id"], s["name"], s["sex"], s["birthday"], s["room"])
            for s in students
        ]
        self.conn.executemany(sql, rows)
        self.conn.commit()

    def insert_rooms_table(self, rooms):
        sql = """
            INSERT INTO Inowise.rooms (rooms_id, name)
            VALUES (%s, %s)
            ON CONFLICT (rooms_id) DO NOTHING;
        """
        rows = [
            (room["id"], room["name"])
            for room in rooms
        ]
        self.conn.executemany(sql, rows)
        self.conn.commit()

    def select_queries(self, sel_query):
        return self.conn.query(sel_query)

    def create_stud_index(self):
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_students_room ON students(room_id);")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_students_birth ON students(birthday);")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_students_sex ON students(sex);")
        self.conn.commit()

    def create_rooms_index(self):
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_rooms_id ON rooms(rooms_id);")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_rooms_name ON rooms(name);")
        self.conn.commit()