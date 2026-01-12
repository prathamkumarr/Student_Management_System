import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import datetime
import requests

import sys

# ---- Get student_id from CLI ----
if len(sys.argv) > 1:
    try:
        STUDENT_ID = int(sys.argv[1])
    except:
        print("Invalid student id received")
        sys.exit()
else:
    print("Student ID not provided!")
    sys.exit()

BASE_API_URL = "http://127.0.0.1:8000/admin"

# ----- API HELPER FUNCTIONS -----
def fetch_subjects():
    try:
        res = requests.get(f"{BASE_API_URL}/subjects", timeout=5)
        if res.status_code == 200:
            return res.json()
    except requests.RequestException as e:
        print("Error fetching subjects:", e)
    return []

# =============
class StudentUI:
    def __init__(self, root, student_id):
        self.root = root

        # Student Logged-In Details (Dummy OR Fetched From Login)
        self.student_id = student_id

        self.root.title(f"School ERP - Student Panel - ID {self.student_id}")
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
            text="STUDENT PANEL",
            bg="#1E2A38",
            fg="white",
            font=("Arial", 18, "bold")
        )
        title.pack(fill="x", pady=(20, 20))
        
        # ---------- WRAPPER PUSHES LOGOUT DOWN ----------
        self.menu_wrapper = tk.Frame(self.sidebar, bg="#1E2A38")
        self.menu_wrapper.pack(fill="both", expand=True)

        # Main Buttons
        att_btn = self.add_btn("View Attendances")
        self.build_attendance_dropdown(att_btn)

        fee_btn = self.add_btn("Pay and View Fees")
        self.build_fees_dropdown(fee_btn)
        
        result_btn = self.add_btn("View Marks and Results")
        self.build_result_dropdown(result_btn)
    
        # Timetable Button
        tt_btn = self.add_btn("View Timetable", self.load_view_timetable_screen)

        # Work Button 
        work_btn = self.add_btn("View Works", self.load_view_work_screen)

        # Extra Curricular Activities Button
        act_btn = self.add_btn("Extra Curricular Activities", self.load_my_activities)

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

        student.add_command(label="Filter by Date", command=self.load_filter_student_attendance_screen)
        student.add_command(label="Attendance Summary", command=self.load_student_attendance_summary_screen)
        menu.add_cascade(label="Student Attendance", menu=student)
        
        parent_label.bind("<Button-1>", lambda e: menu.tk_popup(e.x_root, e.y_root))
    
    # =========================================
    def build_fees_dropdown(self, parent_label):
        menu = tk.Menu(self.root, tearoff=0)

        # always visible
        menu.add_command(label="View Pending Fee", command=self.load_view_pending_fee_screen)
        menu.add_command(label="Fee History", command=self.load_fee_history_screen)
        menu.add_command(label="Download Receipt", command=self.load_download_receipt_screen)
        
        parent_label.bind("<Button-1>", lambda e: menu.tk_popup(e.x_root, e.y_root))

    # =========================================
    def build_result_dropdown(self, parent_label):
        menu = tk.Menu(self.root, tearoff=0)

        # always visible
        menu.add_command(label="View Subject-wise Marks", command=self.load_view_subject_wise_marks)
        menu.add_command(label="View Exam-wise Result", command=self.load_view_exam_wise_result)
        menu.add_command(label="View Final Annual Result", command=self.load_view_final_annual_result)
        menu.add_command(label="Download Result PDF", command=self.load_download_result_pdf)

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

        # ------------ Add Another Button ------------
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

        # ADD ANOTHER BUTTON 
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

    # ============================================================================
    # ===== Button to View attendance by Date Filters =====
    def load_filter_student_attendance_screen(self):
        self.clear_content()

        # ===== PAGE TITLE =====
        tk.Label(
        self.content,
        text="Filter Attendance by Date",
        font=("Arial", 24, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # ===== FORM FRAME =====
        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # ===== STUDENT ID (readonly) =====
        tk.Label(form, text="Student ID:", font=("Arial", 14), bg="#ECF0F1") \
        .grid(row=0, column=0, padx=10, pady=10, sticky="w")

        student_id_var = tk.StringVar(value=str(self.student_id))

        tk.Entry(
        form, textvariable=student_id_var,
        font=("Arial", 14), width=25,
        state="readonly"
        ).grid(row=0, column=1, padx=10, pady=10)

        # ===== DATE FROM =====
        tk.Label(form, text="Date From (YYYY-MM-DD):", font=("Arial", 14), bg="#ECF0F1") \
        .grid(row=1, column=0, padx=10, pady=10, sticky="w")

        date_from_var = tk.StringVar()
        date_from_entry = tk.Entry(
            form, textvariable=date_from_var,
            font=("Arial", 14), width=20)
        date_from_entry.grid(row=1, column=1, padx=5, pady=10)

        tk.Button(
                form,
                text="calendar",
                font=("Arial", 12),
                bg="white",
                relief="flat",
                command=lambda e=date_from_entry, v=date_from_var: self.open_calendar_popup(e, v)
            ).grid(row=1, column=2, padx=5)

        # ===== DATE TO =====
        tk.Label(form, text="Date To (YYYY-MM-DD):", font=("Arial", 14), bg="#ECF0F1") \
        .grid(row=2, column=0, padx=10, pady=10, sticky="w")

        date_to_var = tk.StringVar()
        date_to_entry = tk.Entry(
            form, textvariable=date_to_var,
            font=("Arial", 14), width=20)
        date_to_entry.grid(row=2, column=1, padx=5, pady=10)

        tk.Button(
                form,
                text="calendar",
                font=("Arial", 12),
                bg="white",
                relief="flat",
                command=lambda e=date_to_entry, v=date_to_var: self.open_calendar_popup(e, v)
            ).grid(row=2, column=2, padx=5)

        # ===== SUBJECT ID (optional) =====
        tk.Label(form, text="Subject ID (Optional):", font=("Arial", 14), bg="#ECF0F1") \
        .grid(row=3, column=0, padx=10, pady=10, sticky="w")

        subject_var = tk.StringVar()
        tk.Entry(
        form, textvariable=subject_var,
        font=("Arial", 14), width=25
        ).grid(row=3, column=1, padx=10, pady=10)

        # ===== BACK BUTTON =====
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(pady=10)
        self.create_back_button(back_frame, self.load_dashboard, form)

        # ===== FILTER BUTTON =====
        filter_btn = tk.Label(
        self.content,
        text="Apply Filter",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=12,
        width=15,
        relief="ridge",
        cursor="arrow"
        )
        filter_btn.pack(pady=15)

        # ===== ENABLE / DISABLE BUTTON =====
        def enable_btn():
            filter_btn.config(bg="#000", fg="white", cursor="hand2")
            filter_btn.bind("<Enter>", lambda e: filter_btn.config(bg="#222222"))
            filter_btn.bind("<Leave>", lambda e: filter_btn.config(bg="#000000"))
            filter_btn.bind("<Button-1>", lambda e: apply_filter())

        def disable_btn():
            filter_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            filter_btn.unbind("<Enter>")
            filter_btn.unbind("<Leave>")
            filter_btn.unbind("<Button-1>")

        disable_btn()

        # ===== VALIDATION =====
        def validate(*args):
            d1 = date_from_var.get().strip()
            d2 = date_to_var.get().strip()

            import re
            date_regex = r"^\d{4}-\d{2}-\d{2}$"

            # Don't validate empty fields  
            if d1 == "" and d2 == "":
                disable_btn()
                return

            # Validate only when FULL length reached  
            if (d1 and len(d1) == 10 and not re.match(date_regex, d1)) or \
               (d2 and len(d2) == 10 and not re.match(date_regex, d2)):
                disable_btn()
                self.show_popup("Invalid Date", "Date should be in format YYYY-MM-DD", "warning")
                return

            # Enable only when both dates are valid  
            if re.match(date_regex, d1) and re.match(date_regex, d2):
                enable_btn()
            else:
                disable_btn()

        date_from_var.trace_add("write", validate)
        date_to_var.trace_add("write", validate)

        # ===== RESULTS TABLE =====
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        cols = ("attendance_id", "student_id", "subject_id", "class_id", "lecture_date", "status", "remarks")

        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        self.filter_tree = ttk.Treeview(
        table_frame,
        columns=cols,
        show="headings",
        height=18,
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
        )
        self.filter_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.filter_tree.yview)
        x_scroll.config(command=self.filter_tree.xview)

        col_widths = {
        "attendance_id": 150,
        "student_id": 120,
        "subject_id": 120,
        "class_id": 120,
        "lecture_date": 150,
        "status": 100,
        "remarks": 200
        }

        for col in cols:
            self.filter_tree.heading(col, text=col.replace("_", " ").title())
            self.filter_tree.column(col, width=col_widths[col], anchor="center")

        # ===== APPLY FILTER (API CALL) =====
        def apply_filter():
            payload = {
            "student_id": int(self.student_id),
            "date_from": date_from_var.get().strip(),
            "date_to": date_to_var.get().strip(),
            "subject_id": int(subject_var.get().strip()) if subject_var.get().strip() else None
            }
            import requests
            try:
                response = requests.post("http://127.0.0.1:8000/student/attendance/by-date", json=payload)
                data = response.json() if response.status_code == 200 else []

                for row in self.filter_tree.get_children():
                    self.filter_tree.delete(row)

                for r in data:
                    self.filter_tree.insert(
                    "",
                    "end",
                    values=(
                        r["attendance_id"],
                        r["student_id"],
                        r["subject_id"],
                        r["class_id"],
                        r["lecture_date"],
                        r["status"],
                        r["remarks"]
                    )
                    )
 
            except Exception as e:
                self.show_popup("Backend Error", f"{e}", "error")


    # ============================================================================
    # ===== Button to View Student Attendance Summary =====
    def load_student_attendance_summary_screen(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="Student Attendance Summary",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # ===== FORM FRAME =====
        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # ===== Student ID (AUTO) =====
        tk.Label(
        form,
        text="Student ID:",
        font=("Arial", 14),
        bg="#ECF0F1"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        student_id_var = tk.StringVar(value=str(self.student_id))

        tk.Entry(
        form,
        textvariable=student_id_var,
        font=("Arial", 14),
        width=25,
        state="readonly"
        ).grid(row=0, column=1, padx=10, pady=10)

        # ===== Date From =====
        tk.Label(
            form,
            text="Date From (YYYY-MM-DD):",
            font=("Arial", 14),
            bg="#ECF0F1"
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")

        date_from_var = tk.StringVar()
        date_from_entry = tk.Entry(
            form,
            textvariable=date_from_var,
            font=("Arial", 14),
            width=20)
        date_from_entry.grid(row=1, column=1, padx=5, pady=10)

        tk.Button(
            form,
            text="calendar",
            font=("Arial", 12),
            bg="white",
            relief="flat",
            command=lambda e=date_from_entry, v=date_from_var: self.open_calendar_popup(e, v)
        ).grid(row=1, column=2, padx=5)

        # ===== Date To =====
        tk.Label(
            form,
            text="Date To (YYYY-MM-DD):",
            font=("Arial", 14),
            bg="#ECF0F1"
        ).grid(row=2, column=0, padx=10, pady=10, sticky="w")

        date_to_var = tk.StringVar()
        date_to_entry = tk.Entry(
            form,
            textvariable=date_to_var,
            font=("Arial", 14),
            width=20)
        date_to_entry.grid(row=2, column=1, padx=5, pady=10)

        tk.Button(
            form,
            text="calendar",
            font=("Arial", 12),
            bg="white",
            relief="flat",
            command=lambda e=date_to_entry, v=date_to_var: self.open_calendar_popup(e, v)
        ).grid(row=2, column=2, padx=5)

        # ===== BACK BUTTON =====
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(pady=10)
        self.create_back_button(back_frame, self.load_dashboard, form)

        # ===== SUBMIT BUTTON =====
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

        # ===== BUTTON ENABLE/DISABLE =====
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

        # ===== VALIDATION =====
        def validate(*args):
            d1 = date_from_var.get().strip()
            d2 = date_to_var.get().strip()

            import re
            date_regex = r"^\d{4}-\d{2}-\d{2}$"

            if d1 == "" or d2 == "":
                disable_btn()
                return

            if (len(d1) == 10 and not re.match(date_regex, d1)) or \
               (len(d2) == 10 and not re.match(date_regex, d2)):
                disable_btn()
                self.show_popup("Invalid Date", "Date should be in format YYYY-MM-DD", "warning")
                return

            if re.match(date_regex, d1) and re.match(date_regex, d2):
                enable_btn()
            else:
                disable_btn()

        date_from_var.trace_add("write", validate)
        date_to_var.trace_add("write", validate)

        # ===== SUMMARY OUTPUT FRAME =====
        summary_frame = tk.Frame(self.content, bg="#ECF0F1")
        summary_frame.pack(pady=20)

        # ===== FETCH SUMMARY FUNCTION =====
        def fetch_summary():
            sid = self.student_id
            d1 = date_from_var.get().strip()
            d2 = date_to_var.get().strip()
            import requests
            try:
                url = f"http://127.0.0.1:8000/student/attendance/summary/{sid}?date_from={d1}&date_to={d2}"
                res = requests.get(url)

                if res.status_code != 200:
                    self.show_popup("Error", "Could not fetch summary!", "error")
                    return

                data = res.json()

                # Clear old summary
                for widget in summary_frame.winfo_children():
                    widget.destroy()

                # ===== SUMMARY CARDS =====
                def card(label, value, row):
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

                card("Total Lectures:", data["total_lectures"], 0)
                card("Present:", data["present"], 1)
                card("Absent:", data["absent"], 2)
                card("Late:", data["late"], 3)
                card("Attendance %:", f"{data['percentage']}%", 4)

                self.show_popup("Success", "Summary Loaded!", "info")

            except Exception as e:
                self.show_popup("Backend Error", f"{e}", "error")
    

    # ============================================================================
    # ===== Button to View Pending Fees =====
    def load_view_pending_fee_screen(self):
        self.clear_content()

    # ===== TITLE =====
        tk.Label(
        self.content,
        text="Pending Fees",
        font=("Arial", 24, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
    ).pack(pady=20)

    # ===== BACK BUTTON =====
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)
        self.create_back_button(back_frame, self.load_dashboard, None)

    # ===== TABLE FRAME =====
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Columns returned by backend
        cols = ("invoice_id", "class_id", "amount_due", "amount_paid", "status", "due_date")

    # ===== TABLE =====
        self.pending_tree = ttk.Treeview(
        table_frame,
        columns=cols,
        show="headings",
        height=18
    )
        self.pending_tree.pack(fill="both", expand=True)

        for col in cols:
            self.pending_tree.heading(col, text=col.replace("_", " ").title())
            self.pending_tree.column(col, width=150, anchor="center")

    # ===== FETCH PENDING DATA =====
        import requests
        try:
            res = requests.get(f"http://127.0.0.1:8000/fees/pending/{self.student_id}")
            self.pending_fee_records = res.json() if res.status_code == 200 else []
        except:
            self.pending_fee_records = []

    # Insert rows
        for r in self.pending_fee_records:
            self.pending_tree.insert("", "end", values=(
            r["invoice_id"],
            r["class_id"],
            r["amount_due"],
            r["amount_paid"],
            r["status"],
            r["due_date"]
        ))

    # ===== PAY BUTTON BELOW TABLE =====
        def pay_selected():
            selected = self.pending_tree.focus()
            if not selected:
                self.show_popup("Error", "Please select an invoice to pay!", "warning")
                return

            values = self.pending_tree.item(selected, "values")

            invoice_id = int(values[0])
            amount_due = float(values[2])

        # OPEN PAYMENT PAGE WITH AUTO-FILLED VALUES
            self.load_pay_fee_screen(invoice_id, amount_due)

        # ==== PAY SELECTED BUTTON (BLACK THEME) ====
        pay_selected_btn = tk.Label(
    self.content,
    text="Pay Selected Invoice",
    font=("Arial", 14, "bold"),
    bg="#000000",
    fg="white",
    padx=20,
    pady=10,
    width=20,
    relief="raised",
    cursor="arrow"
)
        pay_selected_btn.pack(pady=15)

# Hover effect
        pay_selected_btn.bind("<Enter>", lambda e: pay_selected_btn.config(bg="#222222"))
        pay_selected_btn.bind("<Leave>", lambda e: pay_selected_btn.config(bg="#000000"))

# Click action
        pay_selected_btn.bind("<Button-1>", lambda e: pay_selected())

    # ============================================================================
    # ===== Button to Pay Fees ======
    def load_pay_fee_screen(self, invoice_id, amount_due):
        self.clear_content()

    # ===== TITLE =====
        tk.Label(
        self.content,
        text="Pay School Fees",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
    ).pack(pady=20)

    # ===== FORM FRAME =====
        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(pady=10)
        self.create_back_button(back_frame, self.load_view_pending_fee_screen, form)

    # ===== STUDENT ID =====
        tk.Label(form, text="Student ID:", font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=0, pady=10)
        tk.Label(form, text=str(self.student_id), font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=1)

    # ===== INVOICE ID =====
        tk.Label(form, text="Invoice ID:", font=("Arial", 14), bg="#ECF0F1").grid(row=1, column=0, pady=10)
        tk.Label(form, text=str(invoice_id), font=("Arial", 14), bg="#ECF0F1").grid(row=1, column=1)

    # ===== AMOUNT =====
        tk.Label(form, text="Amount (₹):", font=("Arial", 14), bg="#ECF0F1").grid(row=2, column=0, pady=10)
        tk.Label(form, text=str(amount_due), font=("Arial", 14), bg="#ECF0F1").grid(row=2, column=1)

    # Payment Method
        tk.Label(form, text="Payment Method:", font=("Arial", 14), bg="#ECF0F1").grid(row=3, column=0, pady=10)

        method_var = tk.StringVar()
        method_dropdown = ttk.Combobox(form, textvariable=method_var, width=20, state="readonly")
        method_dropdown.grid(row=3, column=1)
 
    # Fetch payment methods
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/fees/payment-methods")
            methods = res.json()
        except:
            methods = []

        method_map = {m["method_name"]: m["method_id"] for m in methods}
        method_dropdown["values"] = list(method_map.keys())

    # ===== PAY NOW BUTTON =====
        def perform_pay():
            if not method_var.get():
                self.show_popup("Error", "Select a payment method!", "warning")
                return

            payload = {
            "invoice_id": invoice_id,
            "student_id": self.student_id,
            "amount": amount_due,
            "payment_method_id": method_map.get(method_var.get())
        }

            try:
                res = requests.post("http://127.0.0.1:8000/fees/pay", json=payload)

                if res.status_code == 200:
                    self.show_popup("Success", "Payment Successful!", "info")
                    self.load_view_pending_fee_screen()

                elif res.status_code == 404:
                    self.show_popup("Invoice Not Found", "This invoice does not exist!", "error")

                elif res.status_code == 400:
                    self.show_popup("Invalid Method", "Payment method disabled or invalid!", "error")

                else:
                    self.show_popup("Error", f"Unexpected: {res.text}", "error")

            except Exception as e:
                self.show_popup("Backend Error", str(e), "error")

        # ==== PAY NOW BUTTON (BLACK THEME) ====
        pay_btn = tk.Label(
    self.content,
    text="Pay Now",
    font=("Arial", 16, "bold"),
    bg="#000000",
    fg="white",
    padx=20,
    pady=12,
    width=15,
    relief="raised",
    cursor="arrow"
)
        pay_btn.pack(pady=15)

        pay_btn.bind("<Enter>", lambda e: pay_btn.config(bg="#222222"))
        pay_btn.bind("<Leave>", lambda e: pay_btn.config(bg="#000000"))

# Enable click
        pay_btn.bind("<Button-1>", lambda e: perform_pay())

    # ============================================================================
    # ===== Button to View Fee History =====
    def load_fee_history_screen(self):
        self.clear_content()

    # ===== TITLE =====
        tk.Label(
        self.content,
        text="Fee Payment History",
        font=("Arial", 24, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
    ).pack(pady=20)

    # ===== BACK BUTTON =====
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(fill="x", pady=(0, 10))
        self.create_back_button(back_frame, self.load_dashboard, None)

    # ===== TABLE FRAME =====
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(10, 5))

        cols = (
        "payment_id", "invoice_id", "student_id",
        "amount", "method_id",
        "payment_method_name",
        "status"
    )

    # Scrollbars
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

    # Table
        self.fee_history_tree = ttk.Treeview(
        table_frame,
        columns=cols,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set,
    )
        self.fee_history_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.fee_history_tree.yview)
        x_scroll.config(command=self.fee_history_tree.xview)

        widths = {
        "payment_id": 120,
        "invoice_id": 120,
        "student_id": 120,
        "amount": 120,
        "method_id": 120,
        "payment_method_name": 200,
        "status": 120,
    }

        for col in cols:
            self.fee_history_tree.heading(col, text=col.replace("_", " ").title())
            self.fee_history_tree.column(col, width=widths[col], anchor="center")

    # ===== FILTER + BUTTONS BELOW TABLE =====
        bottom_filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        bottom_filter_frame.pack(pady=15)

    # Sort label
        tk.Label(
        bottom_filter_frame,
        text="Sort By:",
        font=("Arial", 12, "bold"),
        bg="#ECF0F1"
    ).grid(row=0, column=0, padx=5)

    # Dropdown
        filter_var = tk.StringVar()
        filter_dropdown = ttk.Combobox(
        bottom_filter_frame,
        textvariable=filter_var,
        values=list(cols),
        state="readonly",
        width=18
    )
        filter_dropdown.grid(row=0, column=1, padx=10)

    # Value box
        filter_value_var = tk.StringVar()
        filter_value = tk.Entry(
        bottom_filter_frame,
        textvariable=filter_value_var,
        font=("Arial", 12),
        width=20
    )
        filter_value.grid(row=0, column=2, padx=10)

    # ===== BUTTON STYLING =====
        def style_button(btn):
            btn.config(
            bg="#000000", fg="white",
            padx=15, pady=5, width=10,
            relief="raised", cursor="hand2",
            font=("Arial", 12, "bold")
        )
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

    # Load button
        load_btn = tk.Label(bottom_filter_frame, text="Load")
        style_button(load_btn)
        load_btn.grid(row=0, column=3, padx=10)

    # Load All button
        load_all_btn = tk.Label(bottom_filter_frame, text="Load All")
        style_button(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

    # ===== FETCH BACKEND DATA =====
        student_id = self.student_id
        import requests
        try:
            res = requests.get(f"http://127.0.0.1:8000/fees/history/{student_id}")
            self.fee_history_records = res.json() if res.status_code == 200 else []
        except:
            self.fee_history_records = []

    # ===== VALIDATION DICT =====
        self.fee_history_validation = {
        "payment_id": [str(r["payment_id"]) for r in self.fee_history_records],
        "invoice_id": [str(r["invoice_id"]) for r in self.fee_history_records],
        "student_id": [str(r["student_id"]) for r in self.fee_history_records],
        "amount": [str(r["amount"]) for r in self.fee_history_records],
        "payment_method_name": [r["payment_method_name"] for r in self.fee_history_records],
        "method_id": [str(r["method_id"]) for r in self.fee_history_records],
        "status": [r["status"] for r in self.fee_history_records]
    }

    # ===== TABLE UPDATE =====
        def update_fee_history_table(data):
            for row in self.fee_history_tree.get_children():
                self.fee_history_tree.delete(row)

            for r in data:
                self.fee_history_tree.insert(
                "",
                "end",
                values=(
                    r["payment_id"],
                    r["invoice_id"],
                    r["student_id"],
                    r["amount"],
                    r["method_id"],
                    r["payment_method_name"],
                    r["status"]
                )
            )

    # ===== FILTERING =====
        def load_filtered():
            col = filter_var.get().strip()
            val = filter_value_var.get().strip()

            if not col or not val:
                return

            valid_list = self.fee_history_validation.get(col, [])
            valid_lower = [str(v).lower() for v in valid_list]

            if val.lower() not in valid_lower:
                self.show_popup(
                "Invalid Search",
                f"'{val}' not found in '{col}'.",
                "warning"
            )
                filter_value_var.set("")
                return

            filtered = [
            r for r in self.fee_history_records
            if str(r[col]).lower() == val.lower()
        ]

            update_fee_history_table(filtered)

        def load_all():
            update_fee_history_table(self.fee_history_records)

        load_btn.bind("<Button-1>", lambda e: load_filtered())
        load_all_btn.bind("<Button-1>", lambda e: load_all())

    # INITIAL LOAD
        update_fee_history_table(self.fee_history_records)

    # ============================================================================
    # ===== Button to Download Receipt =====
    def load_download_receipt_screen(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="Download Fee Receipt",
        font=("Arial", 24, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # ===== FORM FRAME =====
        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # Invoice ID
        tk.Label(
        form,
        text="Invoice ID:",
        font=("Arial", 14),
        bg="#ECF0F1"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        invoice_var = tk.StringVar()

        tk.Entry(
        form,
        textvariable=invoice_var,
        width=25,
        font=("Arial", 14)
        ).grid(row=0, column=1, padx=10, pady=10)

        # ===== BACK BUTTON =====
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(pady=10)
        self.create_back_button(back_frame, self.load_dashboard, form)

        self.content.update_idletasks()

        # ===== DOWNLOAD BUTTON =====
        download_btn = tk.Label(
        self.content,
        text="Download",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=12,
        width=12,
        relief="ridge",
        cursor="arrow"
        )
        download_btn.pack(pady=20)

        # Enable/disable button
        def enable():
            download_btn.config(bg="#000", fg="white", cursor="hand2")
            download_btn.bind("<Enter>", lambda e: download_btn.config(bg="#222222"))
            download_btn.bind("<Leave>", lambda e: download_btn.config(bg="#000000"))
            download_btn.bind("<Button-1>", lambda e: download_now())

        def disable():
            download_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            download_btn.unbind("<Enter>")
            download_btn.unbind("<Leave>")
            download_btn.unbind("<Button-1>")

        disable()

        # Validation
        def validate(*args):
            inv = invoice_var.get().strip()

            if not inv.isdigit():
                disable()
            else:
                enable()

        invoice_var.trace_add("write", validate)

        # ===== DOWNLOAD FUNCTION =====
        def download_now():
            inv = invoice_var.get().strip()
            import requests
            try:
                url = f"http://127.0.0.1:8000/fees/receipt/{inv}"
                res = requests.get(url)

                if res.status_code != 200:
                    self.show_popup("Error", "Invoice not found!", "error")
                    return

                # -------- Extract filename from headers --------
                fname = f"receipt_{inv}.pdf"
                if "content-disposition" in res.headers:
                    import re
                    cd = res.headers["content-disposition"]
                    match = re.findall('filename="?(.+)"?', cd)
                    if match:
                        fname = match[0]

                # -------- Ask where to save --------
                from tkinter import filedialog
                file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                initialfile=fname
                    )

                if not file_path:
                    return

                # -------- Save File --------
                with open(file_path, "wb") as f:
                    f.write(res.content)

                # -------- Chrome-style bottom-right mini-notification --------
                self.show_mini_notification(f"Downloaded: {fname}")
                self.change_screen(
                    "Receipt Downloaded Successfully!",
                    add_callback=self.load_download_receipt_screen
                )

            except Exception as e:
                self.show_popup("Backend Error", str(e), "error")


    # ============================================================================
    # ----- Button to View Marks Subject - wise
    def load_view_subject_wise_marks(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="View Subject-wise Marks",
        font=("Arial", 24, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # ===== SUBJECT ID INPUT =====
        tk.Label(
        form,
        text="Enter Subject ID:",
        font=("Arial", 14),
        bg="#ECF0F1"
        ).grid(row=0, column=0, padx=10)

        # ===== FETCH SUBJECTS FOR DROPDOWN =====
        subjects = fetch_subjects()

        self.subject_map = {
            f"{s['subject_name']}": s["subject_id"]
            for s in subjects
        }

        subject_values = list(self.subject_map.keys())
        
        from tkinter.ttk import Combobox

        subject_var = tk.StringVar()

        subject_dd = Combobox(
        form,
        textvariable=subject_var,
        values=subject_values,
        state="readonly",
        font=("Arial", 14),
        width=22
        )
        subject_dd.grid(row=0, column=1, padx=10)

        # ===== BACK BUTTON =====
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(pady=10)
        self.create_back_button(back_frame, self.load_dashboard, form)

        # ===== TABLE =====
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
 
        cols = ("exam_id", "marks")
        marks_tree = ttk.Treeview(table_frame, columns=cols, show="headings")

        marks_tree.heading("exam_id", text="Exam ID")
        marks_tree.heading("marks", text="Marks Obtained")

        marks_tree.column("exam_id", anchor="center", width=150)
        marks_tree.column("marks", anchor="center", width=200)

        marks_tree.pack(fill="both", expand=True)

        # ===== LOAD MARKS FUNCTION =====
        def load_marks():
            subject_name = subject_var.get().strip()

            if subject_name not in self.subject_map:
                self.show_popup("Invalid Selection", "Please select a subject!", "warning")
                return

            subject_id = self.subject_map[subject_name]

            import requests
            url = f"http://127.0.0.1:8000/student/result/marks/{self.student_id}/{subject_id}"

            res = requests.get(url)

            if res.status_code != 200:
                self.show_popup("No Data", "No marks found for this subject", "info")
                return
   
            data = res.json()
            marks_tree.delete(*marks_tree.get_children())

            for m in data:
                marks_tree.insert(
                "",
                "end",
                values=(m["exam_id"], f'{m["marks_obtained"]}/{m["max_marks"]}')
                )

        # ===== LOAD BUTTON =====
        load_btn = tk.Label(
        self.content,
        text="Load Marks",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=8,
        width=12,
        relief="ridge",
        cursor="arrow"
        )
        load_btn.pack(pady=15)
        
        def enable_load():
            load_btn.config(bg="#000000", fg="white", cursor="hand2")
            load_btn.bind("<Enter>", lambda e: load_btn.config(bg="#222222"))
            load_btn.bind("<Leave>", lambda e: load_btn.config(bg="#000000"))
            load_btn.bind("<Button-1>", lambda e: load_marks())

        def disable_load():
            load_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            load_btn.unbind("<Enter>")
            load_btn.unbind("<Leave>")
            load_btn.unbind("<Button-1>")

        # ===== ENABLE / DISABLE BASED ON INPUT =====
        def validate_subject(*args):
            if subject_var.get().strip() in self.subject_map:
                enable_load()
            else:
                disable_load()

        subject_var.trace_add("write", validate_subject)

    # ==============================================================================
    # ----- Button to Result Exam - wise -----
    def load_view_exam_wise_result(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="View Exam-wise Result",
        font=("Arial", 24, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # ===== FORM FRAME =====
        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # ===== EXAM DROPDOWN =====
        tk.Label(
        form,
        text="Select Exam:",
        font=("Arial", 14),
        bg="#ECF0F1"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
 
        exam_var = tk.StringVar()
        exam_dropdown = ttk.Combobox(form, textvariable=exam_var, state="readonly", width=30)
        exam_dropdown.grid(row=0, column=1, padx=10, pady=10)

        # ------- Fetch Exams from backend -------
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admin/exams/all")
            exam_data = res.json()

            exam_map = { e["exam_name"]: e["exam_id"] for e in exam_data }
            exam_dropdown["values"] = list(exam_map.keys())
  
        except Exception as e:
            exam_dropdown["values"] = []
            print("Error loading exams:", e)

        # ===== BACK BUTTON =====
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(pady=10)
        self.create_back_button(back_frame, self.load_dashboard, form)
 
        # ===== LOAD RESULT BUTTON =====
        load_btn = tk.Label(
        self.content,
        text="Load Result",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=12,
        width=12,
        relief="ridge",
        cursor="arrow"
        )
        load_btn.pack(pady=20)

        # Enable/disable on selection
        def validate(*args):
            if exam_var.get().strip():
                load_btn.config(bg="#000000", fg="white", cursor="arrow")
                load_btn.bind("<Enter>", lambda e: load_btn.config(bg="#222222"))
                load_btn.bind("<Leave>", lambda e: load_btn.config(bg="#000000"))
                load_btn.bind("<Button-1>", lambda e: load_result())
            else:
                load_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                load_btn.unbind("<Enter>")
                load_btn.unbind("<Leave>")
                load_btn.unbind("<Button-1>")

        exam_var.trace_add("write", validate)

        # ===== RESULT FRAME =====
        result_frame = tk.Frame(self.content, bg="#ECF0F1")
        result_frame.pack(pady=20)

        # ===== LOAD RESULT FUNCTION =====
        def load_result():
            exam_name = exam_var.get()
            exam_id = exam_map[exam_name]

            url = f"http://127.0.0.1:8000/student/result/{self.student_id}/{exam_id}"

            try:
                res = requests.get(url)

                if res.status_code != 200:
                    self.show_popup("Not Found", "No result available for this exam!", "info")
                    return

                data = res.json()

                # Clear old result
                for widget in result_frame.winfo_children():
                    widget.destroy()

                # Show Summary Card
                tk.Label(
                result_frame,
                text=f"Exam: {exam_name}",
                font=("Arial", 18, "bold"),
                bg="#ECF0F1",
                fg="#2C3E50"
                ).pack(pady=10)
  
                tk.Label(
                result_frame,
                text=f"Total Marks: {data['total_marks']}",
                font=("Arial", 16),
                bg="#ECF0F1"
                ).pack(pady=5)

                tk.Label(
                result_frame,
                text=f"Percentage: {data['percentage']}%",
                font=("Arial", 16),
                bg="#ECF0F1"
                ).pack(pady=5)

                tk.Label(
                result_frame,
                text=f"Grade: {data['grade']}",
                font=("Arial", 16),
                bg="#ECF0F1"
                ).pack(pady=5)

            except Exception as e:
                self.show_popup("Error", str(e), "error")

    # ==============================================================================
    # ----- Button to View Final Annual Result ------
    def load_view_final_annual_result(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="Final Annual Result",
        font=("Arial", 24, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # ===== LOADING LABEL =====
        loading_label = tk.Label(
        self.content,
        text="Fetching your annual result...",
        font=("Arial", 14),
        bg="#ECF0F1",
        fg="#2C3E50"
        )
        loading_label.pack(pady=10)

        # ===== RESULT FRAME =====
        result_frame = tk.Frame(self.content, bg="#ECF0F1")
        result_frame.pack(pady=20)

        # ===== BACK BUTTON =====
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(pady=10)
        self.create_back_button(back_frame, self.load_dashboard, result_frame)

        # ===== FETCH RESULT FUNCTION =====
        def fetch_result():
            import requests
            try:
                url = f"http://127.0.0.1:8000/admin/results/final/{self.student_id}"
                res = requests.get(url)

                # Clear loading label
                loading_label.destroy()

                if res.status_code != 200:
                    tk.Label(
                    result_frame,
                    text="No final result found!",
                    font=("Arial", 16),
                    bg="#ECF0F1",
                    fg="red"
                    ).pack()

                    return

                data = res.json()

                # ================= SUMMARY CARD =================
                card = tk.Frame(
                result_frame,
                bg="white",
                bd=1,
                relief="solid"
                )
                card.pack(pady=20, padx=40)

                # Student ID
                tk.Label(
                card,
                text=f"Student ID: {data['student_id']}",
                font=("Arial", 14, "bold"),
                bg="white",
                fg="#2C3E50"
                ).pack(pady=(15, 10))

                # Total Marks (BIG)
                tk.Label(
                card,
                text=f"{data['total_marks']} / {data['max_marks']}",
                font=("Arial", 28, "bold"),
                bg="white",
                fg="#1F618D"
                 ).pack()

                tk.Label(
                card,
                text="Total Marks",
                font=("Arial", 12),
                bg="white",
                fg="#7F8C8D"
                ).pack(pady=(0, 12))

                # Percentage + Grade Row
                row = tk.Frame(card, bg="white")
                row.pack(pady=10)

                tk.Label(
                row,
                text=f"{data['percentage']}%",
                font=("Arial", 18, "bold"),
                bg="white",
                fg="#117864",
                width=12
                ).grid(row=0, column=0, padx=5)

                tk.Label(
                row,
                text=f"Grade {data['final_grade']}",
                font=("Arial", 18, "bold"),
                bg="white",
                fg="#7D3C98",
                width=12
                ).grid(row=0, column=1, padx=5)

                # ================= DIVIDER =================
                tk.Frame(
                result_frame,
                height=1,
                bg="#D5D8DC"
                ).pack(fill="x", padx=60, pady=20)

                # ================= EXAM WISE =================
                tk.Label(
                result_frame,
                text="Exam-wise Breakdown",
                font=("Arial", 16, "bold"),
                bg="#ECF0F1",
                fg="#2C3E50"
                ).pack(pady=(0, 10))

                for exam in data["exam_wise_details"]:
                    exam_row = tk.Frame(result_frame, bg="#ECF0F1")
                    exam_row.pack(pady=4)

                    tk.Label(
                    exam_row,
                    text=f"Exam {exam['exam_id']}",
                    font=("Arial", 13),
                    bg="#ECF0F1",
                    width=10,
                    anchor="w"
                    ).grid(row=0, column=0, padx=10)

                    tk.Label(
                    exam_row,
                    text=f"{exam['obtained_marks']} / {exam['max_marks']}",
                    font=("Arial", 13),
                    bg="#ECF0F1",
                    width=15
                    ).grid(row=0, column=1)
    
                    tk.Label(
                    exam_row,
                    text=f"Grade {exam['grade']}",
                    font=("Arial", 13, "bold"),
                    bg="#ECF0F1",
                    fg="#2E86C1",
                    width=10
                    ).grid(row=0, column=2)

            except Exception as e:
                loading_label.destroy()
                tk.Label(
                result_frame,
                text=f"Error: {str(e)}",
                font=("Arial", 14),
                bg="#ECF0F1",
                fg="red"
                ).pack()

        # Auto-fetch result
        fetch_result()
   
    # ==============================================================================
    # ----- Button to Download PDF -----
    def load_download_result_pdf(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="Download Result PDF",
        font=("Arial", 24, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # ===== FORM FRAME =====
        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)
        
        # ===== Exam ID Label =====
        tk.Label(
        form,
        text="Select Exam:",
        font=("Arial", 14),
        bg="#ECF0F1"
        ).grid(row=0, column=0, padx=10, pady=10)

        # Dropdown
        exam_var = tk.StringVar()
        exam_dropdown = ttk.Combobox(
        form, textvariable=exam_var, width=25, font=("Arial", 14), state="readonly"
        )
        exam_dropdown.grid(row=0, column=1, padx=10, pady=10)
        
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(pady=10)
        self.create_back_button(back_frame, self.load_dashboard, form)

        # === FETCH ALL EXAM OPTIONS ===
        def load_exams():
            import requests
            try:
                url = "http://127.0.0.1:8000/admin/exams/all"
                res = requests.get(url)

                if res.status_code == 200:
                    exams = res.json()
                    exam_dropdown['values'] = [
                    f"{ex['exam_id']} - {ex['exam_name']}"
                    for ex in exams
                ]
            except:
                pass

        load_exams()

        # ===== DOWNLOAD BUTTON =====
        download_btn = tk.Label(
        self.content,
        text="Download PDF",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=12,
        width=15,
        relief="ridge",
        cursor="arrow"
        )
        download_btn.pack(pady=20)

        # ===== ENABLE/DISABLE LOGIC =====
        def enable():
            download_btn.config(bg="#000000", fg="white", cursor="arrow")
            download_btn.bind("<Enter>", lambda e: download_btn.config(bg="#222222"))
            download_btn.bind("<Leave>", lambda e: download_btn.config(bg="#000000"))
            download_btn.bind("<Button-1>", lambda e: download_now())

        def disable():
            download_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            download_btn.unbind("<Enter>")
            download_btn.unbind("<Leave>")
            download_btn.unbind("<Button-1>")

        disable()

        def validate(*args):
            val = exam_var.get().strip()
            if val:
                enable()
            else:
                disable()

        exam_var.trace_add("write", validate)

        # ===== DOWNLOAD FUNCTION =====
        def download_now():
            try:
                import requests

                exam_id = exam_var.get().split(" - ")[0]

                url = f"http://127.0.0.1:8000/student/result/download/{self.student_id}/{exam_id}"
                res = requests.get(url)

                if res.status_code != 200:
                    self.show_popup("Error", "Result not found!", "error")
                    return

                # Ask user where to save file
                from tkinter import filedialog
                path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")],
                initialfile=f"result_{self.student_id}_{exam_id}.pdf"
                )

                if not path:
                    return

                # Save received PDF content
                with open(path, "wb") as f:
                    f.write(res.content)

                self.show_mini_notification("Download Completed!")
                self.change_screen(
                "Result PDF Downloaded Successfully!",
                add_callback=self.load_download_result_pdf
                )

            except Exception as e:
                self.show_popup("Error", str(e), "error")
    # View Timetable Screen------
    def load_view_timetable_screen(self):
        self.clear_content()

        tk.Label(
            self.content,
            text="My Class Timetable",
            font=("Arial", 24, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(pady=20)

        # === Back Button ===
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)
        self.create_back_button(back_frame, self.load_dashboard)

        # === Fetch Timetable Data ===
        try:
            url = f"http://127.0.0.1:8000/student/timetable/{self.student_id}"
            res = requests.get(url)
            data = res.json() if res.status_code == 200 else []

        except Exception as e:
            self.show_popup("Backend Error", str(e), "error")
            data = []

        # === Build Table ===
        cols = ("day", "subject", "teacher_id", "start_time", "end_time", "room_no")
        rows = [
            (
                r.get("day", ""),
                r.get("subject", ""),
                r.get("teacher_id", ""),
                r.get("start_time", ""),
                r.get("end_time", ""),
                r.get("room_no", "")
            )
            for r in data
        ]

        self.create_scrollable_table(self.content, cols, rows)


    # View Work Screen--------
    def load_view_work_screen(self):
        self.clear_content()

        tk.Label(
            self.content,
            text="My Homework / Class Work",
            font=("Arial", 24, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(pady=20)

        # === Back Button ===
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)
        self.create_back_button(back_frame, self.load_dashboard)


        try:
            url = f"http://127.0.0.1:8000/student/work/{self.student_id}"
            res = requests.get(url)
            data = res.json() if res.status_code == 200 else []
        except Exception as e:
            self.show_popup("Backend Error", str(e), "error")
            data = []

        # === Table Columns ===
        cols = ("title", "subject", "due_date", "download")

        table = ttk.Treeview(
            self.content,
            columns=cols,
            show="headings",
            height=18
        )
        table.pack(fill="both", expand=True, padx=20, pady=20)

        for col in cols:
            table.heading(col, text=col.replace("_", " ").title())
            table.column(col, width=180, anchor="center")

        # === Insert Rows ===
        for r in data:
            table.insert(
                "",
                "end",
                values=(
                    r.get("title", ""),
                    r.get("subject", ""),
                    r.get("due_date", ""),
                    "Download"
                )
            )

        # === PDF Download handler ===
        def on_row_click(event):
            selected = table.focus()
            if not selected:
                return
            
            row = table.item(selected, "values")
            work_title = row[0]

            # find corresponding record from backend result
            for item in data:
                if item.get("title") == work_title:
                    work_id = item.get("work_id")
                    break
            else:
                return

            # Now download
            try:
                pdf_url = f"http://127.0.0.1:8000/student/work/download/{work_id}"
                res = requests.get(pdf_url)

                if res.status_code != 200:
                    self.show_popup("Error", "PDF not available!", "error")
                    return

                filename = f"{work_title}.pdf".replace(" ", "_")

                from tkinter import filedialog
                save_path = filedialog.asksaveasfilename(
                    defaultextension=".pdf",
                    filetypes=[("PDF files", "*.pdf")],
                    initialfile=filename
                )

                if save_path:
                    with open(save_path, "wb") as f:
                        f.write(res.content)

                    self.show_mini_notification(f"Downloaded {filename}")

            except Exception as e:
                self.show_popup("Download Error", str(e), "error")

        table.bind("<Double-1>", on_row_click)


    # View Activity Screen-------
    def load_my_activities(self):
        self.clear_content()

        # TITLE
        tk.Label(
            self.content,
            text="My Extra Curricular Activities",
            font=("Arial", 24, "bold"),
            bg="#ECF0F1"
        ).pack(pady=20)

        student_id = self.student_id  # already set at login

        # === Back Button ===
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)
        self.create_back_button(back_frame, self.load_dashboard)


        try:
            res = requests.get(
                f"http://127.0.0.1:8000/student/activities/{student_id}",
                timeout=5
            )
            activities = res.json() if res.status_code == 200 else []
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        # NO ACTIVITIES CASE
        if not activities:
            tk.Label(
                self.content,
                text="No extra curricular activities assigned",
                font=("Arial", 14),
                bg="#ECF0F1"
            ).pack(pady=40)
            return

        # TABLE
        table = ttk.Treeview(
            self.content,
            columns=("ID", "Activity", "Category", "Teacher"),
            show="headings",
            height=12
        )
        table.pack(fill="both", expand=True, padx=20, pady=10)

        table.heading("ID", text="ID")
        table.heading("Activity", text="Activity Name")
        table.heading("Category", text="Category")
        table.heading("Teacher", text="In-charge Teacher")

        table.column("ID", width=80, anchor="center")
        table.column("Activity", width=260, anchor="center")
        table.column("Category", width=180, anchor="center")
        table.column("Teacher", width=220, anchor="center")

        for a in activities:
            table.insert(
                "",
                "end",
                values=(
                    a["activity_id"],
                    a["activity_name"],
                    a["category"],
                    a["teacher_name"]
                )
            )


    # ==============================================================================
    # ===== DASHBOARD PAGE ======
    def load_dashboard(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        tk.Label(
            self.content,
            text="Student Dashboard",
            font=("Arial", 26, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(pady=20)

        box = tk.Frame(self.content, bg="white", bd=2, relief="groove")
        box.pack(pady=60)

        tk.Label(
            box,
            text="Welcome to the Student Panel!",
            font=("Arial", 16),
            bg="white"
        ).pack(padx=40, pady=30)


# ======== RUN UI ========
if __name__ == "__main__":
    root = tk.Tk()
    ui = StudentUI(root, student_id=STUDENT_ID)
    root.mainloop()