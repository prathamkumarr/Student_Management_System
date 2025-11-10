import pymysql
from tkinter import messagebox


def connect_db():
    """
    Connect to the MySQL database using PyMySQL.
    Returns a connection object.
    """
    try:
        con = pymysql.connect(
            host="localhost",            # your MySQL server
            user="admin",                # your MySQL username
            password="admin",            # your MySQL password
            database="student_management",  # your database name
            cursorclass=pymysql.cursors.DictCursor,  # fetch results as dictionaries
            autocommit=False             # manual commits for safety
        )
        return con
    except pymysql.MySQLError as e:
        messagebox.showerror("Database Error", f"Error connecting to MySQL:\n{e}")
        return None


def test_connection():
    """
    Quick test to verify if database connection works.
    Run this file directly once to confirm settings.
    """
    con = connect_db()
    if con:
        try:
            cur = con.cursor()
            cur.execute("SELECT DATABASE();")
            db = cur.fetchone()
            messagebox.showinfo("Connection Successful", f"Connected to database: {db['DATABASE()']}")
        except Exception as e:
            messagebox.showerror("Error", f"Test query failed:\n{e}")
        finally:
            con.close()
    else:
        messagebox.showerror("Error", "Database connection failed!")


if __name__ == "__main__":
    test_connection()
