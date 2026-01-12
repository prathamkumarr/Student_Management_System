import tkinter as tk
from tkinter import ttk, filedialog
from tkcalendar import Calendar
import datetime
import requests
import re
import os
import tempfile
from tkcalendar import Calendar
import datetime
from tkcalendar import DateEntry

import sys

# -----------------------------
# API Helper Functions
# -----------------------------

BASE_API_URL = "http://127.0.0.1:8000/admin"

def fetch_classes():
    try:
        res = requests.get(f"{BASE_API_URL}/classes", timeout=5)
        if res.status_code == 200:
            return res.json()
    except requests.RequestException as e:
        print("Error fetching classes:", e)
    return []


def fetch_teachers():
    try:
        res = requests.get(f"{BASE_API_URL}/teachers", timeout=5)
        if res.status_code == 200:
            return res.json()
    except requests.RequestException as e:
        print("Error fetching teachers:", e)
    return []


def fetch_subjects():
    try:
        res = requests.get(f"{BASE_API_URL}/subjects", timeout=5)
        if res.status_code == 200:
            return res.json()
    except requests.RequestException as e:
        print("Error fetching subjects:", e)
    return []


def fetch_students():
    try:
        res = requests.get(f"{BASE_API_URL}/students", timeout=5)
        if res.status_code == 200:
            return res.json()
    except requests.RequestException as e:
        print("Error fetching students:", e)
    return []




if len(sys.argv) > 1:
    try:
        TEACHER_ID = int(sys.argv[1])
    except:
        print("Invalid teacher id received!")
        sys.exit()
else:
    print("Teacher ID missing!")
    sys.exit()

# -----------------------------
# API Helper Functions
# -----------------------------

BASE_API_URL = "http://127.0.0.1:8000/admin"

def fetch_classes():
    try:
        res = requests.get(f"{BASE_API_URL}/classes", timeout=5)
        if res.status_code == 200:
            return res.json()
    except requests.RequestException as e:
        print("Error fetching classes:", e)
    return []


def fetch_subjects():
    try:
        res = requests.get(f"{BASE_API_URL}/subjects", timeout=5)
        if res.status_code == 200:
            return res.json()
    except requests.RequestException as e:
        print("Error fetching subjects:", e)
    return []


def fetch_exams():
    try:
        res = requests.get(f"{BASE_API_URL}/exams", timeout=5)
        if res.status_code == 200:
            return res.json()
    except requests.RequestException as e:
        print("Error fetching exams:", e)
    return []

# =============
class TeacherUI:
    def __init__(self, root, teacher_id):
        self.root = root

        # teacher Logged-In Details (Dummy OR Fetched From Login)
        self.teacher_id = teacher_id


        self.root.title(f"School ERP - Teacher Panel - ID {self.teacher_id}")
        self.root.geometry("1200x700")
        self.root.configure(bg="#ECF0F1")

        # ---- SIDEBAR ----
        self.sidebar = tk.Frame(self.root, bg="#1E2A38", width=260)
        self.sidebar.pack(side="left", fill="y")

        # ---- CONTENT AREA ----
        self.content = tk.Frame(self.root, bg="#ECF0F1")
        self.content.pack(side="right", expand=True, fill="both")

        self.build_sidebar()
        self.load_dashboard()

    
    # ===== BUTTON CREATOR =====
    def add_btn(self, text, cmd=None):
        btn = tk.Label(
            self.menu_wrapper,
            text=text,
            font=("Arial", 14, "bold"),
            bg="#000000",
            fg="white",
            padx=20,
            pady=12,
            anchor="w",
            width=30,
            cursor="hand2"
        )
        btn.pack(pady=5, fill="x")

        # Hover Effects
        btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

        # Click
        if cmd:
            btn.bind("<Button-1>", lambda e: cmd())

        return btn

    # ------ LOGOUT FUNCTION -------
    def logout(self):
        self.root.destroy()
        import subprocess, sys
        subprocess.Popen(
        [sys.executable, "-m", "Frontends.login.login_main"]
    )

    # ===== SIDEBAR BUILD =====
    def build_sidebar(self):

        # ---------- TITLE TOP ----------
        title = tk.Label(
            self.sidebar,
            text="TEACHER PANEL",
            bg="#1E2A38",
            fg="white",
            font=("Arial", 18, "bold")
        )
        title.pack(fill="x", pady=(20, 20))
        
        # ---------- WRAPPER PUSHES LOGOUT DOWN ----------
        self.menu_wrapper = tk.Frame(self.sidebar, bg="#1E2A38")
        self.menu_wrapper.pack(fill="both", expand=True)

        # Main Buttons
        att_btn = self.add_btn("Manage Attendances")
        self.build_attendance_dropdown(att_btn)

        result_btn = self.add_btn("View and Generate Results")
        self.build_result_dropdown(result_btn)
        tt_btn = self.add_btn("View Timetable", self.load_teacher_timetable)

        work_btn = self.add_btn("Manage Work")
        self.build_work_dropdown(work_btn)

        marks_btn = self.add_btn("Upload / View Marks")
        self.build_marks_dropdown(marks_btn)

        # ------- LOGOUT BUTTON -------
        self.logout_btn = tk.Label(
            self.sidebar,
            text="Logout",
            font=("Arial", 12, "bold"),
            bg="#8E44AD",
            fg="white",
            padx=10,
            pady=10,
            width=14,
            cursor="hand2",
        ) 
        self.logout_btn.pack(side="bottom", pady=(0, 30))

        self.logout_btn.bind("<Enter>", lambda e: self.logout_btn.config(bg="#732d91"))
        self.logout_btn.bind("<Leave>", lambda e: self.logout_btn.config(bg="#8E44AD"))
        self.logout_btn.bind("<Button-1>", lambda e: self.logout())
    
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()


    # ===== DROPDOWN MENUS =====
    # ===============================================
    def build_attendance_dropdown(self, parent_label):
        menu = tk.Menu(self.root, tearoff=0)
        student = tk.Menu(menu, tearoff=0)

        student.add_command(label="Mark Attendance", command=self.load_mark_student_attendance_screen)
        student.add_command(label="Mark Bulk Attendance", command=self.load_mark_bulk_attendance_screen)
        student.add_command(label="Filter by Date", command=self.load_filter_student_attendance_screen)
        student.add_command(label="Attendance Summary", command=self.load_attendance_summary_screen)
        student.add_command(label="Update Attendance", command=self.load_update_student_attendance_screen)
        student.add_command(label="Delete Attendance", command=self.load_delete_student_attendance_screen)
        menu.add_cascade(label="Student Attendance", menu=student)
        
        teacher = tk.Menu(menu, tearoff=0)
        teacher.add_command(label="Mark Self Attendance", command=self.load_mark_self_attendance)
        teacher.add_command(label="Mark Check-Out", command=self.load_teacher_check_out_screen)
        teacher.add_command(label="View All Attendance", command=self.load_teacher_attendance_filter)
        teacher.add_command(label="Attendance Summary", command=self.load_teacher_attendance_summary_screen)

        menu.add_cascade(label="self Attendance", menu=teacher)
        parent_label.bind("<Button-1>", lambda e: menu.tk_popup(e.x_root, e.y_root))
    
    # ===========================================
    def build_result_dropdown(self, parent_label):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Generate and Download Result of a Student", command=lambda: self.load_view_and_download_exam_result_of_student())
        menu.add_command(label="Generate and Download Final Result of a Student", command=lambda: self.load_generate_and_download_final_result_of_student())
        menu.add_command(label="View all Result for an Exam", command=lambda: self.load_view_all_results_for_exam())
        menu.add_command(label="Generate and Download all students Results for a class", command=lambda: self.load_view_and_download_all_students_results_for_a_class())
        menu.add_command(label="Generate and Download all Final Results for a Class", command=lambda: self.load_generate_and_download_all_final_results_for_a_class())
        
        parent_label.bind("<Button-1>", lambda e: menu.tk_popup(e.x_root, e.y_root))
        
    # ===========================================
    def build_work_dropdown(self, parent_label):
        menu = tk.Menu(self.root, tearoff=0)

        menu.add_command(label="View Work", command=self.load_teacher_work_records)
        menu.add_command(label="Add Work", command=self.load_teacher_add_work)

        parent_label.bind("<Button-1>", lambda e: menu.tk_popup(e.x_root, e.y_root))

    # ===========================================
    def build_marks_dropdown(self, parent_label):
        menu = tk.Menu(self.root, tearoff=0)

        menu.add_command(label="Add Marks", command=self.load_add_single_student_marks)
        menu.add_command(label="Bulk Enter Marks", command=self.load_bulk_marks_entry_screen)
        menu.add_command(label="Update Marks", command=self.load_update_student_marks_screen)
        menu.add_command(label="View Marks with Filters", command=self.load_view_student_marks_screen)

        parent_label.bind("<Button-1>", lambda e: menu.tk_popup(e.x_root, e.y_root))    

    # ===== CHANGE SCREEN VIEW =====
    def change_screen(self, message, back_callback=None, add_callback=None):
        self.clear_content()

        # Main Message
        tk.Label(
        self.content,
        text=message,
        font=("Arial", 22, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50",
        wraplength=600,
        justify="center"
        ).pack(pady=40)

        # -------- BUTTON FRAME --------
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=20)

        # Reusable hover function
        def hover(btn):
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

        # ------------ Dashboard / Back Button ------------
        back_btn = tk.Label(
        btn_frame,
        text="Go to Dashboard",
        font=("Arial", 12, "bold"),
        bg="#000000",
        fg="white",
        padx=18,
        pady=7,
        width=15,
        cursor="arrow"
        )
        back_btn.grid(row=0, column=0, padx=10)

        hover(back_btn)
        back_btn.bind("<Button-1>", lambda e: (back_callback or self.load_dashboard)())

        # ------------ Add Another Button  ------------
        if add_callback:
            add_btn = tk.Label(
            btn_frame,
            text="Add Another",
            font=("Arial", 12, "bold"),
            bg="#000000",
            fg="white",
            padx=18,
            pady=7,
            width=15,
            cursor="arrow"
            )
            add_btn.grid(row=0, column=1, padx=10)

            hover(add_btn)
            add_btn.bind("<Button-1>", lambda e: add_callback())

    # ====== ACTION BUTTON =======
    def create_action_buttons(self, parent, back_callback, add_callback=None):
        btn_frame = tk.Frame(parent, bg="#ECF0F1")
        btn_frame.pack(pady=20)

        # BACK BUTTON
        back_btn = tk.Label(
        btn_frame, text="Dashboard",
        font=("Arial", 12, "bold"),
        bg="#000", fg="white",
        padx=15, pady=7,
        width=12, cursor="arrow"
        )
        back_btn.grid(row=0, column=0, padx=10)
        self._hover(back_btn)
        back_btn.bind("<Button-1>", lambda e: back_callback())

        # ADD ANOTHER BUTTON (optional)
        if add_callback:
            another_btn = tk.Label(
            btn_frame, text="Add Another",
            font=("Arial", 12, "bold"),
            bg="#000", fg="white",
            padx=15, pady=7,
            width=12, cursor="arrow"
            )
            another_btn.grid(row=0, column=1, padx=10)
            self._hover(another_btn)
            another_btn.bind("<Button-1>", lambda e: add_callback())

    # ===== creating scrollable output table ====
    def create_scrollable_table(self, parent, columns, data):
        # Frame for table + scrollbar
        table_frame = tk.Frame(parent, bg="#ECF0F1")
        table_frame.pack(pady=20, fill="both", expand=True)

        # Scrollbars
        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")

        # Table
        table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            xscrollcommand=x_scroll.set,
            yscrollcommand=y_scroll.set,
            height=15
        )

        # Scrollbar config
        x_scroll.config(command=table.xview)
        y_scroll.config(command=table.yview)

        x_scroll.pack(side="bottom", fill="x")
        y_scroll.pack(side="right", fill="y")
        table.pack(fill="both", expand=True)

        # Define columns
        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=150, anchor="center")

        # Insert rows
        for row in data:
            table.insert("", "end", values=row)

        return table    
    
    # ----- DATE PICKER ------
    def open_calendar_popup(self, button_widget, target_var):
        # ----- POPUP WINDOW -----
        popup = tk.Toplevel(self.root)
        popup.title("Select Date")
        popup.overrideredirect(True)   # No title bar
        popup.config(bg="white")
        
        def outside_click(event):
            # Get popup bounds
            px1 = popup.winfo_rootx()
            py1 = popup.winfo_rooty()
            px2 = px1 + popup.winfo_width()
            py2 = py1 + popup.winfo_height()

            # Check if click INSIDE popup : DO NOTHING
            if px1 <= event.x_root <= px2 and py1 <= event.y_root <= py2:
                return  # safe click (even month/year click)

            # Click OUTSIDE popup : close
            cleanup()

        def cleanup():
            try:
                self.root.unbind("<Button-1>")
            except:
                pass
            popup.destroy()
            self.root.after(50, lambda: self.root.focus_force())

        # Bind outside-click detection
        self.root.bind("<Button-1>", outside_click)
 
        # ----- POSITION BELOW BUTTON -----
        button_widget.update_idletasks()

        bx = button_widget.winfo_rootx()
        by = button_widget.winfo_rooty()
        bw = button_widget.winfo_width()
        bh = button_widget.winfo_height()

        popup.update_idletasks()
        popup.geometry(f"+{bx + 120}+{by + bh + 10}")

        # ----- DEFAULT DATE -----
        today = datetime.date.today()
        target_var.set(today.strftime("%Y-%m-%d"))  # show in entry immediately

        # ----- CALENDAR WIDGET -----
        cal = Calendar(
        popup,
        selectmode="day",
        date_pattern="yyyy-mm-dd",
        year=today.year,
        month=today.month,
        day=today.day, 
        showweeknumbers=False 
        )
        cal.pack(padx=10, pady=10)

        # ----- CONFIRM BUTTON -----
        def confirm():
            selected_date = cal.get_date()
            target_var.set(selected_date)
            popup.destroy()
            self.root.after(50, lambda: self.root.focus_force())
            self.root.unbind("<Button-1>")
        # ----- CONFIRM BUTTON -----
        confirm_btn = tk.Label(
            popup,
            text="Confirm",
            font=("Arial", 12, "bold"),
            bg="#2C3E50",
            fg="white",
            padx=15,
            pady=7,
            cursor="arrow")

        confirm_btn.pack(pady=8)

        # Hover effects
        def on_enter(e):
            confirm_btn.config(bg="#1B2631")

        def on_leave(e):
            confirm_btn.config(bg="#2C3E50")

        # Bind events
        confirm_btn.bind("<Enter>", on_enter)
        confirm_btn.bind("<Leave>", on_leave)
        confirm_btn.bind("<Button-1>", lambda e: confirm())

        # Popup appears above all
        popup.transient(self.root)
        popup.focus_force()
        
    # ------- BACK BUTTON --------
    def create_back_button(self, parent, go_back_callback, form_frame=None):
        back_btn = tk.Label(
        parent,
        text="Back",
        font=("Arial", 14, "bold"),
        bg="#000000",
        fg="white",
        padx=20, pady=10,
        cursor="arrow"
        )
        back_btn.pack(side="left", padx=10)

        # Hover effects
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#222222"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#000000"))

        # Click function
        def on_back(e):
            # Clear entries if form_frame given
            if form_frame:
                for w in form_frame.winfo_children():
                    if isinstance(w, tk.Entry):
                        w.delete(0, tk.END)

            # Load previous screen
            go_back_callback()

        back_btn.bind("<Button-1>", on_back)

        return back_btn
    

    # ===== POPUP FUNCTION TO SHOW WARNINGS, ERRORS, SUCCESS, CONFIRMS AND INFOS =======
    def show_popup(self, title, msg, type="info"):
        from tkinter import messagebox
        type = type.lower()

        if type == "error":
            messagebox.showerror(title, msg)
        elif type == "warning":
            messagebox.showwarning(title, msg)
        elif type == "success":
            messagebox.showinfo(title, msg)   # success = info
        elif type == "confirm":
            return messagebox.askyesno(title, msg)
        else:
            messagebox.showinfo(title, msg)
    
    def show_mini_notification(self, message):
        toast = tk.Label(
        self.root,
        text=message,
        bg="#323232",
        fg="white",
        font=("Arial", 12),
        padx=15,
        pady=8
    )
        toast.place(relx=0.98, rely=0.98, anchor="se")

        toast.after(3000, toast.destroy)

    # ========================================================================
    # ----- STUDENT ATTENDANCE ------
    # ===== Button to Mark Students Attendances =====
    def on_student_change(self, *args):
            sid = self.mark_vars["student_id"].get().strip()
            if not sid.isdigit():
                return

            try:
                import requests
                res = requests.get(
                f"http://127.0.0.1:8000/students/{sid}/subjects")
                if res.status_code != 200:
                    return

                subjects = res.json()
                self.subject_map = {
                s["subject_name"]: s["subject_id"]
                for s in subjects
                }

                self.subject_combobox["values"] = list(self.subject_map.keys())
                self.subject_combobox.config(state="readonly")
                self.mark_vars["subject_id"].set("")

            except Exception as e:
                print(e)

    def load_mark_student_attendance_screen(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="Mark Student Attendance",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # ===== FORM FRAME =====
        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        fields = [
        ("Student ID", "student_id"),
        ("Subject ID", "subject_id"),
        ("Lecture Date (YYYY-MM-DD)", "lecture_date"),
        ("Status", "status"),
        ("Remarks", "remarks"),
        ]

        self.mark_vars = {}
        
        # ===== FETCH DROPDOWN DATA =====
        self.subject_map = {}
        subject_values = []
        status_values = ["P", "A", "L", "LE"]

        from tkinter.ttk import Combobox

        for i, (label, key) in enumerate(fields):

            tk.Label(
            form,
            text=f"{label}:",
            font=("Arial", 14),
            bg="#ECF0F1"
            ).grid(row=i, column=0, padx=10, pady=8, sticky="e")

            var = tk.StringVar()
            self.mark_vars[key] = var

            # ===== DROPDOWNS =====
            if key == "subject_id":
                entry = Combobox(
                form,
                textvariable=var,
                values=subject_values,
                state="readonly",
                font=("Arial", 14),
                width=26
                )
                entry.grid(row=i, column=1, padx=10, pady=8)
                self.subject_combobox = entry
                self.subject_combobox.config(state="disabled")

            elif key == "status":
                entry = Combobox(
                form,
                textvariable=var,
                values=status_values,
                state="readonly",
                font=("Arial", 14),
                width=26
                )
                entry.grid(row=i, column=1, padx=10, pady=8)

            # ===== DATE =====
            elif key == "lecture_date":
                entry = tk.Entry(form, textvariable=var, font=("Arial", 14), width=28)
                entry.grid(row=i, column=1, padx=10, pady=8)

                tk.Button(
                form,
                text="Calendar",
                font=("Arial", 12),
                bg="white",
                relief="ridge",
                command=lambda e=entry, v=var: self.open_calendar_popup(e, v)
                ).grid(row=i, column=2, padx=8)

            # ===== NORMAL ENTRY =====
            else:
                entry = tk.Entry(form, textvariable=var, font=("Arial", 14), width=28)
                entry.grid(row=i, column=1, padx=10, pady=8)


        # ===== BACK BUTTON =====
        btn_row = tk.Frame(self.content, bg="#ECF0F1")
        btn_row.pack(pady=20)

        self.create_back_button(
        parent=btn_row,
        go_back_callback=self.load_dashboard,
        form_frame=form
        )
        
        self.content.update_idletasks()
        
        # ===== SUBMIT BUTTON =====
        submit_btn = tk.Label(
        self.content,
        text="Mark Attendance",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=12,
        width=18,
        relief="ridge",
        cursor="arrow"
        )
        submit_btn.pack(pady=20)

        # ===== ENABLE/DISABLE LOGIC =====
        def validate():
            data = {k: v.get().strip() for k, v in self.mark_vars.items()}

            if not data["student_id"].isdigit():
                disable(); return

            if data["subject_id"] not in self.subject_map:
                disable(); return

            import re
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", data["lecture_date"]):
                disable(); return

            if data["status"] not in ["P", "A", "L", "LE"]:
                disable(); return

            enable()
 
        def enable():
            submit_btn.config(bg="#000000", fg="white", cursor="hand2")
            submit_btn.bind("<Enter>", lambda e: submit_btn.config(bg="#222222"))
            submit_btn.bind("<Leave>", lambda e: submit_btn.config(bg="#000000"))
            submit_btn.bind("<Button-1>", lambda e: submit())

        def disable():
            submit_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            submit_btn.unbind("<Enter>")
            submit_btn.unbind("<Leave>")
            submit_btn.unbind("<Button-1>")

        for v in self.mark_vars.values():
            v.trace_add("write", lambda *args: validate())

        self.mark_vars["student_id"].trace_add("write", self.on_student_change)
    
        # ===== SUBMIT FUNCTION =====
        def submit():
            data = {k: v.get().strip() for k, v in self.mark_vars.items()}

            # ---- missing fields ----
            required_fields = ["student_id", "subject_id", "lecture_date", "status"]
            missing = [f for f in required_fields if not data[f]]

            if missing:
                # show which fields are missing (friendly labels)
                pretty = ", ".join([m.replace("_", " ").title() for m in missing])
                self.show_popup("Missing Information", f"Please fill: {pretty}", "warning")
                disable()
                return

            payload = {
                "student_id": int(data["student_id"]),
                "subject_id": self.subject_map[data["subject_id"]],
                "lecture_date": data["lecture_date"],
                "status": data["status"],
                "remarks": data["remarks"],
                "teacher_id": self.teacher_id
                }

            try:
                import requests
                res = requests.post(
                "http://127.0.0.1:8000/teacher/attendance/student/mark",
                json=payload
                )

                if res.status_code == 201:
                    self.show_popup("Success", "Attendance Marked Successfully!", "info")
                    self.change_screen(
                    "Attendance Marked Successfully!",
                    add_callback=self.load_mark_student_attendance_screen
                    )
                    return
                try:
                    msg = res.json().get("detail", "Unknown error")
                except:
                    msg = "Unknown error"

                if "issued a TC" in msg:
                    self.show_popup("Rejected", msg, "warning")
                elif "already marked" in msg:
                    self.show_popup("Duplicate Entry", msg, "warning")
                elif "not found" in msg:
                    self.show_popup("Invalid ID", msg, "warning")
                else:
                    self.show_popup("Failed", msg, "error")
                self.change_screen(
                    "Failed to Mark Attendance for this Student ID try Again with a Valid ID",
                    add_callback=self.load_mark_student_attendance_screen
                    )

            except Exception as e:
                self.show_popup("Server Error", str(e), "error")


    # ==========================================================================
    # ===== Button to Mark Attendance in Bulk =====
    def on_bulk_class_change(self, *args):
        class_val = self.bulk_vars["class_id"].get()
        if class_val not in self.bulk_class_map:
            return

        class_id = self.bulk_class_map[class_val]

        try: 
            import requests
            res = requests.get(
            f"http://127.0.0.1:8000/classes/{class_id}/subjects"
            )
            if res.status_code != 200:
                return

            subjects = res.json()
            if not subjects:
                self.show_popup(
                "No Subjects",
                "No subjects assigned to this class",
                "warning")
                return

            self.bulk_subject_map = {
            s["subject_name"]: s["subject_id"] for s in subjects}

            self.bulk_subject_combobox["values"] = list(self.bulk_subject_map.keys())
            self.bulk_subject_combobox.config(state="readonly")
            self.bulk_vars["subject_id"].set("")

        except Exception as e:
            print(e)    

    def load_mark_bulk_attendance_screen(self):
        self.clear_content()

        # ---- TITLE ----
        tk.Label(
        self.content,
        text="Mark Bulk Attendance",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=20)

        # ======== INPUT FIELDS =========
        labels = [
        ("Class ID", "class_id"),
        ("Subject ID", "subject_id"),
        ("Lecture Date (YYYY-MM-DD)", "lecture_date"),
        ("Absent Student IDs (comma separated)", "absent_ids"),
        ]

        self.bulk_vars = {}
        
        from tkinter.ttk import Combobox

        # ===== FETCH DROPDOWN DATA =====
        classes = fetch_classes()

        self.bulk_class_map = {
            f"{c['class_name']} - {c['section']}": c["class_id"]
            for c in classes
            }

        class_values = list(self.bulk_class_map.keys())
        self.bulk_subject_map = {}    
        subject_values = [] 

        for i, (label, key) in enumerate(labels):

            tk.Label(
            form,
            text=label + ":",
            font=("Arial", 14),
            bg="#ECF0F1"
            ).grid(row=i, column=0, padx=10, pady=10, sticky="e")

            var = tk.StringVar()
            self.bulk_vars[key] = var

            # ===== DROPDOWNS =====
            if key == "class_id":
                entry = Combobox(
                form,
                textvariable=var,
                values=class_values,
                state="readonly",
                font=("Arial", 14),
                width=26
                )
                entry.grid(row=i, column=1, padx=10, pady=10)

            elif key == "subject_id":
                entry = Combobox(
                form,
                textvariable=var,
                values=subject_values,
                state="disabled",
                font=("Arial", 14),
                width=26
                )
                entry.grid(row=i, column=1, padx=10, pady=10)
                self.bulk_subject_combobox = entry

            elif key == "lecture_date":
                entry = tk.Entry(form, textvariable=var, font=("Arial", 14), width=28)
                entry.grid(row=i, column=1, padx=10, pady=10)

                tk.Button(
                form,
                text="Calendar",
                font=("Arial", 12),
                bg="white",
                relief="flat",
                command=lambda e=entry, v=var: self.open_calendar_popup(e, v)
                ).grid(row=i, column=2, padx=5)

            else:  # absent_ids
                entry = tk.Entry(form, textvariable=var, font=("Arial", 14), width=28)
                entry.grid(row=i, column=1, padx=10, pady=10)

        # ======== BACK BUTTON ========
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,
        form_frame=form
        )

        self.content.update_idletasks()

        # ======== SUBMIT BUTTON =========
        submit_btn = tk.Label(
        self.content,
        text="Submit",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=25, pady=12,
        width=14,
        cursor="arrow"
        )
        submit_btn.pack(pady=20)

        # -------- ENABLE / DISABLE SUBMIT --------
        def enable():
            submit_btn.config(bg="#000000", fg="white", cursor="hand2")
            submit_btn.bind("<Enter>", lambda e: submit_btn.config(bg="#222222"))
            submit_btn.bind("<Leave>", lambda e: submit_btn.config(bg="#000000"))
            submit_btn.bind("<Button-1>", lambda e: submit_bulk())

        def disable():
            submit_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            submit_btn.unbind("<Enter>")
            submit_btn.unbind("<Leave>")
            submit_btn.unbind("<Button-1>")

        # -------- VALIDATION --------
        def validate(*args):
            class_val = self.bulk_vars["class_id"].get().strip()
            subject_val = self.bulk_vars["subject_id"].get().strip()
            lecture_date = self.bulk_vars["lecture_date"].get().strip()
            abs_vals = self.bulk_vars["absent_ids"].get().strip()

            if class_val not in self.bulk_class_map:
                disable(); return

            if subject_val not in self.bulk_subject_map:
                disable(); return

            import re
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", lecture_date):
                disable(); return

            if abs_vals:
                for p in abs_vals.split(","):
                    p = p.strip()
                    if p == "":
                        continue   
                    if not p.isdigit():
                        disable()
                        return

            enable()
  
        for v in self.bulk_vars.values():
            v.trace_add("write", validate)

        self.bulk_vars["class_id"].trace_add("write", self.on_bulk_class_change)
    
        # -------- SUBMIT FUNCTION --------
        def submit_bulk():
            class_id = self.bulk_class_map[self.bulk_vars["class_id"].get()]
            subject_id = self.bulk_subject_map[self.bulk_vars["subject_id"].get()]
            lecture_date = self.bulk_vars["lecture_date"].get().strip()
            
            raw_ids = self.bulk_vars["absent_ids"].get().strip()

            try:
                absent_ids = [int(x.strip()) for x in raw_ids.split(",") if x.strip()]
            except ValueError:
                self.show_popup("Invalid Input", "Absent IDs must be comma-separated numbers (e.g. 76,101,77)","warning")
                return


            if not all([class_id, subject_id, lecture_date]):
                self.show_popup("Missing Values", "Enter all the Fields", "warning")
                disable()
                return

            payload = {
            "class_id": class_id,
            "subject_id": subject_id,
            "teacher_id": self.teacher_id,
            "lecture_date": lecture_date,
            "absent_ids": absent_ids
            }

            import requests
            try:
                res = requests.post(
                "http://127.0.0.1:8000/teacher/attendance/student/mark-bulk",
                json=payload
            )

                if res.status_code == 201:
                    msg = res.json().get("message", "Marked successfully!")
                    self.show_popup("Success", msg, "info")
                    self.change_screen("Bulk Attendance Marked", add_callback=self.load_mark_bulk_attendance_screen)
                    return
                
                try:
                    detail = res.json().get("detail", "Unknown Error")
                except:
                    detail = "Unknown Error"

                # Make popup messages friendly
                if "comma-separated" in detail:
                    self.show_popup("Invalid Format", "Absent IDs must be comma-separated numbers.", "warning")

                elif "not found" in detail:
                    self.show_popup("Invalid Input", detail, "warning")

                elif "No students found" in detail:
                    self.show_popup("No Students", detail, "warning")

                elif "Student" in detail and "inactive" in detail:
                # Just in case backend sends inactive student warnings
                    self.show_popup("Skipped Students", detail, "info")

                else:
                    self.show_popup("Failed", detail, "error") 

            except Exception as e:
                self.show_popup("Error", f"Server error: {e}", "error")


    # ==========================================================================
    # ===== Button to Filter Student Attendance by Date =====
    def on_filter_student_change(self, *args):
        sid = self.filter_vars["student_id"].get().strip()

        if not sid.isdigit() or int(sid) <= 0:
            # ---- reset subject dropdown if invalid ----
            self.subject_combobox.set("")
            self.subject_combobox["values"] = [""]
            self.subject_combobox.config(state="disabled")
            self.filter_subject_map = {}
            self.subject_id_to_name = {}
            return

        try:
            import requests
            res = requests.get(f"http://127.0.0.1:8000/students/{sid}/subjects")
            if res.status_code != 200:
                return

            subjects = res.json()
            if not subjects:
                return
            
            self.filter_subject_map = {
                s["subject_name"]: s["subject_id"] for s in subjects}
            
            self.subject_id_to_name = {
            v: k for k, v in self.filter_subject_map.items()}

            self.subject_combobox["values"] = [""] + list(self.filter_subject_map.keys())
            self.subject_combobox.config(state="readonly")

        except Exception as e:
            print(e)

    def load_filter_student_attendance_screen(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="Filter Student Attendance",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # ===== FORM =====
        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=20)

        labels = [
        ("Student ID", "student_id"),
        ("Date From (YYYY-MM-DD)", "date_from"),
        ("Date To (YYYY-MM-DD)", "date_to"),
        ("Subject ID (optional)", "subject_id")
        ]

        self.filter_vars = {}
        
        from tkinter.ttk import Combobox

        # ===== FETCH SUBJECTS FOR DROPDOWN =====
        self.filter_subject_map = {}
        self.subject_id_to_name = {}
        subject_values = [""]

        for i, (text_lbl, key) in enumerate(labels):
            tk.Label(
            form,
            text=text_lbl + ":",
            font=("Arial", 14),
            bg="#ECF0F1"
            ).grid(row=i, column=0, padx=10, pady=10, sticky="e")

            var = tk.StringVar()
            self.filter_vars[key] = var

            if key == "subject_id":
                entry = Combobox(
                form,
                textvariable=var,
                values=subject_values,
                state="readonly",
                font=("Arial", 14),
                width=23
                )
                entry.grid(row=i, column=1, padx=10)
                self.subject_combobox = entry

            else:
                entry = tk.Entry(
                form,
                textvariable=var,
                font=("Arial", 14),
                width=25
                )
                entry.grid(row=i, column=1, padx=10)

        # ===== DATE PICKER BUTTONS =====
        def add_calendar_button(row, var):
            entry = form.grid_slaves(row=row, column=1)[0]
            tk.Button(
            form,
            text="Calendar",
            font=("Arial", 12),
            bg="white",
            relief="flat",
            command=lambda: self.open_calendar_popup(entry, var)
            ).grid(row=row, column=2, padx=5)

        add_calendar_button(1, self.filter_vars["date_from"])
        add_calendar_button(2, self.filter_vars["date_to"])

        # ===== BUTTONS FRAME =====
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=20)

        # Back Button
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,
        form_frame=form
        )

        # ===== Filter Button =====
        filter_btn = tk.Label(
        self.content,
        text="Filter",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=25, pady=10,
        width=12,
        cursor="arrow"
        )
        filter_btn.pack(pady=5)

        # ===== Clear Button =====
        clear_btn = tk.Label(
        self.content,
        text="Clear Results",
        font=("Arial", 14),
        bg="#000000",
        fg="white",
        padx=20, pady=8,
        width=12,
        cursor="arrow"
        )
        clear_btn.pack(pady=5)

        # ===== TABLE =====
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        cols = ("attendance_id", "student_id", "subject_id",
            "lecture_date", "status", "remarks")

        self.attendance_tree = ttk.Treeview(
        table_frame,
        columns=cols,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
        )
        self.attendance_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.attendance_tree.yview)
        x_scroll.config(command=self.attendance_tree.xview)

        for col in cols:
            self.attendance_tree.heading(col, text=col.replace("_", " ").title())
            self.attendance_tree.column(col, width=150, anchor="center")

        # ===== ENABLE/DISABLE FILTER BUTTON =====
        def enable():
            filter_btn.config(bg="#000", fg="white", cursor="hand2")
            filter_btn.bind("<Enter>", lambda e: filter_btn.config(bg="#222222"))
            filter_btn.bind("<Leave>", lambda e: filter_btn.config(bg="#000000"))
            filter_btn.bind("<Button-1>", lambda e: do_filter())

        def disable():
            filter_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            filter_btn.unbind("<Enter>")
            filter_btn.unbind("<Leave>")
            filter_btn.unbind("<Button-1>")

        def validate(*args):
            data = {k: v.get().strip() for k, v in self.filter_vars.items()}

            d1 = data["date_from"]
            d2 = data["date_to"]

            # Regex
            import re
            date_regex = r"^\d{4}-\d{2}-\d{2}$"

            if not d1 or not d2:
                disable()
                return

            if not re.match(date_regex, d1) or not re.match(date_regex, d2):
                disable()
                return
              
            if d1 > d2:
                disable()
                self.show_popup(
                    "Invalid Date Range",
                    "'Date From' cannot be after 'Date To'",
                    "warning")
                return

            if not data["student_id"].isdigit():
                disable()
                return

            enable()

        for v in self.filter_vars.values():
            v.trace_add("write", validate)

        self.filter_vars["student_id"].trace_add("write", self.on_filter_student_change)    

        disable()

        # ===== CLEAR TABLE =====
        def clear_table(*args):
            for row in self.attendance_tree.get_children():
                self.attendance_tree.delete(row)

        clear_btn.bind("<Button-1>", clear_table)

        # ===== FILTER FUNCTION =====
        def do_filter():
            subject_val = self.filter_vars["subject_id"].get().strip()

            payload = {
                "student_id": int(self.filter_vars["student_id"].get().strip()),
                "date_from": self.filter_vars["date_from"].get().strip(),
                "date_to": self.filter_vars["date_to"].get().strip(),
                "subject_id": self.filter_subject_map.get(subject_val) if subject_val else None
                }

            import requests
            try:
                res = requests.post("http://127.0.0.1:8000/teacher/attendance/student/by-date", json=payload)
                if res.status_code != 200:
                    self.show_popup("Failed", res.json().get("detail", "No records found"), "error")
                    return

                data = res.json()
                clear_table()

                if not data:
                    self.show_popup("No Records", "No attendance found in this range.", "info")
                    return
                
                STATUS_LABELS = {"P": "Present", "A": "Absent", "L": "Late", "LE": "Leave"}

                for item in data:
                    subject_name = self.subject_id_to_name.get(
                    item["subject_id"], f"ID {item['subject_id']}")

                    status_label = STATUS_LABELS.get(
                    item["status"], item["status"])

                    self.attendance_tree.insert("", "end", values=(
                        item["attendance_id"],
                        item["student_id"],
                        subject_name,         
                        item["lecture_date"],
                        status_label,         
                        item["remarks"]
                    ))

            except Exception as e:
                self.show_popup("Error", f"Server error: {e}", "error")


    # ==========================================================================
    # ===== Button to View Summary of Student Attendance =====
    def load_attendance_summary_screen(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="Student Attendance Summary",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # ===== FORM =====
        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        labels = [
        ("Student ID", "student_id"),
        ("Date From (YYYY-MM-DD)", "date_from"),
        ("Date To (YYYY-MM-DD)", "date_to")
        ]

        self.summary_vars = {}

        for i, (lbl, key) in enumerate(labels):
            tk.Label(
            form,
            text=lbl + ":",
            font=("Arial", 14),
            bg="#ECF0F1"
            ).grid(row=i, column=0, padx=10, pady=10, sticky="e")

            var = tk.StringVar()
            entry = tk.Entry(form, textvariable=var, font=("Arial", 14), width=25)
            entry.grid(row=i, column=1, padx=10)

            self.summary_vars[key] = var
       
        # ===== DATE PICKER BUTTONS =====
        def add_cal_btn(row, var):
            entry = form.grid_slaves(row=row, column=1)[0]
            tk.Button(
            form,
            text="Calendar",
            font=("Arial", 12),
            bg="white",
            relief="flat",
            command=lambda: self.open_calendar_popup(entry, var)
            ).grid(row=row, column=2, padx=5)

        add_cal_btn(1, self.summary_vars["date_from"])
        add_cal_btn(2, self.summary_vars["date_to"])


        # ===== BUTTON ROW =====
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=20)

        # Back Button
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,
        form_frame=form
        )

        # ===== GET SUMMARY BUTTON =====
        summary_btn = tk.Label(
        self.content,
        text="Get Summary",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=25, pady=10,
        width=12,
        cursor="arrow"
        )
        summary_btn.pack(pady=5)

        # ===== CLEAR BUTTON =====
        clear_btn = tk.Label(
        self.content,
        text="Clear",
        font=("Arial", 14),
        bg="#000000",
        fg="white",
        padx=20, pady=8,
        width=10,
        cursor="arrow"
        )
        clear_btn.pack(pady=5)

        # ===== SUMMARY PANEL =====
        summary_frame = tk.Frame(self.content, bg="#ECF0F1")
        summary_frame.pack(pady=25)

        summary_labels = {
        "total_lectures": tk.StringVar(),
        "present": tk.StringVar(),
        "absent": tk.StringVar(),
        "late": tk.StringVar(),
        "leave": tk.StringVar(), 
        "percentage": tk.StringVar()
        }

        row = 0
        for key, var in summary_labels.items():
            tk.Label(
            summary_frame,
            text=key.replace("_", " ").title() + ":",
            font=("Arial", 16),
            bg="#ECF0F1"
            ).grid(row=row, column=0, padx=10, pady=8, sticky="w")

            tk.Entry(
            summary_frame,
            textvariable=var,
            font=("Arial", 16),
            width=20,
            state="disabled",
            disabledbackground="#F7F9F9",
            disabledforeground="#2C3E50"
            ).grid(row=row, column=1, padx=10, pady=8)

            row += 1

        # ===== ENABLE / DISABLE BUTTON =====
        def enable():
            summary_btn.config(bg="#000", fg="white", cursor="hand2")
            summary_btn.bind("<Enter>", lambda e: summary_btn.config(bg="#222222"))
            summary_btn.bind("<Leave>", lambda e: summary_btn.config(bg="#000000"))
            summary_btn.bind("<Button-1>", lambda e: get_summary())

        def disable():
            summary_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            summary_btn.unbind("<Enter>")
            summary_btn.unbind("<Leave>")
            summary_btn.unbind("<Button-1>")

        disable()

        # ===== VALIDATION =====
        def validate(*args):
            sid = self.summary_vars["student_id"].get().strip()
            d1 = self.summary_vars["date_from"].get().strip()
            d2 = self.summary_vars["date_to"].get().strip()

            import re
            date_regex = r"^\d{4}-\d{2}-\d{2}$"

            if (len(d1) == 10 and not re.match(date_regex, d1)) or \
               (len(d2) == 10 and not re.match(date_regex, d2)):
                disable()
                self.show_popup("Invalid Date", "Date should be in format YYYY-MM-DD", "warning")
                return

            # student id first
            if not sid.isdigit():
                disable()
                return

            # dates empty
            if not d1 or not d2:
                disable()
                return

            # format
            if not re.match(date_regex, d1) or not re.match(date_regex, d2):
                disable()
                return

            # logical range
            if d1 > d2:
                disable()
                self.show_popup("Invalid Date Range", "'Date From' cannot be after 'Date To'", "warning")
                return

            enable()

        for v in self.summary_vars.values():
            v.trace_add("write", validate)

        # ===== CLEAR FIELDS =====
        def clear():
            for var in self.summary_vars.values():
                var.set("")
            for var in summary_labels.values():
                var.set("")
            disable()

        clear_btn.bind("<Button-1>", lambda e: clear())

        # ===== API CALL =====
        def get_summary():
            sid = self.summary_vars["student_id"].get().strip()
            d1 = self.summary_vars["date_from"].get().strip()
            d2 = self.summary_vars["date_to"].get().strip()

            import requests
            try:
                url = f"http://127.0.0.1:8000/teacher/attendance/student/summary/{sid}?date_from={d1}&date_to={d2}"
                res = requests.get(url)

                if res.status_code != 200:
                    self.show_popup("Failed", res.json().get("detail", "No summary available"), "warning")
                    return

                data = res.json()

                summary_labels["total_lectures"].set(data["total_lectures"])
                summary_labels["present"].set(data["present"])
                summary_labels["absent"].set(data["absent"])
                summary_labels["late"].set(data["late"])
                summary_labels["leave"].set(data["leave"])
                summary_labels["percentage"].set(str(data["percentage"]) + "%")

            except Exception as e:
                self.show_popup("Error", f"Server Error: {e}", "error")


    # ==========================================================================
    # ===== Button to Update Student Attendance =====
    def load_update_student_attendance_screen(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="Update Student Attendance",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # ===== FORM =====
        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # Attendance ID
        tk.Label(form, text="Attendance ID:", font=("Arial", 14), bg="#ECF0F1")\
        .grid(row=0, column=0, padx=10, pady=10)

        att_id_var = tk.StringVar()
        tk.Entry(form, textvariable=att_id_var, font=("Arial", 14), width=25)\
        .grid(row=0, column=1, padx=10, pady=10)

        # ===== LOAD BUTTON =====
        load_btn = tk.Label(
        form,
        text="Load",
        font=("Arial", 12, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=15, pady=5,
        width=10,
        cursor="arrow"
        )
        load_btn.grid(row=0, column=2, padx=10)

        # INFO FIELDS
        labels = [
        ("Student ID", "student_id"),
        ("Subject ID", "subject_id"),
        ("Class ID", "class_id"),
        ("Lecture Date (YYYY-MM-DD)", "lecture_date"),
        ("Status (P/A/L)", "status"),
        ("Remarks", "remarks")
        ]

        self.update_vars = {}
        self.update_entries = {}
        from tkinter.ttk import Combobox

        # ===== FETCH CLASSES & SUBJECTS =====
        subjects = fetch_subjects()
        classes = fetch_classes()

        self.subject_map = {
            f"{s['subject_name']}": s["subject_id"]
            for s in subjects
            }

        self.class_map = {
            f"{c['class_name']} - {c['section']}": c["class_id"]
            for c in classes
            }

        subject_values = list(self.subject_map.keys())
        class_values = list(self.class_map.keys())
        status_values = ["P", "A", "L"]

        row_index = 1
        for text, key in labels:
            tk.Label(
            form,
            text=text + ":",
            font=("Arial", 14),
            bg="#ECF0F1"
            ).grid(row=row_index, column=0, padx=10, pady=10, sticky="e")

            var = tk.StringVar()

            if key == "subject_id":
                entry = Combobox(
                form,
                textvariable=var,
                values=subject_values,
                state="disabled",
                font=("Arial", 14),
                width=23
                )

            elif key == "class_id":
                entry = Combobox(
                form,
                textvariable=var,
                values=class_values,
                state="disabled",
                font=("Arial", 14),
                width=23
                )

            elif key == "status":
                entry = Combobox(
                form,
                textvariable=var,
                values=status_values,
                state="disabled",
                font=("Arial", 14),
                width=23
                )

            else:
                entry = tk.Entry(
                form,
                textvariable=var,
                font=("Arial", 14),
                width=25,
                state="disabled"
                )

            entry.grid(row=row_index, column=1, padx=10)
            self.update_vars[key] = var
            self.update_entries[key] = entry
            row_index += 1

        # ===== BUTTON ROW =====
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=20)

        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,
        form_frame=form
        )

        # ===== UPDATE BUTTON =====
        update_btn = tk.Label(
        self.content,
        text="Update Attendance",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20, pady=10,
        width=18,
        cursor="arrow"
        )
        update_btn.pack(pady=10)

        def enable_update():
            update_btn.config(bg="#000000", fg="white", cursor="hand2")
            update_btn.bind("<Enter>", lambda e: update_btn.config(bg="#222222"))
            update_btn.bind("<Leave>", lambda e: update_btn.config(bg="#000000"))
            update_btn.bind("<Button-1>", lambda e: update_attendance())

        def disable_update():
            update_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            update_btn.unbind("<Enter>")
            update_btn.unbind("<Leave>")
            update_btn.unbind("<Button-1>")

        disable_update()

        # ===== VALIDATE EVERY CHANGE =====
        def validate_entries(*args):
            status = self.update_vars["status"].get().strip()
            remarks = self.update_vars["remarks"].get().strip()
 
            if status not in ("P", "A", "L"):
                disable_update()
                return

            if remarks == "":
                disable_update()
                return

            enable_update()

        for v in self.update_vars.values():
            v.trace_add("write", validate_entries)

        # ===== LOAD DATA FROM BACKEND =====
        def load_record():
            att_id = att_id_var.get().strip()

            if not att_id.isdigit():
                self.show_popup("Invalid ID", "Attendance ID must be numeric.", "warning")
                return

            import requests
            try:
                res = requests.get(f"http://127.0.0.1:8000/teacher/attendance/student/{att_id}")

                if res.status_code != 200:
                    self.show_popup("Not Found", "Attendance record not found.", "warning")
                    disable_update()
                    for var in self.update_vars.values():
                        var.set("")
                    return

                data = res.json()

                # Enable only editable fields
                for key, entry in self.update_entries.items():
                    if key in ("status", "remarks"):
                        entry.config(state="normal")
                    else:
                        entry.config(state="disabled")

                # Fill data
                self.update_vars["student_id"].set(data["student_id"])

                # Subject
                for label, sid in self.subject_map.items():
                    if sid == data["subject_id"]:
                        self.update_vars["subject_id"].set(label)
                        break

                # Class
                for label, cid in self.class_map.items():
                    if cid == data["class_id"]:
                        self.update_vars["class_id"].set(label)
                        break

                self.update_vars["lecture_date"].set(data["lecture_date"])
                self.update_vars["status"].set(data["status"])
                self.update_vars["remarks"].set(data.get("remarks", ""))

            except Exception as e:
                self.show_popup("Error", f"Server Error: {e}", "error")

        # Bind load button logic
        def validate_load(*args):
            if att_id_var.get().strip().isdigit():
                load_btn.config(bg="#000", fg="white", cursor="hand2")
                load_btn.bind("<Enter>", lambda e: load_btn.config(bg="#222222"))
                load_btn.bind("<Leave>", lambda e: load_btn.config(bg="#000000"))
                load_btn.bind("<Button-1>", lambda e: load_record())
            else:
                load_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                load_btn.unbind("<Enter>")
                load_btn.unbind("<Leave>")
                load_btn.unbind("<Button-1>")

        att_id_var.trace_add("write", validate_load)

        # ===== UPDATE API CALL =====
        def update_attendance():
            att_id = att_id_var.get().strip()

            payload = {
                "status": self.update_vars["status"].get(),
                "remarks": self.update_vars["remarks"].get()
            }

            import requests
            try:
                res = requests.put(
                f"http://127.0.0.1:8000/teacher/attendance/student/update/{att_id}",
                json=payload
                )

                if res.status_code != 200:
                    self.show_popup("Error", "Failed to update attendance.", "error")
                    return

                self.show_popup("Success", "Attendance Updated Successfully!", "success")
                self.change_screen(
                "Attendance Updated Successfully!",
                add_callback=self.load_update_student_attendance_screen
                )

            except Exception as e:
                self.show_popup("Error", f"Update Failed: {e}", "error")


    # ==========================================================================
    # ===== Button to Delete Student Attendance =====
    def load_delete_student_attendance_screen(self):
        self.clear_content()

        # ------- TITLE -------
        tk.Label(
        self.content,
        text="Delete Student Attendance",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # ------- INPUT FIELD -------
        tk.Label(
        form,
        text="Attendance ID:",
        font=("Arial", 14),
        bg="#ECF0F1"
        ).grid(row=0, column=0, padx=10, pady=10)

        att_id_var = tk.StringVar()
        entry = tk.Entry(form, textvariable=att_id_var, font=("Arial", 14), width=25)
        entry.grid(row=0, column=1, padx=10, pady=10)

        # ------- BUTTONS FRAME -------
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=20)

        # Back button (common function)
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,
        form_frame=form
        )
        self.content.update_idletasks()

        # ------- DELETE BUTTON -------
        delete_btn = tk.Label(
        self.content,
        text="Delete",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=12,
        width=12,
        relief="ridge",
        cursor="arrow"      # disabled
        )
        delete_btn.pack(pady=10)

        # ------- ENABLE/DISABLE LOGIC -------
        def enable_delete():
            delete_btn.config(bg="#000000", fg="white", cursor="hand2")
            delete_btn.bind("<Enter>", lambda e: delete_btn.config(bg="#222222"))
            delete_btn.bind("<Leave>", lambda e: delete_btn.config(bg="#000000"))
            delete_btn.bind("<Button-1>", lambda e: perform_delete())

        def disable_delete():
            delete_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            delete_btn.unbind("<Enter>")
            delete_btn.unbind("<Leave>")
            delete_btn.unbind("<Button-1>")

        # ------- VALIDATION -------
        def validate(*args):
            val = att_id_var.get().strip()

            if not val:
                disable_delete()
                return

            if not val.isdigit():
                att_id_var.set("")
                disable_delete()
                return

            if int(val) <= 0:
                att_id_var.set("")
                disable_delete()
                return

            enable_delete()

        att_id_var.trace_add("write", validate)

        # ------- DELETE FUNCTION -------
        def perform_delete():
            att_id = att_id_var.get().strip()

            import requests
            try:
                res = requests.delete(f"http://127.0.0.1:8000/teacher/attendance/student/delete/{att_id}")

                if res.status_code == 204 or res.status_code == 200:
                    self.show_popup("Success", "Attendance Deleted Successfully!", "info")
                    self.change_screen(
                    "Attendance Deleted Successfully!",
                    add_callback=self.load_delete_student_attendance_screen
                )
                else:
                    self.show_popup("Not Found", "No attendance record found for this ID.", "error")

            except Exception as e:
                self.show_popup("Backend Error", f"Error: {e}", "error")


    # ==========================================================================
    # ===== Button to Mark Self Attendance =====
    def load_mark_self_attendance(self):
        self.clear_content()

        # ------- TITLE -------
        tk.Label(
        self.content,
        text="Mark Self Attendance",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # ------- INPUTS -------
        # Teacher ID (auto-filled, not editable)
        tk.Label(
        form,
        text="Teacher ID:",
        font=("Arial", 14),
        bg="#ECF0F1"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        teacher_id_var = tk.StringVar(value=str(self.teacher_id))
        tk.Entry(
        form, textvariable=teacher_id_var, font=("Arial", 14), width=25, state="readonly"
        ).grid(row=0, column=1, padx=10, pady=10)

        # Date (auto-filled)
        tk.Label(
        form,
        text="Date (YYYY-MM-DD):",
        font=("Arial", 14),
        bg="#ECF0F1"
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")

        from datetime import datetime
        today_date = datetime.now().strftime("%Y-%m-%d")
        date_var = tk.StringVar(value=today_date)

        tk.Entry(
        form, textvariable=date_var, font=("Arial", 14), width=25, state="readonly"
        ).grid(row=1, column=1, padx=10, pady=10)
        
        # Status dropdown
        tk.Label(
        form,
        text="Status:",
        font=("Arial", 14),
        bg="#ECF0F1"
        ).grid(row=2, column=0, padx=10, pady=10, sticky="w")

        status_var = tk.StringVar()
        status_dropdown = ttk.Combobox(
        form,
        textvariable=status_var,
        values=["P", "A", "L", "LE"],
        state="readonly",
        width=23,
        font=("Arial", 14)
        )
        status_dropdown.grid(row=2, column=1, padx=10, pady=10)
        status_dropdown.set("P")  # default

        # ------- BUTTONS FRAME -------
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=20)

        # Back button
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,
        form_frame=form
        )

        self.content.update_idletasks()

        # ------- SUBMIT BUTTON -------
        mark_btn = tk.Label(
        self.content,
        text="Mark Attendance",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=12,
        width=15,
        relief="ridge",
        cursor="arrow"  # disabled
        )
        mark_btn.pack(pady=10)

        # ------- ENABLE/DISABLE LOGIC -------
        def enable_btn():
            mark_btn.config(bg="#000000", fg="white", cursor="hand2")
            mark_btn.bind("<Enter>", lambda e: mark_btn.config(bg="#222222"))
            mark_btn.bind("<Leave>", lambda e: mark_btn.config(bg="#000000"))
            mark_btn.bind("<Button-1>", lambda e: perform_mark())
        
        def disable_btn():
            mark_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            mark_btn.unbind("<Enter>")
            mark_btn.unbind("<Leave>")
            mark_btn.unbind("<Button-1>")

        def validate(*args):
            if status_var.get() in ("P", "A", "L", "LE"):
                enable_btn()
            else:
                disable_btn()

        status_var.trace_add("write", validate)

        # ------- API CALL FUNCTION -------
        def perform_mark():
            import requests

            payload = {
            "teacher_id": self.teacher_id,
            "date": date_var.get(),
            "status": status_var.get(),
            "remarks": "Self Attendance Marked"}

            try:
                res = requests.post(
                "http://127.0.0.1:8000/teacher/attendance/mark-self",
                json=payload
                )

                if res.status_code == 201:
                    self.show_popup("Success", "Attendance Marked Successfully!", "info")
                    self.change_screen(
                    "Attendance Marked Successfully!",
                    add_callback=self.load_mark_self_attendance
                    )
                    return

                if res.status_code == 400:
                    self.show_popup("Already Marked", "Attendance already done for today!", "warning")
                    return

                if res.status_code == 404:
                    self.show_popup("Teacher Not Found", "Invalid Teacher ID!", "error")
                    return

                self.show_popup("Error", f"Unexpected Error: {res.text}", "error")

            except Exception as e:
                self.show_popup("Backend Error", f"Error: {e}", "error")


    # ==========================================================================
    # ===== Button to Mark Check-Out =====            
    def load_teacher_check_out_screen(self):
        self.clear_content()

        # ---------- TITLE ----------
        tk.Label(
        self.content,
        text="Teacher Check-Out",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=20)

        # ---------- Teacher ID ----------
        tk.Label(
        form, text="Teacher ID:", font=("Arial", 14), bg="#ECF0F1"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="e")
 
        teacher_id_var = tk.StringVar(value=str(self.teacher_id))
        tk.Entry(
        form, textvariable=teacher_id_var,
        font=("Arial", 14), width=25, state="readonly"
        ).grid(row=0, column=1, padx=10, pady=10)

        # ---------- Date ----------
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")

        tk.Label(
        form, text="Date:", font=("Arial", 14), bg="#ECF0F1"
        ).grid(row=1, column=0, padx=10, pady=10, sticky="e")
   
        date_var = tk.StringVar(value=today)
        tk.Entry(
        form, textvariable=date_var,
        font=("Arial", 14), width=25, state="readonly"
        ).grid(row=1, column=1, padx=10, pady=10)

        # ---------- STATUS ----------
        tk.Label(
        form, text="Current Status:", font=("Arial", 14), bg="#ECF0F1"
        ).grid(row=2, column=0, padx=10, pady=10, sticky="e")

        status_var = tk.StringVar(value="Fetching...")
        tk.Entry(
        form, textvariable=status_var,
        font=("Arial", 14), width=25, state="readonly"
        ).grid(row=2, column=1, padx=10, pady=10)

        self.content.update_idletasks()

        # ---------- CHECK OUT BUTTON ----------
        checkout_btn = tk.Label(
        self.content,
        text="Check Out",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=30,
        pady=12,
        width=14,
        cursor="arrow")
        checkout_btn.pack(pady=20)

        def enable_btn():
            checkout_btn.config(bg="#000000", fg="white", cursor="hand2")
            checkout_btn.bind("<Enter>", lambda e: checkout_btn.config(bg="#222222"))
            checkout_btn.bind("<Leave>", lambda e: checkout_btn.config(bg="#000000"))
            checkout_btn.bind("<Button-1>", lambda e: do_checkout())

        def disable_btn():
            checkout_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            checkout_btn.unbind("<Enter>")
            checkout_btn.unbind("<Leave>")
            checkout_btn.unbind("<Button-1>")

        disable_btn()

        # ---------- FETCH TODAY ATTENDANCE ----------
        def fetch_today_attendance():
            import requests
            try:
                res = requests.get(
                f"http://127.0.0.1:8000/teacher/attendance/today/{self.teacher_id}"
                )

                if res.status_code != 200:
                    status_var.set("Not Marked")
                    return

                data = res.json()
                self.today_record_id = data["record_id"]

                if data["check_out"]:
                    status_var.set("Checked Out")
                    disable_btn()
                else:
                    status_var.set(data["status"])
                    enable_btn()

            except Exception as e:
                status_var.set("Error")

        fetch_today_attendance()

        # ---------- CHECK OUT ----------
        def do_checkout():
            import requests
            try:
                res = requests.put(
                f"http://127.0.0.1:8000/teacher/attendance/check-out/{self.today_record_id}"
                )

                if res.status_code == 200:
                    self.show_popup(
                    "Success",
                    "Check-out successful!",
                    "info")
                    self.change_screen(
                        "Check-out successful!",
                        add_callback=self.load_teacher_check_out_screen
                        )
                    return

                if res.status_code == 400:
                    self.show_popup(
                    "Already Checked Out",
                    "You have already checked out.",
                    "warning"
                    )
                    return

                if res.status_code == 404:
                    self.show_popup(
                    "Not Found",
                    "Attendance record not found.",
                    "error"
                    )
                    disable_btn()
                    return

                self.show_popup("Error", res.text, "error")

            except Exception as e:
                self.show_popup("Backend Error", str(e), "error")

        # ---------- BACK ----------
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(pady=10)

        self.create_back_button(
        parent=back_frame,
        go_back_callback=self.load_dashboard,
        form_frame=form
        )


    # ==========================================================================
    # ===== Button to View Filtered Teacher Attendance by Date =====
    def load_teacher_attendance_filter(self):
        self.clear_content()

        # ---------- TITLE ----------
        tk.Label(
        self.content,
        text="Filter My Attendance",
        font=("Arial", 24, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # ---------- FORM ----------
        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # Teacher ID (readonly)
        tk.Label(form, text="Teacher ID:", font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=0, padx=10, pady=10)
        teacher_id_var = tk.StringVar(value=str(self.teacher_id))
        tk.Entry(form, textvariable=teacher_id_var, font=("Arial", 14), width=25, state="readonly").grid(row=0, column=1)

        # Date From
        tk.Label(
        form,
        text="Date From (YYYY-MM-DD):",
        font=("Arial", 14),
        bg="#ECF0F1"
        ).grid(row=1, column=0, padx=10)

        date_from_var = tk.StringVar()

        date_from_entry = tk.Entry(
        form,
        textvariable=date_from_var,
        font=("Arial", 14),
        width=25)
        date_from_entry.grid(row=1, column=1)

        tk.Button(
        form,
        text="Calendar",
        command=lambda: self.open_calendar_popup(date_from_entry, date_from_var)
        ).grid(row=1, column=2, padx=5)

        # Date To
        tk.Label(
        form,
        text="Date To (YYYY-MM-DD):",
        font=("Arial", 14),
        bg="#ECF0F1"
        ).grid(row=2, column=0, padx=10)

        date_to_var = tk.StringVar()

        date_to_entry = tk.Entry(
        form,
        textvariable=date_to_var,
        font=("Arial", 14),
        width=25)
        date_to_entry.grid(row=2, column=1)

        tk.Button(
        form,
        text="Calendar",
        command=lambda: self.open_calendar_popup(date_to_entry, date_to_var)
        ).grid(row=2, column=2, padx=5)

        # ---------- FILTER BUTTON ----------
        filter_btn = tk.Label(
        self.content,
        text="Filter Attendance",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20, pady=12,
        width=18,
        cursor="arrow"
        )
        filter_btn.pack(pady=15)

        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=20)

        # Back button
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,
        form_frame=form
        )

        def enable_btn():
            filter_btn.config(bg="#000000", fg="white", cursor="hand2")
            filter_btn.bind("<Enter>", lambda e: filter_btn.config(bg="#222222"))
            filter_btn.bind("<Leave>", lambda e: filter_btn.config(bg="#000000"))
            filter_btn.bind("<Button-1>", lambda e: fetch_records())

        def disable_btn():
            filter_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            filter_btn.unbind("<Enter>")
            filter_btn.unbind("<Leave>")
            filter_btn.unbind("<Button-1>")

        disable_btn()

        # ---------- VALIDATION ----------
        def validate(*args):
            import re
            r = r"^\d{4}-\d{2}-\d{2}$"
            d1 = date_from_var.get().strip()
            d2 = date_to_var.get().strip()

            if not d1 or not d2:
                disable_btn()
                return

            if not re.match(r, d1) or not re.match(r, d2):
                disable_btn()
                return
            
            if d1 > d2:
                disable_btn()
                return

            enable_btn()

        date_from_var.trace_add("write", validate)
        date_to_var.trace_add("write", validate)

        # ---------- RESULTS TABLE ----------
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True)

        cols = ("record_id", "date", "check_in", "status", "remarks")

        tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)
        tree.pack(fill="both", expand=True)

        for col in cols:
            tree.heading(col, text=col.replace("_", " ").title())
            tree.column(col, width=140, anchor="center")

        # ---------- FETCH FUNCTION ----------
        def fetch_records():
            tid = teacher_id_var.get()
            d1 = date_from_var.get()
            d2 = date_to_var.get()

            try:
                url = f"http://127.0.0.1:8000/teacher/attendance/self/{tid}?date_from={d1}&date_to={d2}"
                res = requests.get(url)

                if res.status_code != 200:
                    self.show_popup("Error", "Could not fetch attendance!", "error")
                    return
                
                if res.status_code == 404:
                    self.show_popup("No Records", "No attendance found for selected dates.", "info")
                    return

                rows = res.json()

                # clear table
                for r in tree.get_children():
                    tree.delete(r)

                # fill table
                for r in rows:
                    tree.insert("", "end", values=(
                        r.get("record_id", ""),
                        r.get("date", ""),
                        r.get("check_in", ""),
                        r.get("status", ""),
                        r.get("remarks", "")
                    ))

            except Exception as e:
                self.show_popup("Error", str(e), "error")
 
    # ==========================================================================
    # ===== Button to View Teacher Attendance Summary =====
    def load_teacher_attendance_summary_screen(self):
        self.clear_content()

        # ---- TITLE ----
        tk.Label(
        self.content,
        text="Teacher Attendance Summary",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # ---- FORM FRAME ----
        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # ====== FIELDS ======

        # Teacher ID
        tk.Label(
        form,
        text="Teacher ID:",
        font=("Arial", 14),
        bg="#ECF0F1"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        teacher_id_var = tk.StringVar(value=str(self.teacher_id))
        teacher_id_entry = tk.Entry(
            form,
            textvariable=teacher_id_var,
            font=("Arial", 14),
            width=25,
            state="disabled",
            disabledbackground="#F2F3F4",
            disabledforeground="black"
        )
        teacher_id_entry.grid(row=0, column=1, padx=10, pady=10)

        # Date From
        tk.Label(
            form,
            text="Date From (YYYY-MM-DD):",
            font=("Arial", 14),
            bg="#ECF0F1"
            ).grid(row=1, column=0, padx=10, pady=10, sticky="w")

        date_from_var = tk.StringVar()
        date_from_entry = tk.Entry(form, textvariable=date_from_var, font=("Arial", 14), width=25)
        date_from_entry.grid(row=1, column=1, padx=10, pady=10)

        # Calendar button for Date From
        tk.Button(
            form,
            text="Calendar",
            command=lambda: self.open_calendar_popup(date_from_entry, date_from_var)
            ).grid(row=1, column=2, padx=5)

        # Date To
        tk.Label(
            form,
            text="Date To (YYYY-MM-DD):",
            font=("Arial", 14),
            bg="#ECF0F1"
            ).grid(row=2, column=0, padx=10, pady=10, sticky="w")

        date_to_var = tk.StringVar()
        date_to_entry = tk.Entry(form, textvariable=date_to_var, font=("Arial", 14), width=25)
        date_to_entry.grid(row=2, column=1, padx=10, pady=10)

        # Calendar button for Date To
        tk.Button(
            form,
            text="Calendar",
            command=lambda: self.open_calendar_popup(date_to_entry, date_to_var)
            ).grid(row=2, column=2, padx=5)

        # ---- BACK BUTTON ----
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(pady=10)
        self.create_back_button(back_frame, self.load_dashboard, form)

        # ---- SUBMIT BUTTON (disabled initially) ----
        submit_btn = tk.Label(
        self.content,
        text="Get Summary",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=12,
        width=15,
        relief="ridge",
        cursor="arrow")
        submit_btn.pack(pady=15)

        # ---- BUTTON ENABLE/DISABLE ----
        def enable_btn():
            submit_btn.config(bg="#000000", fg="white", cursor="hand2")
            submit_btn.bind("<Enter>", lambda e: submit_btn.config(bg="#222222"))
            submit_btn.bind("<Leave>", lambda e: submit_btn.config(bg="#000000"))
            submit_btn.bind("<Button-1>", lambda e: fetch_summary())

        def disable_btn():
            submit_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            submit_btn.unbind("<Enter>")
            submit_btn.unbind("<Leave>")
            submit_btn.unbind("<Button-1>")

        disable_btn()

        # ---- VALIDATION ----
        def validate(*args):
            import re
            d1 = date_from_var.get().strip()
            d2 = date_to_var.get().strip()

            # Date format check
            date_regex = r"^\d{4}-\d{2}-\d{2}$"
            if not re.match(date_regex, d1) or not re.match(date_regex, d2):
                disable_btn()
                return
            
            if not d1 or not d2:
                disable_btn()
                return
            
            if d1 > d2:
                disable_btn()
                return

            enable_btn()

        date_from_var.trace_add("write", validate)
        date_to_var.trace_add("write", validate)

        # ---- SUMMARY BOX FRAME ----
        summary_frame = tk.Frame(self.content, bg="#ECF0F1")
        summary_frame.pack(pady=20)

        # ---- FETCH SUMMARY FUNCTION ----
        def fetch_summary():
            tid = teacher_id_var.get().strip()
            d1 = date_from_var.get().strip()
            d2 = date_to_var.get().strip()

            try:
                url = f"http://127.0.0.1:8000/teacher/attendance/summary/{tid}?date_from={d1}&date_to={d2}"
                res = requests.get(url)

                if res.status_code != 200:
                    self.show_popup("Error", "Failed to fetch summary.", "error")
                    return

                data = res.json()

                # Clear old summary
                for widget in summary_frame.winfo_children():
                    widget.destroy()

                # ===== SHOW SUMMARY =====
                def make_card(label, value, row):
                    tk.Label(
                    summary_frame,
                    text=label,
                    font=("Arial", 14, "bold"),
                    bg="#ECF0F1",
                    fg="#2C3E50"
                    ).grid(row=row, column=0, padx=10, pady=5, sticky="e")

                    tk.Label(
                    summary_frame,
                    text=value,
                    font=("Arial", 14),
                    bg="#ECF0F1",
                    fg="#000000"
                    ).grid(row=row, column=1, padx=10, pady=5, sticky="w")

                total = data["total_days"]
                present = data["present_days"]
                absent = data["absent_days"]
                late = data["late_days"]
                leave = data["leave_days"]

                percentage = round((present / total) * 100, 2) if total else 0

                make_card("Total Days:", total, 0)
                make_card("Present:", present, 1)
                make_card("Absent:", absent, 2)
                make_card("Late:", late, 3)
                make_card("Leave:", leave, 4)
                make_card("Attendance %:", f"{percentage}%", 5)

                self.show_popup("Success", "Summary Loaded!", "info")

            except Exception as e:
                self.show_popup("Backend Error", f"{e}", "error")
  
    
    # ==============================================================================
    # ----- Button to Generate and Download Result of a Student with Some Exam ID -----
    def load_view_and_download_exam_result_of_student(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="Generate & Download Result of a Student",
        font=("Arial", 24, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
    ).pack(pady=20)

        # ===== FORM FRAME =====
        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # -------- Inputs --------
        tk.Label(form, text="Student ID:", font=("Arial", 14), bg="#ECF0F1")\
        .grid(row=0, column=0, padx=10, pady=10, sticky="w")
        sid_var = tk.StringVar()
        tk.Entry(form, textvariable=sid_var, width=25, font=("Arial", 14))\
        .grid(row=0, column=1, padx=10, pady=10)

        tk.Label(form, text="Exam ID:", font=("Arial", 14), bg="#ECF0F1")\
        .grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        exam_var = tk.StringVar()

        available_exams = fetch_exams()
        self.exam_values = [
            f"{e['exam_id']} - {e['exam_name']}"
            for e in available_exams
        ]
        # Validation
        def validate(*args):
            sid = sid_var.get().strip()
            eid = exam_var.get().strip()

            if sid.isdigit() and eid:
                enable_fetch()
            else:
                disable_fetch()

        exam_dd = ttk.Combobox(
        form,
        textvariable=exam_var,
        font=("Arial", 14),
        width=23,
        state="readonly",
        values=self.exam_values
        )
        exam_dd.grid(row=1, column=1, padx=10, pady=10)
        exam_dd.bind("<<ComboboxSelected>>", validate)

        # ===== BACK BUTTON =====
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(pady=10)
        self.create_back_button(back_frame, self.load_dashboard, form)

        # ====== RESULT SUMMARY CARD FRAME ======
        summary_frame = tk.Frame(self.content, bg="#ECF0F1")
        summary_frame.pack(pady=20)

        summary_vars = {
        "Total Marks": tk.StringVar(),
        "Percentage": tk.StringVar(),
        "Grade": tk.StringVar()
    }

        # Create output card labels (disabled entries)
        for i, (label, var) in enumerate(summary_vars.items()):
            tk.Label(summary_frame, text=f"{label}:", font=("Arial", 14), bg="#ECF0F1")\
            .grid(row=i, column=0, padx=10, pady=6, sticky="e")

            tk.Entry(
            summary_frame,
            textvariable=var,
            font=("Arial", 14),
            width=30,
            state="disabled",
            disabledbackground="#F2F3F4",
            disabledforeground="black"
        ).grid(row=i, column=1, padx=10, pady=6)

        # ====== FETCH BUTTON ======
        fetch_btn = tk.Label(
        self.content,
        text="Generate Result",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20, pady=12,
        width=18,
        relief="ridge",
        cursor="arrow"
    )
        fetch_btn.pack(pady=10)

        # ====== DOWNLOAD BUTTON ======
        download_btn = tk.Label(
        self.content,
        text="Download Result",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20, pady=12,
        width=18,
        relief="ridge",
        cursor="arrow"
    )
        download_btn.pack(pady=10)

        # Disable download button initially
        def disable_download():
            download_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            download_btn.unbind("<Enter>")
            download_btn.unbind("<Leave>")
            download_btn.unbind("<Button-1>")

        disable_download()

        # ====== ENABLE / DISABLE FETCH BUTTON ======
        def enable_fetch():
            fetch_btn.config(bg="#000000", fg="white", cursor="arrow")
            fetch_btn.bind("<Enter>", lambda e: fetch_btn.config(bg="#222222"))
            fetch_btn.bind("<Leave>", lambda e: fetch_btn.config(bg="#000000"))
            fetch_btn.bind("<Button-1>", lambda e: fetch_result())

        def disable_fetch():
            fetch_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            fetch_btn.unbind("<Enter>")
            fetch_btn.unbind("<Leave>")
            fetch_btn.unbind("<Button-1>")

        disable_fetch()

        sid_var.trace_add("write", validate)
        exam_var.trace_add("write", validate)

        # ====== FETCH RESULT FUNCTION ======
        def fetch_result():
            sid = int(sid_var.get().strip())
            exam_raw = exam_var.get().strip()
            eid = int(exam_raw.split("-")[0].strip())

            import requests
            try:
                url = f"http://127.0.0.1:8000/admin/results/student/{sid}/{eid}"
                res = requests.get(url)
 
                if res.status_code != 200:
                    self.show_popup("Not Found", "Result not found!", "warning")
                    return

                data = res.json()

                summary_vars["Total Marks"].set(data["total_marks"])
                summary_vars["Percentage"].set(data["percentage"])
                summary_vars["Grade"].set(data["grade"])

                # Enable download button
                enable_download()

            except Exception as e:
                self.show_popup("Server Error", str(e), "error")

        # ====== ENABLE DOWNLOAD BUTTON ======
        def enable_download():
            download_btn.config(bg="#000000", fg="white", cursor="arrow")
            download_btn.bind("<Enter>", lambda e: download_btn.config(bg="#222222"))
            download_btn.bind("<Leave>", lambda e: download_btn.config(bg="#000000"))
            download_btn.bind("<Button-1>", lambda e: download_pdf())

        # ====== DOWNLOAD FUNCTION ======
        def download_pdf():
            sid = sid_var.get().strip()
            exam_raw = exam_var.get().strip()
            eid = int(exam_raw.split("-")[0].strip())

            import requests
            try:
                url = f"http://127.0.0.1:8000/admin/results/student/{sid}/{eid}/download"
                res = requests.get(url)

                if res.status_code != 200:
                    self.show_popup("Error", "Cannot download result!", "error")
                    return

                # Extract filename
                fname = f"result_{sid}_{eid}.pdf"
                if "content-disposition" in res.headers:
                    import re
                    cd = res.headers["content-disposition"]
                    match = re.findall('filename="?(.+)"?', cd)
                    if match:
                        fname = match[0]

                # Ask where to save
                from tkinter import filedialog
                save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                initialfile=fname,
                filetypes=[("PDF Files", "*.pdf")]
            )

                if not save_path:
                    return

                with open(save_path, "wb") as f:
                    f.write(res.content)

                self.show_mini_notification(f"Downloaded: {fname}")
                self.change_screen("Student's Result Downloaded Successfully!",
                                   add_callback=self.load_generate_and_download_result_of_student)
            except Exception as e:
                self.show_popup("Backend Error", str(e), "error")


    # ==============================================================================
    # ----- Button to View and Download Final Result of a Student -----
    def load_generate_and_download_final_result_of_student(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="Generate & Download Final Result of a Student",
        font=("Arial", 24, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # ===== FORM FRAME =====
        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # -------- Student ID Input --------
        tk.Label(
        form,
        text="Student ID:",
        font=("Arial", 14),
        bg="#ECF0F1"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        sid_var = tk.StringVar()
        tk.Entry(
        form,
        textvariable=sid_var,
        width=25,
        font=("Arial", 14)
        ).grid(row=0, column=1, padx=10, pady=10)

        # ===== BACK BUTTON =====
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(pady=5)
        self.create_back_button(back_frame, self.load_dashboard, form)

        # ===== SUMMARY FRAME (Output) =====
        summary_frame = tk.Frame(self.content, bg="#ECF0F1")
        summary_frame.pack(pady=20)

        summary_vars = {
        "Exam Count": tk.StringVar(),
        "Total Marks": tk.StringVar(),
        "Max Marks": tk.StringVar(),
        "Percentage": tk.StringVar(),
        "Final Grade": tk.StringVar()
        }

        # Create summary card layout
        for i, (label, var) in enumerate(summary_vars.items()):
            tk.Label(
            summary_frame,
            text=f"{label}:",
            font=("Arial", 14),
            bg="#ECF0F1"
        ).grid(row=i, column=0, padx=10, pady=6, sticky="e")

            tk.Entry(
            summary_frame,
            textvariable=var,
            font=("Arial", 14),
            width=30,
            state="disabled",
            disabledbackground="#F2F3F4",
            disabledforeground="black"
        ).grid(row=i, column=1, padx=10, pady=6)

        # ---- Exam-wise result area ----
        tk.Label(
        summary_frame,
        text="Exam-wise Details:",
        font=("Arial", 14, "bold"),
        bg="#ECF0F1"
        ).grid(row=len(summary_vars), column=0, columnspan=2, pady=10)

        exam_list_box = tk.Text(
        summary_frame,
        width=60,
        height=10,
        font=("Arial", 12),
        state="disabled",
        bg="#F2F3F4"
        )
        exam_list_box.grid(row=len(summary_vars) + 1, column=0, columnspan=2, padx=10, pady=5)

        # ====== FETCH BUTTON ======
        fetch_btn = tk.Label(
        self.content,
        text="Generate Final Result",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=12,
        width=20,
        relief="ridge",
        cursor="arrow"
    )
        fetch_btn.pack(pady=5)

        # ====== DOWNLOAD BUTTON ======
        download_btn = tk.Label(
        self.content,
        text="Download Final Result",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=12,
        width=20,
        relief="ridge",
        cursor="arrow"
    )
        download_btn.pack(pady=5)

        # disable until generated
        def disable_download():
            download_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            download_btn.unbind("<Enter>")
            download_btn.unbind("<Leave>")
            download_btn.unbind("<Button-1>")

        disable_download()

        # ====== ENABLE FETCH BUTTON ======
        def enable_fetch():
            fetch_btn.config(bg="#000000", fg="white", cursor="arrow")
            fetch_btn.bind("<Enter>", lambda e: fetch_btn.config(bg="#222222"))
            fetch_btn.bind("<Leave>", lambda e: fetch_btn.config(bg="#000000"))
            fetch_btn.bind("<Button-1>", lambda e: fetch_result())

        def disable_fetch():
            fetch_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            fetch_btn.unbind("<Enter>")
            fetch_btn.unbind("<Leave>")
            fetch_btn.unbind("<Button-1>")

        disable_fetch()

        # ====== VALIDATION ======
        def validate(*args):
            sid = sid_var.get().strip()

            if sid.isdigit() and int(sid) > 0:
                enable_fetch()
            else:
                disable_fetch()

        sid_var.trace_add("write", validate)

        # ====== FETCH RESULT FUNCTION ======
        def fetch_result():
            sid = sid_var.get().strip()

            import requests
            try:
                url = f"http://127.0.0.1:8000/admin/results/final/{sid}"
                res = requests.get(url)

                if res.status_code != 200:
                    self.show_popup("Not Found", "No results found for this student!", "warning")
                    return

                data = res.json()

                # Fill summary card
                summary_vars["Exam Count"].set(data["exam_count"])
                summary_vars["Total Marks"].set(data["total_marks"])
                summary_vars["Max Marks"].set(data["max_marks"])
                summary_vars["Percentage"].set(data["percentage"])
                summary_vars["Final Grade"].set(data["final_grade"])

                # Fill exam-wise details
                exam_list_box.config(state="normal")
                exam_list_box.delete("1.0", tk.END)
                for e in data["exam_wise_details"]:
                    exam_list_box.insert(
                        tk.END,
                        f"Exam {e['exam_id']} : Marks: {e['obtained_marks']} / {e['max_marks']} | Grade: {e['grade']}\n"
                    )

                exam_list_box.config(state="disabled")

                # enable download
                enable_download()

            except Exception as e:
                self.show_popup("Server Error", str(e), "error")

        # ====== ENABLE DOWNLOAD BUTTON ======
        def enable_download():
            download_btn.config(bg="#000", fg="white", cursor="hand2")
            download_btn.bind("<Enter>", lambda e: download_btn.config(bg="#222"))
            download_btn.bind("<Leave>", lambda e: download_btn.config(bg="#000"))
            download_btn.bind("<Button-1>", lambda e: download_pdf())

        # ====== DOWNLOAD FUNCTION ======
        def download_pdf():
            sid = sid_var.get().strip()

            import requests
            try:
                url = f"http://127.0.0.1:8000/admin/results/final/download/{sid}"
                res = requests.get(url)

                if res.status_code != 200:
                    self.show_popup("Error", "Cannot download final result!", "error")
                    return

                # Extract filename
                fname = f"student_{sid}_final_result.pdf"
                if "content-disposition" in res.headers:
                    import re
                    cd = res.headers["content-disposition"]
                    match = re.findall(r'filename="?(.+)"?', cd)
                    if match:
                        fname = match[0]

                # Ask save location
                from tkinter import filedialog
                save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                initialfile=fname,
                filetypes=[("PDF Files", "*.pdf")]
            )

                if not save_path:
                    return

                with open(save_path, "wb") as f:
                    f.write(res.content)

                self.show_mini_notification(f"Downloaded: {fname}")
                self.change_screen(f"PDF of Final Result of Student ID {sid} Downloaded Successfully!",
                                   add_callback=self.load_generate_and_download_final_result_of_student)

            except Exception as e:
                self.show_popup("Backend Error", str(e), "error")

    
    # ==============================================================================
    # ----- Button to View all Results for an Exam -----
    def load_view_all_results_for_exam(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="View All Results for an Exam",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # ===== FORM FRAME =====
        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        tk.Label(
        form,
        text="Exam ID:",
        font=("Arial", 14),
        bg="#ECF0F1"
        ).grid(row=0, column=0, padx=10, pady=10)

        exam_var = tk.StringVar()

        # fetch exams
        available_exams = fetch_exams()

        # dropdown values: "id – name"
        self.exam_values = [
            f"{e['exam_id']} - {e['exam_name']}"
            for e in available_exams
        ]

        exam_dropdown = ttk.Combobox(
        form,
        textvariable=exam_var,
        font=("Arial", 14),
        width=23,
        state="readonly",
        values=self.exam_values
        )
        exam_dropdown.grid(row=0, column=1, padx=10, pady=10)

        # ===== BACK BUTTON =====
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)
        self.create_back_button(back_frame, self.load_dashboard, form)

        # ===== TABLE FRAME =====
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        cols = ("result_id", "student_id", "obtained_marks",
                "total_marks", "percentage", "grade", "result_status")

        # Scrollbars
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        self.result_tree = ttk.Treeview(
        table_frame,
        columns=cols,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
    )
        self.result_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.result_tree.yview)
        x_scroll.config(command=self.result_tree.xview)

        # Configure headings
        for col in cols:
            self.result_tree.heading(col, text=col.replace("_", " ").title())
            self.result_tree.column(col, width=180, anchor="center")

        # ===== LOAD BUTTON =====
        load_btn = tk.Label(
        self.content,
        text="Load Results",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=12,
        width=16,
        relief="ridge",
        cursor="arrow"
    )
        load_btn.pack(pady=10)

        def enable_load():
            load_btn.config(bg="#000000", fg="white", cursor="arrow")
            load_btn.bind("<Enter>", lambda e: load_btn.config(bg="#222222"))
            load_btn.bind("<Leave>", lambda e: load_btn.config(bg="#000000"))
            load_btn.bind("<Button-1>", lambda e: load_results())

        def disable_load():
            load_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            load_btn.unbind("<Enter>")
            load_btn.unbind("<Leave>")
            load_btn.unbind("<Button-1>")

        disable_load()

        # ===== VALIDATION =====
        def validate(*args):
            if exam_var.get().strip() in self.exam_values:
                enable_load()
            else:
                disable_load()

        exam_var.trace_add("write", validate)


        # ===== LOAD RESULTS FUNCTION =====
        def load_results():
            exam_raw = exam_var.get().strip()
            exam_id = exam_raw.split("-")[0].strip()

            import requests
            try:
                url = f"http://127.0.0.1:8000/admin/results/exam/{exam_id}"
                res = requests.get(url)
  
                if res.status_code != 200:
                    self.show_popup("Not Found", "No results found for this Exam ID!", "warning")
                    return

                data = res.json()

                # insert into table
                for row in self.result_tree.get_children():
                    self.result_tree.delete(row)

                for r in data:
                    self.result_tree.insert(
                    "",
                    "end",
                    values=(
                        r["result_id"],
                        r["student_id"],
                        r["obtained_marks"],
                        r["total_marks"],
                        r["percentage"],
                        r["grade"],
                        r["result_status"]
                    )
                )

            except Exception as e:
                self.show_popup("Server Error", str(e), "error")


    # ==============================================================================
    # ----- Button to Generate and Download Results of all Students of a class with Some Exam ID ------
    def load_view_and_download_all_students_results_for_a_class(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="View & Download All Students' Results for a Class",
        font=("Arial", 24, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # ===== FORM =====
        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        tk.Label(form, text="Class ID:", font=("Arial", 14), bg="#ECF0F1")\
        .grid(row=0, column=0, padx=10, pady=8, sticky="e")
        tk.Label(form, text="Exam ID:", font=("Arial", 14), bg="#ECF0F1")\
        .grid(row=1, column=0, padx=10, pady=8, sticky="e")

        class_var = tk.StringVar()
        exam_var = tk.StringVar()
        
        # ===== FETCH DROPDOWN DATA =====
        available_classes = fetch_classes()
        available_exams = fetch_exams()

        self.class_values = [
            f"{c['class_id']} - {c['class_name']} {c['section']}"
            for c in available_classes
        ]

        self.exam_values = [
            f"{e['exam_id']} - {e['exam_name']}"
            for e in available_exams
        ]
        
        class_dd = ttk.Combobox(
        form,
        textvariable=class_var,
        font=("Arial", 14),
        width=23,
        state="readonly",
        values=self.class_values
        )
        class_dd.grid(row=0, column=1, padx=10, pady=8)
        
        exam_dd = ttk.Combobox(
        form,
        textvariable=exam_var,
        font=("Arial", 14),
        width=23,
        state="readonly",
        values=self.exam_values
        )
        exam_dd.grid(row=1, column=1, padx=10, pady=8)

        # BACK BUTTON
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)
        self.create_back_button(back_frame, self.load_dashboard, form)

        # ===== TABLE FRAME =====
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=15)

        cols = ("student_id", "full_name", "obtained_marks", "total_marks", "percentage", "grade", "result_status")

        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        self.class_results_tree = ttk.Treeview(
        table_frame,
        columns=cols,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
    )
        self.class_results_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.class_results_tree.yview)
        x_scroll.config(command=self.class_results_tree.xview)

        # Setup columns
        for col in cols:
            self.class_results_tree.heading(col, text=col.replace("_", " ").title())
            self.class_results_tree.column(col, width=170, anchor="center")

        # ===== BUTTONS =====
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=20)

        load_btn = tk.Label(
        btn_frame, text="Load Results",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC", fg="#AEB6BF",
        padx=20, pady=10, width=15,
        relief="ridge", cursor="arrow"
    )
        load_btn.grid(row=0, column=0, padx=15)

        download_btn = tk.Label(
        btn_frame, text="Download All (ZIP)",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC", fg="#AEB6BF",
        padx=20, pady=10, width=18,
        relief="ridge", cursor="arrow"
    )
        download_btn.grid(row=0, column=1, padx=15)

        # ===== BUTTON ENABLE/DISABLE =====
        def enable(btn):
            btn.config(bg="#000", fg="white", cursor="hand2")
            btn.bind("<Enter>", lambda e: btn.config(bg="#222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000"))

        def disable(btn):
            btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            btn.unbind("<Enter>"); btn.unbind("<Leave>")

        disable(load_btn)
        disable(download_btn)

        # ===== VALIDATION =====
        def validate(*args):
            if (
                class_var.get().strip() in self.class_values
                and exam_var.get().strip() in self.exam_values
            ):
                enable(load_btn)
                enable(download_btn)
                load_btn.bind("<Button-1>", lambda e: load_results())
                download_btn.bind("<Button-1>", lambda e: download_zip())
            else:
                disable(load_btn)
                disable(download_btn)

        class_var.trace_add("write", validate)
        exam_var.trace_add("write", validate)

        # ===== LOAD RESULTS FUNCTION =====
        def load_results():
            self.show_mini_notification("Loading results, please wait…")

            class_raw = class_var.get().strip()
            exam_raw = exam_var.get().strip()

            class_id = int(class_raw.split("-")[0].strip())
            exam_id = int(exam_raw.split("-")[0].strip())


            # Clear table
            for item in self.class_results_tree.get_children():
                self.class_results_tree.delete(item)

            import requests
            url = f"http://127.0.0.1:8000/admin/results/exam/{exam_id}"

            try:
                res = requests.get(url)
                if res.status_code != 200:
                    self.show_popup("Error", "No results found for this exam!", "error")
                    return
    
                all_results = res.json()

                # filter only this class
                for r in all_results:
                    # Fetching student info
                    stu = requests.get(f"http://127.0.0.1:8000/admin/results/students/{r['student_id']}")
                    if stu.status_code != 200:
                        continue

                    stu_data = stu.json()
                    if stu_data["class_id"] != int(class_id):
                        continue

                    self.class_results_tree.insert(
                    "", "end",
                    values=(
                        r["student_id"],
                        stu_data["full_name"],
                        r["obtained_marks"],
                        r["total_marks"],
                        r["percentage"],
                        r["grade"],
                        r["result_status"]
                    )
                )

            except Exception as e:
                self.show_popup("Error", str(e), "error")

        # ===== DOWNLOAD ZIP FUNCTION =====
        def download_zip():
            class_raw = class_var.get().strip()
            exam_raw = exam_var.get().strip()

            class_id = int(class_raw.split("-")[0].strip())
            exam_id = int(exam_raw.split("-")[0].strip())


            import requests
            try:
                url = f"http://127.0.0.1:8000/admin/results/download/class/{class_id}/{exam_id}"
                res = requests.get(url)

                if res.status_code != 200:
                    self.show_popup("Error", "No results available to download!", "error")
                    return

                # Ask save location
                from tkinter import filedialog
                file_path = filedialog.asksaveasfilename(
                defaultextension=".zip",
                filetypes=[("ZIP Files", "*.zip")],
                initialfile=f"class_{class_id}_exam_{exam_id}_results.zip"
            )

                if not file_path:
                    return

                with open(file_path, "wb") as f:
                    f.write(res.content)

                self.show_mini_notification("ZIP Downloaded Successfully!")
                self.change_screen(f"Downloaded Results of all Students for Class ID {class_id} Based on Exam ID {exam_id}",
                                   add_callback=self.load_view_and_download_all_students_results_for_a_class)

            except Exception as e:
                self.show_popup("Error", str(e), "error")


    # ==============================================================================
    # ----- Button to Generate and Download Final Results of a class -----
    def load_generate_and_download_all_final_results_for_a_class(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="Generate & Download Final Results for a Class",
        font=("Arial", 24, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
    ).pack(pady=20)

        # ===== FORM =====
        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        tk.Label(form, text="Class ID:", font=("Arial", 14), bg="#ECF0F1")\
        .grid(row=0, column=0, padx=10, pady=8, sticky="e")

        class_var = tk.StringVar()

        # ===== FETCH CLASSES FOR DROPDOWN =====
        available_classes = fetch_classes()

        self.class_map = {
        f"{c['class_id']} - {c['class_name']} {c['section']}": c["class_id"]
        for c in available_classes
        }
        self.class_values = list(self.class_map.keys())

        class_dd = ttk.Combobox(
        form,
        textvariable=class_var,
        font=("Arial", 14),
        width=23,
        state="readonly",
        values=self.class_values
        )
        class_dd.grid(row=0, column=1, padx=10, pady=8)

        # BACK BUTTON
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)
        self.create_back_button(back_frame, self.load_dashboard, form)

        # ===== TABLE FRAME =====
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=15)

        cols = ("student_id", "full_name", "total_marks", "max_marks", "percentage", "final_grade")

        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        self.final_results_tree = ttk.Treeview(
        table_frame,
        columns=cols,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
    )
        self.final_results_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.final_results_tree.yview)
        x_scroll.config(command=self.final_results_tree.xview)

        for col in cols:
            self.final_results_tree.heading(col, text=col.replace("_", " ").title())
            self.final_results_tree.column(col, width=160, anchor="center")

        # ===== BUTTONS =====
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=20)

        load_btn = tk.Label(
        btn_frame, text="Generate Final Results",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC", fg="#AEB6BF",
        padx=20, pady=10, width=20,
        relief="ridge", cursor="arrow"
    )
        load_btn.grid(row=0, column=0, padx=20)

        download_btn = tk.Label(
        btn_frame, text="Download All (ZIP)",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC", fg="#AEB6BF",
        padx=20, pady=10, width=18,
        relief="ridge", cursor="arrow"
    )
        download_btn.grid(row=0, column=1, padx=20)

        # ===== ENABLE / DISABLE BUTTONS =====
        def enable(btn):
            btn.config(bg="#000000", fg="white", cursor="arrow")
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

        def disable(btn):
            btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            btn.unbind("<Enter>"); btn.unbind("<Leave>")

        disable(load_btn)
        disable(download_btn)

        # ===== VALIDATION =====
        def validate(*args):
            if class_var.get().strip() in self.class_values:
                enable(load_btn)
                enable(download_btn)
                load_btn.bind("<Button-1>", lambda e: load_results())
                download_btn.bind("<Button-1>", lambda e: download_zip())
            else:
                disable(load_btn)
                disable(download_btn)

        class_var.trace_add("write", validate)

        # ===== LOAD FINAL RESULTS (TABLE VIEW) =====
        def load_results():
            class_id = self.class_map[class_var.get()]

            # Clear table
            for item in self.final_results_tree.get_children():
                self.final_results_tree.delete(item)

            import requests

            try:
                # Step 1: get all students of the class
                stu_res = requests.get(f"http://127.0.0.1:8000/admin/master/students/class/{class_id}")
                if stu_res.status_code != 200:
                    self.show_popup("Error", "No active students in this class!", "error")
                    return

                students = stu_res.json()

                # Step 2: For each student fetch FINAL RESULT
                for stu in students:
                    sid = stu["student_id"]
                    res = requests.get(f"http://127.0.0.1:8000/admin/results/final/{sid}")

                    if res.status_code != 200:
                        continue  # skip students with no results

                    r = res.json()

                    self.final_results_tree.insert(
                    "", "end",
                    values=(
                        r["student_id"],
                        stu["full_name"],
                        r["total_marks"],
                        r["max_marks"],
                        r["percentage"],
                        r["final_grade"]
                    )
                )

            except Exception as e:
                self.show_popup("Error", str(e), "error")

        # ===== DOWNLOAD FINAL RESULTS ZIP =====
        def download_zip():
            class_raw = class_var.get().strip()
            class_id = int(class_raw.split("-")[0].strip())

            import requests
            try:
                url = f"http://127.0.0.1:8000/admin/results/final/download/class/{class_id}"
                res = requests.get(url)
 
                if res.status_code != 200:
                    self.show_popup("Error", "Unable to generate ZIP!", "error")
                    return

                # File dialog
                from tkinter import filedialog
                file_path = filedialog.asksaveasfilename(
                defaultextension=".zip",
                filetypes=[("ZIP Files", "*.zip")],
                initialfile=f"class_{class_id}_final_results.zip"
            )

                if not file_path:
                    return

                with open(file_path, "wb") as f:
                    f.write(res.content)

                self.show_mini_notification("Final Results ZIP Downloaded!")
                self.change_screen(f"Successfully Downloaded all Final Results for Class ID {class_id}",
                                   add_callback=self.load_generate_and_download_all_final_results_for_a_class)

            except Exception as e:
                self.show_popup("Error", str(e), "error")


    # ==============================================================================
    # ----- Button to Add Marks of Single Student ------   
    def load_add_single_student_marks(self):
        self.clear_content()

        # ---------- TITLE ----------
        tk.Label(
        self.content,
        text="Add Student Marks",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)
 
        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        from tkinter.ttk import Combobox
        import requests

        self.marks_vars = {}

        fields = [
        ("Class", "class_id"),
        ("Subject", "subject_id"),
        ("Exam", "exam_id"),
        ("Student ID", "student_id"),
        ("Max Marks", "max_marks"),
        ("Marks Obtained", "marks_obtained"),
        ("Remarks", "remarks")
        ]

        # ---------- FETCH DATA ----------
        classes = fetch_classes()
        exams = fetch_exams()

        self.class_map = {
        f"{c['class_name']} - {c['section']}": c["class_id"]
        for c in classes
        }

        self.exam_map = {e["exam_name"]: e["exam_id"] for e in exams}
        self.subject_map = {}

        for i, (label, key) in enumerate(fields):
            tk.Label(
            form,
            text=label + ":",
            font=("Arial", 14),
            bg="#ECF0F1"
            ).grid(row=i, column=0, padx=10, pady=10, sticky="e")

            var = tk.StringVar()
            self.marks_vars[key] = var

            if key == "class_id":
                cb = Combobox(
                form,
                textvariable=var,
                values=list(self.class_map.keys()),
                state="readonly",
                width=26)
                cb.grid(row=i, column=1)

            elif key == "subject_id":
                self.subject_cb = Combobox(
                form,
                textvariable=var,
                state="disabled",
                width=26)
                self.subject_cb.grid(row=i, column=1)

            elif key == "exam_id":
                cb = Combobox(
                form,
                textvariable=var,
                values=list(self.exam_map.keys()),
                state="readonly",
                width=26)
                cb.grid(row=i, column=1)

            else:
                tk.Entry(
                form,
                textvariable=var,
                font=("Arial", 14),
                width=28).grid(row=i, column=1)

        # ---------- LOAD SUBJECTS ----------
        def on_class_change(*args):
            class_val = self.marks_vars["class_id"].get()
            if class_val not in self.class_map:
                return

            class_id = self.class_map[class_val]
            res = requests.get(f"http://127.0.0.1:8000/classes/{class_id}/subjects")

            if res.status_code != 200:
                return

            subjects = res.json()
            self.subject_map = {
            s["subject_name"]: s["subject_id"] for s in subjects
            }

            self.subject_cb.config(
            values=list(self.subject_map.keys()),
            state="readonly"
            )
            self.marks_vars["subject_id"].set("")

        self.marks_vars["class_id"].trace_add("write", on_class_change)

        # ---------- SUBMIT ----------
        submit_btn = tk.Label(
        self.content,
        text="Submit",
        font=("Arial", 16, "bold"),
        bg="#000000",
        fg="white",
        padx=25,
        pady=12,
        cursor="hand2")
        submit_btn.pack(pady=20)

        def submit_marks():
            try:
                payload = {
                "student_id": int(self.marks_vars["student_id"].get()),
                "subject_id": self.subject_map[self.marks_vars["subject_id"].get()],
                "exam_id": self.exam_map[self.marks_vars["exam_id"].get()],
                "marks_obtained": float(self.marks_vars["marks_obtained"].get()),
                "max_marks": float(self.marks_vars["max_marks"].get()),
                "remarks": self.marks_vars["remarks"].get()
            }

                res = requests.post(
                "http://127.0.0.1:8000/teacher/results/marks/add",
                json=payload
            )

                if res.status_code == 200:
                    self.show_popup("Success", "Marks added successfully!", "info")
                    self.change_screen("Marks added successfully!", add_callback=self.load_add_single_student_marks)
                    return

                self.show_popup("Error", res.text, "error")

            except Exception as e:
                self.show_popup("Invalid Input", str(e), "error")

        submit_btn.bind("<Button-1>", lambda e: submit_marks())

        # ---------- BACK ----------
        back_row = tk.Frame(self.content, bg="#ECF0F1")
        back_row.pack(pady=10)

        self.create_back_button(back_row, self.load_dashboard, form_frame=form)         


    # ===================================================================
    # ----- Button to Add Marks in Bulk -----  
    def load_bulk_marks_entry_screen(self):
        self.clear_content()

        import requests
        from tkinter import ttk

        # ---------- TITLE ----------
        tk.Label(
        self.content,
        text="Bulk Marks Entry",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        self.bulk_marks_vars = {}
  
        # ---------- CLASS ----------
        tk.Label(form, text="Class:", font=("Arial", 14), bg="#ECF0F1")\
        .grid(row=0, column=0, padx=10, pady=10, sticky="e")

        class_var = tk.StringVar()
        self.bulk_marks_vars["class"] = class_var

        classes = fetch_classes()
        self.class_map = {
        f"{c['class_name']} - {c['section']}": c["class_id"]
        for c in classes
        }

        class_cb = ttk.Combobox(
        form,
        textvariable=class_var,
        values=list(self.class_map.keys()),
        state="readonly",
        width=25
        )
        class_cb.grid(row=0, column=1, padx=10, pady=10)

        # ---------- SUBJECT ----------
        tk.Label(form, text="Subject:", font=("Arial", 14), bg="#ECF0F1")\
        .grid(row=1, column=0, padx=10, pady=10, sticky="e")

        subject_var = tk.StringVar()
        self.bulk_marks_vars["subject"] = subject_var
        self.subject_map = {}

        subject_cb = ttk.Combobox(
        form,
        textvariable=subject_var,
        state="disabled",
        width=25
        )
        subject_cb.grid(row=1, column=1, padx=10, pady=10)

        # ---------- EXAM ----------
        tk.Label(form, text="Exam:", font=("Arial", 14), bg="#ECF0F1")\
        .grid(row=2, column=0, padx=10, pady=10, sticky="e")

        exam_var = tk.StringVar()
        self.bulk_marks_vars["exam"] = exam_var
        self.exam_map = {}

        exam_cb = ttk.Combobox(
        form,
        textvariable=exam_var,
        state="readonly",
        width=25
        )
        exam_cb.grid(row=2, column=1, padx=10, pady=10)

        # ---------- MAX MARKS ----------
        tk.Label(form, text="Max Marks:", font=("Arial", 14), bg="#ECF0F1")\
        .grid(row=3, column=0, padx=10, pady=10, sticky="e")

        max_marks_var = tk.StringVar()
        tk.Entry(form, textvariable=max_marks_var, font=("Arial", 14), width=27)\
        .grid(row=3, column=1, padx=10, pady=10)

        # ---------- LOAD EXAMS ----------
        try:
            res = requests.get("http://127.0.0.1:8000/admin/exams")
            exams = res.json()
            self.exam_map = {e["exam_name"]: e["exam_id"] for e in exams}
            exam_cb["values"] = list(self.exam_map.keys())
        except:
            pass

        # ---------- TABLE ----------
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, pady=20)

        cols = ("student_id", "student_name", "marks")
        tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=13)
        tree.pack(fill="both", expand=True)
 
        for c in cols:
            tree.heading(c, text=c.replace("_", " ").title())
            tree.column(c, width=180, anchor="center")

        marks_entries = {}

        # ---------- LOAD SUBJECTS ----------
        def on_class_change(*args):
            tree.delete(*tree.get_children())
            subject_cb.set("")
            subject_cb.config(state="disabled")

            class_id = self.class_map.get(class_var.get())
            if not class_id:
                return

            res = requests.get(
            f"http://127.0.0.1:8000/classes/{class_id}/subjects"
            )
            subjects = res.json()
            self.subject_map = {
            s["subject_name"]: s["subject_id"] for s in subjects
            }

            subject_cb["values"] = list(self.subject_map.keys())
            subject_cb.config(state="readonly")

        class_var.trace_add("write", on_class_change)

        # ---------- LOAD STUDENTS ----------
        def load_students(*args):
            tree.delete(*tree.get_children())
            marks_entries.clear()
  
            class_id = self.class_map.get(class_var.get())
            if not class_id:
                return

            res = requests.get(
            f"http://127.0.0.1:8000/classes/{class_id}/students"
            )
            students = res.json()
 
            for s in students:
                iid = tree.insert(
                "",
                "end",
                values=(s["student_id"], s["student_name"], "")
                )
                marks_entries[iid] = tk.StringVar()

        subject_var.trace_add("write", load_students)

        # ---------- SUBMIT ----------
        submit_btn = tk.Label(
        self.content,
        text="Submit Marks",
        font=("Arial", 16, "bold"),
        bg="#000000",
        fg="white",
        padx=25,
        pady=12,
        cursor="hand2"
        )
        submit_btn.pack(pady=10)

        def submit_bulk():
            try:
                payload = {
                "class_id": self.class_map[class_var.get()],
                "subject_id": self.subject_map[subject_var.get()],
                "exam_id": self.exam_map[exam_var.get()],
                "max_marks": float(max_marks_var.get()),
                "marks": []
            }

                for iid in tree.get_children():
                    student_id = int(tree.item(iid)["values"][0])
                    marks = tree.item(iid)["values"][2]

                    if marks == "":
                        continue

                    payload["marks"].append({
                    "student_id": student_id,
                    "marks_obtained": float(marks)
                    })

                res = requests.post(
                "http://127.0.0.1:8000/teacher/results/marks/add-bulk",
                json=payload
            )

                if res.status_code == 201:
                    self.show_popup("Success", "Marks entered successfully!", "info")
                    self.change_screen("Marks Added", add_callback=self.load_bulk_marks_entry_screen)
                    return

                self.show_popup("Error", res.text, "error")

            except Exception as e:
                self.show_popup("Error", str(e), "error")

        submit_btn.bind("<Button-1>", lambda e: submit_bulk())

        # ---------- BACK ----------
        back_row = tk.Frame(self.content, bg="#ECF0F1")
        back_row.pack(pady=10)

        self.create_back_button(back_row, self.load_dashboard, form_frame=form) 


    # ===================================================================
    #----- Button to Update marks of a student -----
    def load_update_student_marks_screen(self):
        self.clear_content()

        # ---------- TITLE ----------
        tk.Label(
        self.content,
        text="Update Student Marks",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        from tkinter.ttk import Combobox

        # ---------- VARIABLES ----------
        self.update_vars = {
        "class": tk.StringVar(),
        "subject": tk.StringVar(),
        "exam": tk.StringVar(),
        "student": tk.StringVar(),
        "marks_obtained": tk.StringVar(),
        "max_marks": tk.StringVar(),
        "remarks": tk.StringVar()}

        # ---------- DROPDOWN DATA ----------
        self.update_class_map = {}
        self.update_subject_map = {}
        self.update_exam_map = {}
        self.update_student_map = {}  
        self.update_marks_cache = {}

        # ---------- CLASS ----------
        tk.Label(form, text="Class:", font=("Arial", 14), bg="#ECF0F1")\
        .grid(row=0, column=0, padx=10, pady=8, sticky="e")

        classes = fetch_classes()
        self.update_class_map = {
        f"{c['class_name']} - {c['section']}": c["class_id"]
        for c in classes}

        class_cb = Combobox(
        form,
        textvariable=self.update_vars["class"],
        values=list(self.update_class_map.keys()),
        state="readonly",
        width=26,
        font=("Arial", 14))
        class_cb.grid(row=0, column=1, padx=10, pady=8)

        # ---------- SUBJECT ----------
        tk.Label(form, text="Subject:", font=("Arial", 14), bg="#ECF0F1")\
        .grid(row=1, column=0, padx=10, pady=8, sticky="e")

        subject_cb = Combobox(
        form,
        textvariable=self.update_vars["subject"],
        state="disabled",
        width=26,
        font=("Arial", 14))
        subject_cb.grid(row=1, column=1, padx=10, pady=8)

        # ---------- EXAM ----------
        tk.Label(form, text="Exam:", font=("Arial", 14), bg="#ECF0F1")\
        .grid(row=2, column=0, padx=10, pady=8, sticky="e")

        exam_cb = Combobox(
        form,
        textvariable=self.update_vars["exam"],
        state="disabled",
        width=26,
        font=("Arial", 14))
        exam_cb.grid(row=2, column=1, padx=10, pady=8)

        # ---------- STUDENT ----------
        tk.Label(form, text="Student:", font=("Arial", 14), bg="#ECF0F1")\
        .grid(row=3, column=0, padx=10, pady=8, sticky="e")

        student_cb = Combobox(
        form,
        textvariable=self.update_vars["student"],
        state="disabled",
        width=26,
        font=("Arial", 14))
        student_cb.grid(row=3, column=1, padx=10, pady=8)

        # ---------- MARKS ----------
        tk.Label(form, text="Marks Obtained:", font=("Arial", 14), bg="#ECF0F1")\
        .grid(row=4, column=0, padx=10, pady=8, sticky="e")

        tk.Entry(
        form,
        textvariable=self.update_vars["marks_obtained"],
        font=("Arial", 14),
        width=28
        ).grid(row=4, column=1, padx=10, pady=8)

        tk.Label(form, text="Max Marks:", font=("Arial", 14), bg="#ECF0F1")\
        .grid(row=5, column=0, padx=10, pady=8, sticky="e")

        tk.Entry(
        form,
        textvariable=self.update_vars["max_marks"],
        font=("Arial", 14),
        width=28
        ).grid(row=5, column=1, padx=10, pady=8)

        tk.Label(form, text="Remarks:", font=("Arial", 14), bg="#ECF0F1")\
        .grid(row=6, column=0, padx=10, pady=8, sticky="e")

        tk.Entry(
        form,
        textvariable=self.update_vars["remarks"],
        font=("Arial", 14),
        width=28
        ).grid(row=6, column=1, padx=10, pady=8)

        # ---------- SUBMIT BUTTON ----------
        submit_btn = tk.Label(
        self.content,
        text="Update Marks",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=25,
        pady=12,
        width=16,
        cursor="arrow")
        submit_btn.pack(pady=20)

        def enable():
            submit_btn.config(bg="#000", fg="white", cursor="hand2")
            submit_btn.bind("<Button-1>", lambda e: submit_update())

        def disable():
            submit_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            submit_btn.unbind("<Button-1>")

        disable()

        def on_update_class_change(*args):
            class_id = self.update_class_map.get(self.update_vars["class"].get())
            if not class_id:
                return

            res = requests.get(
            f"http://127.0.0.1:8000/classes/{class_id}/subjects")
            if res.status_code != 200:
                return

            self.update_subject_map = {
            s["subject_name"]: s["subject_id"] for s in res.json()}
            subject_cb["values"] = list(self.update_subject_map.keys())
            subject_cb.config(state="readonly")

        def on_update_subject_change(*args):
            subject_id = self.update_subject_map.get(self.update_vars["subject"].get())
            if not subject_id:
                return

            exams = fetch_exams()  # should return list

            self.update_exam_map = {
                e["exam_name"]: e["exam_id"] for e in exams}

            exam_cb["values"] = list(self.update_exam_map.keys())
            exam_cb.config(state="readonly")

        def on_update_exam_change(*args):
            class_name = self.update_vars["class"].get()
            subject_name = self.update_vars["subject"].get()
            exam_name = self.update_vars["exam"].get()

            if not class_name or not subject_name or not exam_name:
                return

            class_id = self.update_class_map[class_name]
            subject_id = self.update_subject_map[subject_name]
            exam_id = self.update_exam_map[exam_name]

            url = (
            "http://127.0.0.1:8000/teacher/results/marks/filter"
            f"?class_id={class_id}&subject_id={subject_id}&exam_id={exam_id}")

            res = requests.get(url)
            if res.status_code != 200:
                self.show_popup("Error", "No marks found", "warning")
                return

            data = res.json()

            self.update_student_map = {
                f"ID {r['student_id']}": r["mark_id"] for r in data
            }

            self.update_marks_cache = {
                f"ID {r['student_id']}": r for r in data
            }

            student_cb["values"] = list(self.update_student_map.keys())
            student_cb.config(state="readonly")

        def on_student_select(*args):
            key = self.update_vars["student"].get()

            if not key or key not in self.update_marks_cache:
                return

            data = self.update_marks_cache[key]

            self.update_vars["marks_obtained"].set(data["marks_obtained"])
            self.update_vars["max_marks"].set(data["max_marks"])
            self.update_vars["remarks"].set(data.get("remarks", ""))

            enable()
       
        self.update_vars["student"].trace_add("write", on_student_select)
        self.update_vars["class"].trace_add("write", on_update_class_change)
        self.update_vars["subject"].trace_add("write", on_update_subject_change)
        self.update_vars["exam"].trace_add("write", on_update_exam_change)

        # ---------- SUBMIT ----------
        def submit_update():
            mark_id = self.update_student_map[self.update_vars["student"].get()]

            if not self.update_vars["student"].get():
                self.show_popup("Error", "Select a student", "warning")
                return

            if float(self.update_vars["marks_obtained"].get()) > float(self.update_vars["max_marks"].get()):
                self.show_popup("Error", "Marks cannot exceed max marks", "warning")
                return

            payload = {
            "marks_obtained": float(self.update_vars["marks_obtained"].get()),
            "max_marks": float(self.update_vars["max_marks"].get()),
            "remarks": self.update_vars["remarks"].get()}

            import requests
            res = requests.put(
            f"http://127.0.0.1:8000/teacher/results/marks/{mark_id}",
            json=payload)

            if res.status_code == 200:
                self.show_popup("Success", "Marks Updated Successfully!", "info")
                self.change_screen("Marks Updated", add_callback=self.load_update_student_marks_screen)
            else:
                self.show_popup("Error", res.json().get("detail", "Update failed"), "error")

    # ===================================================================
    # ----- Button to View marks of a Student with Filters -----    
    def load_view_student_marks_screen(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="View Student Marks",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=15)

        from tkinter.ttk import Combobox

        # ===== FILTER VARIABLES =====
        self.marks_filter_vars = {
        "exam_id": tk.StringVar(),
        "student_id": tk.StringVar(),
        "subject_id": tk.StringVar(),
        "class_id": tk.StringVar()}

        labels = [
        ("Exam", "exam_id"),
        ("Student ID", "student_id"),
        ("Subject", "subject_id"),
        ("Class", "class_id")]

        # ===== FETCH DROPDOWN DATA =====
        exams = fetch_exams()
        subjects = fetch_subjects()
        classes = fetch_classes()

        exam_map = {e["exam_name"]: e["exam_id"] for e in exams}
        subject_map = {s["subject_name"]: s["subject_id"] for s in subjects}
        class_map = {
        f"{c['class_name']} - {c['section']}": c["class_id"]
        for c in classes}

        dropdown_maps = {
        "exam_id": exam_map,
        "subject_id": subject_map,
        "class_id": class_map}

        # ===== FILTER INPUTS =====
        for i, (label, key) in enumerate(labels):
            tk.Label(
            form,
            text=f"{label}:",
            font=("Arial", 14),
            bg="#ECF0F1"
            ).grid(row=i, column=0, padx=10, pady=10, sticky="e")

            if key in dropdown_maps:
                entry = Combobox(
                form,
                textvariable=self.marks_filter_vars[key],
                values=[""] + list(dropdown_maps[key].keys()),
                state="readonly",
                font=("Arial", 14),
                width=25
                )
            else:
                entry = tk.Entry(
                form,
                textvariable=self.marks_filter_vars[key],
                font=("Arial", 14),
                width=27
                )

            entry.grid(row=i, column=1, padx=10, pady=10)

        # ===== BUTTONS =====
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=15)

        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,
        form_frame=form
        )

        filter_btn = tk.Label(
        self.content,
        text="Filter Marks",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=25,
        pady=10,
        width=16,
        cursor="arrow")
        filter_btn.pack(pady=10)

        # ===== TABLE =====
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        cols = (
        "mark_id",
        "student_id",
        "subject_id",
        "exam_id",
        "marks_obtained",
        "max_marks",
        "is_pass",
        "remarks"
        )

        tree = ttk.Treeview(
        table_frame,
        columns=cols,
        show="headings",
        yscrollcommand=y_scroll.set
        )
        tree.pack(fill="both", expand=True)
        y_scroll.config(command=tree.yview)

        for col in cols:
            tree.heading(col, text=col.replace("_", " ").title())
            tree.column(col, width=140, anchor="center")

        # ===== ENABLE / DISABLE FILTER =====
        def enable():
            filter_btn.config(bg="#000", fg="white", cursor="hand2")
            filter_btn.bind("<Enter>", lambda e: filter_btn.config(bg="#222"))
            filter_btn.bind("<Leave>", lambda e: filter_btn.config(bg="#000"))
            filter_btn.bind("<Button-1>", lambda e: fetch_marks())

        def disable():
            filter_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            filter_btn.unbind("<Enter>")
            filter_btn.unbind("<Leave>")
            filter_btn.unbind("<Button-1>")

        disable()

        def validate(*args):
            # At least one filter must be filled
            for v in self.marks_filter_vars.values():
                if v.get().strip():
                    enable()
                    return
            disable()

        for v in self.marks_filter_vars.values():
            v.trace_add("write", validate)

        # ===== FETCH MARKS =====
        def fetch_marks():
            params = []
 
            if self.marks_filter_vars["exam_id"].get():
                params.append(
                f"exam_id={exam_map[self.marks_filter_vars['exam_id'].get()]}"
                )

            if self.marks_filter_vars["student_id"].get().isdigit():
                params.append(f"student_id={self.marks_filter_vars['student_id'].get()}")

            if self.marks_filter_vars["subject_id"].get():
                params.append(
                f"subject_id={subject_map[self.marks_filter_vars['subject_id'].get()]}"
                )

            if self.marks_filter_vars["class_id"].get():
                params.append(
                f"class_id={class_map[self.marks_filter_vars['class_id'].get()]}"
                )

            url = "http://127.0.0.1:8000/teacher/results/marks"
            if params:
                url += "?" + "&".join(params)

            import requests
            try:
                res = requests.get(url)

                for r in tree.get_children():
                    tree.delete(r)

                if res.status_code != 200:
                    self.show_popup("No Data", "No marks found.", "info")
                    return

                for row in res.json():
                    tree.insert("", "end", values=(
                    row["mark_id"],
                    row["student_id"],
                    row["subject_id"],
                    row["exam_id"],
                    row["marks_obtained"],
                    row["max_marks"],
                    "PASS" if row["is_pass"] else "FAIL",
                    row["remarks"]
                ))

            except Exception as e:
                self.show_popup("Error", str(e), "error")        


    # ===================================================================
    #-----Timetable Screen-----
    def load_teacher_timetable(self):
        self.clear_content()

        tk.Label(
            self.content,
            text="My Timetable",
            font=("Arial", 26, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(pady=20)

        # ----------------------
        # FILTER FRAME
        # ----------------------
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=10)

        # ---- Day Dropdown ----
        tk.Label(filter_frame, text="Day:", font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=0, padx=10)
        self.day_filter = tk.StringVar()
        day_dropdown = ttk.Combobox(
            filter_frame,
            textvariable=self.day_filter,
            values=["None", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            state="readonly",
            width=20
        )
        day_dropdown.grid(row=0, column=1, padx=10)
        day_dropdown.current(0)

        # ---- Subject Dropdown ----
        tk.Label(filter_frame, text="Subject:", font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=2, padx=10)

        # (filled after fetching data)
        self.subject_filter = tk.StringVar()
        subject_dropdown = ttk.Combobox(
            filter_frame,
            textvariable=self.subject_filter,
            state="readonly",
            width=20
        )
        subject_dropdown.grid(row=0, column=3, padx=10)

        # ---- Class Dropdown ----
        tk.Label(filter_frame, text="Class:", font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=4, padx=10)

        self.class_filter = tk.StringVar()
        class_dropdown = ttk.Combobox(
            filter_frame,
            textvariable=self.class_filter,
            state="readonly",
            width=20
        )
        class_dropdown.grid(row=0, column=5, padx=10)

        # ----------------------
        # LOAD DATA FROM API
        # ----------------------
        try:
            url = f"http://127.0.0.1:8000/teacher/timetable/{self.teacher_id}"
            res = requests.get(url)

            if res.status_code != 200:
                self.show_popup("Error", "Failed to fetch timetable", "error")
                return

            self.timetable_data = res.json()  # store for filtering

            if not self.timetable_data:
                self.show_popup("No Timetable", "No schedule found for you.", "info")
                return

        except Exception as e:
            self.show_popup("Error", str(e), "error")
            return

        # Fill SUBJECT dropdown →unique subjects
        subjects = sorted({d["subject"] for d in self.timetable_data})
        subject_dropdown["values"] = ["None"] + subjects
        subject_dropdown.current(0)

        # Fill CLASS dropdown → e.g. "8 (A)"
        classes = sorted({f"{d['class_name']} ({d['section']})" for d in self.timetable_data})
        class_dropdown["values"] = ["None"] + classes
        class_dropdown.current(0)

        # ----------------------
        # RESET BUTTON
        # ----------------------
        reset_btn = tk.Button(
            filter_frame,
            text="Reset Filters",
            bg="#000",
            fg="white",
            font=("Arial", 12, "bold"),
            command=lambda: reset_filters()
        )
        reset_btn.grid(row=0, column=6, padx=20)

        # ----------------------
        # BACK BUTTON
        # ----------------------
        top_bar = tk.Frame(self.content, bg="#ECF0F1")
        top_bar.pack(fill="x", pady=5)

        back_btn = tk.Label(
            top_bar,
            text="Back",
            font=("Arial", 14, "bold"),
            bg="#000",
            fg="white",
            padx=18,
            pady=8,
            cursor="hand2"
        )
        back_btn.pack(side="left", padx=10)
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#222"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#000"))
        back_btn.bind("<Button-1>", lambda e: self.load_dashboard())

        # ----------------------
        # TABLE AREA
        # ----------------------
        columns = ("day", "subject", "class", "start_time", "end_time", "room_no")

        self.table_frame = tk.Frame(self.content, bg="#ECF0F1")
        self.table_frame.pack(fill="both", expand=True, pady=10)

        # -------- DISPLAY TABLE --------
        def load_table(filtered):
            for wid in self.table_frame.winfo_children():
                wid.destroy()

            table_data = [
                (d["day"], d["subject"],
                f"{d['class_name']} ({d['section']})",
                d["start_time"], d["end_time"], d["room_no"])
                for d in filtered
            ]

            self.create_scrollable_table(self.table_frame, columns, table_data)

        # Initial load
        load_table(self.timetable_data)

        # ----------------------
        # FILTERING FUNCTION
        # ----------------------
        def apply_filters(*args):
            f_day = self.day_filter.get()
            f_subject = self.subject_filter.get()
            f_class = self.class_filter.get()

            filtered = self.timetable_data

            if f_day != "None":
                filtered = [d for d in filtered if d["day"] == f_day]

            if f_subject != "None":
                filtered = [d for d in filtered if d["subject"] == f_subject]

            if f_class != "None":
                filtered = [
                    d for d in filtered
                    if f"{d['class_name']} ({d['section']})" == f_class
                ]

            load_table(filtered)

        # Bind dropdown changes
        self.day_filter.trace_add("write", apply_filters)
        self.subject_filter.trace_add("write", apply_filters)
        self.class_filter.trace_add("write", apply_filters)

        # ----------------------
        # RESET FUNCTION
        # ----------------------
        def reset_filters():
            self.day_filter.set("None")
            self.subject_filter.set("None")
            self.class_filter.set("None")
            load_table(self.timetable_data)

    #----------Work -------------
    def load_teacher_work_records(self):
        self.clear_content()

        # TITLE
        tk.Label(
            self.content,
            text="My Work",
            font=("Arial", 26, "bold"),
            bg="#ECF0F1"
        ).pack(pady=20)

        # BACK BUTTON
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", pady=(0, 10), padx=20)

        tk.Button(
            back_frame,
            text="Back",
            font=("Arial", 12, "bold"),
            bg="black",
            fg="white",
            padx=20,
            pady=5,
            command=self.load_dashboard
        ).pack()

        # FETCH TEACHER WORK
        try:
            url = f"http://127.0.0.1:8000/teacher/work/{self.teacher_id}"
            res = requests.get(url)
            all_records = res.json() if res.status_code == 200 else []
        except:
            all_records = []

        # FILTER BAR
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=10)

        subject_var = tk.StringVar(value="None")
        type_var = tk.StringVar(value="None")
        class_var = tk.StringVar(value="None")

        # Safe dropdown lists
        subject_list = ["None"] + sorted({
            r.get("subject", "")
            for r in all_records if r.get("subject")
        })

        type_list = ["None", "Classwork", "Homework", "Assignment"]

        class_list = ["None"] + sorted({
            f'{r.get("class_name", "")} {r.get("section", "")}'.strip()
            for r in all_records
        })

        # Subject
        tk.Label(filter_frame, text="Subject:", font=("Arial", 14), bg="#ECF0F1")\
            .grid(row=0, column=0, padx=10)
        ttk.Combobox(filter_frame, textvariable=subject_var,
                    values=subject_list, state="readonly", width=18)\
            .grid(row=0, column=1)

        # Class
        tk.Label(filter_frame, text="Class:", font=("Arial", 14), bg="#ECF0F1")\
            .grid(row=0, column=2, padx=10)
        ttk.Combobox(filter_frame, textvariable=class_var,
                    values=class_list, state="readonly", width=18)\
            .grid(row=0, column=3)

        # Type
        tk.Label(filter_frame, text="Type:", font=("Arial", 14), bg="#ECF0F1")\
            .grid(row=0, column=4, padx=10)
        ttk.Combobox(filter_frame, textvariable=type_var,
                    values=type_list, state="readonly", width=18)\
            .grid(row=0, column=5)

        # RESET BUTTON
        tk.Button(
            filter_frame,
            text="Reset",
            font=("Arial", 12, "bold"),
            bg="#7F8C8D",
            fg="white",
            command=lambda: reset_filter()
        ).grid(row=0, column=6, padx=15)

        # TABLE
        table_frame = tk.Frame(self.content, bg="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        columns = ("Class", "Subject", "Type", "Title", "Due Date", "PDF")
        work_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        work_table.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=work_table.yview)
        scrollbar.pack(side="right", fill="y")
        work_table.configure(yscrollcommand=scrollbar.set)

        for col in columns:
            work_table.heading(col, text=col)
            work_table.column(col, width=150, anchor="center")

        # INSERT DATA
        def render_table(data):
            work_table.delete(*work_table.get_children())

            for r in data:
                cls = f'{r.get("class_name", "")} {r.get("section", "")}'.strip()
                work_table.insert(
                    "",
                    "end",
                    iid=r["work_id"],
                    values=(
                        cls,
                        r.get("subject", ""),
                        r.get("work_type", ""),
                        r.get("title", ""),
                        r.get("due_date", ""),
                        "Preview PDF"
                    )
                )

        render_table(all_records)

        # AUTO FILTER FUNCTION
        def apply_filter(*args):
            filtered = all_records

            if subject_var.get() != "None":
                filtered = [r for r in filtered if r.get("subject") == subject_var.get()]

            if class_var.get() != "None":
                cls_text = class_var.get()
                filtered = [
                    r for r in filtered if
                    f'{r.get("class_name","")} {r.get("section","")}'.strip() == cls_text
                ]

            if type_var.get() != "None":
                filtered = [r for r in filtered if r.get("work_type") == type_var.get()]

            render_table(filtered)

        subject_var.trace("w", apply_filter)
        type_var.trace("w", apply_filter)
        class_var.trace("w", apply_filter)

        def reset_filter():
            subject_var.set("None")
            class_var.set("None")
            type_var.set("None")
            render_table(all_records)

        # ----- RIGHT-CLICK MENU -----
        menu = tk.Menu(work_table, tearoff=0)

        menu.add_command(
            label="Preview PDF",
            command=lambda: self._teacher_preview_selected(work_table)
        )

        menu.add_command(
            label="Edit Work",
            command=lambda: self._teacher_work_edit_selected(work_table)
        )

        menu.add_command(
            label="Delete Work",
            command=lambda: self._teacher_work_delete_selected(work_table)
        )

        def show_menu(event):
            row = work_table.identify_row(event.y)
            if row:
                work_table.selection_set(row)
                menu.post(event.x_root, event.y_root)

        work_table.bind("<Button-3>", show_menu)   # Right-click

        # DOUBLE CLICK PREVIEW
        work_table.bind("<Double-1>", lambda e: self._teacher_preview_selected(work_table))


    def load_teacher_add_work(self):
        self.clear_content()

        tk.Label(
            self.content,
            text="Add Work",
            font=("Arial", 26, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(pady=20)

        # BACK BUTTON
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", pady=(0, 10), padx=20)

        tk.Button(
            back_frame,
            text="Back",
            font=("Arial", 12, "bold"),
            bg="black",
            fg="white",
            padx=20,
            pady=5,
            command=self.load_teacher_work_records
        ).pack()

        # ---------------- FETCH CLASSES ----------------
        classes = fetch_classes()
        if not isinstance(classes, list):
            classes = []

        # ---------------- FETCH SUBJECT  ----------------
        try:
            t = requests.get(
                f"http://127.0.0.1:8000/admin/teachers/{self.teacher_id}",
                timeout=5
            ).json()
            subject_name = t.get("subject_name", "")
        except:
            subject_name = ""

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        vars = {
            "class": tk.StringVar(),
            "subject": tk.StringVar(value=subject_name),
            "work_type": tk.StringVar(),
            "title": tk.StringVar(),
            "description": tk.StringVar(),
        }

        # CLASS DROPDOWN
        tk.Label(form, text="Class:", bg="#ECF0F1", font=("Arial", 14))\
            .grid(row=0, column=0, sticky="w", pady=6)

        class_display = [f'{c["class_name"]} {c["section"]}' for c in classes]

        ttk.Combobox(
            form,
            textvariable=vars["class"],
            values=class_display,
            state="readonly",
            width=30
        ).grid(row=0, column=1, pady=6, padx=10)

        # SUBJECT (LOCKED)
        tk.Label(form, text="Subject:", bg="#ECF0F1", font=("Arial", 14))\
            .grid(row=1, column=0, sticky="w", pady=6)

        tk.Entry(
            form,
            textvariable=vars["subject"],
            width=32,
            font=("Arial", 14),
            state="readonly"
        ).grid(row=1, column=1, padx=10, pady=6)

        # WORK TYPE
        tk.Label(form, text="Work Type:", bg="#ECF0F1", font=("Arial", 14))\
            .grid(row=2, column=0, sticky="w", pady=6)

        ttk.Combobox(
            form,
            textvariable=vars["work_type"],
            values=["Classwork", "Homework", "Assignment"],
            state="readonly",
            width=30
        ).grid(row=2, column=1, pady=6, padx=10)

        # TITLE
        tk.Label(form, text="Title:", bg="#ECF0F1", font=("Arial", 14))\
            .grid(row=3, column=0, sticky="w", pady=6)

        tk.Entry(form, textvariable=vars["title"], width=32, font=("Arial", 14))\
            .grid(row=3, column=1, padx=10, pady=6)

        # DESCRIPTION
        tk.Label(form, text="Description:", bg="#ECF0F1", font=("Arial", 14))\
            .grid(row=4, column=0, sticky="w", pady=6)

        tk.Entry(form, textvariable=vars["description"], width=32, font=("Arial", 14))\
            .grid(row=4, column=1, padx=10, pady=6)

        # DUE DATE
        tk.Label(form, text="Due Date:", bg="#ECF0F1", font=("Arial", 14))\
            .grid(row=5, column=0, sticky="w", pady=6)

        due_date = DateEntry(form, width=28, date_pattern='yyyy-mm-dd')
        due_date.grid(row=5, column=1, padx=10, pady=6)

        # PDF SELECT
        pdf_frame = tk.Frame(self.content, bg="#ECF0F1")
        pdf_frame.pack(pady=10)

        pdf_label = tk.StringVar(value="No File Selected")
        tk.Label(pdf_frame, textvariable=pdf_label, bg="#ECF0F1").pack(side="left", padx=10)

        selected_file = {"path": None}

        def choose_pdf():
            path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
            if path:
                selected_file["path"] = path
                pdf_label.set(os.path.basename(path))

        tk.Button(pdf_frame, text="Choose PDF", command=choose_pdf).pack(side="left")

        # SAVE HANDLER
        def save():
            class_text = vars["class"].get()
            class_id = next(
                (c["class_id"] for c in classes
                if f'{c["class_name"]} {c["section"]}' == class_text),
                None
            )

            if not class_id:
                self.show_popup("Missing Data", "Please select a class", "warning")
                return

            if not selected_file["path"]:
                self.show_popup("Missing PDF", "Please choose a PDF file", "warning")
                return

            payload = {
                "class_id": class_id,
                "teacher_id": self.teacher_id,
                "subject": vars["subject"].get(),
                "work_type": vars["work_type"].get(),
                "title": vars["title"].get(),
                "description": vars["description"].get(),
                "due_date": due_date.get_date().isoformat(),
            }

            with open(selected_file["path"], "rb") as f:
                files = {
                    "file": (
                        os.path.basename(selected_file["path"]),
                        f,
                        "application/pdf"
                    )
                }
                r = requests.post(
                    "http://127.0.0.1:8000/teacher/work/add",
                    data=payload,
                    files=files
                )

            if r.status_code in (200, 201):
                self.show_popup("Success", "Work Added Successfully!", "success")
                self.load_teacher_work_records()
            else:
                self.show_popup("Error", r.text, "error")

        tk.Button(self.content, text="Save Work", command=save).pack(pady=20)


    def load_teacher_edit_work(self, work_id: int):
        self.clear_content()

        tk.Label(
            self.content,
            text="Edit My Work",
            font=("Arial", 26, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(pady=20)

        # FETCH WORK
        try:
            res = requests.get(f"http://127.0.0.1:8000/admin/work/{work_id}")
            if res.status_code != 200:
                self.show_popup("Error", "Work not found", "error")
                return
            work = res.json()
        except:
            self.show_popup("Error", "Server error", "error")
            return

        if work["teacher_name"] != self.teacher_full_name:
            self.show_popup("Not Allowed", "You can edit only your own work.", "warning")
            return

        # ---------------- FETCH CLASSES ----------------
        classes = fetch_classes()
        if not isinstance(classes, list):
            classes = []

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        vars = {
            "class": tk.StringVar(value=f'{work["class_name"]} {work["section"]}'),
            "subject": tk.StringVar(value=work["subject"]),
            "work_type": tk.StringVar(value=work["work_type"]),
            "title": tk.StringVar(value=work["title"]),
            "description": tk.StringVar(value=work["description"]),
        }

        # CLASS
        tk.Label(form, text="Class:", font=("Arial", 14), bg="#ECF0F1")\
            .grid(row=0, column=0, sticky="w", pady=6)

        class_display = [f'{c["class_name"]} {c["section"]}' for c in classes]

        ttk.Combobox(
            form,
            textvariable=vars["class"],
            values=class_display,
            state="readonly",
            width=30
        ).grid(row=0, column=1, pady=6, padx=10)

        # SUBJECT
        tk.Label(form, text="Subject:", font=("Arial", 14), bg="#ECF0F1")\
            .grid(row=1, column=0, sticky="w", pady=6)

        tk.Entry(
            form,
            textvariable=vars["subject"],
            width=30,
            font=("Arial", 14),
            state="readonly"
        ).grid(row=1, column=1, padx=10)

        # WORK TYPE
        tk.Label(form, text="Work Type:", font=("Arial", 14), bg="#ECF0F1")\
            .grid(row=2, column=0, sticky="w", pady=6)

        ttk.Combobox(
            form,
            textvariable=vars["work_type"],
            values=["Classwork", "Homework", "Assignment"],
            state="readonly",
            width=30
        ).grid(row=2, column=1, padx=10, pady=6)

        # TITLE
        tk.Label(form, text="Title:", font=("Arial", 14), bg="#ECF0F1")\
            .grid(row=3, column=0, sticky="w", pady=6)

        tk.Entry(form, textvariable=vars["title"], width=32, font=("Arial", 14))\
            .grid(row=3, column=1, padx=10, pady=6)

        # DESCRIPTION
        tk.Label(form, text="Description:", font=("Arial", 14), bg="#ECF0F1")\
            .grid(row=4, column=0, sticky="w", pady=6)

        tk.Entry(form, textvariable=vars["description"], width=32, font=("Arial", 14))\
            .grid(row=4, column=1, padx=10, pady=6)

        # DUE DATE
        tk.Label(form, text="Due Date:", font=("Arial", 14), bg="#ECF0F1")\
            .grid(row=5, column=0, sticky="w", pady=6)

        due_entry = DateEntry(form, width=28, date_pattern='yyyy-mm-dd')
        due_entry.set_date(work["due_date"])
        due_entry.grid(row=5, column=1, padx=10, pady=6)

        def save():
            class_text = vars["class"].get()
            class_id = next(
                (c["class_id"] for c in classes
                if f'{c["class_name"]} {c["section"]}' == class_text),
                None
            )

            payload = {
                "class_id": class_id,
                "teacher_id": self.teacher_id,
                "subject": vars["subject"].get(),
                "title": vars["title"].get(),
                "description": vars["description"].get(),
                "work_type": vars["work_type"].get(),
                "due_date": due_entry.get_date().isoformat(),
            }

            r = requests.put(
                f"http://127.0.0.1:8000/teacher/work/{work_id}",
                json=payload
            )

            if r.status_code == 200:
                self.show_popup("Success", "Work Updated Successfully!", "success")
                self.load_teacher_work_records()
            else:
                self.show_popup("Error", r.text, "error")

        tk.Button(self.content, text="Save Changes", command=save).pack(pady=20)


    #-------HELPER FUNCTIONS FOR RIGHT-CLICK MENU--------
    def _teacher_preview_selected(self, table):

        selected = table.selection()
        if not selected:
            return

        work_id = selected[0]
        url = f"http://127.0.0.1:8000/teacher/work/download/{work_id}"

        r = requests.get(url)
        if r.status_code != 200:
            self.show_popup("Error", "Could not download PDF", "error")
            return

        temp_path = os.path.join(tempfile.gettempdir(), f"work_{work_id}.pdf")
        with open(temp_path, "wb") as f:
            f.write(r.content)

        os.startfile(temp_path)


    def _teacher_work_edit_selected(self, table):
        selected = table.selection()
        if not selected:
            return
        work_id = int(selected[0])
        self.load_teacher_edit_work(work_id)


    def _teacher_work_delete_selected(self, table):
        selected = table.selection()
        if not selected:
            return
        work_id = int(selected[0])

        # Confirm delete
        if not self.show_popup("Confirm Delete", "Delete this work?", "confirm"):
            return

        r = requests.delete(f"http://127.0.0.1:8000/teacher/work/{work_id}")

        if r.status_code in (200, 204):
            self.show_popup("Success", "Work deleted", "info")
            self.load_teacher_work_records()
        else:
            self.show_popup("Error", r.text, "error")


    # ==============================================================================
    # ===== DASHBOARD PAGE ======
    def load_dashboard(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        tk.Label(
            self.content,
            text="Teacher Dashboard",
            font=("Arial", 26, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
            ).pack(pady=20)

        box = tk.Frame(self.content, bg="white", bd=2, relief="groove")
        box.pack(pady=60)

        tk.Label(
            box,
            text="Welcome to the Teacher Panel!",
            font=("Arial", 16),
            bg="white"
            ).pack(padx=40, pady=30)


# ======== RUN UI ========
if __name__ == "__main__":
    root = tk.Tk()
    ui = TeacherUI(root, teacher_id=TEACHER_ID)
    root.mainloop()
