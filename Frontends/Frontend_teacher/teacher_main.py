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

# =============
class TeacherUI:
    def __init__(self, root, teacher_id = 4):
        self.root = root

        # teacher Logged-In Details (Dummy OR Fetched From Login)
        self.teacher_id = teacher_id


        self.root.title("School ERP - Teacher Panel")
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
            self.sidebar,
            text=text,
            font=("Arial", 14, "bold"),
            bg="#000000",
            fg="white",
            padx=20,
            pady=12,
            anchor="w",
            width=30,
            cursor="arrow"
        )
        btn.pack(pady=5, fill="x")

        # Hover Effects
        btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

        # Click
        if cmd:
            btn.bind("<Button-1>", lambda e: cmd())

        return btn


    # ===== SIDEBAR BUILD =====
    def build_sidebar(self):

        tk.Label(
            self.sidebar,
            text="TEACHER PANEL",
            bg="#1E2A38",
            fg="white",
            font=("Arial", 18, "bold")
            ).pack(pady=20)

        # Main Buttons
        att_btn = self.add_btn("Manage Attendances")
        self.build_attendance_dropdown(att_btn)

        result_btn = self.add_btn("View and Generate Results")
        self.build_result_dropdown(result_btn)
        tt_btn = self.add_btn("View Timetable", self.load_teacher_timetable)

        work_btn = self.add_btn("Manage Work")
        self.build_work_dropdown(work_btn)

    
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
        teacher.add_command(label="View All Attendance", command=self.load_teacher_attendance_filter)
        teacher.add_command(label="Attendance Summary", command=self.load_teacher_attendance_summary_screen)

        menu.add_cascade(label="self Attendance", menu=teacher)
        parent_label.bind("<Button-1>", lambda e: menu.tk_popup(e.x_root, e.y_root))
    
    # ===========================================
    def build_result_dropdown(self, parent_label):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Generate and Download Result of a Student", command=lambda: self.load_generate_and_download_result_of_student())
        menu.add_command(label="Generate and Download Final Result of a Student", command=lambda: self.load_generate_and_download_final_result_of_student())
        menu.add_command(label="View all Result for an Exam", command=lambda: self.load_view_all_results_for_exam())
        menu.add_command(label="Generate and Download all students Results for a class", command=lambda: self.load_view_and_download_all_students_results_for_a_class())
        menu.add_command(label="Generate and Download all Final Results for a Class", command=lambda: self.load_generate_and_download_all_final_results_for_a_class())
        
        parent_label.bind("<Button-1>", lambda e: menu.tk_popup(e.x_root, e.y_root))
        

    def build_work_dropdown(self, parent_label):
        menu = tk.Menu(self.root, tearoff=0)

        menu.add_command(label="View Work", command=self.load_teacher_work_records)
        menu.add_command(label="Add Work", command=self.load_teacher_add_work)

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


    # ------ SCROLLABLE SCREEN WRAPPER -------
    def create_scrollable_area(self):
        # MAIN container (takes entire content area)
        outer = tk.Frame(self.content, bg="#ECF0F1")
        outer.pack(fill="both", expand=True)

        # Canvas inside content
        canvas = tk.Canvas(outer, bg="#ECF0F1", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        # Inner frame where all widgets go
        inner = tk.Frame(canvas, bg="#ECF0F1")
        canvas.create_window((0, 0), window=inner, anchor="n")

        # *** CENTER THE SCREEN CONTENT ***
        inner.grid_columnconfigure(0, weight=1)

        # Resize scroll region
        def update_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig("inner_window", width=canvas.winfo_width())

        canvas.bind("<Configure>", update_scroll)

        return inner
    
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
        ("Class ID", "class_id"),
        ("Subject ID", "subject_id"),
        ("Lecture Date (YYYY-MM-DD)", "lecture_date"),
        ("Status (P/A/L)", "status"),
        ("Remarks", "remarks"),
        ]

        self.mark_vars = {}

        for i, (label, key) in enumerate(fields):
    # Label
            tk.Label(
        form,
        text=f"{label}:",
        font=("Arial", 14),
        bg="#ECF0F1"
    ).grid(row=i, column=0, padx=10, pady=8, sticky="e")

    # Entry field
            var = tk.StringVar()
            entry = tk.Entry(form, textvariable=var, font=("Arial", 14), width=28)
            entry.grid(row=i, column=1, padx=10, pady=8)

            self.mark_vars[key] = var

    # ===== ADD CALENDAR BUTTON ONLY FOR lecture_date =====
            if key == "lecture_date":
                tk.Button(
            form,
            text="Calendar",
            font=("Arial", 12),
            bg="white",
            relief="ridge",
            command=lambda e=entry, v=var: self.open_calendar_popup(e, v)
        ).grid(row=i, column=2, padx=8)

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

            # ---- student id ----
            if not data["student_id"].isdigit():
                disable()
                return

            # ---- class id ----
            if not data["class_id"].isdigit():
                disable()
                return

            # ---- subject id ----
            if not data["subject_id"].isdigit():
                disable()
                return

            # ---- lecture date format ----
            import re
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", data["lecture_date"]):
                disable()
                return
     
            # ---- status value ----
            if data["status"].upper() not in ["P", "A", "L"]:
                disable()
                return

            # all good
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
 
        # ===== SUBMIT FUNCTION =====
        def submit():
            data = {k: v.get().strip() for k, v in self.mark_vars.items()}
            # ---- missing fields ----
            missing = [k for k, v in data.items() if not v]
            if missing:
                # show which fields are missing (friendly labels)
                pretty = ", ".join([m.replace("_", " ").title() for m in missing])
                self.show_popup("Missing Information", f"Please fill: {pretty}", "warning")
                disable()
                return

            payload = {
                "student_id": int(data["student_id"]),
                "class_id": int(data["class_id"]),
                "subject_id": int(data["subject_id"]),
                "lecture_date": data["lecture_date"],
                "status": data["status"].upper(),
                "remarks": data["remarks"]
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

        for i, (label, key) in enumerate(labels):
            tk.Label(
            form,
            text=label + ":",
            font=("Arial", 14),
            bg="#ECF0F1"
        ).grid(row=i, column=0, padx=10, pady=10, sticky="e")

            var = tk.StringVar()
            entry = tk.Entry(form, textvariable=var, font=("Arial", 14), width=28)
            entry.grid(row=i, column=1, padx=10)

            self.bulk_vars[key] = var

    # DATE PICKER BUTTON
        date_entry = form.grid_slaves(row=2, column=1)[0]
        tk.Button(
        form,
        text="Calendar",
        font=("Arial", 12),
        bg="white",
        relief="flat",
        command=lambda: self.open_calendar_popup(date_entry, self.bulk_vars["lecture_date"])
    ).grid(row=2, column=2, padx=5)

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
        import re

        def validate(*args):
            class_id = self.bulk_vars["class_id"].get().strip()
            subject_id = self.bulk_vars["subject_id"].get().strip()
            lecture_date = self.bulk_vars["lecture_date"].get().strip()
            abs_vals = self.bulk_vars["absent_ids"].get().strip()

            if not class_id.isdigit():
                disable()
                return

            if not subject_id.isdigit():
                disable()
                return

            if not re.match(r"^\d{4}-\d{2}-\d{2}$", lecture_date):
                disable()
                return

        # validate comma separated integers
            if abs_vals:
                parts = abs_vals.split(",")
                for p in parts:
                    if not p.strip().isdigit():
                        disable()
                        return

            enable()
  
        for v in self.bulk_vars.values():
            v.trace_add("write", validate)

    # -------- SUBMIT FUNCTION --------
        def submit_bulk():
            class_id = int(self.bulk_vars["class_id"].get().strip())
            subject_id = int(self.bulk_vars["subject_id"].get().strip())
            lecture_date = self.bulk_vars["lecture_date"].get().strip()
            abs_vals = self.bulk_vars["absent_ids"].get().strip()

            if not all([class_id, subject_id, lecture_date]):
                self.show_popup("Missing Values", "Enter all the Fields", "warning")
                disable()
                return

            payload = {
            "class_id": class_id,
            "subject_id": subject_id,
            "lecture_date": lecture_date,
            "absent_ids": abs_vals  # e.g. "8,7"
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

        for i, (text_lbl, key) in enumerate(labels):
            tk.Label(
            form,
            text=text_lbl + ":",
            font=("Arial", 14),
            bg="#ECF0F1"
            ).grid(row=i, column=0, padx=10, pady=10, sticky="e")

            var = tk.StringVar()
            entry = tk.Entry(form, textvariable=var, font=("Arial", 14), width=25)
            entry.grid(row=i, column=1, padx=10)

            self.filter_vars[key] = var

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

        cols = ("attendance_id", "student_id", "subject_id", "class_id",
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

            # ----- Disable until fields filled -----
            if d1 == "" or d2 == "":
                disable()
                return

            # ----- Validate ONLY when length = 10 -----
            if (len(d1) == 10 and not re.match(date_regex, d1)) or \
               (len(d2) == 10 and not re.match(date_regex, d2)):
                disable()
                self.show_popup("Invalid Date Format", "Use YYYY-MM-DD format.", "error")
                return

            if not data["student_id"].isdigit():
                disable()
                return
            
            if not data["subject_id"].isdigit():
                disable()
                return
            
            enable()

        for v in self.filter_vars.values():
            v.trace_add("write", validate)

        disable()

        # ===== CLEAR TABLE =====
        def clear_table(*args):
            for row in self.attendance_tree.get_children():
                self.attendance_tree.delete(row)

        clear_btn.bind("<Button-1>", clear_table)

        # ===== FILTER FUNCTION =====
        def do_filter():
            payload = {
            "student_id": int(self.filter_vars["student_id"].get().strip()),
            "date_from": self.filter_vars["date_from"].get().strip(),
            "date_to": self.filter_vars["date_to"].get().strip(),
            "subject_id": int(self.filter_vars["subject_id"].get().strip())
                if self.filter_vars["subject_id"].get().strip()
                else None
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

                for item in data:
                    self.attendance_tree.insert("", "end", values=(
                    item["attendance_id"],
                    item["student_id"],
                    item["subject_id"],
                    item["class_id"],
                    item["lecture_date"],
                    item["status"],
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

            if d1 == "" or d2 == "":
                disable()
                return

            if (len(d1) == 10 and not re.match(date_regex, d1)) or \
               (len(d2) == 10 and not re.match(date_regex, d2)):
                disable()
                self.show_popup("Invalid Date", "Date should be in format YYYY-MM-DD", "warning")
                return

            if re.match(date_regex, d1) and re.match(date_regex, d2):
                enable()
            else:
                disable()

            if not sid.isdigit():
                disable()
                self.show_popup("Invalid Student ID", "Student ID must be numeric.", "warning")
                return

        for v in self.summary_vars.values():
            v.trace_add("write", validate)

        # ===== CLEAR FIELDS =====
        def clear():
            for var in summary_labels.values():
                var.set("")

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

        row_index = 1
        for text, key in labels:
            tk.Label(form, text=text + ":", font=("Arial", 14), bg="#ECF0F1")\
            .grid(row=row_index, column=0, padx=10, pady=10, sticky="e")

            var = tk.StringVar()
            entry = tk.Entry(
            form, textvariable=var,
            font=("Arial", 14), width=25,
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
            data = {k: v.get().strip() for k, v in self.update_vars.items()}

    # --- First normalize Status field ---
            status_raw = data["status"].strip().lower()

            if status_raw.startswith("p"):
                self.update_vars["status"].set("P")
                data["status"] = "P"

            elif status_raw.startswith("a"):
                self.update_vars["status"].set("A")
                data["status"] = "A"

            elif status_raw.startswith("l"):
                self.update_vars["status"].set("L")
                data["status"] = "L"

            else:
                disable_update()
                return

    # --- NOW check for emptiness ---
            if not all(data.values()):
                disable_update()
                return

    # --- Numeric validations ---
            if not data["student_id"].isdigit():
                disable_update()
                return

            if not data["subject_id"].isdigit():
                disable_update()
                return

            if not data["class_id"].isdigit():
                disable_update()
                return

    # --- Date format ---
            import re
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", data["lecture_date"]):
                disable_update()
                return

    # --- All good ---
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

                # Enable fields
                for entry in self.update_entries.values():
                    entry.config(state="normal")

                # Fill data
                for key in self.update_vars:
                    self.update_vars[key].set(data.get(key, ""))

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
            "student_id": int(self.update_vars["student_id"].get()),
            "subject_id": int(self.update_vars["subject_id"].get()),
            "class_id": int(self.update_vars["class_id"].get()),
            "lecture_date": self.update_vars["lecture_date"].get(),
            "status": self.update_vars["status"].get().upper(),
            "remarks": self.update_vars["remarks"].get(),
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
            delete_btn.config(bg="#000000", fg="white", cursor="arrow")
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
                self.show_popup("Missing Values", "Entry Fields can not be empty", "error")
                disable_delete()
                return

            if not val.isdigit():
                self.show_popup("Invalid Attendance ID", "Attendance ID should be numeric only.", "warning")
                att_id_var.set("")
                disable_delete()
                return

            if int(val) <= 0:
                self.show_popup("Invalid Attendance ID", "Attendance ID must be a positive number.", "warning")
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
    text="Status (P/A/L):",
    font=("Arial", 14),
    bg="#ECF0F1"
).grid(row=2, column=0, padx=10, pady=10, sticky="w")

        status_var = tk.StringVar()
        status_dropdown = ttk.Combobox(
    form,
    textvariable=status_var,
    values=["P", "A", "L"],
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
            mark_btn.config(bg="#000000", fg="white", cursor="arrow")
            mark_btn.bind("<Enter>", lambda e: mark_btn.config(bg="#222222"))
            mark_btn.bind("<Leave>", lambda e: mark_btn.config(bg="#000000"))
            mark_btn.bind("<Button-1>", lambda e: perform_mark())
        
        def disable_btn():
            mark_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            mark_btn.unbind("<Enter>")
            mark_btn.unbind("<Leave>")
            mark_btn.unbind("<Button-1>")

        def validate(*args):
            status_text = status_var.get().strip().lower()

    # No status entered → disable
            if not status_text:
                disable_btn()
                return

    # Recognize status using startswith
            if status_text.startswith("p"):
                status_var.set("P")   # Normalize
                enable_btn()
                return

            elif status_text.startswith("a"):
                status_var.set("A")
                enable_btn()
                return

            elif status_text.startswith("l"):
                status_var.set("L")
                enable_btn()
                return

    # If neither P/A/L matched → disable
            disable_btn()

        status_var.trace_add("write", validate)

        # ------- API CALL FUNCTION -------
        def perform_mark():
            from datetime import datetime
            import requests

            payload = {
    "teacher_id": int(teacher_id_var.get().strip()),
    "date": date_var.get().strip(),
    "check_in": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    "status": status_var.get(),   # P / A / L
    "remarks": "Self Attendance Marked"
}

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
        tk.Label(form, text="Date From (YYYY-MM-DD):", font=("Arial", 14), bg="#ECF0F1").grid(row=1, column=0, padx=10)
        date_from_var = tk.StringVar()
        tk.Entry(form, textvariable=date_from_var, font=("Arial", 14), width=25).grid(row=1, column=1)

        # Calendar button
        tk.Button(
        form, text="Calendar", command=lambda: self.open_calendar_popup(form.grid_slaves(row=1, column=1)[0], date_from_var)
        ).grid(row=1, column=2, padx=5)

        # Date To
        tk.Label(form, text="Date To (YYYY-MM-DD):", font=("Arial", 14), bg="#ECF0F1").grid(row=2, column=0, padx=10)
        date_to_var = tk.StringVar()
        tk.Entry(form, textvariable=date_to_var, font=("Arial", 14), width=25).grid(row=2, column=1)

        tk.Button(
        form, text="Calendar", command=lambda: self.open_calendar_popup(form.grid_slaves(row=2, column=1)[0], date_to_var)
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
            r = r"^\d{4}-\d{2}-\d{2}$"
            d1 = date_from_var.get().strip()
            d2 = date_to_var.get().strip()

            if not d1 or not d2:
                disable_btn()
                return

            if not re.match(r, d1) or not re.match(r, d2):
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

                rows = res.json()

                # clear table
                for r in tree.get_children():
                    tree.delete(r)

                # fill table
                for r in rows:
                    tree.insert("", "end", values=(
                    r["record_id"],
                    r["date"],
                    r["check_in"],
                    r["status"],
                    r["remarks"]
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
        cursor="arrow"
    )
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
            d1 = date_from_var.get().strip()
            d2 = date_to_var.get().strip()

            if not d1 or not d2:
                disable_btn()
                return

            # Date format check
            date_regex = r"^\d{4}-\d{2}-\d{2}$"
            if not re.match(date_regex, d1) or not re.match(date_regex, d2):
                disable_btn()
                return

            enable_btn()

        teacher_id_var.trace_add("write", validate)
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

                make_card("Total Days:", data["total_days"], 0)
                make_card("Present:", data["present"], 1)
                make_card("Absent:", data["absent"], 2)
                make_card("Leave:", data["leave"], 3)
                make_card("Attendance %:", f"{data['percentage']}%", 4)

                self.show_popup("Success", "Summary Loaded!", "info")

            except Exception as e:
                self.show_popup("Backend Error", f"{e}", "error")
  
    
    # ==============================================================================
    # ----- Button to Generate and Download Result of a Student with Some Exam ID -----
    def load_generate_and_download_result_of_student(self):
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
        tk.Entry(form, textvariable=exam_var, width=25, font=("Arial", 14))\
        .grid(row=1, column=1, padx=10, pady=10)

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

        # Validation
        def validate(*args):
            sid = sid_var.get().strip()
            eid = exam_var.get().strip()

            if sid.isdigit() and eid.isdigit():
                enable_fetch()
            else:
                disable_fetch()

        sid_var.trace_add("write", validate)
        exam_var.trace_add("write", validate)

        # ====== FETCH RESULT FUNCTION ======
        def fetch_result():
            sid = int(sid_var.get().strip())
            eid = int(exam_var.get().strip())

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
            eid = exam_var.get().strip()

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
 
        tk.Entry(
        form,
        textvariable=exam_var,
        font=("Arial", 14),
        width=25
    ).grid(row=0, column=1, padx=10, pady=10)

        # ===== BACK BUTTON =====
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)
        self.create_back_button(back_frame, self.load_dashboard, form)

        # ===== TABLE FRAME =====
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        cols = ("result_id", "student_id", "exam_id", "total_marks", "percentage", "grade")

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
            if exam_var.get().strip().isdigit():
                enable_load()
            else:
                disable_load()

        exam_var.trace_add("write", validate)

        # ===== LOAD RESULTS FUNCTION =====
        def load_results():
            exam_id = exam_var.get().strip()

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
                        r["exam_id"],
                        r["total_marks"],
                        r["percentage"],
                        r["grade"]
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

        tk.Entry(form, textvariable=class_var, font=("Arial", 14), width=25)\
        .grid(row=0, column=1, padx=10, pady=8)
        tk.Entry(form, textvariable=exam_var, font=("Arial", 14), width=25)\
        .grid(row=1, column=1, padx=10, pady=8)

        # BACK BUTTON
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)
        self.create_back_button(back_frame, self.load_dashboard, form)

        # ===== TABLE FRAME =====
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=15)

        cols = ("student_id", "full_name", "exam_id", "total_marks", "percentage", "grade")

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
            if class_var.get().strip().isdigit() and exam_var.get().strip().isdigit():
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
            class_id = class_var.get().strip()
            exam_id = exam_var.get().strip()

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
                        r["exam_id"],
                        r["total_marks"],
                        r["percentage"],
                        r["grade"]
                    )
                )

            except Exception as e:
                self.show_popup("Error", str(e), "error")

        # ===== DOWNLOAD ZIP FUNCTION =====
        def download_zip():
            class_id = class_var.get().strip()
            exam_id = exam_var.get().strip()

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

        tk.Entry(form, textvariable=class_var, font=("Arial", 14), width=25)\
        .grid(row=0, column=1, padx=10, pady=8)

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
            if class_var.get().strip().isdigit():
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
            class_id = class_var.get().strip()

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
            class_id = class_var.get().strip()

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

        # FETCH CLASSES
        try:
            classes = requests.get("http://127.0.0.1:8000/admin/timetable/classes").json()
        except:
            classes = []

        # FETCH SUBJECT NAME (since teacher is fixed)
        try:
            t = requests.get(f"http://127.0.0.1:8000/admin/teachers/{self.teacher_id}").json()
            subject_name = t["subject_name"]
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
        tk.Label(form, text="Class:", bg="#ECF0F1", font=("Arial", 14)).grid(row=0, column=0, sticky="w", pady=6)
        class_display = [f'{c["class_name"]} {c["section"]}' for c in classes]

        ttk.Combobox(
            form,
            textvariable=vars["class"],
            values=class_display,
            state="readonly",
            width=30
        ).grid(row=0, column=1, pady=6, padx=10)

        # SUBJECT (LOCKED)
        tk.Label(form, text="Subject:", bg="#ECF0F1", font=("Arial", 14)).grid(row=1, column=0, sticky="w", pady=6)
        tk.Entry(form, textvariable=vars["subject"], width=32, font=("Arial", 14), state="readonly")\
            .grid(row=1, column=1, padx=10, pady=6)

        # WORK TYPE
        tk.Label(form, text="Work Type:", bg="#ECF0F1", font=("Arial", 14)).grid(row=2, column=0, sticky="w", pady=6)
        ttk.Combobox(
            form,
            textvariable=vars["work_type"],
            values=["Classwork", "Homework", "Assignment"],
            state="readonly",
            width=30
        ).grid(row=2, column=1, pady=6, padx=10)

        # TITLE
        tk.Label(form, text="Title:", bg="#ECF0F1", font=("Arial", 14)).grid(row=3, column=0, sticky="w", pady=6)
        tk.Entry(form, textvariable=vars["title"], width=32, font=("Arial", 14))\
            .grid(row=3, column=1, padx=10, pady=6)

        # DESCRIPTION
        tk.Label(form, text="Description:", bg="#ECF0F1", font=("Arial", 14)).grid(row=4, column=0, sticky="w", pady=6)
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

        # SAVE BUTTON
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=20)

        save_btn = tk.Button(btn_frame, text="Save Work")
        save_btn.pack()

        # SAVE HANDLER
        def save():
            class_text = vars["class"].get()
            class_id = next((c["class_id"] for c in classes
                            if f'{c["class_name"]} {c["section"]}' == class_text), None)

            payload = {
                "class_id": class_id,
                "teacher_id": self.teacher_id,
                "subject": vars["subject"].get(),
                "work_type": vars["work_type"].get(),
                "title": vars["title"].get(),
                "description": vars["description"].get(),
                "due_date": due_date.get_date().isoformat(),
            }

            if not selected_file["path"]:
                self.show_popup("Missing PDF", "Please choose a PDF file", "warning")
                return

            with open(selected_file["path"], "rb") as f:
                files = {"file": (os.path.basename(selected_file["path"]), f, "application/pdf")}
                r = requests.post("http://127.0.0.1:8000/teacher/work/add", data=payload, files=files)

            if r.status_code in (200, 201):
                self.show_popup("Success", "Work Added")
                self.load_teacher_work_records()
            else:
                self.show_popup("Error", r.text, "error")

        save_btn.config(command=save)


    def load_teacher_edit_work(self, work_id: int):
        self.clear_content()

        tk.Label(
            self.content,
            text="Edit My Work",
            font=("Arial", 26, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(pady=20)

        # FETCH WORK (from teacher side)
        try:
            res = requests.get(f"http://127.0.0.1:8000/admin/work/{work_id}")
            if res.status_code != 200:
                self.show_popup("Error", "Work not found", "error")
                return
            work = res.json()
        except:
            self.show_popup("Error", "Server error", "error")
            return

        # SECURITY: teacher can edit only their own work
        if work["teacher_name"] != self.teacher_full_name:
            self.show_popup("Not Allowed", "You can edit only your own work.", "warning")
            return

        # FETCH CLASSES
        try:
            classes = requests.get("http://127.0.0.1:8000/admin/timetable/classes").json()
        except:
            classes = []

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        vars = {
            "class": tk.StringVar(value=f'{work.get("class_name","")} {work.get("section","")}'.strip()),
            "subject": tk.StringVar(value=work.get("subject")),
            "title": tk.StringVar(value=work.get("title")),
            "work_type": tk.StringVar(value=work.get("work_type")),
            "description": tk.StringVar(value=work.get("description")),
        }

        # CLASS
        tk.Label(form, text="Class:", font=("Arial", 14), bg="#ECF0F1")\
            .grid(row=0, column=0, sticky="w", pady=6)
        class_display = [f'{c["class_name"]} {c["section"]}' for c in classes]
        ttk.Combobox(
            form, textvariable=vars["class"], values=class_display,
            state="readonly", width=30
        ).grid(row=0, column=1, pady=6, padx=10)

        # SUBJECT
        tk.Label(form, text="Subject:", font=("Arial", 14), bg="#ECF0F1")\
            .grid(row=1, column=0, sticky="w", pady=6)
        tk.Entry(form, textvariable=vars["subject"], font=("Arial", 14),
                width=30, state="readonly").grid(row=1, column=1, padx=10)

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

        # BUTTONS
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Back", command=self.load_teacher_work_records)\
            .pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancel", command=self.load_teacher_work_records)\
            .pack(side="left", padx=10)

        save_btn = tk.Button(btn_frame, text="Save Changes")
        save_btn.pack(side="left", padx=10)

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

            r = requests.put(f"http://127.0.0.1:8000/teacher/work/{work_id}", json=payload)

            if r.status_code == 200:
                self.show_popup("Success", "Work Updated", "info")
                self.load_teacher_work_records()
            else:
                self.show_popup("Error", r.text, "error")

        save_btn.config(command=save)


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
    app = TeacherUI(root)
    root.mainloop()
