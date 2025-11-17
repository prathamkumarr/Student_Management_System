import os
import shutil
from config import connect_db

UPLOAD_DIR = os.path.join(os.getcwd(), "Uploads", "Work")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ------------------ INSERT NEW RECORD ------------------
def add_work_record(class_id, subject, work_type, title, desc, due_date, teacher_id, file_path):
    dest_path = os.path.join(UPLOAD_DIR, os.path.basename(file_path))
    shutil.copy(file_path, dest_path)

    con = connect_db()
    cur = con.cursor()
    try:
        cur.execute("""
            INSERT INTO work_records (class_id, subject, type, title, description, due_date, teacher_id, file_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (class_id, subject, work_type, title, desc, due_date, teacher_id, dest_path))
        con.commit()
        return True
    except Exception as e:
        raise e
    finally:
        con.close()


# ------------------ UPDATE RECORD ------------------
def update_work_record(work_id, class_id, subject, work_type, title, desc, due_date, teacher_id, file_path):
    con = connect_db()
    cur = con.cursor()
    try:
        cur.execute("""
            UPDATE work_records
            SET class_id=%s, subject=%s, type=%s, title=%s, description=%s, due_date=%s, teacher_id=%s, file_path=%s
            WHERE work_id=%s
        """, (class_id, subject, work_type, title, desc, due_date, teacher_id, file_path, work_id))
        con.commit()
        return True
    except Exception as e:
        raise e
    finally:
        con.close()


# ------------------ DELETE RECORD ------------------
def delete_work_record(work_id):
    con = connect_db()
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM work_records WHERE work_id=%s", (work_id,))
        con.commit()
        return True
    except Exception as e:
        raise e
    finally:
        con.close()


# ------------------ FETCH RECORDS ------------------
def fetch_work_records():
    con = connect_db()
    cur = con.cursor()
    try:
        cur.execute("""
            SELECT w.work_id, c.class_name, w.type, w.subject, w.title, w.due_date,
                   t.name AS teacher, w.file_path, w.description
            FROM work_records w
            JOIN classes c ON w.class_id = c.class_id
            LEFT JOIN teachers t ON w.teacher_id = t.teacher_id
            ORDER BY w.due_date DESC
        """)
        return cur.fetchall()
    except Exception as e:
        raise e
    finally:
        con.close()


# ------------------ COMBOBOX DATA HELPERS ------------------
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
