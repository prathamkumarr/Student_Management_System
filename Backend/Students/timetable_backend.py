from config import connect_db


# ---------- Add ----------
def add_timetable_record(class_id, day, subject, teacher_id, start_time, end_time):
    con = connect_db()
    cur = con.cursor()
    try:
        cur.execute("""
            INSERT INTO timetable (class_id, day, subject, teacher_id, start_time, end_time)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (class_id, day, subject, teacher_id, start_time, end_time))
        con.commit()
    finally:
        con.close()


# ---------- Update ----------
def update_timetable_record(timetable_id, class_id, day, subject, teacher_id, start_time, end_time):
    con = connect_db()
    cur = con.cursor()
    try:
        cur.execute("""
            UPDATE timetable
            SET class_id=%s, day=%s, subject=%s, teacher_id=%s, start_time=%s, end_time=%s
            WHERE timetable_id=%s
        """, (class_id, day, subject, teacher_id, start_time, end_time, timetable_id))
        con.commit()
    finally:
        con.close()


# ---------- Delete ----------
def delete_timetable_record(timetable_id):
    con = connect_db()
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM timetable WHERE timetable_id=%s", (timetable_id,))
        con.commit()
    finally:
        con.close()


# ---------- Fetch with filters ----------
def fetch_timetable_records(class_id=None, teacher_id=None, subject=None, day=None):
    con = connect_db()
    cur = con.cursor()
    try:
        query = """
            SELECT 
                t.timetable_id,
                c.class_name,
                t.day,
                t.subject,
                tr.name AS teacher,
                t.start_time,
                t.end_time
            FROM timetable t
            JOIN classes c ON t.class_id = c.class_id
            LEFT JOIN teachers tr ON t.teacher_id = tr.teacher_id
            WHERE 1=1
        """
        params = []

        if class_id:
            query += " AND t.class_id = %s"
            params.append(class_id)
        if teacher_id:
            query += " AND t.teacher_id = %s"
            params.append(teacher_id)
        if subject:
            query += " AND t.subject = %s"
            params.append(subject)
        if day:
            query += " AND t.day = %s"
            params.append(day)

        query += """
            ORDER BY 
                c.class_name,
                FIELD(t.day, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'),
                t.start_time
        """

        cur.execute(query, tuple(params))
        return cur.fetchall()

    finally:
        con.close()


# ---------- Dropdown Data ----------
def get_class_data():
    con = connect_db()
    cur = con.cursor()
    try:
        cur.execute("SELECT class_id, class_name FROM classes ORDER BY LENGTH(class_name), class_name")
        return cur.fetchall()
    finally:
        con.close()


def get_teacher_data():
    con = connect_db()
    cur = con.cursor()
    try:
        cur.execute("SELECT teacher_id, name, subject FROM teachers ORDER BY name")
        return cur.fetchall()
    finally:
        con.close()


def get_subject_data():
    con = connect_db()
    cur = con.cursor()
    try:
        cur.execute("SELECT DISTINCT subject FROM teachers WHERE subject IS NOT NULL AND subject <> ''")
        return [row["subject"] for row in cur.fetchall()]
    finally:
        con.close()
