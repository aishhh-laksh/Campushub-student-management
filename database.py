import sqlite3


# -------------------------
# Database Connection
# -------------------------

def create_database():
    connection = sqlite3.connect("campushub.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_number TEXT UNIQUE NOT NULL,
            course TEXT NOT NULL,
            marks REAL DEFAULT 0,
            attendance REAL DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()


# -------------------------
# Add Student
# -------------------------

def add_student(name, roll_number, course, marks=0, attendance=0):
    connection = sqlite3.connect("campushub.db")
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO students
            (name, roll_number, course, marks, attendance)
            VALUES (?, ?, ?, ?, ?)
        """, (name, roll_number, course, marks, attendance))

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


# -------------------------
# Get All Students
# -------------------------

def get_students():
    connection = sqlite3.connect("campushub.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    connection.close()

    return students


# -------------------------
# Search Student
# -------------------------

def search_student(search_text):
    connection = sqlite3.connect("campushub.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM students
        WHERE name LIKE ?
        OR roll_number LIKE ?
    """, (f"%{search_text}%", f"%{search_text}%"))

    students = cursor.fetchall()

    connection.close()

    return students


# -------------------------
# Update Student
# -------------------------

def update_student(student_id, name, roll_number, course, marks, attendance):
    connection = sqlite3.connect("campushub.db")
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE students
            SET name = ?,
                roll_number = ?,
                course = ?,
                marks = ?,
                attendance = ?
            WHERE id = ?
        """, (
            name,
            roll_number,
            course,
            marks,
            attendance,
            student_id
        ))

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


# -------------------------
# Delete Student
# -------------------------

def delete_student(student_id):
    connection = sqlite3.connect("campushub.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    connection.commit()
    connection.close()


# -------------------------
# Dashboard Statistics
# -------------------------

def get_statistics():
    connection = sqlite3.connect("campushub.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(marks) FROM students")
    average_marks = cursor.fetchone()[0] or 0

    cursor.execute("SELECT AVG(attendance) FROM students")
    average_attendance = cursor.fetchone()[0] or 0

    connection.close()

    return total_students, average_marks, average_attendance


# -------------------------
# Create Database
# -------------------------

create_database()