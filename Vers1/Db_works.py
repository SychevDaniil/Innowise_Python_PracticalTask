import psycopg

Select_count_romms = """SELECT r.name, COUNT(s.room_id) AS student_count
            FROM inowise.rooms r
            LEFT JOIN inowise.students s ON r.rooms_id = s.room_id
            GROUP BY r.name
            ORDER BY student_count DESC;"""
Select_low_5ages = """select rooms.name , round(avg(EXTRACT(year from age(current_date, birthday)))) avg_age from inowise.rooms
            inner join inowise.students
            on rooms.rooms_id = students.room_id 
            group by rooms.name
            order by avg_age ASC
            limit 5 """
Select_higt_betwen_ages = """select rooms.name , MAX(round(EXTRACT(year from age(current_date, birthday))))-MIN(round(EXTRACT(year from age(current_date, birthday)))) max_age
            from inowise.rooms
            inner join inowise.students
            on rooms.rooms_id = students.room_id 
            group by rooms.name
            order by max_age DESC
            limit 5"""
Select_genders = """SELECT r.rooms_id, r.name
            FROM inowise.rooms r
            JOIN inowise.students s ON s.room_id = r.rooms_id
            GROUP BY r.rooms_id, r.name
            HAVING COUNT(DISTINCT s.sex) > 1"""

def insert_rooms(conn, rooms):
    with conn.cursor() as cur:
        for room in rooms:
            cur.execute("""
                INSERT INTO Inowise.rooms (rooms_id, name)
                VALUES (%s, %s)
                ON CONFLICT (rooms_id) DO NOTHING;
            """, (room["id"], room["name"]))
    conn.commit()

def insert_students(conn, students):
    with conn.cursor() as cur:
        for student in students:
            cur.execute("""
                INSERT INTO Inowise.students (students_id, name, sex, birthday, room_id)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (students_id) DO NOTHING;
            """, (
                student["id"],
                student["name"],
                student["sex"],
                student["birthday"],
                student["room"]
            ))
    conn.commit()

def Select_queries_json(conn , sel_query ):
        with conn.cursor() as cur:
            cur.execute(sel_query)
            rows = cur.fetchall()
            description = cur.description
        return {"rows": rows, "description": description}


def Select_queries(conn, sel_query):
    with conn.cursor() as cur:
        cur.execute(sel_query)
        rows = cur.fetchall()
        description = cur.description
    return {"rows": rows, "description": description}