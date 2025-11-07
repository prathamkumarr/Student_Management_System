import pymysql

def create_result_tables():
    con = pymysql.connect(host="localhost", user="root", password="", database="school_db")
    cur = con.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS exam_schedule (
        exam_id INT PRIMARY KEY AUTO_INCREMENT,
        exam_name VARCHAR(100),
        class_id INT,
        subject_id INT,
        exam_date DATE
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS exam_results (
        result_id INT PRIMARY KEY AUTO_INCREMENT,
        student_id INT,
        exam_id INT,
        subject_id INT,
        marks_obtained FLOAT,
        total_marks FLOAT,
        grade VARCHAR(5)
    )
    """)

    con.commit()
    con.close()

create_result_tables()