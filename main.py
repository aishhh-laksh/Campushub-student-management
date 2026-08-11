import customtkinter as ctk
from tkinter import messagebox

from database import (
    add_student,
    get_students,
    search_student,
    update_student,
    delete_student,
    get_statistics
)


# =========================================================
# ADD STUDENT
# =========================================================

def add_student_window(parent):

    window = ctk.CTkToplevel(parent)
    window.title("Add Student")
    window.geometry("500x620")
    window.resizable(False, False)

    title = ctk.CTkLabel(
        window,
        text="Add New Student",
        font=("Arial", 28, "bold")
    )
    title.pack(pady=(30, 25))

    name_entry = ctk.CTkEntry(
        window, width=320, height=42,
        placeholder_text="Student Name"
    )
    name_entry.pack(pady=8)

    roll_entry = ctk.CTkEntry(
        window, width=320, height=42,
        placeholder_text="Roll Number"
    )
    roll_entry.pack(pady=8)

    course_entry = ctk.CTkEntry(
        window, width=320, height=42,
        placeholder_text="Course"
    )
    course_entry.pack(pady=8)

    marks_entry = ctk.CTkEntry(
        window, width=320, height=42,
        placeholder_text="Marks (0 - 100)"
    )
    marks_entry.pack(pady=8)

    attendance_entry = ctk.CTkEntry(
        window, width=320, height=42,
        placeholder_text="Attendance % (0 - 100)"
    )
    attendance_entry.pack(pady=8)

    message = ctk.CTkLabel(window, text="")
    message.pack(pady=10)

    def save_student():

        name = name_entry.get().strip()
        roll = roll_entry.get().strip()
        course = course_entry.get().strip()

        if not name or not roll or not course:
            message.configure(
                text="Please fill all required fields.",
                text_color="red"
            )
            return

        try:
            marks = float(marks_entry.get() or 0)
            attendance = float(attendance_entry.get() or 0)

            if not 0 <= marks <= 100:
                raise ValueError

            if not 0 <= attendance <= 100:
                raise ValueError

        except ValueError:
            message.configure(
                text="Marks and attendance must be 0-100.",
                text_color="red"
            )
            return

        success = add_student(
            name,
            roll,
            course,
            marks,
            attendance
        )

        if success:

            message.configure(
                text="Student added successfully!",
                text_color="green"
            )

            for entry in (
                name_entry,
                roll_entry,
                course_entry,
                marks_entry,
                attendance_entry
            ):
                entry.delete(0, "end")

        else:

            message.configure(
                text="Roll number already exists.",
                text_color="red"
            )

    ctk.CTkButton(
        window,
        text="Save Student",
        width=320,
        height=45,
        command=save_student
    ).pack(pady=10)


# =========================================================
# VIEW / SEARCH STUDENTS
# =========================================================

def view_students_window(parent):

    window = ctk.CTkToplevel(parent)
    window.title("Student Records")
    window.geometry("1050x650")
    window.resizable(False, False)

    title = ctk.CTkLabel(
        window,
        text="Student Records",
        font=("Arial", 28, "bold")
    )
    title.pack(pady=(25, 15))

    search_frame = ctk.CTkFrame(window)
    search_frame.pack(pady=10)

    search_entry = ctk.CTkEntry(
        search_frame,
        width=400,
        height=40,
        placeholder_text="Search name or roll number"
    )
    search_entry.grid(row=0, column=0, padx=10, pady=10)

    table_frame = ctk.CTkScrollableFrame(
        window,
        width=950,
        height=470
    )
    table_frame.pack(padx=20, pady=10)

    def display_students(students):

        for widget in table_frame.winfo_children():
            widget.destroy()

        if not students:

            ctk.CTkLabel(
                table_frame,
                text="No students found.",
                font=("Arial", 18)
            ).pack(pady=30)

            return

        headers = [
            "ID",
            "Name",
            "Roll Number",
            "Course",
            "Marks",
            "Attendance"
        ]

        for column, header in enumerate(headers):

            ctk.CTkLabel(
                table_frame,
                text=header,
                font=("Arial", 14, "bold"),
                width=140
            ).grid(
                row=0,
                column=column,
                padx=5,
                pady=8
            )

        for row, student in enumerate(students, start=1):

            for column, value in enumerate(student):

                ctk.CTkLabel(
                    table_frame,
                    text=str(value),
                    width=140
                ).grid(
                    row=row,
                    column=column,
                    padx=5,
                    pady=5
                )

    def perform_search():

        text = search_entry.get().strip()

        if text:
            students = search_student(text)
        else:
            students = get_students()

        display_students(students)

    ctk.CTkButton(
        search_frame,
        text="Search",
        width=120,
        height=40,
        command=perform_search
    ).grid(row=0, column=1, padx=10)

    display_students(get_students())


# =========================================================
# UPDATE STUDENT
# =========================================================

def edit_student_window(parent):

    window = ctk.CTkToplevel(parent)
    window.title("Update Student")
    window.geometry("500x650")
    window.resizable(False, False)

    ctk.CTkLabel(
        window,
        text="Update Student",
        font=("Arial", 28, "bold")
    ).pack(pady=(25, 20))

    id_entry = ctk.CTkEntry(
        window, width=320, height=40,
        placeholder_text="Student ID"
    )
    id_entry.pack(pady=7)

    name_entry = ctk.CTkEntry(
        window, width=320, height=40,
        placeholder_text="Student Name"
    )
    name_entry.pack(pady=7)

    roll_entry = ctk.CTkEntry(
        window, width=320, height=40,
        placeholder_text="Roll Number"
    )
    roll_entry.pack(pady=7)

    course_entry = ctk.CTkEntry(
        window, width=320, height=40,
        placeholder_text="Course"
    )
    course_entry.pack(pady=7)

    marks_entry = ctk.CTkEntry(
        window, width=320, height=40,
        placeholder_text="Marks"
    )
    marks_entry.pack(pady=7)

    attendance_entry = ctk.CTkEntry(
        window, width=320, height=40,
        placeholder_text="Attendance"
    )
    attendance_entry.pack(pady=7)

    message = ctk.CTkLabel(window, text="")
    message.pack(pady=8)

    def save_changes():

        try:
            student_id = int(id_entry.get())
        except ValueError:
            message.configure(
                text="Enter a valid Student ID.",
                text_color="red"
            )
            return

        name = name_entry.get().strip()
        roll = roll_entry.get().strip()
        course = course_entry.get().strip()

        if not name or not roll or not course:
            message.configure(
                text="Please fill all required fields.",
                text_color="red"
            )
            return

        try:
            marks = float(marks_entry.get() or 0)
            attendance = float(attendance_entry.get() or 0)

            if not 0 <= marks <= 100:
                raise ValueError

            if not 0 <= attendance <= 100:
                raise ValueError

        except ValueError:
            message.configure(
                text="Marks and attendance must be 0-100.",
                text_color="red"
            )
            return

        success = update_student(
            student_id,
            name,
            roll,
            course,
            marks,
            attendance
        )

        if success:
            message.configure(
                text="Student updated successfully!",
                text_color="green"
            )
        else:
            message.configure(
                text="Update failed. Check the roll number.",
                text_color="red"
            )

    ctk.CTkButton(
        window,
        text="Update Student",
        width=320,
        height=45,
        command=save_changes
    ).pack(pady=10)


# =========================================================
# DELETE STUDENT
# =========================================================

def delete_student_window(parent):

    window = ctk.CTkToplevel(parent)
    window.title("Delete Student")
    window.geometry("420x300")
    window.resizable(False, False)

    ctk.CTkLabel(
        window,
        text="Delete Student",
        font=("Arial", 26, "bold")
    ).pack(pady=35)

    id_entry = ctk.CTkEntry(
        window,
        width=280,
        height=40,
        placeholder_text="Student ID"
    )
    id_entry.pack(pady=15)

    message = ctk.CTkLabel(window, text="")
    message.pack(pady=5)

    def remove_student():

        try:
            student_id = int(id_entry.get())
        except ValueError:
            message.configure(
                text="Enter a valid Student ID.",
                text_color="red"
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this student?"
        )

        if confirm:

            delete_student(student_id)

            message.configure(
                text="Student deleted successfully.",
                text_color="green"
            )

            id_entry.delete(0, "end")

    ctk.CTkButton(
        window,
        text="Delete Student",
        width=280,
        height=45,
        command=remove_student
    ).pack(pady=10)


# =========================================================
# STUDENT MANAGEMENT
# =========================================================

def student_management(parent):

    window = ctk.CTkToplevel(parent)
    window.title("Student Management")
    window.geometry("900x600")
    window.resizable(False, False)

    ctk.CTkLabel(
        window,
        text="Student Management",
        font=("Arial", 30, "bold")
    ).pack(pady=(45, 30))

    buttons = [
        ("Add Student", lambda: add_student_window(window)),
        ("View / Search Students", lambda: view_students_window(window)),
        ("Update Student", lambda: edit_student_window(window)),
        ("Delete Student", lambda: delete_student_window(window))
    ]

    for text, command in buttons:

        ctk.CTkButton(
            window,
            text=text,
            width=320,
            height=48,
            command=command
        ).pack(pady=9)


# =========================================================
# DASHBOARD
# =========================================================

def open_dashboard():

    app.withdraw()

    dashboard = ctk.CTkToplevel(app)
    dashboard.title("CampusHub Dashboard")
    dashboard.geometry("1050x700")
    dashboard.resizable(False, False)

    # Sidebar

    sidebar = ctk.CTkFrame(
        dashboard,
        width=230,
        corner_radius=0
    )
    sidebar.pack(
        side="left",
        fill="y"
    )
    sidebar.pack_propagate(False)

    ctk.CTkLabel(
        sidebar,
        text="CampusHub",
        font=("Arial", 26, "bold")
    ).pack(pady=(45, 10))

    ctk.CTkLabel(
        sidebar,
        text="Student Management",
        font=("Arial", 13)
    ).pack(pady=(0, 40))

    ctk.CTkButton(
        sidebar,
        text="Student Management",
        width=190,
        height=45,
        command=lambda: student_management(dashboard)
    ).pack(pady=10)

    ctk.CTkButton(
        sidebar,
        text="Refresh Dashboard",
        width=190,
        height=45,
        command=lambda: refresh_dashboard(
            total_label,
            marks_label,
            attendance_label
        )
    ).pack(pady=10)

    ctk.CTkButton(
        sidebar,
        text="Logout",
        width=190,
        height=45,
        command=lambda: logout(dashboard)
    ).pack(side="bottom", pady=35)

    # Main area

    content = ctk.CTkFrame(
        dashboard,
        corner_radius=0
    )
    content.pack(
        side="right",
        fill="both",
        expand=True
    )

    ctk.CTkLabel(
        content,
        text="Dashboard",
        font=("Arial", 34, "bold")
    ).pack(
        anchor="w",
        padx=45,
        pady=(45, 5)
    )

    ctk.CTkLabel(
        content,
        text="Overview of your student records",
        font=("Arial", 16)
    ).pack(
        anchor="w",
        padx=45,
        pady=(0, 35)
    )

    total_students, average_marks, average_attendance = get_statistics()

    cards = ctk.CTkFrame(content)
    cards.pack(pady=10)

    total_card = ctk.CTkFrame(
        cards,
        width=210,
        height=140
    )
    total_card.grid(row=0, column=0, padx=10)
    total_card.pack_propagate(False)

    total_label = ctk.CTkLabel(
        total_card,
        text=f"{total_students}\n\nTotal Students",
        font=("Arial", 18, "bold")
    )
    total_label.pack(expand=True)

    marks_card = ctk.CTkFrame(
        cards,
        width=210,
        height=140
    )
    marks_card.grid(row=0, column=1, padx=10)
    marks_card.pack_propagate(False)

    marks_label = ctk.CTkLabel(
        marks_card,
        text=f"{average_marks:.1f}\n\nAverage Marks",
        font=("Arial", 18, "bold")
    )
    marks_label.pack(expand=True)

    attendance_card = ctk.CTkFrame(
        cards,
        width=210,
        height=140
    )
    attendance_card.grid(row=0, column=2, padx=10)
    attendance_card.pack_propagate(False)

    attendance_label = ctk.CTkLabel(
        attendance_card,
        text=f"{average_attendance:.1f}%\n\nAvg. Attendance",
        font=("Arial", 18, "bold")
    )
    attendance_label.pack(expand=True)

    ctk.CTkLabel(
        content,
        text="Manage your student records efficiently.",
        font=("Arial", 18)
    ).pack(pady=(45, 10))

    ctk.CTkButton(
        content,
        text="Open Student Management",
        width=330,
        height=50,
        command=lambda: student_management(dashboard)
    ).pack(pady=10)


# =========================================================
# REFRESH
# =========================================================

def refresh_dashboard(total_label, marks_label, attendance_label):

    total, marks, attendance = get_statistics()

    total_label.configure(
        text=f"{total}\n\nTotal Students"
    )

    marks_label.configure(
        text=f"{marks:.1f}\n\nAverage Marks"
    )

    attendance_label.configure(
        text=f"{attendance:.1f}%\n\nAvg. Attendance"
    )


# =========================================================
# LOGOUT
# =========================================================

def logout(dashboard):

    dashboard.destroy()
    app.deiconify()


# =========================================================
# LOGIN
# =========================================================

def login():

    username = username_entry.get().strip()
    password = password_entry.get()

    if username == "admin" and password == "1234":

        message.configure(
            text="Login successful!",
            text_color="green"
        )

        app.after(500, open_dashboard)

    else:

        message.configure(
            text="Invalid username or password",
            text_color="red"
        )


# =========================================================
# MAIN APPLICATION
# =========================================================

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

app.title("CampusHub")
app.geometry("900x600")
app.resizable(False, False)

ctk.CTkLabel(
    app,
    text="CampusHub",
    font=("Arial", 38, "bold")
).pack(pady=(90, 10))

ctk.CTkLabel(
    app,
    text="Student Management System",
    font=("Arial", 18)
).pack(pady=(0, 35))

username_entry = ctk.CTkEntry(
    app,
    width=320,
    height=45,
    placeholder_text="Username"
)
username_entry.pack(pady=10)

password_entry = ctk.CTkEntry(
    app,
    width=320,
    height=45,
    placeholder_text="Password",
    show="*"
)
password_entry.pack(pady=10)

ctk.CTkButton(
    app,
    text="Login",
    width=320,
    height=45,
    command=login
).pack(pady=25)

message = ctk.CTkLabel(
    app,
    text="",
    font=("Arial", 14)
)
message.pack()

app.mainloop()