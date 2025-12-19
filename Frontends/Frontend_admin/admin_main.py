import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
from tkinter import messagebox
from tkcalendar import Calendar
import datetime
import os
import requests
import tempfile

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


# ===========
class AdminUI:
    def __init__(self, root):
        self.root = root
        self.root.title("School ERP - Admin Panel")
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


    def _style_button(self, btn):
        btn.config(bg="#000", fg="white", padx=12, pady=6, cursor="hand2", font=("Arial", 12, "bold"))
        btn.bind("<Enter>", lambda e: btn.config(bg="#222"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#000"))

    
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
            text="ADMIN PANEL",
            bg="#1E2A38",
            fg="white",
            font=("Arial", 18, "bold")
        )
        title.pack(fill="x", pady=(20, 20))
        
        # ---------- WRAPPER PUSHES LOGOUT DOWN ----------
        self.menu_wrapper = tk.Frame(self.sidebar, bg="#1E2A38")
        self.menu_wrapper.pack(fill="both", expand=True)

        # Main Buttons
        admission_btn = self.add_btn("Manage Admissions")
        self.build_admission_dropdown(admission_btn)

        att_btn = self.add_btn("Manage Attendances")
        self.build_attendance_dropdown(att_btn)

        fee_btn = self.add_btn("Manage Fees")
        self.build_fees_dropdown(fee_btn)
        
        result_btn = self.add_btn("Manage Exams and Results")
        self.build_result_dropdown(result_btn)

        tc_btn = self.add_btn("Manage TCs")
        self.build_tc_dropdown(tc_btn)

        timetable_btn = self.add_btn("Manage Timetable")
        self.build_timetable_dropdown(timetable_btn)

        work_btn = self.add_btn("Manage Work")
        self.build_work_dropdown(work_btn)

        onboarding_btn = self.add_btn("Manage Onboardings")
        self.build_onboarding_dropdown(onboarding_btn)

        offboarding_btn = self.add_btn("Manage Offboardings and Transfers")
        self.build_offboarding_dropdown(offboarding_btn)
        
        master_btn = self.add_btn("View Master Tables")
        self.build_master_dropdown(master_btn)

        activity_btn = self.add_btn("Manage Extra-Curricular Activities")
        self.build_activity_dropdown(activity_btn)

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

        student.add_command(label="View All Attendance", command=self.load_view_all_student_attendance)
        student.add_command(label="View by ID", command=self.load_view_attendance_by_id)
        student.add_command(label="Filter by Student", command=self.load_filter_student_attendance_screen)
        student.add_command(label="Attendance Summary", command=self.load_attendance_summary_screen)
        student.add_command(label="Update Attendance", command=self.load_update_student_attendance_screen)
        student.add_command(label="Delete Attendance", command=self.load_delete_student_attendance_screen)
        menu.add_cascade(label="Student Attendance", menu=student)
        
        teacher = tk.Menu(menu, tearoff=0)
        teacher.add_command(label="View All Attendance", command=self.load_view_all_teacher_attendance)
        teacher.add_command(label="View by ID", command=self.load_view_teacher_attendance_by_id)
        teacher.add_command(label="Attendance Summary", command=self.load_teacher_attendance_summary_screen)
        teacher.add_command(label="Update Attendance", command=self.load_update_teacher_attendance_screen)
        teacher.add_command(label="Delete Attendance", command=self.load_delete_teacher_attendance_screen)

        menu.add_cascade(label="Teacher Attendance", menu=teacher)
        parent_label.bind("<Button-1>", lambda e: menu.tk_popup(e.x_root, e.y_root))

        staff = tk.Menu(menu, tearoff=0)
        staff.add_command(label="View All Attendance", command=self.load_view_all_staff_attendance)
        staff.add_command(label="View by ID", command=self.load_view_staff_attendance_by_id)
        staff.add_command(label="Attendance Summary", command=self.load_staff_attendance_summary_screen)
        staff.add_command(label="Update Attendance", command=self.load_update_staff_attendance_screen)
        staff.add_command(label="Delete Attendance", command=self.load_delete_staff_attendance_screen)

        menu.add_cascade(label="Staff Attendance", menu=staff)
        parent_label.bind("<Button-1>", lambda e: menu.tk_popup(e.x_root, e.y_root))
    
    # =========================================
    def build_fees_dropdown(self, parent_label):
        menu = tk.Menu(self.root, tearoff=0)

        menu.add_command(label="Create Fee", command=lambda: self.load_create_fee_screen())
        menu.add_command(label="Assign Fee", command=lambda: self.load_assign_fee_screen())
        menu.add_command(label="View Fees", command=lambda: self.load_view_fees_screen())
        menu.add_command(label="Update Fee", command=lambda: self.load_update_fee_screen())
        menu.add_command(label="Delete Fee", command=lambda: self.load_delete_fee_screen())
        menu.add_command(label="Fee History", command=lambda: self.load_fee_history_screen())

        pm = tk.Menu(menu, tearoff=0)
        pm.add_command(label="Add Method", command=lambda: self.load_add_payment_method_screen())
        pm.add_command(label="View Methods", command=lambda: self.load_view_methods_screen())
        pm.add_command(label="View by ID", command=lambda: self.load_view_method_by_id_screen())
        pm.add_command(label="Update Method", command=lambda: self.load_update_method_screen())
        pm.add_command(label="Delete Method", command=lambda: self.load_delete_method_screen())
 
        menu.add_cascade(label="Payment Methods", menu=pm)

        parent_label.bind("<Button-1>", lambda e: menu.tk_popup(e.x_root, e.y_root))
    
    # =========================================
    def build_admission_dropdown(self, parent_label):
        menu = tk.Menu(self.root, tearoff=0)

        menu.add_command(label="Create Admission", command=self.load_create_admission_screen)
        menu.add_command(label="View All Admissions", command=self.load_view_all_admissions_screen)
        menu.add_command(label="View Admission by ID", command=self.load_view_admission_by_id_screen)
        menu.add_command(label="Approve Admission", command=self.load_approve_admission_screen)
        
        parent_label.bind("<Button-1>", lambda e: menu.tk_popup(e.x_root, e.y_root))

    # =========================================
    def build_tc_dropdown(self, parent_label):
        menu = tk.Menu(self.root, tearoff=0)

        menu.add_command(label="Apply TC", command=self.load_issue_tc_screen)
        menu.add_command(label="View TC", command=self.load_view_all_tc_screen)
        menu.add_command(label="Approve TC", command=self.load_approve_tc_screen)

        parent_label.bind("<Button-1>", lambda e: menu.tk_popup(e.x_root, e.y_root))

    # =========================================
    def build_timetable_dropdown(self, parent_label):
        menu = tk.Menu(self.root, tearoff=0)

        menu.add_command(label="View Timetable", command=self.load_view_timetable)
        menu.add_command(label="Add Timetable", command=self.load_add_timetable)

        parent_label.bind("<Button-1>", lambda e: menu.tk_popup(e.x_root, e.y_root))

    # =========================================
    def build_work_dropdown(self, parent_label):
        menu = tk.Menu(self.root, tearoff=0)

        menu.add_command(label="View Work Records", command=self.load_work_records)
        menu.add_command(label="Add Work", command=self.load_add_work)

        parent_label.bind("<Button-1>", lambda e: menu.tk_popup(e.x_root, e.y_root))

    # ==========================================
    def build_onboarding_dropdown(self, parent_label):
        menu = tk.Menu(self.root, tearoff=0)

        menu.add_command(label="Create Teacher Onboarding", command=lambda: self.load_create_onboarding_screen())
        menu.add_command(label="View Teacher Onboarding Queue", command=lambda: self.load_view_onboarding_queue_screen())
        menu.add_command(label="Approve Teacher Onboarding", command=lambda: self.load_approve_teacher_onboarding_screen())

        so = tk.Menu(menu, tearoff=0)
        so.add_command(label="Create Onboarding", command=lambda: self.load_create_staff_onboarding_screen())
        so.add_command(label="View Onboarding Queue", command=lambda: self.load_view_staff_onboarding_queue_screen())
        so.add_command(label="Approve Onboarding", command=lambda: self.load_approve_staff_onboarding_screen())
 
        menu.add_cascade(label="Staff Onboardings", menu=so)

        parent_label.bind("<Button-1>", lambda e: menu.tk_popup(e.x_root, e.y_root))

    # ===========================================
    def build_offboarding_dropdown(self, parent_label):
        menu = tk.Menu(self.root, tearoff=0)

        # ========== TEACHER MENUS ==========
        teacher_menu = tk.Menu(menu, tearoff=0)

        # ---- TEACHER OFFBOARDING SUBMENU ----
        teacher_off_menu = tk.Menu(teacher_menu, tearoff=0)
        teacher_off_menu.add_command(label="Create Separation Request", command=lambda: self.load_issue_teacher_separation_screen())
        teacher_off_menu.add_command(label="View Separation Queue", command=lambda: self.load_view_all_teacher_separation_screen())
        teacher_off_menu.add_command(label="Approve Separation", command=lambda: self.load_approve_teacher_separation_screen())

        teacher_menu.add_cascade(label="Manage Offboardings", menu=teacher_off_menu)

        # ---- TEACHER TRANSFER SUBMENU ----
        teacher_trans_menu = tk.Menu(teacher_menu, tearoff=0)
        teacher_trans_menu.add_command(label="Create Transfer Request", command=lambda: self.load_create_teacher_transfer_screen())
        teacher_trans_menu.add_command(label="View Transfer Queue", command=lambda: self.load_view_all_teacher_transfers_screen())
        teacher_trans_menu.add_command(label="Approve Transfer", command=lambda: self.load_approve_teacher_transfer_screen())

        teacher_menu.add_cascade(label="Manage Transfers", menu=teacher_trans_menu)

        menu.add_cascade(label="For Teachers", menu=teacher_menu)

        # ========== STAFF MENUS ==========
        staff_menu = tk.Menu(menu, tearoff=0)

        staff_off_menu = tk.Menu(staff_menu, tearoff=0)
        staff_off_menu.add_command(label="Create Offboarding", command=lambda: self.load_issue_staff_separation_screen())
        staff_off_menu.add_command(label="View Offboarding Queue", command=lambda: self.load_view_all_staff_separation_screen())
        staff_off_menu.add_command(label="Approve Offboarding", command=lambda: self.load_approve_staff_separation_screen())
        
        staff_menu.add_cascade(label="Manage Offboardings", menu=staff_off_menu)

        staff_trans_menu = tk.Menu(staff_menu, tearoff=0)
        staff_trans_menu.add_command(label="Create Transfer", command=lambda: self.load_create_staff_transfer_screen())
        staff_trans_menu.add_command(label="View Transfer Queue", command=lambda: self.load_view_all_staff_transfers_screen())
        staff_trans_menu.add_command(label="Approve Transfer", command=lambda: self.load_approve_staff_transfer_screen())
        
        staff_menu.add_cascade(label="Manage Transfers", menu=staff_trans_menu)

        menu.add_cascade(label="For Staff", menu=staff_menu)

        parent_label.bind("<Button-1>", lambda e: menu.tk_popup(e.x_root, e.y_root))

    # =========================================
    def build_result_dropdown(self, parent_label):
        menu = tk.Menu(self.root, tearoff=0)

        menu.add_command(label="Create Exam Type", command=lambda: self.load_create_exam_type_screen())
        menu.add_command(label="View all Exam Types", command=lambda: self.load_view_all_exams_screen())
        menu.add_command(label="Update Exam Type", command=lambda: self.load_update_exam_screen())
        menu.add_command(label="Delete Exam Type", command=lambda: self.load_delete_exam_screen())

        rg = tk.Menu(menu, tearoff=0)
        rg.add_command(label="Generate and Download Result of a Student", command=lambda: self.load_generate_and_download_result_of_student())
        rg.add_command(label="Generate and Download Final Result of a Student", command=lambda: self.load_generate_and_download_final_result_of_student())
        rg.add_command(label="View all Result for an Exam", command=lambda: self.load_view_all_results_for_exam())
        rg.add_command(label="Generate and Download all students Results for a class", command=lambda: self.load_view_and_download_all_students_results_for_a_class())
        rg.add_command(label="Generate and Download all Final Results for a Class", command=lambda: self.load_generate_and_download_all_final_results_for_a_class())

        menu.add_cascade(label="Generate Results", menu=rg)

        parent_label.bind("<Button-1>", lambda e: menu.tk_popup(e.x_root, e.y_root))

    # ========================================
    def build_master_dropdown(self, parent_label):
        menu = tk.Menu(self.root, tearoff=0)

        menu.add_command(label="Student Master", command=self.load_student_master)
        menu.add_command(label="Class Master", command=self.load_class_master)
        menu.add_command(label="Teacher Master", command=self.load_teacher_master)
        menu.add_command(label="Subject Master", command=self.load_subject_master)
        menu.add_command(label="Fee Master", command=self.load_fee_master)
        menu.add_command(label="Exam Master", command=self.load_exam_master)
        menu.add_command(label="Result Master", command=self.load_result_master)
        menu.add_command(label="Staff Master", command=self.load_staff_master)
        menu.add_command(label="Salary Master", command=self.load_salary_master)

        parent_label.bind("<Button-1>", lambda e: menu.tk_popup(e.x_root, e.y_root))
    # ========================================
    def build_activity_dropdown(self, parent_label):
        menu = tk.Menu(self.root, tearoff=0)

        menu.add_command(label="View Activities", command=self.load_view_activity)
        menu.add_command(label="Add Activity", command=self.load_add_activity)

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
        cursor="hand2"
    )
        back_btn.grid(row=0, column=0, padx=10)

        hover(back_btn)
        back_btn.bind("<Button-1>", lambda e: (back_callback or self.load_dashboard)())

    # ------------ Add Another Button (Optional) ------------
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
            cursor="hand2"
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
        width=12, cursor="hand2"
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
            width=12, cursor="hand2"
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
       
        # make table available to other methods (right-click / edit / delete etc.)
        self.current_table = table
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

        # Check if click INSIDE popup → DO NOTHING
            if px1 <= event.x_root <= px2 and py1 <= event.y_root <= py2:
                return  # safe click (even month/year click)

        # Click OUTSIDE popup → close
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
    
    def update_method_table(self, data):
    # Remove old rows
        for row in self.method_tree.get_children():
            self.method_tree.delete(row)

    # Add rows
        for row in data:
            self.method_tree.insert("", "end", values=(
            row["method_id"],
            row["method_name"],
            row["is_active"]
        ))
    
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
        
    # ==============================================================================
    # ==== Button to create fee ====
    def load_create_fee_screen(self):
        self.clear_content()

        title = tk.Label(self.content, text="Create Fee", font=("Arial", 26, "bold"),
                        bg="#ECF0F1", fg="#2C3E50")
        title.pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=20)

        labels = ["class_id", "fee_type", "amount", "effective_from", "effective_to", "notes"]
        self.entries = {}

        # StringVar storage for auto tracking
        self.vars = {}

        for i, text in enumerate(labels):
            # Label
            tk.Label(
                form,
                text=text + ":",
                bg="#ECF0F1",
                fg="#2C3E50",
                font=("Arial", 14)
                ).grid(row=i, column=0, sticky="e", padx=10, pady=10)

                # StringVar
            var = tk.StringVar()
            var.trace_add("write", lambda *args: self.validate_fee_form())

            # ---- SPECIAL CASE FOR DATE FIELDS ----
            if text in ("effective_from", "effective_to"):
                entry = tk.Entry(
            form,
            textvariable=var,
            font=("Arial", 14),
            width=20
        )
                entry.grid(row=i, column=1, padx=5, pady=10)

        # calendar button
                tk.Button(
            form,
            text="Calendar",
            font=("Arial", 12),
            bg="white",
            relief="flat",
            command=lambda v=var, e=entry: self.open_calendar_popup(e, v)
        ).grid(row=i, column=2, padx=5)

            else:
        # Normal entry
                entry = tk.Entry(
            form,
            textvariable=var,
            font=("Arial", 14),
            width=25
        )
                entry.grid(row=i, column=1, padx=10, pady=10)

            self.vars[text] = var
            self.entries[text] = entry

        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

        # Back Button from global function
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,    
        form_frame=form                          
        )

        self.content.update_idletasks()

        # Submit Button
        self.submit_btn = tk.Label(
            self.content,
            text="Submit",
            font=("Arial", 16, "bold"),
            bg="#D5D8DC",
            fg="#AEB6BF",
            padx=20,
            pady=12,
            width=12,
            bd=0,
            relief="flat",
            cursor="arrow"   # disabled look
        )
        self.submit_btn.pack(pady=20)

    # ======================
    def enable_submit(self):
        self.submit_btn.config(
        bg="#000000",
        fg="white",
        cursor="hand2"
        )
        self.submit_btn.bind("<Enter>", lambda e: self.submit_btn.config(bg="#222222"))
        self.submit_btn.bind("<Leave>", lambda e: self.submit_btn.config(bg="#000000"))
        self.submit_btn.bind("<Button-1>", lambda e: self.submit_create_fee())
 
    # ======================
    def disable_submit(self):
        self.submit_btn.config(
        bg="#D5D8DC",
        fg="#AEB6BF",
        cursor="arrow"
        )
        self.submit_btn.unbind("<Enter>")
        self.submit_btn.unbind("<Leave>")
        self.submit_btn.unbind("<Button-1>")

    # =========================
    def validate_fee_form(self):
        class_id = self.vars["class_id"].get().strip()
        fee_type = self.vars["fee_type"].get().strip()
        amount = self.vars["amount"].get().strip()
        effective_from = self.vars["effective_from"].get().strip()
        effective_to = self.vars["effective_to"].get().strip()
        notes = self.vars["notes"].get().strip()

        if not all([class_id, fee_type, amount, effective_from, effective_to, notes]):
            self.disable_submit()
            return
    
        if not class_id.isdigit():
            self.disable_submit()
            return

        if not amount.isdigit():
            self.disable_submit()
            return

        import re
        date_regex = r"^\d{4}-\d{2}-\d{2}$"

        if not re.match(date_regex, effective_from) or not re.match(date_regex, effective_to):
            self.disable_submit()
            return

        self.enable_submit()

    def submit_create_fee(self):
        from datetime import datetime
        payload = {
            "class_id": int(self.entries["class_id"].get()),
            "fee_type": str(self.entries["fee_type"].get()),
            "amount": float(self.entries["amount"].get()),
            "effective_from": datetime.strptime(self.entries["effective_from"].get().strip(), "%Y-%m-%d").date().isoformat(),
            "effective_to": datetime.strptime(self.entries["effective_to"].get().strip(), "%Y-%m-%d").date().isoformat(),
            "notes": str(self.entries["notes"].get())
        }
        for field, value in payload.items():
            if value == "":
                self.show_popup("Missing Information", f"{field} cannot be empty.", "warning")
                return
    
        class_id = self.entries["class_id"].get().strip()
        if not class_id.isdigit() or int(class_id) <= 0:
            self.show_popup("Invalid Class ID", "Class ID must be a positive number.", "warning")
            return
        
        amount = self.entries["amount"].get().strip()
        if not amount.replace(".", "", 1).isdigit() or float(amount) <= 0:
            self.show_popup("Invalid Amount", "Amount must be a positive number.", "warning")
            return
        
        import re
        from_dt = self.entries["effective_from"].get().strip()
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", from_dt):
            self.show_popup("Invalid Date", "Effective From must be in YYYY-MM-DD format.", "error")
            return
        
        to_dt = self.entries["effective_to"].get().strip()
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", to_dt):
            self.show_popup("Invalid Date", "Effective To must be in YYYY-MM-DD format.", "error")
            return

        from datetime import datetime

        from_date = datetime.strptime(from_dt, "%Y-%m-%d").date()
        to_date = datetime.strptime(to_dt, "%Y-%m-%d").date()

        if to_date < from_date:
            self.show_popup("Invalid Range", "Effective To cannot be earlier than Effective From!", "error")
            return

        import requests
        requests.post("http://127.0.0.1:8000/admin/fees/create", json=payload)
        self.show_popup("Success", "Fee Created Successfully!", "Success")
        self.change_screen("Fee Created Successfully", 
                        add_callback=self.load_create_fee_screen)

    # ====================
    # button to assign fee
    def load_assign_fee_screen(self):
        self.clear_content()

    # Title
        tk.Label(
        self.content,
        text="Assign Fee to Student",
        font=("Arial", 22, "bold"),
        bg="#ECF0F1"
        ).pack(pady=20)

    # ==== FORM ====
        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

    # Variables
        student_id = tk.StringVar()
        class_id = tk.StringVar()
        fee_id = tk.StringVar()
        amount_due = tk.StringVar()
        due_date = tk.StringVar()

        fields = [
        ("Student ID:", student_id),
        ("Class ID:", class_id),
        ("Fee ID:", fee_id),
        ("Amount Due:", amount_due),
        ("Due Date:", due_date),
        ]
        for i, (label, var) in enumerate(fields):

    # LABEL
            tk.Label(
        form,
        text=label,
        font=("Arial", 14),
        bg="#ECF0F1"
    ).grid(row=i, column=0, padx=10, pady=8)

    # ---- SPECIAL CASE: DUE DATE WITH CALENDAR ----
            if label.startswith("Due Date"):
                entry = tk.Entry(form, textvariable=var, font=("Arial", 14), width=20)
                entry.grid(row=i, column=1, padx=5, pady=8)

        # Calendar Button
                tk.Button(
            form,
            text="calendar",
            font=("Arial", 12),
            bg="white",
            relief="flat",
            command=lambda v=var, e=entry: self.open_calendar_popup(e, v)
        ).grid(row=i, column=2, padx=5)

            else:
        # NORMAL ENTRY FIELD
                entry = tk.Entry(form, textvariable=var, font=("Arial", 14), width=25)
                entry.grid(row=i, column=1, padx=10, pady=8)

    # ==== ASSIGN BACKEND CALL ====
        def assign_fee_backend():
            try:
                payload = {
                "student_id": int(student_id.get().strip()),
                "class_id": int(class_id.get().strip()),
                "fee_id": int(fee_id.get().strip()),
                "amount_due": float(amount_due.get().strip()),
                "due_date": due_date.get().strip()
            }
                for field, value in payload.items():
                    if value == "":
                        self.show_popup("Missing Information", f"{field} cannot be empty.", "warning")
                        return

                sid = student_id.get().strip()
                if not sid.isdigit() or int(sid) <= 0:
                    self.show_popup("Invalid Student ID", "Student ID must be a positive number.", "warning")
                    return
                cid = class_id.get().strip()
                if not cid.isdigit() or int(cid) <= 0:
                    self.show_popup("Invalid Class ID", "Class ID must be a positive number.", "warning")
                    return
                fid = fee_id.get().strip()
                if not fid.isdigit() or int(fid) <= 0:
                    self.show_popup("Invalid Fee ID", "Fee ID must be a positive number.", "warning")
                    return
                amt = amount_due.get().strip()
                if not amt.replace(".", "", 1).isdigit() or float(amt) <= 0:
                    self.show_popup("Invalid Amount", "Amount must be a valid positive number.", "warning")
                    return
                import re
                date_str = due_date.get().strip()
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
                    self.show_popup("Invalid Date", "Date must be YYYY-MM-DD format!", "error")
                    return

                from datetime import datetime
                try:
                    datetime.strptime(date_str, "%Y-%m-%d")
                except:
                    self.show_popup("Invalid Date", "Please enter a valid Due Date!", "error")
                    return

                import requests
                res = requests.post("http://127.0.0.1:8000/admin/fees/assign", json=payload)

                if res.status_code == 201:
                    self.show_popup("Success", "Fee Assigned Successfully", "Success")
                    self.change_screen(
                    "Fee Assigned Successfully!",
                    add_callback=self.load_assign_fee_screen
                )
                else:
                    error_msg = "Failed to assign fee!"
                    try:
                        err = res.json()
                        if "detail" in err:
                            error_msg = err["detail"]
                    except:
                            pass
   
                    self.show_popup("Request Failed", error_msg, "error")
                    self.change_screen(
                    "Failed to Assign Fees Try Again with a Valid Student ID!",
                    add_callback=self.load_assign_fee_screen
                )

            except:
                self.show_popup("Error","Error in Assigning Fees", "error")

    # ==== BUTTON FRAME ====
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

    # BACK BUTTON
        self.create_back_button(btn_frame, self.load_dashboard, form)

    # ==== ASSIGN BUTTON (LABEL STYLE) ====
        assign_btn = tk.Label(
        btn_frame,
        text="Assign Fee",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=10,
        width=12,
        relief="ridge",
        cursor="arrow"
    )
        assign_btn.pack(side="left", padx=15)
    # ==== ACTIVATION STYLE ====
        def activate_button():
            assign_btn.config(
            bg="#000000",
            fg="white",
            cursor="arrow",
            relief="flat"
        )
            assign_btn.bind("<Enter>", lambda e: assign_btn.config(bg="#222222"))
            assign_btn.bind("<Leave>", lambda e: assign_btn.config(bg="#000000"))
            assign_btn.bind("<Button-1>", lambda e: assign_fee_backend())

        def disable_button():
            assign_btn.config(
            bg="#D5D8DC",
            fg="#AEB6BF",
            cursor="arrow",
            relief="ridge"
        )
            assign_btn.unbind("<Enter>")
            assign_btn.unbind("<Leave>")
            assign_btn.unbind("<Button-1>")

    # ==== VALIDATION ====
        def validate(*args):
            if all(v.get().strip() for _, v in fields):
                activate_button()
            else:
                disable_button()

    # Trace all vars
        for _, var in fields:
            var.trace_add("write", validate)

        disable_button()  # initial state


    # ===== button to view all fees from DB =====
    def load_view_fees_screen(self):
        self.clear_content()

    # ---- Title ----
        tk.Label(
        self.content, text="All Fees",
        font=("Arial", 26, "bold"), bg="#ECF0F1", fg="#2C3E50"
    ).pack(pady=20)

    # ---- Back Button ----
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)
        self.create_back_button(back_frame, self.load_dashboard, None)

    # ---- Table Frame ----
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        cols = (
        "fee_id", "class_id", "fee_type", "amount", "currency",
        "effective_from", "effective_to", "is_active", "notes"
    )

    # ====================================================
    #     FILTER BAR (Dropdown + Entry + Black Buttons)
    # ====================================================
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=10)

    # Label
        tk.Label(
        filter_frame,
        text="Sort By:",
        font=("Arial", 12, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
    ).grid(row=0, column=0, padx=5)

    # Dropdown (column names)
        filter_var = tk.StringVar()
        filter_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=list(cols),
        state="readonly",
        width=18
    )
        filter_dropdown.grid(row=0, column=1, padx=10)

    # Value Entry
        filter_value_var = tk.StringVar()
        filter_value = tk.Entry(filter_frame, font=("Arial", 12), width=20, textvariable=filter_value_var)
        filter_value.grid(row=0, column=2, padx=10)
    # ---------- BUTTON STYLE ----------
        def style_button(btn):
            btn.config(
            bg="#000000",
            fg="white",
            padx=15,
            pady=5,
            width=10,
            relief="raised",
            cursor="hand2",
            font=("Arial", 12, "bold")
        )
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

    # ----- LOAD BUTTON -----
        load_btn = tk.Label(filter_frame, text="Load")
        style_button(load_btn)
        load_btn.grid(row=0, column=3, padx=10)

    # ----- LOAD ALL BUTTON -----
        load_all_btn = tk.Label(filter_frame, text="Load All")
        style_button(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

    # ------------------------- CALLBACKS -------------------------
        def update_fees_table(data):
            for row in self.tree.get_children():
                self.tree.delete(row)

            for row in data:
                self.tree.insert("", "end", values=(
                row["fee_id"],
                row["class_id"],
                row["fee_type"],
                row["amount"],
                row["currency"],
                row["effective_from"],
                row["effective_to"],
                row["is_active"],
                row["notes"]
            ))

        def load_filtered():
            col = filter_var.get().strip()
            val = filter_value_var.get().strip()

            if not col or not val:
                return
            valid_list = self.column_values_fee_master.get(col, [])
            valid_lower = [str(v).lower() for v in valid_list]

            if val not in valid_lower:
                self.show_popup(
            "Invalid Search Value",
            f"'{val}' not found in column '{col}'.",
            "warning"
        )
                filter_value_var.set("")      # clear invalid input
                return
            
            filtered = [
                r for r in self.all_fees
                if str(r[col]).lower() == val.lower()
        ]
            update_fees_table(filtered)

        def load_all():
            update_fees_table(self.all_fees)

        load_btn.bind("<Button-1>", lambda e: load_filtered())
        load_all_btn.bind("<Button-1>", lambda e: load_all())

    # =========== TABLE + SCROLLBARS =============
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        self.tree = ttk.Treeview(
        table_frame,
        columns=cols,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
    )
        self.tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.tree.yview)
        x_scroll.config(command=self.tree.xview)

    # Headings
        for col in cols:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=180, anchor="center")

    # ====================== FETCH DATA ======================
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admin/fees")
            self.all_fees = res.json() if res.status_code == 200 else []
            # ------------ COLLECT VALID COLUMN VALUES FOR SEARCH ------------
            self.column_values_fee_master = {
    "fee_id": [str(r["fee_id"]) for r in self.all_fees],
    "class_id": [str(r["class_id"]) for r in self.all_fees],
    "fee_type": [r["fee_type"] for r in self.all_fees],
    "amount": [str(r["amount"]) for r in self.all_fees],
    "currency": [r["currency"] for r in self.all_fees],
    "effective_from": [r["effective_from"] for r in self.all_fees],
    "effective_to": [r["effective_to"] for r in self.all_fees],
    "is_active": [str(r["is_active"]) for r in self.all_fees],
    "notes": [r["notes"] for r in self.all_fees],
}

        except:
            self.all_fees = []

        update_fees_table(self.all_fees)


    # ===== button to update fee =====
    def load_update_fee_screen(self):
        self.clear_content()

        title = tk.Label(self.content, text="Update Fee", font=("Arial", 26, "bold"),
                        bg="#ECF0F1", fg="#2C3E50")
        title.pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        tk.Label(form, text="Enter Fee ID:", font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=0, padx=10, pady=10)
        fid_entry = tk.Entry(form, font=("Arial", 14), width=25)
        fid_entry.grid(row=0, column=1, padx=10)

        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

        # Back Button from global function
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,    
        form_frame=form                          
        )
        self.content.update_idletasks
        # Search Button (Label style)
        search_btn = tk.Label(
        form,
        text="Search",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=10,
        width=10,
        bd=0,
        relief="flat",
        cursor="arrow"
        )
        search_btn.grid(row=1, columnspan=2, pady=15)

        # Enabling search when fee id entered
        fid_var = tk.StringVar()
        fid_entry.config(textvariable=fid_var)

        fid_var.trace_add("write", lambda *args: self.enable_disable_button(fid_var, search_btn))

        # Binding the button click later when enabled
        search_btn.bind("<Button-1>", lambda e: self.fetch_fee_details(fid_var.get()))

    # =========================
    def enable_disable_button(self, variable, btn):
        if variable.get().strip():
            btn.config(bg="#000000", fg="white", cursor="hand2")

            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))
        else:
            btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")

            btn.unbind("<Enter>")
            btn.unbind("<Leave>")
            btn.unbind("<Button-1>")

    # ============================
    def fetch_fee_details(self, fee_id):
        fee_id = str(fee_id).strip()
        if not fee_id.isdigit() or int(fee_id) <= 0:
            self.show_popup("Invalid Fee ID", "Fee ID must be a positive number.", "warning")
            return

        import requests
        try:
            res = requests.get(f"http://127.0.0.1:8000/admin/fees/get/{fee_id}")
            if res.status_code != 200:
                self.show_popup("Failure", "Fee not found for this Fee ID", "error")
                return

            data = res.json()
            self.show_update_form(data)

        except:
            self.show_popup("Failure", "Error Fetching Fee Data", "error")
            self.change_screen("Error Fetching Fee Data")
    
    # ===== Button to Update any fee record =====
    def show_update_form(self, data):
        self.clear_content()

        tk.Label(self.content, text="Update Fee",
                font=("Arial", 26, "bold"),
                bg="#ECF0F1", fg="#2C3E50").pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        labels = ["class_id", "fee_type", "amount", "effective_from", "effective_to", "notes"]
        fields = ["class_id", "fee_type", "amount", "effective_from", "effective_to", "notes"]

        self.update_vars = {}
        self.update_entries = {}

        for i, field in enumerate(fields):

    # LABEL
            tk.Label(
        form,
        text=labels[i] + ":",
        font=("Arial", 14),
        bg="#ECF0F1"
    ).grid(row=i, column=0, padx=10, pady=10)

    # VARIABLE
            var = tk.StringVar(value=str(data[field]))

    # --- DATE FIELDS ---
            if field in ("effective_from", "effective_to"):
                entry = tk.Entry(form, textvariable=var, font=("Arial", 14), width=20)
                entry.grid(row=i, column=1, padx=5, pady=10)

        # Calendar button
                tk.Button(
            form,
            text="Calendar",
            font=("Arial", 12),
            bg="white",
            relief="flat",
            command=lambda v=var, e=entry: self.open_calendar_popup(e, v)
        ).grid(row=i, column=2, padx=5)

            else:
        # NORMAL ENTRY FIELD
                entry = tk.Entry(form, textvariable=var, font=("Arial", 14), width=25)
                entry.grid(row=i, column=1, padx=10, pady=10)

            self.update_vars[field] = var
            self.update_entries[field] = entry

            # enable update button when entries valid
            var.trace_add("write", lambda *args: self.validate_update_form())

        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

        # Back Button from global function
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,    
        form_frame=form                          
        )
        self.content.update_idletasks()
        # UPDATE BUTTON
        self.update_btn = tk.Label(
        self.content,
        text="Update",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20, pady=12,
        width=12,
        bd=0,
        relief="flat",
        cursor="arrow"
        )
        self.update_btn.pack(pady=20)

    # ===========================
    def validate_update_form(self):
        if all(v.get().strip() for v in self.update_vars.values()):
            self.enable_disable_button(self.update_vars["class_id"], self.update_btn)

            self.update_btn.bind(
            "<Button-1>",
            lambda e: self.submit_fee_update()
            )
        else:
            self.update_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            self.update_btn.unbind("<Button-1>")
    
    # =========================
    def submit_fee_update(self, fee_id):
        payload = {
        "class_id": int(self.update_vars["class_id"].get().strip()),
        "fee_type": str(self.update_vars["fee_type"].get().strip()),
        "amount": float(self.update_vars["amount"].get().strip()),
        "effective_from": self.update_vars["effective_from"].get().strip(),
        "effective_to": self.update_vars["effective_to"].get().strip(),
        "notes": self.update_vars["notes"].get().strip()
        }
        for field, val in payload.items():
            if val == "":
                self.show_popup("Missing Information", f"{field} cannot be empty.", "warning")
                return

        cid = self.update_vars["class_id"].get().strip()
        if not cid.isdigit() or int(cid) <= 0:
            self.show_popup("Invalid Class ID", "Class ID must be a positive number.", "warning")
            return

        amt = self.update_vars["amount"].get().strip()
        try:
            amt_f = float(amt)
            if amt_f <= 0:
                self.show_popup("Invalid Amount", "Amount must be greater than zero.", "warning")
                return
        except:
            self.show_popup("Invalid Amount", "Amount must be a number.", "error")
            return
        import re
        date_pattern = r"^\d{4}-\d{2}-\d{2}$"

        for field_name, date_val in [
        ("effective_from", self.update_vars["effective_from"]),
        ("effective_to", self.update_vars["effective_to"])
    ]:
            if not re.match(date_pattern, date_val):
                self.show_popup("Invalid Date",
                            f"{field_name} must be YYYY-MM-DD.",
                            "error")
                return

        import requests
        requests.put(f"http://127.0.0.1:8000/admin/fees/update/{fee_id}", json=payload)
        
        self.show_popup("Success", " Fee Updated Successfully", "success")
        self.change_screen("Fee Updated Successfully!",
                        add_callback=self.load_update_fee_screen)


    # ===== button to delete a fee using fee_id =====
    def load_delete_fee_screen(self):
        self.clear_content()

        tk.Label(
        self.content,
        text="Delete Fee",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=25)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=20)

        tk.Label(
        form, text="Enter Fee ID:", font=("Arial", 16), bg="#ECF0F1"
        ).grid(row=0, column=0, padx=10, pady=10)

        fee_id_var = tk.StringVar()
        entry = tk.Entry(form, textvariable=fee_id_var, font=("Arial", 14), width=25)
        entry.grid(row=0, column=1, padx=10)

        # Back Button
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)
        self.create_back_button(btn_frame, self.load_dashboard, form)
        self.content.update_idletasks()

        # SEARCH BUTTON
        search_btn = tk.Label(
        form,
        text="Search",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=10,
        width=10,
        cursor="arrow"
        )
        search_btn.grid(row=1, columnspan=2, pady=15)

        # Enable when user types Fee ID
        def validate(*args):
            if fee_id_var.get().strip():
                search_btn.config(bg="#000", fg="white", cursor="hand2")
                search_btn.bind("<Enter>", lambda e: search_btn.config(bg="#222"))
                search_btn.bind("<Leave>", lambda e: search_btn.config(bg="#000"))
                search_btn.bind("<Button-1>",
                    lambda e: self.fetch_fee_for_delete(fee_id_var.get().strip())
                )
            else:
                search_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                search_btn.unbind("<Enter>")
                search_btn.unbind("<Leave>")
                search_btn.unbind("<Button-1>")

        fee_id_var.trace_add("write", validate)

    # ----- Fetch Fee Details -----
    def fetch_fee_for_delete(self, fee_id):
        self.clear_content()

        tk.Label(
        self.content,
        text="Confirm Delete",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="red"
    ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        fee_id = str(fee_id).strip()

        if not fee_id.isdigit() or int(fee_id)<=0:
            self.show_popup("Invalid Fee ID", "Fee ID should be a positive number", "warning")
            return

        import requests

        try:
            res = requests.get(f"http://127.0.0.1:8000/admin/fees/get/{fee_id}")

            if res.status_code != 200:
                self.show_popup("Not Found", "Fee record not found.", "error")
                self.change_screen("Fee Not Found",
                                   add_callback=self.load_delete_fee_screen)
                return

            data = res.json()
            self.show_delete_confirm(data)

        except Exception as e:
            self.show_popup("Backend Error", str(e), "error")
            return


    def show_delete_confirm(self, data):
        self.clear_content()

        tk.Label(
        self.content,
        text="Confirm Delete",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#C0392B"
    ).pack(pady=20)

    # info_frame will contain ONLY grid-managed widgets (labels + values)
        info = tk.Frame(self.content, bg="#ECF0F1")
        info.pack(pady=10)   # packing the frame itself is fine

    # Put all label/value rows using grid (consistent inside this frame)
        row = 0
        for key, value in data.items():
            tk.Label(info, text=f"{key}:", font=("Arial", 14), bg="#ECF0F1")\
            .grid(row=row, column=0, padx=10, pady=5, sticky="w")
            tk.Label(info, text=str(value), font=("Arial", 14), bg="#ECF0F1")\
            .grid(row=row, column=1, padx=10, pady=5, sticky="w")
            row += 1

    # BUTTONS FRAME: separate frame, use pack for the buttons
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=30)

    # back button (your helper probably packs into parent; pass btn_frame NOT info)
        self.create_back_button(btn_frame, self.load_dashboard, info)

    # Delete button — PACK here (because btn_frame is packed)
        delete_btn = tk.Label(
        btn_frame,
        text="Delete",
        font=("Arial", 14, "bold"),
        bg="#000000",
        fg="white",
        padx=15, pady=8,
        width=12,
        cursor="hand2",
        relief="ridge"
    )
        delete_btn.pack()   # <-- pack, not grid
        delete_btn.bind("<Enter>", lambda e: delete_btn.config(bg="#222"))
        delete_btn.bind("<Leave>", lambda e: delete_btn.config(bg="#000"))
        delete_btn.bind("<Button-1>", lambda e: self.perform_fee_delete(data["fee_id"]))


    def perform_fee_delete(self, fee_id):
        import requests

        try:
            res = requests.delete(f"http://127.0.0.1:8000/admin/fees/delete/{fee_id}")

            if res.status_code == 200:
                self.show_popup("Success", "Fee deleted successfully!", "info")
                self.change_screen("Fee Deleted Successfully!",
                                add_callback=self.load_delete_fee_screen)
            else:
                msg = res.json().get("detail", "Delete failed.")
                self.show_popup("Error", msg, "error")

        except Exception as e:
            self.show_popup("Backend Error", str(e), "error")


    # ===== Button to Fetch History =====
    def load_fee_history_screen(self):
        import requests
        self.clear_content()

    # ---- TITLE ----
        tk.Label(
        self.content,
        text="Fee History",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
    ).pack(pady=25)

    # ---- BACK BUTTON ----
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)

        self.create_back_button(
        parent=back_frame,
        go_back_callback=self.load_dashboard,
        form_frame=None
    )

    # ---- COLUMN DEFINITIONS ----
        columns = (
        "invoice_id", "student_id", "class_id", "fee_id",
        "amount_due", "amount_paid", "due_date",
        "status", "receipt_path"
    )

    # ---- FETCH ALL FEE HISTORY ----
        try:
            res = requests.get("http://127.0.0.1:8000/admin/fees/all")
            self.all_fee_history = res.json() if res.status_code == 200 else []
        except:
            self.all_fee_history = []
        # ------------ COLLECT VALID COLUMN VALUES ------------
        self.column_values_fee = {
    "invoice_id": [str(r["invoice_id"]) for r in self.all_fee_history],
    "student_id": [str(r["student_id"]) for r in self.all_fee_history],
    "class_id": [str(r["class_id"]) for r in self.all_fee_history],
    "fee_id": [str(r["fee_id"]) for r in self.all_fee_history],
    "amount_due": [str(r["amount_due"]) for r in self.all_fee_history],
    "amount_paid": [str(r["amount_paid"]) for r in self.all_fee_history],
    "due_date": [r["due_date"] for r in self.all_fee_history],
    "status": [r["status"] for r in self.all_fee_history],
    "receipt_path": [r.get("receipt_path", "None") for r in self.all_fee_history],
}

    # ---- TABLE CONTAINER ----
        table_frame = tk.Frame(self.content)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # ---- TABLE WIDGET ----
        self.history_tree = ttk.Treeview(
        table_frame, columns=columns, show="headings"
    )
        self.history_tree.pack(fill="both", expand=True, side="left")

    # ---- SCROLLBAR ----
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=y_scroll.set)
        y_scroll.pack(side="right", fill="y")

    # ---- HEADERS ----
        for col in columns:
            self.history_tree.heading(col, text=col.replace("_", " ").title())
            self.history_tree.column(col, width=150, anchor="center")

    # ====================================================
    #               FILTER BAR (DROPDOWN + ENTRY)
    # ====================================================

        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=10)

    # Sort by label
        tk.Label(
        filter_frame,
        text="Sort By:",
        font=("Arial", 12, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
    ).grid(row=0, column=0, padx=5)

    # Dropdown
        filter_var = tk.StringVar()
        filter_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=list(columns),
        state="readonly",
        width=18
    )
        filter_dropdown.grid(row=0, column=1, padx=10)

        # Value entry
        filter_value_var = tk.StringVar()
        # Value Entry (ONLY ONE ENTRY)
        filter_value = tk.Entry(
    filter_frame,
    textvariable=filter_value_var,
    font=("Arial", 12),
    width=20
)
        filter_value.grid(row=0, column=2, padx=10)


    # ---------- BLACK BUTTON STYLE ----------
        def style_button(btn):
            btn.config(
            bg="#000000",
            fg="white",
            padx=15,
            pady=5,
            width=10,
            relief="raised",
            cursor="arrow",
            font=("Arial", 12, "bold")
        )

            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

    # ---- LOAD BUTTON ----
        load_btn = tk.Label(filter_frame, text="Load")
        style_button(load_btn)
        load_btn.grid(row=0, column=3, padx=10)

    # ---- LOAD ALL BUTTON ----
        load_all_btn = tk.Label(filter_frame, text="Load All")
        style_button(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

    # ====================================================
    #                LOAD / FILTER FUNCTIONS
    # ====================================================
    
        def update_fee_history_table(data):
            for row in self.history_tree.get_children():
                self.history_tree.delete(row)

            for row in data:
                self.history_tree.insert("", "end", values=(
                row["invoice_id"],
                row["student_id"],
                row["class_id"],
                row["fee_id"],
                row["amount_due"],
                row["amount_paid"],
                row["due_date"],
                row["status"],
                row.get("receipt_path", "None")
            ))

        def load_filtered():
            col = filter_var.get().strip()
            val = filter_value.get().strip()

            if not col or not val:
                return
            
            valid_list = self.column_values_fee.get(col, [])
            valid_lower = [str(v).lower() for v in valid_list]

            if val not in valid_lower:
                self.show_popup(
            "Invalid Search Value",
            f"'{val}' not found in column '{col}'.",
            "warning"
        )
                filter_value_var.set("")      # clear invalid input
                return
            
            filtered = [
            row for row in self.all_fee_history
            if str(row[col]).lower() == val.lower()
        ]

            update_fee_history_table(filtered)

        def load_all():
            update_fee_history_table(self.all_fee_history)

        load_btn.bind("<Button-1>", lambda e: load_filtered())
        load_all_btn.bind("<Button-1>", lambda e: load_all())

    # ---- DEFAULT LOAD ----
        update_fee_history_table(self.all_fee_history)


    # ====== Add Payment Methods ======
    def load_add_payment_method_screen(self):
        self.clear_content()

        tk.Label(
        self.content,
        text="Add Payment Method",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=20)

        # --------- INPUT VARS ----------
        name_var = tk.StringVar()
        desc_var = tk.StringVar()

        # --------- FORM LABELS + ENTRIES ----------
        tk.Label(form, text="Method Name:", font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=0, padx=10, pady=10)
        name_entry = tk.Entry(form, textvariable=name_var, font=("Arial", 14), width=25)
        name_entry.grid(row=0, column=1, padx=10)

        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

        # Back Button from global function
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,    
        form_frame=form                          
        )
        self.content.update_idletasks()
        # ---- DISABLED BUTTON (initial) ----
        add_btn = tk.Label(
        self.content,
        text="Add Method",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=25,
        pady=12,
        width=14,
        borderwidth=1,
        relief="solid",
        cursor="arrow"
        )
        add_btn.pack(pady=30)

        # ------ VALIDATION ------
        def validate_add_method(*args):
            if name_var.get().strip() and desc_var.get().strip():
                add_btn.config(bg="#000000", fg="white", cursor="hand2")

                add_btn.bind("<Enter>", lambda e: add_btn.config(bg="#222222"))
                add_btn.bind("<Leave>", lambda e: add_btn.config(bg="#000000"))
                add_btn.bind("<Button-1>", lambda e: submit_method())
            else:
                add_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                add_btn.unbind("<Enter>")
                add_btn.unbind("<Leave>")
                add_btn.unbind("<Button-1>")

        # Track input changes
        name_var.trace_add("write", validate_add_method)
        desc_var.trace_add("write", validate_add_method)

        # ---------- SUBMIT FUNCTION ----------
        def submit_method():
            method_name = name_var.get().strip()
            if not method_name:
                self.show_popup("Missing Input", "Method Name cannot be empty!", "warning")
                return
            method_name = method_name.title()
            payload = {
            "method_name": method_name
            }
            try:
                import requests
                res = requests.post("http://127.0.0.1:8000/admin/payment-methods/add", json=payload)

                if res.status_code == 200:
                    self.change_screen("Payment Method Added!",
                                    add_callback=self.load_add_payment_method_screen)
                else:
                    self.change_screen("Error Adding Method!")

            except Exception as e:
                print("UPLOAD ERROR:", e)
                self.change_screen("Backend Error!")


    # ===== Button to View Payment Methods =====
    def load_view_methods_screen(self):
        self.clear_content()

    # ---- Title ----
        tk.Label(
        self.content, text="Payment Methods",
        font=("Arial", 26, "bold"), bg="#ECF0F1", fg="#2C3E50"
    ).pack(pady=20)

    # ---- Back button ----
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)
        self.create_back_button(back_frame, self.load_dashboard, None)

    # ----- TABLE FRAME -----
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        cols = ("method_id", "method_name", "is_active")

    # ====================================================
    #     FILTER BAR (Dropdown + Entry + Black Buttons)
    # ====================================================
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=10)

    # Label
        tk.Label(
        filter_frame,
        text="Sort By:",
        font=("Arial", 12, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
    ).grid(row=0, column=0, padx=5)

    # Dropdown
        filter_var = tk.StringVar()
        filter_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=["method_id", "method_name", "is_active"],
        state="readonly",
        width=18
    )
        filter_dropdown.grid(row=0, column=1, padx=10)

    # Value Entry
        filter_value_var = tk.StringVar()

# Value Entry (ONLY ONE ENTRY)
        filter_value = tk.Entry(
    filter_frame,
    textvariable=filter_value_var,
    font=("Arial", 12),
    width=20
)
        filter_value.grid(row=0, column=2, padx=10)

    # ---------- BUTTON STYLE ----------
        def style_button(btn):
            btn.config(
            bg="#000000",
            fg="white",
            padx=15,
            pady=5,
            width=10,
            relief="raised",
            cursor="hand2",
            font=("Arial", 12, "bold")
        )
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

    # ----- LOAD BUTTON -----
        load_btn = tk.Label(filter_frame, text="Load")
        style_button(load_btn)
        load_btn.grid(row=0, column=3, padx=10)

    # ----- LOAD ALL BUTTON -----
        load_all_btn = tk.Label(filter_frame, text="Load All")
        style_button(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

    # ------------------------- CALLBACKS -------------------------
        def load_filtered():
            col = filter_var.get().strip()
            val = filter_value.get().strip()

            if not col or not val:
                return
            valid_list = self.column_values_payment_methods.get(col, [])
            valid_lower = [str(v).lower() for v in valid_list]

            if val not in valid_lower:
                self.show_popup(
            "Invalid Search Value",
            f"'{val}' not found in column '{col}'.",
            "warning"
        ) 
                filter_value_var.set("")
                return
            filtered = [
            row for row in self.all_methods
            if str(row[col]).lower() == val.lower()
            ]
            self.update_method_table(filtered)

        def load_all():
            self.update_method_table(self.all_methods)

        load_btn.bind("<Button-1>", lambda e: load_filtered())
        load_all_btn.bind("<Button-1>", lambda e: load_all())

    # ---------- SCROLLBARS ----------
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

    # ----------- TABLE -----------
        self.method_tree = ttk.Treeview(
            table_frame, columns=cols, show="headings",
            yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set
        )
        self.method_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.method_tree.yview)
        x_scroll.config(command=self.method_tree.xview)

        for col in cols:
            self.method_tree.heading(col, text=col)
            self.method_tree.column(col, width=200, anchor="center")

    # ====================== FETCH INITIAL DATA ======================
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admin/payment-methods")
            self.all_methods = res.json() if res.status_code == 200 else []
            # ------------ COLLECT VALID COLUMN VALUES FOR SEARCH ------------
            self.column_values_payment_methods = {
    "method_id": [str(r["method_id"]) for r in self.all_methods],
    "method_name": [r["method_name"] for r in self.all_methods],
    "is_active": [str(r["is_active"]) for r in self.all_methods],
}
        except:
            self.all_methods = []

        self.update_method_table(self.all_methods)


    # ===== View method by IDs =====
    def load_view_method_by_id_screen(self):
        self.clear_content()

        tk.Label(
        self.content, text="View Payment Method",
        font=("Arial", 26, "bold"), bg="#ECF0F1", fg="#2C3E50"
        ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=20)

        tk.Label(form, text="Enter Method ID:", font=("Arial", 16), bg="#ECF0F1").grid(
        row=0, column=0, padx=10, pady=10
        )

        method_id_var = tk.StringVar()
        entry = tk.Entry(form, textvariable=method_id_var, font=("Arial", 14), width=25)
        entry.grid(row=0, column=1, padx=10, pady=10)

        # Back button
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(pady=5)

        self.create_back_button(
        parent=back_frame,
        go_back_callback=self.load_dashboard,
        form_frame=None     # table screen : no form entries
        )
        # Search button
        search_btn = tk.Label(
        form,
        text="Search",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=10,
        width=10,
        cursor="arrow"
        )
        search_btn.grid(row=1, columnspan=2, pady=20)

        # Enable / Disable search button
        def validate(*args):
            if method_id_var.get().strip():
                search_btn.config(bg="#000", fg="white", cursor="hand2")
                search_btn.bind("<Enter>", lambda e: search_btn.config(bg="#222"))
                search_btn.bind("<Leave>", lambda e: search_btn.config(bg="#000"))
                search_btn.bind("<Button-1>", lambda e: self.fetch_method_details(method_id_var.get().strip()))
            else:
                search_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                search_btn.unbind("<Enter>")
                search_btn.unbind("<Leave>")
                search_btn.unbind("<Button-1>")

        method_id_var.trace_add("write", validate)

    #---------------
    def show_method_details(self, data):
            self.clear_content()
            tk.Label(
                self.content,
                text="Payment Method Details",
                font=("Arial", 26, "bold"),
                bg="#ECF0F1",
                fg="#2C3E50"
                ).pack(pady=20)

            info = tk.Frame(self.content, bg="#ECF0F1")
            info.pack(pady=20)

            for i, (key, value) in enumerate(data.items()):
                tk.Label(info, text=f"{key}:", font=("Arial", 14), bg="#ECF0F1").grid(row=i, column=0, padx=10, pady=8)
                tk.Label(info, text=str(value), font=("Arial", 14), bg="#ECF0F1").grid(row=i, column=1, padx=10, pady=8)

            # Back button
            btn_frame = tk.Frame(self.content, bg="#ECF0F1")
            btn_frame.pack(pady=20)
        
            self.create_back_button(
            parent=btn_frame,
            go_back_callback=self.load_dashboard,
            form_frame=None     # table screen : no form entries
            )
            
    def fetch_method_details(self, method_id):
        if not method_id.strip():
            self.show_popup("Missing Input", "Method ID cannot be empty!", "warning")
            return
        if not method_id.isdigit() or int(method_id) <= 0:
            self.show_popup("Invalid Method ID", "Method ID must be a positive number!", "warning")
            return 
        import requests
        try:
            res = requests.get(f"http://127.0.0.1:8000/admin/payment-methods/{method_id}")

            if res.status_code != 200:
                self.show_popup(
                "Not Found",
                f"No payment method found with ID {method_id}.",
                "error"
            )
                return

            data = res.json()
            self.show_method_details(data)

        except Exception as e:
            self.show_popup("Backend Error", str(e), "error")
            return


    # ===== Button to Update Payment Method =====
    def load_update_method_screen(self):
        self.clear_content()

        title = tk.Label(
        self.content,
        text="Update Payment Method",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        )
        title.pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=20)

        # ----- Input: Method ID -----
        tk.Label(form, text="Method ID:", font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=0, padx=10, pady=8)
        method_id_var = tk.StringVar()
        method_id_entry = tk.Entry(form, textvariable=method_id_var, font=("Arial", 14), width=25)
        method_id_entry.grid(row=0, column=1, padx=10, pady=8)

        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

        # Back Button from global function
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,    
        form_frame=form                          
        )
        self.content.update_idletasks()
        # ----- Load Button -----
        load_btn = tk.Label(
        form,
        text="Load",
        font=("Arial", 12, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=15, pady=5,
        width=12,
        relief="ridge",
        cursor="arrow"
        )
        load_btn.grid(row=0, column=2, padx=10)

        # ===== Method Name & Details Fields =====
        tk.Label(form, text="Method Name:", font=("Arial", 14), bg="#ECF0F1").grid(row=1, column=0, padx=10, pady=8)
        name_var = tk.StringVar()
        name_entry = tk.Entry(form, textvariable=name_var, font=("Arial", 14), width=25, state="disabled")
        name_entry.grid(row=1, column=1, padx=10, pady=8)

        tk.Label(form, text="Is_Active:", font=("Arial", 14), bg="#ECF0F1").grid(row=2, column=0, padx=10, pady=8)
        details_var = tk.StringVar()
        details_entry = tk.Entry(form, textvariable=details_var, font=("Arial", 14), width=25, state="disabled")
        details_entry.grid(row=2, column=1, padx=10, pady=8)

        # ----- Update Button -----
        update_btn = tk.Button(
        self.content, text="Update Method",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC", fg="#AEB6BF",
        state="disabled",
        padx=20, pady=10
        )
        update_btn.pack(pady=25)

        # ====== VALIDATE LOAD BUTTON ======
        def validate_load_btn(*args):
            if method_id_var.get().strip():
               load_btn.config(bg="#000000", fg="white", cursor="hand2")
               load_btn.bind("<Enter>", lambda e: load_btn.config(bg="#222222"))
               load_btn.bind("<Leave>", lambda e: load_btn.config(bg="#000000"))
               load_btn.bind("<Button-1>", lambda e: self.load_method_details(
                    method_id_var.get(), name_entry, details_entry, name_var, details_var, update_btn
                ))
            else:
                load_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                load_btn.unbind("<Enter>")
                load_btn.unbind("<Leave>")
                load_btn.unbind("<Button-1>")

        method_id_var.trace_add("write", validate_load_btn)
        
    def load_method_details(self, method_id, name_entry, details_entry, name_var, details_var, update_btn):
    
        import requests

        try:
            url = f"http://127.0.0.1:8000/admin/payment-methods/{method_id}"
            response = requests.get(url)

            if response.status_code == 200:
                if response.status_code != 200:
                    self.show_popup("Not Found", "Payment Method not found!", "error")
                    return
                data = response.json()

                name_entry.config(state="normal")
                details_entry.config(state="normal")

                name_var.set(data["method_name"])
                details_var.set(data["details"])

                print("Loaded:", data)
            else:
                self.show_popup("Backend Error", str(e), "error")
                return

        except Exception as e:
            print("Error loading method details:", e)
            return

        # ===== VALIDATE & ENABLE UPDATE BUTTON =====
        def validate_update(*args):
            if name_var.get().strip() and details_var.get().strip():
                update_btn.config(
                state="normal",
                bg="#000000", fg="white",
                activebackground="#111111",
                activeforeground="white",
                cursor="hand2"
                )
                update_btn.bind("<Enter>", lambda e: update_btn.config(bg="#222222"))
                update_btn.bind("<Leave>", lambda e: update_btn.config(bg="#000000"))
            else:
                update_btn.config(
                state="disabled",
                bg="#D5D8DC", fg="#AEB6BF",
                cursor="arrow"
                )

        name_var.trace_add("write", validate_update)
        details_var.trace_add("write", validate_update)

        # ===== SUBMIT UPDATE =====
        def update_method():
            method_name = name_var.get().strip()
            details = details_var.get().strip()

    # ---------- VALIDATION: METHOD NAME ----------
            if not method_name:
                self.show_popup("Missing Input", "Method Name cannot be empty!", "warning")
                return

    # Title case name
            method_name = method_name.title()

            allowed_values = ["true", "false"]
            if details.lower() not in allowed_values:
                self.show_popup(
            "Invalid Value",
            "Details must be either 'True' or 'False' only.",
            "warning"
        )
                return

            details = "True" if details.lower() == "true" else "False"

            payload = {
        "method_name": method_name,
        "details": details
    }       
            try:
                res = requests.put(
            f"http://127.0.0.1:8000/admin/payment-methods/update/{method_id}",
            json=payload
        )

                if res.status_code == 200:
                    self.show_popup("Success", "Payment Method Updated Successfully!", "info")
                    self.change_screen(
                "Payment Method Updated!",
                add_callback=self.load_update_method_screen
            )
                else:
                    msg = res.json().get("detail", "Update failed!")
                    self.show_popup("Error", msg, "error")

            except Exception as e:
                self.show_popup("Backend Error", str(e), "error")
                return

        update_btn.config(command=update_method)
   
    # ==== Button to delete any payment method ====
    def load_delete_method_screen(self):
        self.clear_content()

        # Title
        tk.Label(
        self.content,
        text="Delete Payment Method",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # Form container
        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=20)

        # ----- Method ID -----
        tk.Label(
        form, text="Method ID:",
        font=("Arial", 14), bg="#ECF0F1"
        ).grid(row=0, column=0, padx=10, pady=8)

        method_id_var = tk.StringVar()
        method_entry = tk.Entry(
            form, textvariable=method_id_var,
            font=("Arial", 14), width=25
        )
        method_entry.grid(row=0, column=1, padx=10, pady=8)

        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

        # Back Button from global function
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,    
        form_frame=form                          
        )
        self.content.update_idletasks()
        # ----- DELETE BUTTON -----
        delete_btn = tk.Label(
            form,
            text="Delete",
            font=("Arial", 12, "bold"),
            bg="#D5D8DC",
            fg="#AEB6BF",
            padx=15, pady=7,
            width=12,
            relief="ridge",
            cursor="arrow"
        )
        delete_btn.grid(row=1, columnspan=2, pady=20)

        # ====== VALIDATION for DARK MODE ======
        def validate_delete(*args):
            if method_id_var.get().strip():
                delete_btn.config(bg="#000000", fg="white", cursor="hand2")

                delete_btn.bind("<Enter>", lambda e: delete_btn.config(bg="#222222"))
                delete_btn.bind("<Leave>", lambda e: delete_btn.config(bg="#000000"))

                delete_btn.bind("<Button-1>", lambda e: perform_delete())

            else:
                delete_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                delete_btn.unbind("<Enter>")
                delete_btn.unbind("<Leave>")
                delete_btn.unbind("<Button-1>")

        method_id_var.trace_add("write", validate_delete)

        # ====== DELETE API CALL ======
        def perform_delete():
            mid = method_id_var.get().strip()
            if not mid.isdigit() or int(mid) <= 0:
                self.show_popup("Invalid ID", "Method ID should be a Positve Number!", "warning")

            import requests
            try:
                res = requests.delete(
                f"http://127.0.0.1:8000/admin/payment-methods/delete/{mid}"
                )

                if res.status_code == 200:
                    self.show_popup("Success", "Payment Method Deactivated Successfully", "success")
                    self.change_screen("Payment Method Deactivated Successfully",
                                    add_callback=self.load_delete_method_screen)
                else:
                    self.show_popup("Failure", "Dactivation Failed", "error")
                    self.change_screen("Failed to Delete Payment Method")

            except:
                self.show_popup("Error", "Backend Error", "error")
                return

    # ===================================================================================
    # --- STUDENTS ATTENDANCE ---
    # ==== Button to view Attendance of All students====
    def load_view_all_student_attendance(self):
        self.clear_content()

    # ---- Page Title ----
        tk.Label(
        self.content,
        text="All Student Attendance Records",
        font=("Arial", 24, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
    ).pack(pady=20)

    # ---- Back Button ----
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)
        self.create_back_button(back_frame, self.load_dashboard, None)

    # ---- Table Frame ----
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # ---- FILTER BAR ----
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=10)

    # Columns available for filtering
        cols = (
        "attendance_id", "student_id", "student_name", "subject_id",
        "subject_name", "class_id", "teacher_id",
        "lecture_date", "status", "remarks"
    )

    # Label
        tk.Label(
        filter_frame,
        text="Sort By:",
        font=("Arial", 12, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
    ).grid(row=0, column=0, padx=5)

    # Dropdown
        filter_var = tk.StringVar()
        filter_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=list(cols),
        state="readonly",
        width=18
    )
        filter_dropdown.grid(row=0, column=1, padx=10)

    # Entry for filter value
        filter_value_var = tk.StringVar()
        filter_value = tk.Entry(
    filter_frame,
    textvariable=filter_value_var,
    font=("Arial", 12),
    width=20
)
        filter_value.grid(row=0, column=2, padx=10)


    # ---- Button Styler ----
        def style_button(btn):
            btn.config(
            bg="#000000", fg="white",
            padx=15, pady=5, width=10,
            relief="raised", cursor="hand2",
            font=("Arial", 12, "bold")
        )
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

    # Load Button
        load_btn = tk.Label(filter_frame, text="Load")
        style_button(load_btn)
        load_btn.grid(row=0, column=3, padx=10)

    # Load All Button
        load_all_btn = tk.Label(filter_frame, text="Load All")
        style_button(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

    # ---- Scrollbars ----
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

    # ---- Table Widget ----
        self.att_tree = ttk.Treeview(
        table_frame,
        columns=cols,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set,
        height=18
    )
        self.att_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.att_tree.yview)
        x_scroll.config(command=self.att_tree.xview)

    # Column widths
        col_widths = {
        "attendance_id": 120,
        "student_id": 100,
        "student_name": 180,
        "subject_id": 100,
        "subject_name": 180,
        "class_id": 100,
        "teacher_id": 100,
        "lecture_date": 150,
        "status": 80,
        "remarks": 200
    }

    # Table headers
        for col in cols:
            self.att_tree.heading(col, text=col.replace("_", " ").title())
            self.att_tree.column(col, width=col_widths[col], anchor="center")

    # ---- Fetch backend data ----
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admin/attendance/student")
            self.all_attendance = res.json() if res.status_code == 200 else []
            # ====== VALIDATION DICT FOR ATTENDANCE TABLE ======
            self.column_values_attendance = {
    "attendance_id": [str(r["attendance_id"]) for r in self.all_attendance],
    "student_id":     [str(r["student_id"]) for r in self.all_attendance],
    "student_name":   [r["student_name"] for r in self.all_attendance],
    "subject_id":     [str(r["subject_id"]) for r in self.all_attendance],
    "subject_name":   [r["subject_name"] for r in self.all_attendance],
    "class_id":       [str(r["class_id"]) for r in self.all_attendance],
    "teacher_id":     [str(r["teacher_id"]) for r in self.all_attendance],
    "lecture_date":   [r["lecture_date"] for r in self.all_attendance],
    "status":         [r["status"] for r in self.all_attendance],
    "remarks":        [r["remarks"] for r in self.all_attendance],
}

        except:
            self.all_attendance = []

    # ---- Update table ----
        def update_att_table(data):
            for row in self.att_tree.get_children():
                self.att_tree.delete(row)

            for r in data:
                self.att_tree.insert(
                "", "end",
                values=(
                    r["attendance_id"],
                    r["student_id"],
                    r["student_name"],
                    r["subject_id"],
                    r["subject_name"],
                    r["class_id"],
                    r["teacher_id"],
                    r["lecture_date"],
                    r["status"],
                    r["remarks"]
                )
            )

    # ---- FILTER LOGIC ----
        def load_filtered():
            col = filter_var.get().strip()
            val = filter_value.get().strip()

            if not col or not val:
                return
            valid_list = self.column_values_attendance.get(col, [])
            valid_lower = [str(v).lower() for v in valid_list]

            if val not in valid_lower:
                self.show_popup(
            "Invalid Search Value",
            f"'{val}' not found in column '{col}'.",
            "warning"
        )
                filter_value_var.set("")
                return
            
            filtered = [
            row for row in self.all_attendance
            if str(row[col]).lower() == val.lower()
        ]

            update_att_table(filtered)

        def load_all():
            update_att_table(self.all_attendance)

        load_btn.bind("<Button-1>", lambda e: load_filtered())
        load_all_btn.bind("<Button-1>", lambda e: load_all())

    # INITIAL LOAD
        update_att_table(self.all_attendance)


    # ===== Button to view attendance using attendance_id ====
    def load_view_attendance_by_id(self):
        self.clear_content()

        # ------ PAGE TITLE ------
        tk.Label(
        self.content,
        text="View Attendance by ID",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # ------ ATTENDANCE ID INPUT ------
        tk.Label(form, text="Attendance ID:", font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=0, padx=10, pady=8)

        att_id_var = tk.StringVar()
        att_entry = tk.Entry(form, textvariable=att_id_var, font=("Arial", 14), width=25)
        att_entry.grid(row=0, column=1, padx=10, pady=8)
        
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

        # Back Button from global function
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,    
        form_frame=form                          
        )
        # ------ LOAD BUTTON ------
        load_btn = tk.Label(
        form,
        text="Load",
        font=("Arial", 12, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=15, pady=5,
        width=12,
        relief="ridge",
        cursor="arrow"
        )
        load_btn.grid(row=0, column=2, padx=10)

        # Enable dark mode on typing
        def validate_load(*args):
            if att_id_var.get().strip():
                load_btn.config(bg="#000000", fg="white", cursor="hand2")
                load_btn.bind("<Enter>", lambda e: load_btn.config(bg="#222222"))
                load_btn.bind("<Leave>", lambda e: load_btn.config(bg="#000000"))
                load_btn.bind("<Button-1>", lambda e: load_attendance())
            else:
                load_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                load_btn.unbind("<Enter>")
                load_btn.unbind("<Leave>")
                load_btn.unbind("<Button-1>")

        att_id_var.trace_add("write", validate_load)

        # ------ RESULT BOX ------
        result_frame = tk.Frame(self.content, bg="#ECF0F1")
        result_frame.pack(pady=20)

        result_box = tk.Text(
        result_frame,
        width=80,
        height=12,
        font=("Arial", 13),
        bg="#FBFCFC",
        fg="#2C3E50",
        relief="solid",
        borderwidth=1
        )
        result_box.pack()

        # ------ BACKEND FETCH ------
        def load_attendance():
            att_id = att_id_var.get().strip()
            result_box.delete("1.0", "end")
            if not att_id:
                self.show_popup("Missing Input", "Attendance ID cannot be empty!", "warning")
                return
            import requests

            if not att_id.isdigit() or int(att_id) <= 0:
                self.show_popup(
            "Invalid ID",
            "Attendance ID must be a positive number!",
            "warning"
        )
                return

            try:
                res = requests.get(f"http://127.0.0.1:8000/admin/attendance/student/{att_id}")

                if res.status_code == 404:
                    result_box.insert("end", "Attendance record not found")
                    return

                data = res.json()

                formatted = f"""
                    Attendance ID : {data['attendance_id']}
                    Student ID    : {data['student_id']}
                    Student Name  : {data['student_name']}
                    Subject ID    : {data['subject_id']}
                    Subject Name  : {data['subject_name']}
                    Class ID      : {data['class_id']}
                    Teacher ID    : {data['teacher_id']}
                    Lecture Date  : {data['lecture_date']}
                    Status        : {data['status']}
                    Remarks       : {data['remarks']}
                    """
                result_box.insert("end", formatted)

            except Exception as e:
                result_box.insert("end", f"Error fetching data: {e}")

    # ==== Button to view student's attendance with date filters ====
    def load_filter_student_attendance_screen(self):
        self.clear_content()

    # ---------------- PAGE HEADER ----------------
        tk.Label(
        self.content,
        text="Filter Student Attendance by Date",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # ---- FORM INPUTS -----
        labels = ["Student ID:", "Date From (YYYY-MM-DD):", "Date To (YYYY-MM-DD):", "Subject ID (optional):"]
        vars_list = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
    
        entries = []

        # DATE PICKER ENABLED VERSION
        for i, label in enumerate(labels):

            tk.Label(form, text=label, font=("Arial", 14), bg="#ECF0F1").grid(row=i, column=0, padx=10, pady=8)

            var = vars_list[i]

            if label.startswith("Date From") or label.startswith("Date To"):

                entry = tk.Entry(form, textvariable=var, font=("Arial", 14), width=20)
                entry.grid(row=i, column=1, padx=5, pady=8)

                tk.Button(
            form,
            text="calendar",
            font=("Arial", 12),
            bg="white",
            relief="flat",
            command=lambda v=var, e=entry: self.open_calendar_popup(e, v)
        ).grid(row=i, column=2, padx=5)

            else:
                entry = tk.Entry(form, textvariable=var, font=("Arial", 14), width=25)
                entry.grid(row=i, column=1, padx=10, pady=8)

            entries.append(entry)

# -------------------------------------
#  LOOP FINISH → NOW unpack variables
# -------------------------------------
        student_var = vars_list[0]
        from_var    = vars_list[1]
        to_var      = vars_list[2]
        subject_var = vars_list[3]

        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

        # Back Button from global function
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,    
        form_frame=form                          
        )
        # ----- LOAD BUTTON -----
        load_btn = tk.Label(
        form,
        text="Load",
        font=("Arial", 12, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=15, pady=5,
        width=12,
        relief="ridge",
        cursor="arrow"
        )
        load_btn.grid(row=4, column=1, pady=12)

        # --------- VALIDATION FOR DARK MODE ----------
        def validate_load(*args):
            if student_var.get().strip() and from_var.get().strip() and to_var.get().strip():
                load_btn.config(bg="#000000", fg="white", cursor="hand2")

                load_btn.bind("<Enter>", lambda e: load_btn.config(bg="#222222"))
                load_btn.bind("<Leave>", lambda e: load_btn.config(bg="#000000"))
                load_btn.bind("<Button-1>", lambda e: load_attendance())
            else:
                load_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                load_btn.unbind("<Enter>")
                load_btn.unbind("<Leave>")
                load_btn.unbind("<Button-1>")

        student_var.trace_add("write", validate_load)
        from_var.trace_add("write", validate_load)
        to_var.trace_add("write", validate_load)

        # ----------- RESULT TABLE FRAME -----------
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(pady=20, fill="both", expand=True)

        # ---------- BACKEND FUNCTION ----------
        def load_attendance():
            import requests
            student_id = student_var.get().strip()
            date_from = from_var.get().strip()
            date_to = to_var.get().strip()
            subject_id_raw = subject_var.get().strip()

            if not student_id or not student_id.isdigit() or int(student_id) <= 0:
                self.show_popup("Invalid Student ID", "Student ID must be a positive number.", "warning")
                return

            if not date_from or not date_to:
                self.show_popup("Missing Dates", "Both Date From and Date To are required!", "warning")
                return

            def is_valid_date(d):
                try:
                    datetime.strptime(d, "%Y-%m-%d")
                    return True
                except:
                    return False

            if not is_valid_date(date_from):
                self.show_popup("Invalid Date", "Date From must be in YYYY-MM-DD format.", "warning")
                return

            if not is_valid_date(date_to):
                self.show_popup("Invalid Date", "Date To must be in YYYY-MM-DD format.", "warning")
                return
            if datetime.strptime(date_from, "%Y-%m-%d") > datetime.strptime(date_to, "%Y-%m-%d"):
                self.show_popup("Invalid Range", "Date From cannot be greater than Date To.", "warning")
                return

            if subject_id_raw:
                if not subject_id_raw.isdigit() or int(subject_id_raw) <= 0:
                    self.show_popup("Invalid Subject ID", "Subject ID must be a positive number.", "warning")
                    return
                subject_id = int(subject_id_raw)
            else:
                subject_id = None      
            try:
                payload = {
                    "student_id": int(student_id),
                    "date_from": date_from,
                    "date_to": date_to,
                    "subject_id": (int(subject_id) if subject_id.get().strip() else None)
                }

                # Clear old results
                for w in table_frame.winfo_children():
                    w.destroy()

                response = requests.post(
                    "http://127.0.0.1:8000/admin/attendance/student/by-date",
                    json=payload
                )

                if response.status_code != 200:
                    msg = response.json().get("detail", "Failed to fetch attendance.")
                    self.show_popup("Error", msg, "error")
                    tk.Label(
                        table_frame,
                        text="No Attendance Found!",
                        font=("Arial", 16),
                        fg="red",
                        bg="#ECF0F1"
                        ).pack()
                    return

                records = response.json()

                if not records:
                    self.show_popup("No Records", "No attendance records found for this filter.", "info")
                    tk.Label(
                        table_frame,
                        text="No Records Found For This Filter!",
                        font=("Arial", 16),
                        fg="red",
                        bg="#ECF0F1"
                    ).pack()
                    return

                cols = ["attendance_id", "student_id", "subject_id",
                        "class_id", "lecture_date", "status", "remarks"]

                tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=12)

        # scroll
                y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
                tree.configure(yscroll=y_scroll.set)
                y_scroll.pack(side="right", fill="y")

        # headings
                for col in cols:
                    tree.heading(col, text=col.replace("_", " ").title())
                    tree.column(col, width=150, anchor="center")

        # insert rows
                for r in records:
                    tree.insert("", "end", values=(
                        r["attendance_id"],
                        r["student_id"],
                        r["subject_id"],
                        r["class_id"],
                        r["lecture_date"],
                        r["status"],
                        r["remarks"]
                    ))

                tree.pack(fill="both", expand=True)

            except Exception as e:
                self.show_popup("Backend Error", str(e), "error")
                tk.Label(
            table_frame,
            text=f"Error: {e}",
            font=("Arial", 14),
            fg="red",
            bg="#ECF0F1"
                ).pack()


    # ==== Button to View attendance summary of any student ====
    def load_attendance_summary_screen(self):
        self.clear_content()

        # ---------- HEADER -----------
        tk.Label(
        self.content,
        text="Student Attendance Summary",
        bg="#ECF0F1",
        fg="#2C3E50",
        font=("Arial", 26, "bold")
        ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # ----------- FORM VARIABLES ------------
        student_var = tk.StringVar()
        from_var = tk.StringVar()
        to_var = tk.StringVar()

        # ---------------- FORM UI ----------------
        fields = [
        ("Student ID:", student_var),
        ("Date From (YYYY-MM-DD):", from_var),
        ("Date To (YYYY-MM-DD):", to_var)
        ]

        for i, (label_text, var) in enumerate(fields):

    # LABEL
            tk.Label(
        form,
        text=label_text,
        bg="#ECF0F1",
        font=("Arial", 14)
    ).grid(row=i, column=0, padx=10, pady=8)

    # -------------------------
    # DATE PICKER FIELDS
    # -------------------------
            if label_text.startswith("Date From") or label_text.startswith("Date To"):
        # entry box
                entry = tk.Entry(form, textvariable=var, font=("Arial", 14), width=20)
                entry.grid(row=i, column=1, padx=5, pady=8)

        # calendar button
                tk.Button(
            form,
            text="Calendar",
            font=("Arial", 12),
            bg="white",
            relief="flat",
            command=lambda v=var, e=entry: self.open_calendar_popup(e, v)
        ).grid(row=i, column=2, padx=5)

            else:
        # NORMAL ENTRY
                tk.Entry(
            form,
            textvariable=var,
            font=("Arial", 14),
            width=25
        ).grid(row=i, column=1, padx=10, pady=8)

        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

        # Back Button from global function
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,    
        form_frame=form                          
        )
        # ---------------- LOAD BUTTON ----------------
        load_btn = tk.Label(
        form,
        text="Load Summary",
        font=("Arial", 12, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=15, pady=7,
        width=15,
        relief="ridge",
        cursor="arrow"
        )
        load_btn.grid(row=3, column=1, pady=15)

        # ---------------- ENABLE/DISABLE BUTTON ----------------
        def validate_load(*args):
            if student_var.get().strip() and from_var.get().strip() and to_var.get().strip():
                load_btn.config(bg="#000000", fg="white", cursor="hand2")
                load_btn.bind("<Enter>", lambda e: load_btn.config(bg="#222222"))
                load_btn.bind("<Leave>", lambda e: load_btn.config(bg="#000000"))
                load_btn.bind("<Button-1>", lambda e: load_summary())
            else:
                load_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                load_btn.unbind("<Enter>")
                load_btn.unbind("<Leave>")
                load_btn.unbind("<Button-1>")

        student_var.trace_add("write", validate_load)
        from_var.trace_add("write", validate_load)
        to_var.trace_add("write", validate_load)

        # ---------------- RESULT FRAME ----------------
        result_frame = tk.Frame(self.content, bg="#ECF0F1")
        result_frame.pack(pady=20)

        # ---------------- CALL BACKEND ----------------
        def load_summary():
    # Clear previous result
            from datetime import datetime
            for w in result_frame.winfo_children():
                w.destroy()

            import requests
            student_raw = student_var.get().strip()
            if not student_raw.isdigit() or int(student_raw) <= 0:
                self.show_popup("Invalid Student ID", "Student ID must be a positive number.", "warning")
                return

            student_id = int(student_raw)

            date_from = from_var.get().strip()
            date_to = to_var.get().strip()

    # Empty date check
            if not date_from or not date_to:
                self.show_popup("Missing Dates", "Both Date From and Date To are required!", "warning")
                return

    # Format check
            def is_valid_date(d):
                try:
                    datetime.strptime(d, "%Y-%m-%d")
                    return True
                except:
                    return False

            if not is_valid_date(date_from):
                self.show_popup("Invalid Date", "Date From must be in YYYY-MM-DD format!", "warning")
                return

            if not is_valid_date(date_to):
                self.show_popup("Invalid Date", "Date To must be in YYYY-MM-DD format!", "warning")
                return

            # From ≤ To check
            if datetime.strptime(date_from, "%Y-%m-%d") > datetime.strptime(date_to, "%Y-%m-%d"):
                self.show_popup("Invalid Range", "Date From cannot be greater than Date To.", "warning")
                return
    # ---- SAFE student_id ----
            try:
                student_id = int(student_var.get().strip())
            except:
                tk.Label(
            result_frame,
            text="Invalid Student ID!",
            bg="#ECF0F1",
            fg="red",
            font=("Arial", 14)
            ).pack()
                return

            url = (
                f"http://127.0.0.1:8000/admin/attendance/student/summary/{student_id}"
                f"?date_from={date_from}"
                f"&date_to={date_to}"
                )

            try:
                res = requests.get(url)

        # ---- If backend error or student doesn't exist ----
                if res.status_code != 200:
                    self.show_popup("Not Found", "Student not found or no summary available!", "warning")
                    tk.Label(
                result_frame,
                text="Student not found or no summary available!",
                bg="#ECF0F1",
                fg="red",
                font=("Arial", 14)
                ).pack()
                    return

                data = res.json()

        # ------- Summary Card -------
                card = tk.Frame(result_frame, bg="white", bd=2, relief="groove", padx=30, pady=30)
                card.pack(pady=20)

                items = [
            ("Student ID", data["student_id"]),
            ("Total Lectures", data["total_lectures"]),
            ("Present", data["present"]),
            ("Absent", data["absent"]),
            ("Late", data["late"]),
            ("Attendance %", f"{data['percentage']}%"),
            ]

                for idx, (label_text, value) in enumerate(items):
                    tk.Label(card, text=f"{label_text}: ", font=("Arial", 14, "bold"), bg="white")\
                        .grid(row=idx, column=0, sticky="w", pady=5)
                    tk.Label(card, text=value, font=("Arial", 14), bg="white")\
                        .grid(row=idx, column=1, sticky="w", pady=5)

            except Exception as e:
                self.show_popup("Backend Error", str(e), "error")
                tk.Label(
            result_frame,
            text=f"Error: {e}",
            bg="#ECF0F1",
            fg="red",
            font=("Arial", 14)
            ).pack()


    # ==== Button to update attendance of any student using attendance_id ====
    def load_update_student_attendance_screen(self):
        self.clear_content()

    # ===== HEADER =====    
        tk.Label(
        self.content,
        text="Update Student Attendance",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
    ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

    # ERROR MESSAGE HOLDER
        self.update_error_label = None

    # ===== ATTENDANCE ID INPUT =====
        tk.Label(form, text="Attendance ID:", font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=0, pady=8)
        att_id_var = tk.StringVar()

        tk.Entry(
        form, textvariable=att_id_var,
        font=("Arial", 14), width=25
    ).grid(row=0, column=1, padx=10, pady=8)

    # Load Button (Label Style)
        load_btn = tk.Label(
        form, text="Load", font=("Arial", 12, "bold"),
        bg="#D5D8DC", fg="#AEB6BF",
        padx=15, pady=7, width=12,
        relief="ridge", cursor="arrow"
    )
        load_btn.grid(row=0, column=2, padx=10)

    # ===== FORM FIELDS =====
        labels = [
    "Student ID", "Class ID", "Subject ID", "Teacher ID",
    "Date (YYYY-MM-DD)", "Status (P/A/L)", "Remarks"
]
        self.update_vars = {}
        self.update_fields = {}

        for i, t in enumerate(labels, start=1):

    # Label
            tk.Label(
        form,
        text=f"{t}:",
        font=("Arial", 14),
        bg="#ECF0F1"
    ).grid(row=i, column=0, pady=8)

    # Create Var
            var = tk.StringVar()

    # -----------------------------
    # SPECIAL CASE: DATE FIELD
    # -----------------------------
            if t == "Date (YYYY-MM-DD)":

        # ENABLED entry (editable)
                entry = tk.Entry(
            form,
            textvariable=var,
            font=("Arial", 14),
            width=20,
        )
                entry.grid(row=i, column=1, padx=5, pady=8)

        # Add Calendar Button
                tk.Button(
            form,
            text="Calendar",
            font=("Arial", 12),
            bg="white",
            relief="flat",
            command=lambda v=var, e=entry: self.open_calendar_popup(e, v)
        ).grid(row=i, column=2, padx=5)

            else:
        # OTHER FIELDS → DISABLED
                entry = tk.Entry(
            form,
            textvariable=var,
            font=("Arial", 14),
            width=25,
            state="disabled"
        )
                entry.grid(row=i, column=1, padx=10, pady=8)

            self.update_vars[t] = var
            self.update_fields[t] = entry

    # ===== BUTTON FRAME =====
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=20)

        self.create_back_button(btn_frame, self.load_dashboard, form)

    # ===== UPDATE BUTTON (LABEL STYLE) =====
        update_btn = tk.Label(
        self.content,
        text="Update Attendance",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC", fg="#AEB6BF",
        padx=20, pady=10,
        width=18,
        relief="ridge",
        cursor="arrow"
    )
        update_btn.pack(pady=20)


    # ===== SUBMIT FUNCTION (must be defined before activation!) =====
        def submit_update():
            from datetime import datetime
            import requests

            att_id = att_id_var.get().strip()
            att_id = att_id_var.get().strip()
            if not att_id.isdigit() or int(att_id) <= 0:
                self.show_popup("Invalid Attendance ID",
                        "Attendance ID must be a positive number.",
                        "warning")
                return
            def safe_int(value, field_name):
                v = value.strip()
                if not v.isdigit():
                    self.show_popup("Invalid Input",
                            f"{field_name} must be a valid number.",
                            "warning")
                    return None
                if int(v) <= 0:
                    self.show_popup("Invalid Value",
                            f"{field_name} must be greater than 0.",
                            "warning")
                    return None
                return int(v)
            
            sid = safe_int(self.update_vars["Student ID"].get(), "Student ID")
            if sid is None: return

            cid = safe_int(self.update_vars["Class ID"].get(), "Class ID")
            if cid is None: return

            subid = safe_int(self.update_vars["Subject ID"].get(), "Subject ID")
            if subid is None: return

        # Teacher ID safe convert
            teacher_raw = self.update_vars["Teacher ID"].get().strip()
            if teacher_raw == "":
                teacher_conv = None
            elif teacher_raw.isdigit() and int(teacher_raw) > 0:
                teacher_conv = int(teacher_raw)
            else:
                self.show_popup("Invalid Teacher ID",
                        "Teacher ID must be a positive number or empty.",
                        "warning")
                return
            
            date_raw = self.update_vars["Date (YYYY-MM-DD)"].get().strip()

            def valid_date(d):
                try:
                    datetime.strptime(d, "%Y-%m-%d")
                    return True
                except:
                    return False

            if not valid_date(date_raw):
                self.show_popup("Invalid Date Format",
                        "Date must be in YYYY-MM-DD format.",
                        "warning")
                return
            status = self.update_vars["Status (P/A/L)"].get().strip().upper()
            if status not in ("P", "A", "L"):
                self.show_popup("Invalid Status",
                        "Status must be P (Present), A (Absent), or L (Leave).",
                        "warning")
                return
            remarks = self.update_vars["Remarks"].get().strip()

            payload = {
        "student_id": sid,
        "class_id": cid,
        "subject_id": subid,
        "teacher_id": teacher_conv,
        "lecture_date": date_raw,
        "status": status,
        "remarks": remarks
    }
            try: 
                res= requests.put(
            f"http://127.0.0.1:8000/admin/attendance/student/update/{att_id}",
            json=payload
        )
                if res.status_code == 200:
                    self.show_popup("Success",
                            "Student attendance updated successfully!",
                            "info")
                    self.change_screen(
            "Student Attendance Updated Successfully!",
            add_callback=self.load_update_student_attendance_screen
        )
                else:
                    msg = res.json().get("detail", "Update failed.")
                    self.show_popup("Error", msg, "error")
            except Exception as e:
                self.show_popup("Backend Error", str(e), "error")
                return

    # ===== ACTIVATE / DISABLE UPDATE BUTTON =====
        def enable_update_button():
            update_btn.config(
            bg="#000", fg="white",
            cursor="arrow", relief="flat"
        )
            update_btn.bind("<Enter>", lambda e: update_btn.config(bg="#222"))
            update_btn.bind("<Leave>", lambda e: update_btn.config(bg="#000"))
            update_btn.bind("<Button-1>", lambda e: submit_update())

        def disable_update_button():
            update_btn.config(
            bg="#D5D8DC", fg="#AEB6BF",
            cursor="arrow", relief="ridge"
        )
            update_btn.unbind("<Enter>")
            update_btn.unbind("<Leave>")
            update_btn.unbind("<Button-1>")


        disable_update_button()   # initial state


    # ===== ENABLE UPDATE WHEN ALL FIELDS FULL =====
        def validate_update(*args):
            if all(v.get().strip() for v in self.update_vars.values()):
                enable_update_button()
            else:
                disable_update_button()

        for v in self.update_vars.values():
            v.trace_add("write", validate_update)


    # ===== LOAD ATTENDANCE RECORD =====
        def load_attendance():
            import requests

            att_id = att_id_var.get().strip()
            if not att_id:
                self.show_popup("Missing Input",
                        "Please enter an Attendance ID.",
                        "warning")
                return

            if not att_id.isdigit() or int(att_id) <= 0:
                self.show_popup("Invalid Attendance ID",
                        "Attendance ID must be a positive number.",
                        "warning")
                return

        # Clear old error label
            if self.update_error_label:
                self.update_error_label.destroy()
                self.update_error_label = None

            try:
                res = requests.get(f"http://127.0.0.1:8000/admin/attendance/student/{att_id}")
  
                if res.status_code != 200:
                    self.show_popup("Not Found",
                            "Attendance record not found for this ID.",
                            "error")
                    self.update_error_label = tk.Label(
                    self.content,
                    text="Attendance not found",
                    fg="red", bg="#ECF0F1",
                    font=("Arial", 14)
                )
                    self.update_error_label.pack()
                    return

                data = res.json()

            # Enable all fields
                for entry in self.update_fields.values():
                    entry.config(state="normal")

                self.update_vars["Student ID"].set(data["student_id"])
                self.update_vars["Class ID"].set(data["class_id"])
                self.update_vars["Subject ID"].set(data["subject_id"])
                self.update_vars["Teacher ID"].set("" if data["teacher_id"] is None else data["teacher_id"])
                self.update_vars["Date (YYYY-MM-DD)"].set(data["lecture_date"])
                self.update_vars["Status (P/A/L)"].set(data["status"])
                self.update_vars["Remarks"].set(data.get("remarks", ""))

            except Exception as e:
                self.show_popup("Backend Error",
                        f"Unable to fetch attendance.\nError: {e}",
                        "error")
                return

    # ===== LOAD BUTTON VALIDATION =====
        def validate_load(*args):
            if att_id_var.get().strip():
                load_btn.config(bg="#000", fg="white", cursor="hand2")
                load_btn.bind("<Enter>", lambda e: load_btn.config(bg="#222"))
                load_btn.bind("<Leave>", lambda e: load_btn.config(bg="#000"))
                load_btn.bind("<Button-1>", lambda e: load_attendance())
            else:
                load_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                load_btn.unbind("<Enter>")
                load_btn.unbind("<Leave>")
                load_btn.unbind("<Button-1>")

        att_id_var.trace_add("write", validate_load)


    # ==== Button to delete attendance of a student using atten_id ====
    def load_delete_student_attendance_screen(self):
        self.clear_content()

        # ----------- HEADER -----------
        tk.Label(
        self.content,
        text="Delete Student Attendance",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=20)

        # ----------- Attendance ID Input -----------
        tk.Label(
        form, text="Attendance ID:", bg="#ECF0F1",
        font=("Arial", 14)
        ).grid(row=0, column=0, pady=10, padx=10)

        att_id_var = tk.StringVar()
        entry = tk.Entry(form, textvariable=att_id_var, font=("Arial", 14), width=25)
        entry.grid(row=0, column=1, padx=10, pady=10)

        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

        # Back Button from global function
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,    
        form_frame=form                          
        )
        self.content.update_idletasks()
        # ----------- DELETE BUTTON (disabled initially) -----------
        delete_btn = tk.Label(
        form,
        text="Delete",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20, pady=8,
        width=12,
        relief="ridge",
        cursor="arrow"
        )
        delete_btn.grid(row=1, column=1, pady=20)

        # ----------- VALIDATE FIELD -----------
        def validate_delete_btn(*args):
            if att_id_var.get().strip():
                delete_btn.config(bg="#000000", fg="white", cursor="hand2")
                delete_btn.bind("<Enter>", lambda e: delete_btn.config(bg="#222222"))
                delete_btn.bind("<Leave>", lambda e: delete_btn.config(bg="#000000"))
                delete_btn.bind("<Button-1>", lambda e: perform_delete())
            else:
                delete_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                delete_btn.unbind("<Enter>")
                delete_btn.unbind("<Leave>")
                delete_btn.unbind("<Button-1>")

        att_id_var.trace_add("write", validate_delete_btn)

        # ----------- PERFORM DELETE CALL -----------
        def perform_delete():
            import requests
            att_id = att_id_var.get().strip()
            if not att_id:
                self.show_popup(
            "Missing Input",
            "Please enter an Attendance ID.",
            "warning"
        )
                return

            if not att_id.isdigit() or int(att_id) <= 0:
                self.show_popup(
            "Invalid Attendance ID",
            "Attendance ID must be a positive number.",
            "warning"
        )
                return

            try:
                url = f"http://127.0.0.1:8000/admin/attendance/student/delete/{att_id}"
                response = requests.delete(url)

                if response.status_code == 200:
                    self.show_popup(
                "Success",
                "Attendance deactivated successfully!",
                "info"
            )
                    self.change_screen("Attendance Deactivated Successfully",
                                       add_callback=self.load_delete_student_attendance_screen)
                else:
                    self.show_popup(
                "Not Found",
                "Attendance record not found for this ID.",
                "error"
            )
                    tk.Label(
                    self.content, text="Attendance Not Found",
                    fg="red", bg="#ECF0F1", font=("Arial", 14)
                    ).pack(pady=10)

            except Exception as e:
                self.show_popup(
            "Backend Error",
            f"Something went wrong.\nError: {e}",
            "error"
        )
                tk.Label(
                self.content, text=f"Error: {e}",
                fg="red", bg="#ECF0F1", font=("Arial", 14)
                ).pack(pady=10)
 

    # ===========================================================================
    # --- TEACHERS ATTENDANCE ---
    # ==== Button to View Attendance of teachers ====
    def load_view_all_teacher_attendance(self):
        self.clear_content()

    # ---- Title ----
        tk.Label(
        self.content,
        text="All Teacher Attendance Records",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
    ).pack(pady=20)

    # ---- Back Button ----
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)
        self.create_back_button(back_frame, self.load_dashboard, None)

    # ---- Table Frame ----
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Columns
        cols = ("record_id", "teacher_id", "date", "status", "remarks")

    # ====================================================
    #     FILTER BAR (Dropdown + Entry + Black Buttons)
    # ====================================================
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=10)

        tk.Label(
        filter_frame,
        text="Sort By:",
        font=("Arial", 12, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
    ).grid(row=0, column=0, padx=5)

        filter_var = tk.StringVar()
        filter_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=list(cols),
        state="readonly",
        width=18
    )
        filter_dropdown.grid(row=0, column=1, padx=10)

        filter_value_var = tk.StringVar()
        filter_value = tk.Entry(
    filter_frame,
    textvariable=filter_value_var,
    font=("Arial", 12),
    width=20
)
        filter_value.grid(row=0, column=2, padx=10)

    # ---------- Button Style ----------
        def style_button(btn):
            btn.config(
            bg="#000000",
            fg="white",
            padx=15,
            pady=5,
            width=10,
            relief="raised",
            cursor="hand2",
            font=("Arial", 12, "bold")
        )
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

    # LOAD Button
        load_btn = tk.Label(filter_frame, text="Load")
        style_button(load_btn)
        load_btn.grid(row=0, column=3, padx=10)

    # LOAD ALL Button
        load_all_btn = tk.Label(filter_frame, text="Load All")
        style_button(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

    # ---- Scrollbars ----
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

    # ---- TABLE ----
        self.teacher_tree = ttk.Treeview(
        table_frame,
        columns=cols,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set,
        height=18
    )
        self.teacher_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.teacher_tree.yview)
        x_scroll.config(command=self.teacher_tree.xview)

    # Column Widths
        widths = {
        "record_id": 120,
        "teacher_id": 120,
        "date": 150,
        "status": 100,
        "remarks": 220,
    }

        for col in cols:
            self.teacher_tree.heading(col, text=col.replace("_", " ").title())
            self.teacher_tree.column(col, width=widths[col], anchor="center")

    # ---- FETCH BACKEND DATA ----
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admin/attendance/teacher")
            self.all_teacher_att = res.json() if res.status_code == 200 else []
            self.column_values_teacher_att = {
    "record_id":   [str(r["record_id"]) for r in self.all_teacher_att],
    "teacher_id":  [str(r["teacher_id"]) for r in self.all_teacher_att],
    "date":        [r["date"] for r in self.all_teacher_att],
    "status":      [r["status"] for r in self.all_teacher_att],
    "remarks":     [r["remarks"] for r in self.all_teacher_att],
}
        except:
            self.all_teacher_att = []

    # ---- UPDATE TABLE ----
        def update_table(data):
            for r in self.teacher_tree.get_children():
                self.teacher_tree.delete(r)

            for row in data:
                self.teacher_tree.insert(
                "",
                "end",
                values=(
                    row["record_id"],
                    row["teacher_id"],
                    row["date"],
                    row["status"],
                    row.get("remarks", "")
                )
            )

    # ---- FILTER LOGIC ----
        def load_filtered():
            col = filter_var.get().strip()
            val = filter_value.get().strip()

            if not col or not val:
                return
            valid_list = self.column_values_teacher_att.get(col, [])
            valid_lower = [str(v).lower() for v in valid_list]

            if val not in valid_lower:
                self.show_popup(
            "Invalid Search Value",
            f"'{val}' not found in column '{col}'.",
            "warning"
        )
                filter_value_var.set("")
                return
            filtered = [
            r for r in self.all_teacher_att
            if str(r[col]).lower() == val.lower()
        ]
            update_table(filtered)

        def load_all():
            update_table(self.all_teacher_att)

        load_btn.bind("<Button-1>", lambda e: load_filtered())
        load_all_btn.bind("<Button-1>", lambda e: load_all())

    # ---- INITIAL LOAD ----
        update_table(self.all_teacher_att)

    
    # ==== Button to view attendance of a teacher using record_id ====
    def load_view_teacher_attendance_by_id(self):
        self.clear_content()

        title = tk.Label(
        self.content,
        text="View Teacher Attendance by Record ID",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        )
        title.pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=20)

        # ===== record ID input =====
        tk.Label(form, text="Record ID:", font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=0, padx=10, pady=8)

        rec_var = tk.StringVar()
        rec_entry = tk.Entry(form, textvariable=rec_var, font=("Arial", 14), width=25)
        rec_entry.grid(row=0, column=1, padx=10, pady=8)
        
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

        # Back Button from global function
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,    
        form_frame=form                          
        )
        # ===== Search Button (Label style) =====
        search_btn = tk.Label(
        form,
        text="Search",
        font=("Arial", 12, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=15,
        pady=5,
        width=12,
        relief="ridge",
        cursor="arrow"
        )
        search_btn.grid(row=0, column=2, padx=10)

        # ====== Output fields ======
        tk.Label(form, text="Teacher ID:", font=("Arial", 14), bg="#ECF0F1").grid(row=1, column=0, padx=10, pady=8)
        tk_id = tk.Entry(form, font=("Arial", 14), width=25, state="disabled")
        tk_id.grid(row=1, column=1, padx=10, pady=8)

        tk.Label(form, text="Date:", font=("Arial", 14), bg="#ECF0F1").grid(row=2, column=0, padx=10, pady=8)
        date_entry = tk.Entry(form, font=("Arial", 14), width=25, state="disabled")
        date_entry.grid(row=2, column=1, padx=10, pady=8)

        tk.Label(form, text="Status:", font=("Arial", 14), bg="#ECF0F1").grid(row=3, column=0, padx=10, pady=8)
        status_entry = tk.Entry(form, font=("Arial", 14), width=25, state="disabled")
        status_entry.grid(row=3, column=1, padx=10, pady=8)

        tk.Label(form, text="Remarks:", font=("Arial", 14), bg="#ECF0F1").grid(row=4, column=0, padx=10, pady=8)
        remarks_entry = tk.Entry(form, font=("Arial", 14), width=25, state="disabled")
        remarks_entry.grid(row=4, column=1, padx=10, pady=8)

        tk.Label(form, text="Record ID:", font=("Arial", 14), bg="#ECF0F1").grid(row=5, column=0, padx=10, pady=8)
        rec_id_entry = tk.Entry(form, font=("Arial", 14), width=25, state="disabled")
        rec_id_entry.grid(row=5, column=1, padx=10, pady=8)

        # ===== ENABLE / DISABLE SEARCH BUTTON =====
        def validate_search_btn(*args):
            if rec_var.get().strip():
                search_btn.config(bg="#000000", fg="white", cursor="hand2")
                search_btn.bind("<Enter>", lambda e: search_btn.config(bg="#222222"))
                search_btn.bind("<Leave>", lambda e: search_btn.config(bg="#000000"))

                search_btn.bind("<Button-1>", lambda e: fetch_attendance())
            else:
                search_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                search_btn.unbind("<Enter>")
                search_btn.unbind("<Leave>")
                search_btn.unbind("<Button-1>")

        rec_var.trace_add("write", validate_search_btn)

        # ===== FETCH DATA FROM BACKEND =====
        def fetch_attendance():
            record_id = rec_var.get().strip()
            if not record_id:
                self.show_popup(
            "Missing Input",
            "Please enter a Record ID.",
            "warning"
        )
                return
            if not record_id.isdigit() or int(record_id) <= 0:
                self.show_popup(
            "Invalid Record ID",
            "Record ID must be a positive number.",
            "warning"
        )
                return
            import requests
            try:
                res = requests.get(f"http://127.0.0.1:8000/admin/attendance/teacher/{record_id}")

                if res.status_code == 200:
                    data = res.json()

            # Enable all entries
                    for box in (tk_id, date_entry, status_entry, remarks_entry, rec_id_entry):
                        box.config(state="normal")

            # Clear previous values
                    tk_id.delete(0, "end")
                    date_entry.delete(0, "end")
                    status_entry.delete(0, "end")
                    remarks_entry.delete(0, "end")
                    rec_id_entry.delete(0, "end")

            # Fill new data
                    tk_id.insert(0, data["teacher_id"])
                    date_entry.insert(0, data["date"])
                    status_entry.insert(0, data["status"])
                    remarks_entry.insert(0, data.get("remarks", ""))
                    rec_id_entry.insert(0, data.get("record_id", ""))

            # Disable them again
                    for box in (tk_id, date_entry, status_entry, remarks_entry, rec_id_entry):
                        box.config(state="disabled")

                else:
                    self.show_popup(
                "Not Found",
                f"No attendance record found for ID {record_id}.",
                "error"
            )
                    return

            except Exception as e:
                self.show_popup(
            "Backend Error",
            f"Something went wrong.\nError: {e}",
            "error"
        )
                return


    # ==== Button to View teacher attendance summary ====
    def load_teacher_attendance_summary_screen(self):
        self.clear_content()

        title = tk.Label(
        self.content,
        text="Teacher Attendance Summary",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        )
        title.pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # ===== Inputs =====
        tk.Label(form, text="Teacher ID:", font=("Arial", 14), bg="#ECF0F1")\
            .grid(row=0, column=0, padx=10, pady=8)
        tid_var = tk.StringVar()
        tid_entry = tk.Entry(form, textvariable=tid_var, font=("Arial", 14), width=25)
        tid_entry.grid(row=0, column=1, padx=10, pady=8)

        # ---- FROM DATE ----
        tk.Label(
    form,
    text="From Date (YYYY-MM-DD):",
    font=("Arial", 14),
    bg="#ECF0F1"
).grid(row=1, column=0, padx=10, pady=8)

        from_var = tk.StringVar()
        from_entry = tk.Entry(form, textvariable=from_var, font=("Arial", 14), width=20)
        from_entry.grid(row=1, column=1, padx=5, pady=8)

        tk.Button(
    form,
    text="Calendar",
    font=("Arial", 12),
    bg="white",
    relief="flat",
    command=lambda v=from_var, e=from_entry: self.open_calendar_popup(e, v)
).grid(row=1, column=2, padx=5)


# ---- TO DATE ----
        tk.Label(
    form,
    text="To Date (YYYY-MM-DD):",
    font=("Arial", 14),
    bg="#ECF0F1"
).grid(row=2, column=0, padx=10, pady=8)

        to_var = tk.StringVar()
        to_entry = tk.Entry(form, textvariable=to_var, font=("Arial", 14), width=20)
        to_entry.grid(row=2, column=1, padx=5, pady=8)

        tk.Button(
    form,
    text="Calendar",
    font=("Arial", 12),
    bg="white",
    relief="flat",
    command=lambda v=to_var, e=to_entry: self.open_calendar_popup(e, v)
).grid(row=2, column=2, padx=5)

        
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

        # Back Button from global function
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,    
        form_frame=form                          
        )
        # ===== Submit Button =====
        summary_btn = tk.Label(
        form,
        text="Get Summary",
        font=("Arial", 12, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        relief="ridge",
        padx=15,
        pady=5,
        width=14,
        cursor="arrow"
        )
        summary_btn.grid(row=3, column=1, pady=15)

        # ===== OUTPUT FRAME =====
        output = tk.Frame(self.content, bg="#ECF0F1")
        output.pack(pady=20)

        labels = {}
        for i, field in enumerate(["Teacher ID", "Total Days", "Present", "Absent", "Leave", "Percentage"]):
            labels[field] = tk.Label(output, text=f"{field}: -", font=("Arial", 16), bg="#ECF0F1", fg="#2C3E50")
            labels[field].pack(anchor="w", padx=30, pady=3)

        # ===== Enable Button on Input =====
        def validate_btn(*args):
            if tid_var.get().strip() and from_var.get().strip() and to_var.get().strip():
                summary_btn.config(bg="#000000", fg="white", cursor="hand2")
                summary_btn.bind("<Enter>", lambda e: summary_btn.config(bg="#222222"))
                summary_btn.bind("<Leave>", lambda e: summary_btn.config(bg="#000000"))
                summary_btn.bind("<Button-1>", lambda e: fetch_summary())
            else:
                summary_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                summary_btn.unbind("<Enter>")
                summary_btn.unbind("<Leave>")
                summary_btn.unbind("<Button-1>")

        tid_var.trace_add("write", validate_btn)
        from_var.trace_add("write", validate_btn)
        to_var.trace_add("write", validate_btn)

        # ===== BACKEND CALL =====
        def fetch_summary():
            teacher_id = tid_var.get().strip()
            date_from = from_var.get().strip()
            date_to = to_var.get().strip()
            if not teacher_id:
                self.show_popup(
            "Missing Input",
            "Teacher ID cannot be empty.",
            "warning"
        )
                return

    # Teacher ID must be a positive integer
            if not teacher_id.isdigit() or int(teacher_id) <= 0:
                self.show_popup(
            "Invalid Teacher ID",
            "Teacher ID must be a positive number.",
            "warning"
        )
                return

    # Date From empty
            if not date_from:
                self.show_popup(
            "Missing Date",
            "Please enter a 'From' date.",
            "warning"
        )
                return

    # Date To empty
            if not date_to:
                self.show_popup(
            "Missing Date",
            "Please enter a 'To' date.",
            "warning"
        )
                return

    # Date format validation
            import re
            date_pattern = r"^\d{4}-\d{2}-\d{2}$"

            if not re.match(date_pattern, date_from):
                self.show_popup(
            "Invalid Date Format",
            "From Date must be in YYYY-MM-DD format.",
            "error"
        )
                return

            import requests
            url = (
                f"http://127.0.0.1:8000/admin/attendance/teacher/summary/{teacher_id}"
                f"?date_from={date_from}"
                f"&date_to={date_to}"
            )

            try:
                res = requests.get(url)     
                if res.status_code != 200:
                    res = requests.get(url)
                    self.show_popup(
                "Not Found",
                "Teacher not found or no summary available for given date range.",
                "error"
            )
                    return
                data = res.json()
                
                labels["Teacher ID"].config(text=f"Teacher ID: {data['teacher_id']}")
                labels["Total Days"].config(text=f"Total Days: {data['total_days']}")
                labels["Present"].config(text=f"Present: {data['present']}")
                labels["Absent"].config(text=f"Absent: {data['absent']}")
                labels["Leave"].config(text=f"Leave: {data['leave']}")
                labels["Percentage"].config(text=f"Percentage: {data['percentage']}%")

            except Exception as e:
                self.show_popup(
            "Backend Error",
            f"Failed to fetch summary.\nError: {e}",
            "error"
        )
                return
            

    # ==== Button to Update a teacher's attendance ====
    def load_update_teacher_attendance_screen(self):
        self.clear_content()

        title = tk.Label(
        self.content,
        text="Update Teacher Attendance",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        )
        title.pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=20)

        # ====== INPUT FIELDS ======
        tk.Label(form, text="Record ID:", font=("Arial", 14), bg="#ECF0F1")\
            .grid(row=0, column=0, padx=10, pady=8)
        record_var = tk.StringVar()
        record_entry = tk.Entry(form, textvariable=record_var, font=("Arial", 14), width=25)
        record_entry.grid(row=0, column=1, padx=10, pady=8)

        # ----- Load Button -----
        load_btn = tk.Label(
        form,
        text="Load",
        font=("Arial", 12, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        relief="ridge",
        width=12,
        padx=10, pady=5,
        cursor="arrow"
        )
        load_btn.grid(row=0, column=2, padx=12)

        # ==== Fields that get filled AFTER load ====
        fields = {
        "Teacher ID": tk.StringVar(),
        "Date": tk.StringVar(),
        "Status": tk.StringVar(),
        "Remarks": tk.StringVar()
        }
        row_index = 1
        entries = {}
        for label, var in fields.items():

            tk.Label(
        form,
        text=f"{label}:",
        font=("Arial", 14),
        bg="#ECF0F1"
    ).grid(row=row_index, column=0, padx=10, pady=8)

    # ---- DATE FIELD GETS SPECIAL TREATMENT ----
            if label == "Date":
                ent = tk.Entry(
            form,
            textvariable=var,
            font=("Arial", 14),
            width=20,
            state="disabled"
        )
                ent.grid(row=row_index, column=1, padx=5, pady=8)

        # Calendar button
                cal_btn = tk.Button(
            form,
            text="Calendar",
            font=("Arial", 12),
            bg="white",
            relief="flat",
            command=lambda v=var, e=ent: self.open_calendar_popup(e, v)
        )
                cal_btn.grid(row=row_index, column=2, padx=5)

            else:
        # ---- NORMAL DISABLED ENTRY ----
                ent = tk.Entry(
            form,
            textvariable=var,
            font=("Arial", 14),
            width=25,
            state="disabled"
        )
                ent.grid(row=row_index, column=1, padx=10, pady=8)

            entries[label] = ent
            row_index += 1
        
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

        # Back Button from global function
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,    
        form_frame=form                          
        )
        self.content.update_idletasks()
        # ====== UPDATE BUTTON ======
        update_btn = tk.Label(
        self.content,
        text="Update Attendance",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        relief="ridge",
        padx=20, pady=10,
        width=20,
        cursor="arrow"
        )
        update_btn.pack(pady=25)

        # ===== VALIDATION FOR LOAD BUTTON =====
        def validate_load(*args):
            if record_var.get().strip():
                load_btn.config(bg="#000000", fg="white", cursor="hand2")
                load_btn.bind("<Enter>", lambda e: load_btn.config(bg="#222222"))
                load_btn.bind("<Leave>", lambda e: load_btn.config(bg="#000000"))
                load_btn.bind("<Button-1>", lambda e: load_record())
            else:
                load_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                load_btn.unbind("<Enter>")
                load_btn.unbind("<Leave>")
                load_btn.unbind("<Button-1>")

        record_var.trace_add("write", validate_load)

        # ===== LOAD EXISTING RECORD =====
        def load_record():
            rec_id = record_var.get().strip()
            if not rec_id:
                self.show_popup("Missing Input", "Record ID cannot be empty!", "warning")
                return

    # Must be positive integer
            if not rec_id.isdigit() or int(rec_id) <= 0:
                self.show_popup("Invalid Record ID", "Record ID must be a positive number.", "warning")
                return

            import requests
            try:
                res = requests.get(f"http://127.0.0.1:8000/admin/attendance/teacher/{rec_id}")
                if res.status_code != 200:
                    self.show_popup(
                "Not Found",
                f"No attendance record found for ID {rec_id}.",
                "error"
            )
                    return
                data = res.json()

                # Enable all input fields
                for ent in entries.values():
                    ent.config(state="normal")

                # Fill values
                fields["Teacher ID"].set(data["teacher_id"])
                fields["Date"].set(data["date"])
                fields["Status"].set(data["status"])
                fields["Remarks"].set(data.get("remarks", ""))

                enable_update_validation()

            except Exception as e:
                self.show_popup(
            "Backend Error",
            f"Could not fetch teacher attendance.\nError: {e}",
            "error"
        )

        # ===== VALIDATE ALL FIELDS BEFORE UPDATE =====
        def enable_update_validation():

            def validate_all(*args):
                if all(v.get().strip() for v in fields.values()):
                    update_btn.config(
                    bg="#000000", fg="white",
                    cursor="hand2"
                    )
                    update_btn.bind("<Enter>", lambda e: update_btn.config(bg="#222222"))
                    update_btn.bind("<Leave>", lambda e: update_btn.config(bg="#000000"))
                    update_btn.bind("<Button-1>", lambda e: submit_update())
                else:
                    update_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                    update_btn.unbind("<Enter>")
                    update_btn.unbind("<Leave>")
                    update_btn.unbind("<Button-1>")

            # Track all fields live
            for var in fields.values():
                var.trace_add("write", validate_all)

        # ===== SUBMIT UPDATE TO BACKEND =====
        def submit_update():
            rec_id = record_var.get().strip()

            if not rec_id:
                self.show_popup("Missing Record ID", "Please enter a Record ID!", "warning")
                return

            if not rec_id.isdigit() or int(rec_id) <= 0:
                self.show_popup("Invalid Record ID", "Record ID must be a positive number.", "warning")
                return
            
            teacher_raw = fields["Teacher ID"].get().strip()
            if not teacher_raw.isdigit() or int(teacher_raw) <= 0:
                self.show_popup("Invalid Teacher ID", "Teacher ID must be a positive number.", "warning")
                return
            teacher_id = int(teacher_raw)

    # Date
            date_val = fields["Date"].get().strip()
            import re
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_val):
                self.show_popup("Invalid Date", "Date must be in YYYY-MM-DD format!", "error")
                return

    # Status
            status_val = fields["Status"].get().strip().upper()
            if status_val not in ["P", "A", "L"]:
                self.show_popup("Invalid Status", "Status must be P, A, or L only!", "warning")
                return
            
            remarks_val = fields["Remarks"].get().strip()

            payload = {
            "teacher_id": teacher_id,
            "date": date_val,
            "status": status_val,
            "remarks": remarks_val
            }

            import requests
            rec_id = record_var.get().strip()
            try:
                res = requests.put(f"http://127.0.0.1:8000/admin/attendance/teacher/update/{rec_id}", json=payload)
                if res.status_code == 200:
                    self.show_popup("Success", "Teacher Attendance Updated Successfully!", "info")
                    self.change_screen(
                "Teacher Attendance Updated Successfully",
                add_callback=self.load_update_teacher_attendance_screen
            )   
                else:
                    msg = res.json().get("detail", "Update failed!")
                    self.show_popup("Error", msg, "error")
    
            except Exception as e:
                self.show_popup("Backend Error", f"Error updating data:\n{e}", "error")


    # ==== Button to delete a teacher's attendance ====
    def load_delete_teacher_attendance_screen(self):
        self.clear_content()

        title = tk.Label(
        self.content,
        text="Delete Teacher Attendance",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        )
        title.pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=20)

        # ---- RECORD ID INPUT ----
        tk.Label(form, text="Record ID:", font=("Arial", 14), bg="#ECF0F1")\
            .grid(row=0, column=0, padx=10, pady=8)

        record_var = tk.StringVar()
        record_entry = tk.Entry(form, textvariable=record_var, font=("Arial", 14), width=25)
        record_entry.grid(row=0, column=1, padx=10, pady=8)

        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

        # Back Button from global function
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,    
        form_frame=form                          
        )
        self.content.update_idletasks()
        # ---- DELETE BUTTON ----
        delete_btn = tk.Label(
        self.content,
        text="Delete Attendance",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        relief="ridge",
        padx=20, pady=10,
        width=20,
        cursor="arrow"
        )
        delete_btn.pack(pady=25)

       # ===== VALIDATE DELETE BUTTON (Enable / Disable) =====
        def validate_delete(*args):
            if record_var.get().strip():
                delete_btn.config(bg="#000000", fg="white", cursor="hand2")

                # Hover
                delete_btn.bind("<Enter>", lambda e: delete_btn.config(bg="#222222"))
                delete_btn.bind("<Leave>", lambda e: delete_btn.config(bg="#000000"))

                # Click
                delete_btn.bind("<Button-1>", lambda e: submit_delete())

            else:
                delete_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                delete_btn.unbind("<Enter>")
                delete_btn.unbind("<Leave>")
                delete_btn.unbind("<Button-1>")

        record_var.trace_add("write", validate_delete)

        # ===== DELETE REQUEST TO BACKEND =====
        def submit_delete():
            rec_id = record_var.get().strip()
            if not rec_id:
                self.show_popup("Missing Record ID", "Please enter Record ID!", "warning")
                return

            if not rec_id.isdigit() or int(rec_id) <= 0:
                self.show_popup("Invalid Record ID",
                        "Record ID must be a positive number.",
                        "warning")
                return

            import requests
            try:
                url = f"http://127.0.0.1:8000/admin/attendance/teacher/delete/{rec_id}"
                res = requests.delete(url)

                if res.status_code == 200:
                    self.show_popup("Success",
                            "Teacher Attendance Deactivated Successfully!",
                            "info")
                    self.change_screen("Teacher Attendance Deactivated Successfully",
                                       add_callback=self.load_delete_teacher_attendance_screen)
                else:
                    msg = res.json().get("detail", "Record Not Found")
                    self.show_popup("Delete Failed", msg, "error")
                    return

            except Exception as e:
                self.show_popup("Backend Error",
                        f"Unable to delete record.\n{e}",
                        "error")

    # ==============================================================================
    # ==== NEW ADMISSIONS ====
    # ---- Button to add new student ----
    def load_create_admission_screen(self):
        self.clear_content()

        tk.Label(self.content, text="New Admission Form",
                font=("Arial", 26, "bold"), bg="#ECF0F1",
                fg="#2C3E50").pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        fields = [
        ("Full Name", "full_name"),
        ("Gender (M/F/O)", "gender"),
        ("Date of Birth", "date_of_birth"),
        ("Address", "address"),
        ("Class ID", "class_id"),
        ("previous school", "previous_school"),
        ("Father Name", "father_name"),
        ("Mother Name", "mother_name"),
        ("Phone", "parent_phone"),
        ("Email", "parent_email")
        ]
 
        vars = {}

        for i, (label, key) in enumerate(fields):

            tk.Label(form, text=f"{label}:", font=("Arial", 14), bg="#ECF0F1")\
                .grid(row=i, column=0, padx=10, pady=6)

            vars[key] = tk.StringVar()

            if key == "date_of_birth":
                entry = tk.Entry(form, textvariable=vars[key], font=("Arial", 14), width=28)
                entry.grid(row=i, column=1, padx=5, pady=6)
                cal_btn = tk.Button(
        form,
        text="Calendar",
        font=("Arial", 12),
        bg="white",
        relief="flat",
        cursor="arrow",
        command=lambda v=vars[key], b=entry: self.open_calendar_popup(b, v)
    )
                cal_btn.grid(row=i, column=2, padx=5)

            else:
                entry = tk.Entry(form, textvariable=vars[key], font=("Arial", 14), width=30)
                entry.grid(row=i, column=1, padx=10, pady=6)

        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

        # Back Button from global function
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,   
        form_frame=form                         
        )
    
        self.content.update_idletasks()

        submit_btn = tk.Label(
        form,
        text="Submit",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20, pady=10,
        width=20,
        cursor="arrow",
        relief="ridge"
        )
        submit_btn.grid(row=len(fields), columnspan=2, pady=20)

        def validate_form(*args):
            if all(vars[k].get().strip() for k in vars):
                submit_btn.config(bg="#000000", fg="white", cursor="hand2")
                submit_btn.bind("<Enter>", lambda e: submit_btn.config(bg="#222222"))
                submit_btn.bind("<Leave>", lambda e: submit_btn.config(bg="#000000"))
                submit_btn.bind("<Button-1>", lambda e: submit())
            else:
                submit_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                submit_btn.unbind("<Enter>")
                submit_btn.unbind("<Leave>")
                submit_btn.unbind("<Button-1>")

        for v in vars.values():
            v.trace_add("write", validate_form)

        def submit():
            data = {k: v.get().strip() for k, v in vars.items()}
            for key, val in vars.items():
                if not val.get().strip():
                    self.show_popup("Missing Information",
                                f"{key.replace('_', ' ').title()} is required!",
                                "warning")
                    return
                
            name_fields = ["full_name", "father_name", "mother_name", "previous_school"]
            for n in name_fields:
                if data.get(n):
                    data[n] = data[n].title() 
                   
            gender = vars["gender"].get().strip().upper()
            if gender not in ["M", "F", "O"]:
                self.show_popup("Invalid Gender",
                             "Gender must be M, F or O only!",
                             "error")
                return
            
            class_id = vars["class_id"].get().strip()
            if not class_id.isdigit():
                self.show_popup("Invalid Class ID", "Class ID must be a numeric value!", "warning")
                return
            
            import re
            dob = vars["date_of_birth"].get().strip()
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", dob):
                self.show_popup("Invalid Date",
                             "Date of Birth must be in YYYY-MM-DD format!",
                             "error")
                return

            from datetime import datetime, date
            try:
                dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
                age = (date.today() - dob_date).days // 365

                if age < 3:
                    self.show_popup("Age Restriction",
                                 "Student must be at least 3 years old!",
                                 "error")
                    return
            except:
                self.show_popup("Invalid Date",
                             "Please enter a valid Date of Birth!",
                             "error")
                return
            
            phone = vars["parent_phone"].get().strip()
            if not phone.isdigit() or len(phone) != 10:
                self.show_popup("Invalid Phone",
                             "Phone number must be 10 digits!",
                             "warning")
                return
            
            email = vars["parent_email"].get().strip()
            # Auto append gmail domain
            if "@gmail.com" not in email:
                email = email + "@gmail.com"
                vars["parent_email"].set(email)
                data["parent_email"] = email
   
            try:
                import requests
                res = requests.post("http://127.0.0.1:8000/admin/admissions/", json=data)

                if res.status_code == 200:
                    self.show_popup("Success", "Admission Submitted Successfully!", "info")
                    self.change_screen("Admission Submitted Successfully!",
                    add_callback=self.load_create_admission_screen
                )

                else:
                    msg = res.json().get("detail", "Something went wrong!")
                    self.show_popup("Submission Failed", msg, "error")
            except requests.exceptions.ConnectionError:
                self.show_popup("Server Error", "Server not reachable. Please try later.", "error")
    

    # ============================================================
    # ====== Button to view all admissions ======
    def load_view_all_admissions_screen(self):
        self.clear_content()

    # -------- TITLE --------
        tk.Label(
        self.content,
        text="All Admissions",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
    ).pack(pady=20)

    # -------- BACK BUTTON --------
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)
        self.create_back_button(back_frame, self.load_dashboard, None)

    # -------- TABLE FRAME --------
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        cols = (
        "admission_id", "full_name", "date_of_birth", "gender", "address",
        "father_name", "mother_name", "parent_phone", "parent_email",
        "class_id", "previous_school"
    )

    # ====================================================
    #        FILTER BAR (Dropdown + Entry + Black Buttons)
    # ====================================================
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=10)

    # Sort by label
        tk.Label(
        filter_frame,
        text="Sort By:",
        font=("Arial", 12, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
    ).grid(row=0, column=0, padx=5)

    # Dropdown
        filter_var = tk.StringVar()
        filter_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=list(cols),
        state="readonly",
        width=20
    )
        filter_dropdown.grid(row=0, column=1, padx=10)
        
        # Value Entry
        filter_var_value = tk.StringVar()

        filter_value = tk.Entry(
    filter_frame, 
    textvariable=filter_var_value,
    font=("Arial", 12), 
    width=25
)
        filter_value.grid(row=0, column=2, padx=10) 

    # ---- Button Style ----
        def style_button(btn):
            btn.config(
            bg="#000000",
            fg="white",
            padx=15,
            pady=5,
            width=10,
            relief="raised",
            cursor="hand2",
            font=("Arial", 12, "bold")
        )
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

    # LOAD button
        load_btn = tk.Label(filter_frame, text="Load")
        style_button(load_btn)
        load_btn.grid(row=0, column=3, padx=10)

    # LOAD ALL button
        load_all_btn = tk.Label(filter_frame, text="Load All")
        style_button(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

    # ======================================================
    #                 TABLE + SCROLLBARS
    # ======================================================
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        self.admission_tree = ttk.Treeview(
        table_frame,
        columns=cols,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
    )
        self.admission_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.admission_tree.yview)
        x_scroll.config(command=self.admission_tree.xview)

    # Table headings
        for col in cols:
            self.admission_tree.heading(col, text=col.replace("_", " ").title())
            self.admission_tree.column(col, width=180, anchor="center")

    # ======================================================
    #                     BACKEND FETCH
    # ======================================================
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admin/admissions/")
            self.all_admissions = res.json() if res.status_code == 200 else []
            self.column_values = {
    "admission_id": [str(r["admission_id"]) for r in self.all_admissions],
    "full_name": [r["full_name"] for r in self.all_admissions],
    "date_of_birth": [r["date_of_birth"] for r in self.all_admissions],
    "gender": [r["gender"] for r in self.all_admissions],
    "address": [r["address"] for r in self.all_admissions],
    "father_name": [r["father_name"] for r in self.all_admissions],
    "mother_name": [r["mother_name"] for r in self.all_admissions],
    "parent_phone": [r["parent_phone"] for r in self.all_admissions],
    "parent_email": [r["parent_email"] for r in self.all_admissions],
    "class_id": [str(r["class_id"]) for r in self.all_admissions],
    "previous_school": [r["previous_school"] for r in self.all_admissions],
    }

        except:
            self.all_admissions = []

    # ----------- UPDATE TABLE FUNCTION -----------
        def update_table(data):
            for row in self.admission_tree.get_children():
                self.admission_tree.delete(row)

            for row in data:
                self.admission_tree.insert(
                "", "end",
                values=(
                    row["admission_id"],
                    row["full_name"],
                    row["date_of_birth"],
                    row["gender"],
                    row["address"],
                    row["father_name"],
                    row["mother_name"],
                    row["parent_phone"],
                    row["parent_email"],
                    row["class_id"],
                    row["previous_school"]
                )
            )

    # ----------- FILTER FUNCTION -----------
        def load_filtered():
            col = filter_var.get().strip()
            val = filter_value.get().strip().lower()

            if not col or not val:
                return
            
            valid_list = self.column_values.get(col, [])
            valid_lower = [str(v).lower() for v in valid_list]

            if val not in valid_lower:
                self.show_popup(
            "Invalid Search Value",
            f"'{val}' not found in column '{col}'.",
            "warning"
        )
                filter_var_value.set("")  # clear invalid
                return
            filtered = [
            r for r in self.all_admissions
            if str(r[col]).lower() == val.lower()
        ]
            update_table(filtered)

        def load_all():
            update_table(self.all_admissions)

        load_btn.bind("<Button-1>", lambda e: load_filtered())
        load_all_btn.bind("<Button-1>", lambda e: load_all())

    # INITIAL LOAD
        update_table(self.all_admissions)


    # ==========================================================
    # ===== Button to view admission by id =====
    def load_view_admission_by_id_screen(self):
        self.clear_content()

        # Title
        tk.Label(
        self.content,
        text="View Admission by ID",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=25)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=20)

        # --------- ID Input ---------
        tk.Label(form, text="Admission ID:", font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=0, padx=10, pady=10)
        adm_id_var = tk.StringVar()
        adm_id_entry = tk.Entry(form, textvariable=adm_id_var, font=("Arial", 14), width=25)
        adm_id_entry.grid(row=0, column=1, padx=10, pady=10)

        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

        # Back Button from global function
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,    
        form_frame=form                          
        )
        # --------- View Button (dark mode after typing) ---------
        view_btn = tk.Label(
        form,
        text="View",
        font=("Arial", 12, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=15, pady=5,
        width=12,
        relief="ridge",
        cursor="arrow"
        )
        view_btn.grid(row=0, column=2, padx=10)

        # Enable dark mode after typing
        def validate_btn(*args):
            if adm_id_var.get().strip():
                view_btn.config(bg="#000000", fg="white", cursor="hand2")
                view_btn.bind("<Enter>", lambda e: view_btn.config(bg="#222222"))
                view_btn.bind("<Leave>", lambda e: view_btn.config(bg="#000000"))
                view_btn.bind("<Button-1>", lambda e: fetch_admission())
            else:
                view_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                view_btn.unbind("<Enter>")
                view_btn.unbind("<Leave>")
                view_btn.unbind("<Button-1>")

        adm_id_var.trace_add("write", validate_btn)

        # --------- Output Fields ---------
        output_frame = tk.Frame(self.content, bg="#ECF0F1")
        output_frame.pack(pady=10)

        labels = ["full_name", "date_of_birth", "gender", "address", "father_name", "mother_name", "parent_phone", "parent_email", "class_id", "previous_school"]

        vars_dict = {}

        for i, label in enumerate(labels):
            tk.Label(output_frame, text=f"{label}:", font=("Arial", 14), bg="#ECF0F1").grid(row=i, column=0, padx=10, pady=6)
            var = tk.StringVar()
            entry = tk.Entry(
                output_frame,
                textvariable=var,
                font=("Arial", 14),
                width=30,
                state="disabled",
                disabledbackground="#F2F3F4",   # Light background (same as your normal)
                disabledforeground="black"      
            ) 

            entry.grid(row=i, column=1, padx=10, pady=6)
            vars_dict[label] = var

        # ---------- FETCH FUNCTION ----------
        def fetch_admission():
            adm_id = str(adm_id_var).get().strip()

            if not adm_id.isdigit() or int(adm_id) <= 0:
                self.show_popup("Wrong","Admission ID should be a Number!", "warning")
                return

            import requests
            try:
                res = requests.get(f"http://127.0.0.1:8000/admin/admissions/{adm_id}")

                if res.status_code != 200:
                    self.show_popup("Failed","Record for this Admission ID is Not Found!", "info")
                    for k in vars_dict.values():
                        k.set("")
                    return

                data = res.json()

                vars_dict["full_name"].set(data["full_name"])
                vars_dict["gender"].set(data["gender"])
                vars_dict["date_of_birth"].set(data["date_of_birth"])
                vars_dict["class_id"].set(data["class_id"])
                vars_dict["address"].set(data["address"])
                vars_dict["parent_phone"].set(data["parent_phone"])
                vars_dict["parent_email"].set(data["parent_email"])
                vars_dict["father_name"].set(data["father_name"])
                vars_dict["mother_name"].set(data["mother_name"])
                vars_dict["previous_school"].set(data["previous_school"])

            except:
                self.show_popup("Error","Error in Fetching Details from Server", "error")

    # ==========================================================
    # ===== Button to approve admissions =====
    def load_approve_admission_screen(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="Approve Admission",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=25)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # ---------- ADMISSION ID INPUT ----------
        tk.Label(form, text="Admission ID:", font=("Arial", 14), bg="#ECF0F1").grid(
            row=0, column=0, padx=10, pady=10
        )
        adm_id_var = tk.StringVar()
        adm_id_entry = tk.Entry(form, textvariable=adm_id_var, font=("Arial", 14), width=25)
        adm_id_entry.grid(row=0, column=1, padx=10, pady=10)

        # ---------- LOAD BUTTON ----------
        load_btn = tk.Label(
        form,
        text="Load",
        font=("Arial", 12, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=15, pady=5,
        width=12,
        relief="ridge",
        cursor="arrow"
        )
        load_btn.grid(row=0, column=2, padx=10)

        # DARK MODE LOGIC FOR LOAD BUTTON
        def validate_load(*args):
            if adm_id_var.get().strip():
                load_btn.config(bg="#000000", fg="white", cursor="hand2")
                load_btn.bind("<Enter>", lambda e: load_btn.config(bg="#222222"))
                load_btn.bind("<Leave>", lambda e: load_btn.config(bg="#000000"))
                load_btn.bind("<Button-1>", lambda e: load_admission())
            else:
                load_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                load_btn.unbind("<Enter>")
                load_btn.unbind("<Leave>")
                load_btn.unbind("<Button-1>")

        adm_id_var.trace_add("write", validate_load)

        # ---------- OUTPUT PANEL (READ-ONLY DETAILS) ----------
        output_frame = tk.Frame(self.content, bg="#ECF0F1")
        output_frame.pack(pady=20)

        fields = ["full_name", "date_of_birth", "gender", "address", "father_name", "mother_name", "parent_phone", "parent_email", "class_id", "previous_school"]
        vars_dict = {}

        for i, label in enumerate(fields):
            tk.Label(output_frame, text=f"{label}:", font=("Arial", 14), bg="#ECF0F1").grid(
            row=i, column=0, padx=10, pady=6, sticky="w"
            )
            var = tk.StringVar()
            entry = tk.Entry(
                output_frame,
                textvariable=var,
                font=("Arial", 14),
                width=30,
                state="disabled",
                disabledbackground="#F2F3F4",
                disabledforeground="black"
            )
            entry.grid(row=i, column=1, padx=10, pady=6)
            vars_dict[label] = var

        btn_row = tk.Frame(self.content, bg="#ECF0F1")
        btn_row.pack(pady=30, anchor="center")

        # Back Button from global function
        self.create_back_button(
        parent=btn_row,
        go_back_callback=self.load_dashboard,    
        form_frame=form                          
        )

        self.content.update_idletasks()

        # ---------- APPROVE BUTTON ----------
        approve_btn = tk.Label(
        self.content,
        text="Approve Admission",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=10,
        width=18,
        relief="ridge",
        cursor="arrow"
        )
        approve_btn.pack(pady=20)

        # ----- APPROVE BUTTON DISABLED UNTIL DATA LOADED -----
        def enable_approve():
            approve_btn.config(bg="#000000", fg="white", cursor="hand2")
            approve_btn.bind("<Enter>", lambda e: approve_btn.config(bg="#222222"))
            approve_btn.bind("<Leave>", lambda e: approve_btn.config(bg="#000000"))
            approve_btn.bind("<Button-1>", lambda e: approve_admission())

        def disable_approve():
            approve_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            approve_btn.unbind("<Enter>")
            approve_btn.unbind("<Leave>")
            approve_btn.unbind("<Button-1>")

            disable_approve()

        # ---------- LOAD ADMISSION DETAILS ----------
        def load_admission():
            adm_id = adm_id_var.get().strip()

            if not adm_id.isdigit() or int(adm_id) <= 0:
                self.show_popup("Failed", "Admission ID should be a Number!", "warning")
                return
            
            import requests

            try:
                res = requests.get(f"http://127.0.0.1:8000/admin/admissions/{adm_id}")

                if res.status_code != 200:
                    self.show_popup("Failed", "No Record Found for this Admission ID", "info")
                    disable_approve()
                    for v in vars_dict.values():
                        v.set("")
                    return

                data = res.json()

                vars_dict["full_name"].set(data["full_name"])
                vars_dict["gender"].set(data["gender"])
                vars_dict["date_of_birth"].set(data["date_of_birth"])
                vars_dict["class_id"].set(data["class_id"])
                vars_dict["address"].set(data["address"])
                vars_dict["parent_phone"].set(data["parent_phone"])
                vars_dict["parent_email"].set(data["parent_email"])
                vars_dict["father_name"].set(data["father_name"])
                vars_dict["mother_name"].set(data["mother_name"])
                vars_dict["previous_school"].set(data["previous_school"])

                enable_approve()

            except:
                self.show_popup("Error", "Error in Fetching Data from Server", "error")

        # ---------- APPROVE ADMISSION FUNCTION ----------
        def approve_admission():
            adm_id = adm_id_var.get().strip()
            import requests

            try:
                res = requests.post(f"http://127.0.0.1:8000/admin/admissions/approve/{adm_id}")

                if res.status_code == 200:
                    self.show_popup("Admission Approved Successfully, Student data added in Database successfully!", "success")
                    self.change_screen(
                        f"Admission Approved Successfully!\nStudent ID: {res.json()['student_id']}",
                        add_callback=self.load_approve_admission_screen
                    )
                else:
                    self.show_popup("Failed", "Admission Not Approved", res.text)

            except:
                self.show_popup("Error", "Error approving admission", "error")

    
    # ==============================================================================
    # ======== TRANSFER CERTIFICATES =========
    # ======== Button to Issue Tc ========
    def load_issue_tc_screen(self):
        self.clear_content()

        tk.Label(
        self.content, text="Issue Transfer Certificate",
        font=("Arial", 26, "bold"), bg="#ECF0F1", fg="#2C3E50"
        ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=20)

        # ------- FIELDS -------
        fields = [
        ("Student ID", "student_id"),
        ("Reason", "reason"),
        ("Issue Date (YYYY-MM-DD)", "issue_date")
        ]

        vars = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(form, text=f"{label}:", font=("Arial", 14), bg="#ECF0F1")\
            .grid(row=i, column=0, padx=10, pady=8)

            vars[key] = tk.StringVar()

            # calendar for date
            if key == "issue_date":
                entry = tk.Entry(form, textvariable=vars[key], font=("Arial", 14), width=28)
                entry.grid(row=i, column=1, padx=10)

                cal_btn = tk.Button(
                form,
                text="Calendar",
                font=("Arial", 12),
                bg="white",
                relief="flat",
                cursor="arrow",
                command=lambda v=vars[key], b=entry: self.open_calendar_popup(b, v)
                )
                cal_btn.grid(row=i, column=2, padx=5)
            else:
                entry = tk.Entry(form, textvariable=vars[key], font=("Arial", 14), width=30)
                entry.grid(row=i, column=1, padx=10, pady=6)
        
        btn_frame = tk.Frame(self.content, bg = "#ECF0F1")
        btn_frame.pack(pady=25)

        # ------- Back Button --------
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,   
        form_frame=form                         
        )
    
        self.content.update_idletasks()

        # -------- ISSUE TC BUTTON --------
        # Submit button inside FORM (grid-based)
        submit = tk.Label(
            form,
            text="Issue TC",
            font=("Arial", 16, "bold"),
            bg="#D5D8DC",
            fg="#AEB6BF",
            padx=20,
            pady=10,
            width=20,
            cursor="arrow",
            relief="ridge"
        )
        submit.grid(row=len(fields), column=0, columnspan=3, pady=20)

        # --------- VALIDATION ----------
        def validate(*args):
            if all(vars[k].get().strip() for k in vars):
                submit.config(bg="#000000", fg="white", cursor="hand2")
                submit.bind("<Enter>", lambda e: submit.config(bg="#222222"))
                submit.bind("<Leave>", lambda e: submit.config(bg="#000000"))
                submit.bind("<Button-1>", lambda e: issue_tc())
            else:
                submit.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                submit.unbind("<Enter>")
                submit.unbind("<Leave>")
                submit.unbind("<Button-1>")

        for v in vars.values():
            v.trace_add("write", validate)

        # -------- SUBMITTING TO BACKEND ---------
        def issue_tc():
            sid = vars["student_id"].get().strip()

            import re
            date_str = vars["issue_date"].get().strip()
            if not re.match(r"\d{4}-\d{2}-\d{2}", date_str):
                self.show_popup("Invalid Date", "Date must be YYYY-MM-DD!", "warning")
                return

            payload = {
        "student_id": int(sid),
        "reason": vars["reason"].get().strip(),
        "remarks": None,
        "issue_date": date_str
    }

            import requests
            res = requests.post("http://127.0.0.1:8000/admin/tc/issue", json=payload)

            if res.status_code == 200:
                self.show_popup("Success", "TC Issued Successfully!", "info")
                self.change_screen("TC Issued!", add_callback=self.load_issue_tc_screen)
            else:
                self.show_popup("Error", f"Failed to Issue TC! {res.text}", "error")


    # ===========================================================
    # ======= Button View all Issued TCs =========
    def load_view_all_tc_screen(self):
        self.clear_content()
 
        # ----- TITLE -----
        tk.Label(
        self.content,
        text="All Transfer Certificates",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # -------- BACK BUTTON --------
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)
        self.create_back_button(back_frame, self.load_dashboard, None)

        # -------- TABLE FRAME --------
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # ---- TC TABLE COLUMNS ----
        cols = (
        "tc_id", "student_id", "issue_date",
        "reason", "remarks", "status"
        )

        # ====== FILTER BAR (Dropdown + Entry + Black Buttons) ======
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=10)

        tk.Label(
        filter_frame,
        text="Sort By:",
        font=("Arial", 12, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).grid(row=0, column=0, padx=5)

        filter_var = tk.StringVar()
        filter_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=list(cols),
        state="readonly",
        width=20
        )
        filter_dropdown.grid(row=0, column=1, padx=10)

        filter_val_var = tk.StringVar()
        filter_val = tk.Entry(filter_frame, textvariable=filter_val_var,
                            font=("Arial", 12), width=25)
        filter_val.grid(row=0, column=2, padx=10)

        # ---- Button styling ----
        def style_button(btn):
            btn.config(
            bg="#000000",
            fg="white",
            padx=15,
            pady=5,
            width=10,
            relief="raised",
            cursor="arrow",
            font=("Arial", 12, "bold")
            )
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))
        
        # ---- Load Button -----
        load_btn = tk.Label(filter_frame, text="Load")
        style_button(load_btn)
        load_btn.grid(row=0, column=3, padx=10)
        
        # ---- Load all Button -----
        load_all_btn = tk.Label(filter_frame, text="Load All")
        style_button(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

        # ------ TABLE + SCROLLBARS ------
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        self.tc_tree = ttk.Treeview(
        table_frame,
        columns=cols,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
        )
        self.tc_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.tc_tree.yview)
        x_scroll.config(command=self.tc_tree.xview)

        for col in cols:
            self.tc_tree.heading(col, text=col.replace("_", " ").title())
            self.tc_tree.column(col, width=180, anchor="center")

        # ----- BACKEND FETCH ------
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admin/tc/all")
            self.all_tc = res.json() if res.status_code == 200 else []

            # ------- For Validations -------
            self.tc_column_values = {
            "tc_id": [str(r["tc_id"]) for r in self.all_tc],
            "student_id": [str(r["student_id"]) for r in self.all_tc],
            "issue_date": [r["issue_date"] for r in self.all_tc],
            "reason": [r["reason"] for r in self.all_tc],
            "remarks": [r["remarks"] for r in self.all_tc],
            "status": [1 if r["status"] else 0 for r in self.all_tc]
            }

        except:
            self.all_tc = []

        # ------- UPDATE TABLE FUNCTION -------
        def update_table(data):
            for row in self.tc_tree.get_children():
                self.tc_tree.delete(row)

            for row in data:
                self.tc_tree.insert(
                "", "end",
                values=(
                    row["tc_id"],
                    row["student_id"],
                    row["issue_date"],
                    row["reason"],
                    row["remarks"], 
                    1 if row["status"] else 0
                    )
                )

        # ------- FILTER FUNCTION -------
        def load_filtered():
            col = filter_var.get().strip()
            val = filter_val.get().strip().lower()

            if not col or not val:
                return

            valid_list = self.tc_column_values.get(col, [])
            valid_lower = [str(v).lower() for v in valid_list]

            if val not in valid_lower:
                self.show_popup(
                "Invalid Search Value",
                f"'{val}' not found in column '{col}'.",
                "warning"
                )
                filter_val_var.set("")
                return

            filtered = [
            r for r in self.all_tc
            if str(r[col]).lower() == val.lower()
            ]
            update_table(filtered)

        def load_all():
            update_table(self.all_tc)

        load_btn.bind("<Button-1>", lambda e: load_filtered())
        load_all_btn.bind("<Button-1>", lambda e: load_all())

        # INITIAL LOAD
        update_table(self.all_tc)


    # ==================================================================
    # ====== Button to Approve Tc ======
    def load_approve_tc_screen(self):
        self.clear_content()

        # ----- TITLE -----
        tk.Label(
        self.content,
        text="Approve Transfer Certificate",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=25)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # ---------- TC ID INPUT ----------
        tk.Label(form, text="TC ID:", font=("Arial", 14), bg="#ECF0F1").grid(
        row=0, column=0, padx=10, pady=10
        )

        tc_id_var = tk.StringVar()
        tc_id_entry = tk.Entry(form, textvariable=tc_id_var, font=("Arial", 14), width=25)
        tc_id_entry.grid(row=0, column=1, padx=10, pady=10)

        # ---------- LOAD BUTTON ----------
        load_btn = tk.Label(
        form,
        text="Load",
        font=("Arial", 12, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=15, pady=5,
        width=12,
        relief="ridge",
        cursor="arrow"
        )
        load_btn.grid(row=0, column=2, padx=10)

        # Enable/Disable LOAD Button
        def validate_load(*args):
            if tc_id_var.get().strip():
                load_btn.config(bg="#000000", fg="white", cursor="hand2")
                load_btn.bind("<Enter>", lambda e: load_btn.config(bg="#222222"))
                load_btn.bind("<Leave>", lambda e: load_btn.config(bg="#000000"))
                load_btn.bind("<Button-1>", lambda e: load_tc())
            else:
                load_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                load_btn.unbind("<Enter>")
                load_btn.unbind("<Leave>")
                load_btn.unbind("<Button-1>")

        tc_id_var.trace_add("write", validate_load)

        # ---------- OUTPUT PANEL ----------
        output_frame = tk.Frame(self.content, bg="#ECF0F1")
        output_frame.pack(pady=20)

        fields = ["student_id", "issue_date", "reason", "status"]
        vars_dict = {}

        for i, label in enumerate(fields):
            tk.Label(
            output_frame,
            text=f"{label.replace('_',' ').title()}:",
            font=("Arial", 14),
            bg="#ECF0F1"
            ).grid(row=i, column=0, padx=10, pady=6, sticky="w")

            var = tk.StringVar()
            entry = tk.Entry(
            output_frame,
            textvariable=var,
            font=("Arial", 14),
            width=30,
            state="disabled",
            disabledbackground="#F2F3F4",
            disabledforeground="black"
            )
            entry.grid(row=i, column=1, padx=10, pady=6)
            vars_dict[label] = var

        # ---------- BUTTONS ROW ----------
        btn_row = tk.Frame(self.content, bg="#ECF0F1")
        btn_row.pack(pady=30)

        self.create_back_button(
        parent=btn_row,
        go_back_callback=self.load_dashboard,
        form_frame=form
        )

        # ---------- APPROVE BUTTON ----------
        approve_btn = tk.Label(
        self.content,
        text="Approve TC",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=10,
        width=18,
        relief="ridge",
        cursor="arrow"
        )
        approve_btn.pack(pady=20)

        def enable_approve():
            approve_btn.config(bg="#000000", fg="white", cursor="hand2")
            approve_btn.bind("<Enter>", lambda e: approve_btn.config(bg="#222222"))
            approve_btn.bind("<Leave>", lambda e: approve_btn.config(bg="#000000"))
            approve_btn.bind("<Button-1>", lambda e: approve_tc())

        def disable_approve():
            approve_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            approve_btn.unbind("<Enter>")
            approve_btn.unbind("<Leave>")
            approve_btn.unbind("<Button-1>")

        disable_approve()

        # ---------- LOAD TC DETAILS ----------
        def load_tc():
            tc_id = tc_id_var.get().strip()

            if not tc_id.isdigit() or int(tc_id) <= 0:
                self.show_popup("Invalid TC ID", "TC ID must be a positive number!", "warning")
                return

            import requests
            try:
                res = requests.get(f"http://127.0.0.1:8000/admin/tc/{tc_id}")

                if res.status_code != 200:
                    self.show_popup("Not Found", "No record found for this TC ID!", "info")
                    disable_approve()
                    for v in vars_dict.values():
                        v.set("")
                    return

                data = res.json()

                vars_dict["student_id"].set(data["student_id"])
                vars_dict["issue_date"].set(data["issue_date"])
                vars_dict["reason"].set(data["reason"])
                vars_dict["status"].set("1" if data["status"] else "0")

                enable_approve()

            except:
                self.show_popup("Error", "Server not reachable!", "error")

        # ---------- APPROVE TC ----------
        def approve_tc():
            tc_id = tc_id_var.get().strip()
            import requests

            try:
                res = requests.post(f"http://127.0.0.1:8000/admin/tc/approve/{tc_id}")

                if res.status_code == 200:
                    self.show_popup("Success", "TC Approved Successfully!", "info")
                    self.change_screen(
                    f"TC Approved Successfully!",
                    add_callback=self.load_approve_tc_screen
                )
                else:
                    self.show_popup("Failed", "TC approval failed!", "error")

            except:
                self.show_popup("Error", "Unable to approve TC!", "error")


    #===================================================================
    #-------Timetable Screens------
    def load_view_timetable(self):
        self.clear_content()

        tk.Label(self.content, text="View Timetable", font=("Arial", 26, "bold"), bg="#ECF0F1").pack(pady=20)

        # BACK BUTTON 
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)

        self.create_back_button(
            parent=back_frame,
            go_back_callback=self.load_dashboard,
            form_frame=None
        )

        # ---- Fetch dropdown data ----
        classes = fetch_classes()
        teachers = fetch_teachers()
        subjects = fetch_subjects()

        # CLASS LIST FOR DISPLAY
        class_list = ["None"] + [f"{c['class_name']} {c['section']}" for c in classes]

        # MAP display → ID
        class_map = {
            f"{c['class_name']} {c['section']}": c['class_id']
            for c in classes
        }

        # TEACHER LIST FOR DISPLAY
        teacher_list = ["None"] + [f"{t['teacher_id']} - {t['full_name']}" for t in teachers]

        # MAP display → ID
        teacher_map = {
            f"{t['teacher_id']} - {t['full_name']}": t['teacher_id']
            for t in teachers
        }

        # SUBJECT LIST
        subject_list = ["None"] + [s["subject_name"] for s in subjects]


        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=10)

        # ========== CLASS FILTER ==========
        tk.Label(filter_frame, text="Class:", font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=0, padx=10)
        class_var = tk.StringVar()
        class_dd = ttk.Combobox(
            filter_frame,
            textvariable=class_var,
            values=class_list,
            state="readonly",
            width=20
        )
        class_dd.grid(row=0, column=1)
        class_dd.current(0)          # default "None"
        class_var.set("None")

        # ========== TEACHER FILTER ==========
        tk.Label(filter_frame, text="Teacher:", font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=2, padx=10)
        teacher_var = tk.StringVar()
        teacher_dd = ttk.Combobox(
            filter_frame,
            textvariable=teacher_var,
            values=teacher_list,
            state="readonly",
            width=22
        )
        teacher_dd.grid(row=0, column=3)
        teacher_dd.current(0)
        teacher_var.set("None")

        # ========== SUBJECT FILTER ==========
        tk.Label(filter_frame, text="Subject:", font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=4, padx=10)
        subject_var = tk.StringVar(value="None")

        subject_dd = ttk.Combobox(
            filter_frame,
            textvariable=subject_var,
            values=subject_list,
            state="readonly",
            width=18
        )
        subject_dd.grid(row=0, column=5)
        subject_dd.current(0)
        subject_var.set("None")

        # ========== RESET FILTER BUTTON ==========
        reset_btn = tk.Button(
            filter_frame,
            text="Reset",
            font=("Arial", 12, "bold"),
            bg="#7F8C8D",
            fg="white",
            command=lambda: reset_filters()
        )
        reset_btn.grid(row=0, column=6, padx=10)

        # TABLE
        columns = ("Day", "Class", "Subject", "Teacher", "Start", "End")
        table = self.create_scrollable_table(self.content, columns, [])

        # --- RIGHT CLICK MENU ---
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Edit", command=lambda: edit_selected())
        menu.add_command(label="Delete", command=lambda: delete_selected())

        def show_menu(event):
            try:
                item_id = table.identify_row(event.y)
                if item_id:
                    table.selection_set(item_id)
                    menu.post(event.x_root, event.y_root)
            except:
                pass

        table.bind("<Button-3>", show_menu)   # Right-click

        def edit_selected():
            selected = table.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a record to edit.")
                return

            item_id = table.item(selected[0])["text"]   # this is timetable_id
            self.load_edit_timetable(item_id)

        def delete_selected():
            selected = table.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a record to delete.")
                return

            row_data = table.item(selected[0])["values"]
            class_name = row_data[1]
            day = row_data[0]
            subject = row_data[2]

            if not messagebox.askyesno("Confirm Delete", f"Delete timetable entry:\n{class_name}, {day}, {subject}?"):
                return

            timetable_id = table.item(selected[0])["text"]

            res = requests.delete(f"http://127.0.0.1:8000/admin/timetable/{timetable_id}")

            if res.status_code == 204:
                messagebox.showinfo("Success", "Record deleted successfully.")
                load_filtered_timetable()
            else:
                messagebox.showerror("Error", "Unable to delete record.")

        # ========= FILTER FUNCTION =========
        def load_filtered_timetable():
            payload = {
                "class_id": class_map.get(class_var.get()) if class_var.get() not in [None, "", "None"] else None,
                "teacher_id": teacher_map.get(teacher_var.get()) if teacher_var.get() not in [None, "", "None"] else None,
                "subject": subject_var.get() if subject_var.get() not in [None, "", "None"] else None
            }

            print("FILTER PAYLOAD:", payload)

            res = requests.post("http://127.0.0.1:8000/admin/timetable/filter", json=payload)
            data = res.json() if res.status_code == 200 else []

            # Clear old rows
            for r in table.get_children():
                table.delete(r)

            # Insert rows
            for item in data:
                table.insert("", "end", text=item["timetable_id"], values=(
                    item["day"],
                    item["class_name"],
                    item["subject"],
                    item["teacher_name"],
                    item["start_time"],
                    item["end_time"]
                ))

        # initial load (no filters)
        load_filtered_timetable()

        # ========= RESET FUNCTION =========
        def reset_filters():
            class_var.set("None")
            teacher_var.set("None")
            subject_var.set("None")
            load_filtered_timetable()

        # ========= NEW: AUTO-APPLY FILTER ON DROPDOWN CHANGE =========
        class_dd.bind("<<ComboboxSelected>>", lambda e: load_filtered_timetable())
        teacher_dd.bind("<<ComboboxSelected>>", lambda e: load_filtered_timetable())
        subject_dd.bind("<<ComboboxSelected>>", lambda e: load_filtered_timetable())


    def load_add_timetable(self):
        self.clear_content()

        tk.Label(
            self.content,
            text="Add Timetable",
            font=("Arial", 26, "bold"),
            bg="#ECF0F1"
        ).pack(pady=20)

        # Fetch dropdown data
        classes = fetch_classes()
        teachers = fetch_teachers()
        subjects = fetch_subjects()

        # Prepare dropdown lists
        class_list = [f"{c['class_name']} {c['section']}" for c in classes]
        class_map = {f"{c['class_name']} {c['section']}": c['class_id'] for c in classes}

        teacher_list = [t["full_name"] for t in teachers]
        teacher_map = {t["full_name"]: t["teacher_id"] for t in teachers}

        subject_list = subjects

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=20)

        # --- CLASS ---
        tk.Label(form, text="Class:", font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=0, sticky="w", pady=5)
        class_var = tk.StringVar()
        class_dd = ttk.Combobox(form, textvariable=class_var, values=class_list, state="readonly", width=25)
        class_dd.grid(row=0, column=1, pady=5)

        # --- SUBJECT ---
        tk.Label(form, text="Subject:", font=("Arial", 14), bg="#ECF0F1").grid(row=1, column=0, sticky="w", pady=5)
        subject_var = tk.StringVar()
        subject_dd = ttk.Combobox(form, textvariable=subject_var, values=subject_list, state="readonly", width=25)
        subject_dd.grid(row=1, column=1, pady=5)

        # --- TEACHER ---
        tk.Label(form, text="Teacher:", font=("Arial", 14), bg="#ECF0F1").grid(row=2, column=0, sticky="w", pady=5)
        teacher_var = tk.StringVar()
        teacher_dd = ttk.Combobox(form, textvariable=teacher_var, values=teacher_list, state="readonly", width=25)
        teacher_dd.grid(row=2, column=1, pady=5)

        # --- DAY ---
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        tk.Label(form, text="Day:", font=("Arial", 14), bg="#ECF0F1").grid(row=3, column=0, sticky="w", pady=5)
        day_var = tk.StringVar()
        day_dd = ttk.Combobox(form, textvariable=day_var, values=days, state="readonly", width=25)
        day_dd.grid(row=3, column=1, pady=5)

        # --- START TIME ---
        tk.Label(form, text="Start Time (HH:MM):", font=("Arial", 14), bg="#ECF0F1").grid(row=4, column=0, sticky="w", pady=5)
        start_entry = tk.Entry(form, font=("Arial", 14), width=23)
        start_entry.grid(row=4, column=1, pady=5)

        # --- END TIME ---
        tk.Label(form, text="End Time (HH:MM):", font=("Arial", 14), bg="#ECF0F1").grid(row=5, column=0, sticky="w", pady=5)
        end_entry = tk.Entry(form, font=("Arial", 14), width=23)
        end_entry.grid(row=5, column=1, pady=5)

        # --- ROOM NO ---
        tk.Label(form, text="Room No:", font=("Arial", 14), bg="#ECF0F1").grid(row=6, column=0, sticky="w", pady=5)
        room_entry = tk.Entry(form, font=("Arial", 14), width=23)
        room_entry.grid(row=6, column=1, pady=5)

        # --- SUBMIT BUTTON ---
        def save_timetable():
            payload = {
                "class_id": class_map.get(class_var.get()),
                "teacher_id": teacher_map.get(teacher_var.get()),
                "subject": subject_var.get(),
                "day": day_var.get(),
                "start_time": start_entry.get(),
                "end_time": end_entry.get(),
                "room_no": room_entry.get()
            }

            res = requests.post("http://127.0.0.1:8000/admin/timetable/add", json=payload)

            if res.status_code == 201:
                messagebox.showinfo("Success", "Timetable added successfully!")
            else:
                messagebox.showerror("Error", "Failed to add timetable.")

        tk.Button(
            form,
            text="Save Timetable",
            font=("Arial", 14, "bold"),
            bg="black",
            fg="white",
            command=save_timetable
        ).grid(row=7, column=0, columnspan=2, pady=20)


    def load_edit_timetable(self, timetable_id):
        self.clear_content()

        # ---- TITLE ----
        tk.Label(self.content, text="Edit Timetable", font=("Arial", 26, "bold"), bg="#ECF0F1").pack(pady=20)

        # ---- FETCH DATA ----
        res = requests.get(f"http://127.0.0.1:8000/admin/timetable/{timetable_id}")
        if res.status_code != 200:
            messagebox.showerror("Error", "Could not load timetable data.")
            return

        data = res.json()

        # Fetch dropdown values
        classes = fetch_classes()
        teachers = fetch_teachers()
        subjects = fetch_subjects()

        # Build dropdown lists
        class_list = [f"{c['class_name']} {c['section']}" for c in classes]
        class_map = {f"{c['class_name']} {c['section']}": c['class_id'] for c in classes}
        reverse_class_map = {v: k for k, v in class_map.items()}

        teacher_list = [f"{t['teacher_id']} - {t['full_name']}" for t in teachers]
        teacher_map = {f"{t['teacher_id']} - {t['full_name']}": t['teacher_id'] for t in teachers}
        reverse_teacher_map = {v: k for k, v in teacher_map.items()}

        subject_list = subjects

        # ---- FORM FRAME ----
        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=20)

        # CLASS
        tk.Label(form, text="Class:", font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=0, pady=10, padx=10, sticky="w")
        class_var = tk.StringVar()
        class_dd = ttk.Combobox(form, textvariable=class_var, values=class_list, state="readonly", width=25)
        class_dd.grid(row=0, column=1)
        class_dd.set(reverse_class_map[data["class_id"]])

        # TEACHER
        tk.Label(form, text="Teacher:", font=("Arial", 14), bg="#ECF0F1").grid(row=1, column=0, pady=10, padx=10, sticky="w")
        teacher_var = tk.StringVar()
        teacher_dd = ttk.Combobox(form, textvariable=teacher_var, values=teacher_list, state="readonly", width=25)
        teacher_dd.grid(row=1, column=1)
        teacher_dd.set(reverse_teacher_map.get(data["teacher_id"], teacher_list[0]))

        # SUBJECT
        tk.Label(form, text="Subject:", font=("Arial", 14), bg="#ECF0F1").grid(row=2, column=0, pady=10, padx=10, sticky="w")
        subject_var = tk.StringVar()
        subject_dd = ttk.Combobox(form, textvariable=subject_var, values=subject_list, state="readonly", width=25)
        subject_dd.grid(row=2, column=1)
        subject_dd.set(data["subject"])

        # DAY
        tk.Label(form, text="Day:", font=("Arial", 14), bg="#ECF0F1").grid(row=3, column=0, pady=10, padx=10, sticky="w")
        day_var = tk.StringVar()
        day_dd = ttk.Combobox(form, textvariable=day_var, values=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"], state="readonly", width=25)
        day_dd.grid(row=3, column=1)
        day_dd.set(data["day"])

        # START TIME
        tk.Label(form, text="Start Time (HH:MM):", font=("Arial", 14), bg="#ECF0F1").grid(row=4, column=0, pady=10, padx=10, sticky="w")
        start_var = tk.Entry(form, width=28)
        start_var.grid(row=4, column=1)
        start_var.insert(0, data["start_time"])

        # END TIME
        tk.Label(form, text="End Time (HH:MM):", font=("Arial", 14), bg="#ECF0F1").grid(row=5, column=0, pady=10, padx=10, sticky="w")
        end_var = tk.Entry(form, width=28)
        end_var.grid(row=5, column=1)
        end_var.insert(0, data["end_time"])

        # ---- UPDATE BUTTON ----
        def update_timetable():
            payload = {
                "class_id": class_map[class_var.get()],
                "teacher_id": teacher_map[teacher_var.get()],
                "subject": subject_var.get(),
                "day": day_var.get(),
                "start_time": start_var.get(),
                "end_time": end_var.get()
            }

            res = requests.put(f"http://127.0.0.1:8000/admin/timetable/{timetable_id}", json=payload)

            if res.status_code == 200:
                messagebox.showinfo("Success", "Timetable updated successfully!")
                self.load_view_timetable()
            else:
                messagebox.showerror("Error", "Failed to update timetable.")

        tk.Button(
            form,
            text="Update Timetable",
            font=("Arial", 14, "bold"),
            bg="black",
            fg="white",
            command=update_timetable
        ).grid(row=6, column=0, columnspan=2, pady=20)



    #-------WORK SCREENS-------
    def load_work_records(self):
        self.clear_content()

        # TITLE -----------
        tk.Label(self.content, text="View Work", font=("Arial", 26, "bold"), bg="#ECF0F1").pack(pady=20)

        # BACK BUTTON -----------
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)

        self.create_back_button(
            parent=back_frame,
            go_back_callback=self.load_dashboard,
            form_frame=None
        )

        # FETCH ALL WORK RECORDS --------------
        try:
            res = requests.get("http://127.0.0.1:8000/admin/work/")
            all_records = res.json() if res.status_code == 200 else []
        except:
            all_records = []

        # FILTER FRAME -----------
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=10)

        class_var = tk.StringVar(value="None")
        teacher_var = tk.StringVar(value="None")
        subject_var = tk.StringVar(value="None")
        type_var = tk.StringVar(value="None")

        # Dropdown lists built from API
        class_list = ["None"] + sorted({
            f'{(r.get("class_name") or "")} {(r.get("section") or "")}'.strip()
            for r in all_records if r.get("class_name")
        })

        teacher_list = ["None"] + sorted({
            r.get("teacher_name", "")
            for r in all_records if r.get("teacher_name")
        })

        subject_list = ["None"] + sorted({
            r.get("subject", "")
            for r in all_records if r.get("subject")
        })

        type_list = ["None", "Classwork", "Homework", "Assignment"]

        # AUTO FILTER FUNCTION ------------------
        def auto_filter(*args):
            payload = {}

            if class_var.get() != "None":
                payload["class_name"] = class_var.get()

            if teacher_var.get() != "None":
                payload["teacher_name"] = teacher_var.get()

            if subject_var.get() != "None":
                payload["subject"] = subject_var.get()

            if type_var.get() != "None":
                payload["work_type"] = type_var.get()

            if payload:
                try:
                    filtered = requests.post("http://127.0.0.1:8000/admin/work/filter", json=payload).json()
                except:
                    filtered = []
                render_table(filtered)
            else:
                render_table(all_records)

        # FILTER DROPDOWNS 
        # ====================================================
        tk.Label(filter_frame, text="Class:", font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=0, padx=10)
        cb_class = ttk.Combobox(filter_frame, textvariable=class_var, values=class_list, state="readonly", width=20)
        cb_class.grid(row=0, column=1)
        cb_class.bind("<<ComboboxSelected>>", auto_filter)

        tk.Label(filter_frame, text="Teacher:", font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=2, padx=10)
        cb_teacher = ttk.Combobox(filter_frame, textvariable=teacher_var, values=teacher_list, state="readonly", width=22)
        cb_teacher.grid(row=0, column=3)
        cb_teacher.bind("<<ComboboxSelected>>", auto_filter)

        tk.Label(filter_frame, text="Subject:", font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=4, padx=10)
        cb_subject = ttk.Combobox(filter_frame, textvariable=subject_var, values=subject_list, state="readonly", width=18)
        cb_subject.grid(row=0, column=5)
        cb_subject.bind("<<ComboboxSelected>>", auto_filter)

        tk.Label(filter_frame, text="Type:", font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=6, padx=10)
        cb_type = ttk.Combobox(filter_frame, textvariable=type_var, values=type_list, state="readonly", width=18)
        cb_type.grid(row=0, column=7)
        cb_type.bind("<<ComboboxSelected>>", auto_filter)

        # RESET BUTTON (like timetable)
        def reset_filters():
            class_var.set("None")
            teacher_var.set("None")
            subject_var.set("None")
            type_var.set("None")
            render_table(all_records)

        tk.Button(
            filter_frame,
            text="Reset",
            font=("Arial", 12, "bold"),
            bg="#7F8C8D",
            fg="white",
            command=reset_filters
        ).grid(row=0, column=8, padx=10)

        # TABLE -------------------------
        table_frame = tk.Frame(self.content, bg="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        columns = ("Class", "Teacher", "Subject", "Type", "Title", "Due Date")
        work_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        work_table.pack(fill="both", expand=True, side="left")

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=work_table.yview)
        scrollbar.pack(side="right", fill="y")
        work_table.configure(yscrollcommand=scrollbar.set)

        for col in columns:
            work_table.heading(col, text=col)
            work_table.column(col, width=150, anchor="center")

        # RENDER TABLE ----------------
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
                        r.get("teacher_name", ""),
                        r.get("subject", ""),
                        r.get("work_type", ""),
                        r.get("title", ""),
                        r.get("due_date", "")
                    )
                )

        render_table(all_records)

        # ------------- RIGHT CLICK MENU ------------
        menu = tk.Menu(work_table, tearoff=0)
        menu.add_command(label="Preview PDF", command=lambda: self._work_preview_selected(work_table))
        menu.add_command(label="Edit", command=lambda: self._work_edit_selected(work_table))
        menu.add_command(label="Delete", command=lambda: self._work_delete_selected(work_table))

        def show_menu(event):
            row = work_table.identify_row(event.y)
            if row:
                work_table.selection_set(row)
                menu.post(event.x_root, event.y_root)

        work_table.bind("<Button-3>", show_menu)


    def _work_preview_selected(self, table):
        selected = table.selection()
        if not selected:
            return

        work_id = selected[0]   

        try:
            url = f"http://127.0.0.1:8000/admin/work/{work_id}/download"
            r = requests.get(url, timeout=6)

            if r.status_code != 200:
                self.show_popup("Error", "Could not download PDF", "error")
                return

            # Save to temp file
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, f"work_{work_id}.pdf")

            with open(temp_path, "wb") as f:
                f.write(r.content)

            # Open in default system PDF viewer (Windows)
            os.startfile(temp_path)

        except Exception as e:
            self.show_popup("Error", str(e), "error")


    def _work_edit_selected(self, table):
        selected = table.selection()
        if not selected:
            return

        work_id = int(selected[0])   
        self.load_edit_work(work_id)


    def _work_delete_selected(self, table):

        selected = table.selection()
        if not selected:
            return
        item_id = selected[0]
        try:
            work_id = int(item_id)
        except:
            work_id = item_id

        # Confirm using your show_popup confirm type
        if not self.show_popup("Confirm Delete", "Delete this record?", "confirm"):
            return

        try:
            res = requests.delete(f"http://127.0.0.1:8000/admin/work/{work_id}", timeout=6)
            if res.status_code in (200, 204):
                self.show_popup("Success", "Work deleted successfully.", "success")
                # refresh the work records screen
                self.load_work_records()
            else:
                # try to show backend message if any
                try:
                    msg = res.json().get("detail", res.text)
                except:
                    msg = res.text
                self.show_popup("Delete Failed", f"Status {res.status_code}: {msg}", "error")
        except Exception as e:
            self.show_popup("Delete Error", str(e), "error")


    def load_add_work(self):
        self.clear_content()

        tk.Label(
            self.content,
            text="Add Work",
            font=("Arial", 26, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(pady=20)

        # ---------- FETCH  ----------
        classes = fetch_classes()
        teachers = fetch_teachers()
        subjects = fetch_subjects()

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        vars = {
            "class": tk.StringVar(),
            "teacher": tk.StringVar(),
            "subject": tk.StringVar(),
            "work_type": tk.StringVar(),
            "title": tk.StringVar(),
            "description": tk.StringVar(),
            "due_date": tk.StringVar(),
        }

        # ------------------ CLASS ------------------
        tk.Label(form, text="Class:", font=("Arial", 14), bg="#ECF0F1") \
            .grid(row=0, column=0, sticky="w", pady=6)

        class_display = [f'{c["class_name"]} {c["section"]}' for c in classes]

        ttk.Combobox(
            form, textvariable=vars["class"], values=class_display,
            state="readonly", width=30
        ).grid(row=0, column=1, padx=10, pady=6)

        # ------------------ TEACHER ------------------
        tk.Label(form, text="Teacher:", font=("Arial", 14), bg="#ECF0F1") \
            .grid(row=1, column=0, sticky="w", pady=6)

        teacher_display = [t["full_name"] for t in teachers]

        ttk.Combobox(
            form, textvariable=vars["teacher"], values=teacher_display,
            state="readonly", width=30
        ).grid(row=1, column=1, padx=10, pady=6)

        # ------------------ SUBJECT (NEW) ------------------
        tk.Label(form, text="Subject:", font=("Arial", 14), bg="#ECF0F1") \
            .grid(row=2, column=0, sticky="w", pady=6)

        ttk.Combobox(
            form,
            textvariable=vars["subject"],
            values=subjects,
            state="readonly",
            width=30
        ).grid(row=2, column=1, padx=10, pady=6)

        # ------------------ WORK TYPE ------------------
        tk.Label(form, text="Work Type:", font=("Arial", 14), bg="#ECF0F1") \
            .grid(row=3, column=0, sticky="w", pady=6)

        ttk.Combobox(
            form, textvariable=vars["work_type"],
            values=["Classwork", "Homework", "Assignment"],
            state="readonly", width=30
        ).grid(row=3, column=1, padx=10, pady=6)

        # ------------------ TITLE ------------------
        tk.Label(form, text="Title:", font=("Arial", 14), bg="#ECF0F1") \
            .grid(row=4, column=0, pady=6, sticky="w")

        tk.Entry(form, textvariable=vars["title"], font=("Arial", 14), width=30) \
            .grid(row=4, column=1, padx=10, pady=6)

        # ------------------ DESCRIPTION ------------------
        tk.Label(form, text="Description:", font=("Arial", 14), bg="#ECF0F1") \
            .grid(row=5, column=0, pady=6, sticky="w")

        tk.Entry(form, textvariable=vars["description"], font=("Arial", 14), width=30) \
            .grid(row=5, column=1, padx=10, pady=6)

        # ------------------ DUE DATE + CALENDAR ------------------
        tk.Label(form, text="Due Date:", font=("Arial", 14), bg="#ECF0F1") \
            .grid(row=6, column=0, pady=6, sticky="w")

        due_entry = tk.Entry(form, textvariable=vars["due_date"], font=("Arial", 14), width=30)
        due_entry.grid(row=6, column=1, padx=10, pady=6)

        tk.Button(
            form,
            text="Calendar",
            command=lambda: self.open_calendar_popup(due_entry, vars["due_date"])
        ).grid(row=6, column=2, padx=5)

        # ------------------ PDF SELECTOR ------------------
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

        # ------------------ BUTTONS ------------------
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Back", command=self.load_work_records).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancel", command=self.load_work_records).pack(side="left", padx=10)

        save_btn = tk.Button(btn_frame, text="Save Work")
        save_btn.pack(side="left", padx=10)

        def save():
            # Class → ID
            class_text = vars["class"].get()
            class_id = next((c["class_id"] for c in classes
                            if f'{c["class_name"]} {c["section"]}' == class_text), None)

            # Teacher → ID
            teacher_text = vars["teacher"].get()
            teacher_id = next((t["teacher_id"] for t in teachers
                            if t["full_name"] == teacher_text), None)

            payload = {
                "class_id": class_id,
                "teacher_id": teacher_id,
                "work_type": vars["work_type"].get(),
                "title": vars["title"].get(),
                "subject": vars["subject"].get(),
                "description": vars["description"].get(),
                "due_date": vars["due_date"].get(),
            }

            if not selected_file["path"]:
                self.show_popup("Missing PDF", "Please choose a PDF", "warning")
                return

            with open(selected_file["path"], "rb") as f:
                files = {"file": (os.path.basename(selected_file["path"]), f, "application/pdf")}
                r = requests.post("http://127.0.0.1:8000/admin/work/add", data=payload, files=files)

            if r.status_code in (200, 201):
                self.show_popup("Success", "Work Added")
                self.load_work_records()
            else:
                self.show_popup("Error", r.text, "error")

        save_btn.config(command=save)


    def load_edit_work(self, work_id):
        self.clear_content()

        tk.Label(
            self.content,
            text="Edit Work",
            font=("Arial", 26, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(pady=20)

        # ---------- FETCH EXISTING WORK ----------
        try:
            res = requests.get(f"http://127.0.0.1:8000/admin/work/{work_id}")
            if res.status_code != 200:
                self.show_popup("Error", "Work not found")
                return
            work = res.json()
        except Exception as e:
            self.show_popup("Error", str(e))
            return

        # ---------- FETCH  ----------
        classes = fetch_classes()
        teachers = fetch_teachers()
        subjects = fetch_subjects()

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        vars = {
            "class": tk.StringVar(value=f'{work.get("class_name","")} {work.get("section","")}'.strip()),
            "teacher": tk.StringVar(value=work.get("teacher_name", "")),
            "subject": tk.StringVar(value=work.get("subject", "")),
            "work_type": tk.StringVar(value=work.get("work_type", "")),
            "title": tk.StringVar(value=work.get("title", "")),
            "description": tk.StringVar(value=work.get("description", "")),
            "due_date": tk.StringVar(value=str(work.get("due_date", ""))),
        }

        # ------------------ CLASS ------------------
        tk.Label(form, text="Class:", font=("Arial", 14), bg="#ECF0F1") \
            .grid(row=0, column=0, pady=6, sticky="w")

        class_display = [f'{c["class_name"]} {c["section"]}' for c in classes]

        ttk.Combobox(
            form, textvariable=vars["class"], values=class_display,
            state="readonly", width=30
        ).grid(row=0, column=1, padx=10, pady=6)

        # ------------------ TEACHER ------------------
        tk.Label(form, text="Teacher:", font=("Arial", 14), bg="#ECF0F1") \
            .grid(row=1, column=0, pady=6, sticky="w")

        teacher_display = [t["full_name"] for t in teachers]

        ttk.Combobox(
            form, textvariable=vars["teacher"], values=teacher_display,
            state="readonly", width=30
        ).grid(row=1, column=1, padx=10, pady=6)

        # ------------------ SUBJECT (NEW) ------------------
        tk.Label(form, text="Subject:", font=("Arial", 14), bg="#ECF0F1") \
            .grid(row=2, column=0, pady=6, sticky="w")

        ttk.Combobox(
            form, textvariable=vars["subject"],
            values=subjects,
            state="readonly",
            width=30
        ).grid(row=2, column=1, padx=10, pady=6)

        # ------------------ WORK TYPE ------------------
        tk.Label(form, text="Work Type:", font=("Arial", 14), bg="#ECF0F1") \
            .grid(row=3, column=0, pady=6, sticky="w")

        ttk.Combobox(
            form, textvariable=vars["work_type"],
            values=["Classwork", "Homework", "Assignment"],
            state="readonly", width=30
        ).grid(row=3, column=1, padx=10, pady=6)

        # ------------------ TITLE ------------------
        tk.Label(form, text="Title:", font=("Arial", 14), bg="#ECF0F1") \
            .grid(row=4, column=0, pady=6, sticky="w")

        tk.Entry(form, textvariable=vars["title"], font=("Arial", 14), width=30) \
            .grid(row=4, column=1, padx=10, pady=6)

        # ------------------ DESCRIPTION ------------------
        tk.Label(form, text="Description:", font=("Arial", 14), bg="#ECF0F1") \
            .grid(row=5, column=0, pady=6, sticky="w")

        tk.Entry(form, textvariable=vars["description"], font=("Arial", 14), width=30) \
            .grid(row=5, column=1, padx=10, pady=6)

        # ------------------ DUE DATE + CALENDAR ------------------
        tk.Label(form, text="Due Date:", font=("Arial", 14), bg="#ECF0F1") \
            .grid(row=6, column=0, pady=6, sticky="w")

        due_entry = tk.Entry(form, textvariable=vars["due_date"], font=("Arial", 14), width=30)
        due_entry.grid(row=6, column=1, padx=10, pady=6)

        tk.Button(
            form, text="Calendar",
            command=lambda: self.open_calendar_popup(due_entry, vars["due_date"])
        ).grid(row=6, column=2, padx=5)

        # ------------------ BUTTONS ------------------
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Back", command=self.load_work_records).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancel", command=self.load_work_records).pack(side="left", padx=10)

        save_btn = tk.Button(btn_frame, text="Save Changes")
        save_btn.pack(side="left", padx=10)

        # ------------------ SAVE HANDLER ------------------
        def save():
            class_id = next(
                (c["class_id"] for c in classes
                if f'{c["class_name"]} {c["section"]}' == vars["class"].get()),
                None
            )

            teacher_id = next(
                (t["teacher_id"] for t in teachers
                if t["full_name"] == vars["teacher"].get()),
                None
            )

            payload = {
                "class_id": class_id,
                "teacher_id": teacher_id,
                "work_type": vars["work_type"].get(),
                "title": vars["title"].get(),
                "subject": vars["subject"].get(),
                "description": vars["description"].get(),
                "due_date": vars["due_date"].get(),
            }

            try:
                r = requests.put(f"http://127.0.0.1:8000/admin/work/{work_id}", json=payload)
                if r.status_code == 200:
                    self.show_popup("Success", "Work Updated")
                    self.load_work_records()
                else:
                    self.show_popup("Error", r.text)
            except Exception as e:
                self.show_popup("Error", str(e))

        save_btn.config(command=save)



    #-------ACTIVITY SCREENS----------
    def load_view_activity(self):
        self.clear_content()

        # TITLE
        tk.Label(
            self.content,
            text="View Activities",
            font=("Arial", 26, "bold"),
            bg="#ECF0F1"
        ).pack(pady=20)

        # BACK BUTTON 
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)

        self.create_back_button(
            parent=back_frame,
            go_back_callback=self.load_dashboard,
            form_frame=None
        )

        # TABLE FRAME
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = (
            "activity_id",
            "activity_name",
            "category",
            "teacher"
        )

        table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )
        table.pack(fill="both", expand=True)

        # HEADINGS
        table.heading("activity_id", text="ID")
        table.heading("activity_name", text="Title")
        table.heading("category", text="Type")
        table.heading("teacher", text="Teacher Assigned")

        # COLUMN WIDTHS
        table.column("activity_id", width=60, anchor="center")
        table.column("activity_name", width=250, anchor="center")
        table.column("category", width=160, anchor="center")
        table.column("teacher", width=220, anchor="center")

        # FETCH ACTIVITIES
        try:
            res = requests.get(f"{BASE_API_URL}/activities", timeout=5)
            activities = res.json() if res.status_code == 200 else []
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        # INSERT DATA
        for a in activities:
            table.insert(
                "",
                "end",
                values=(
                    a["activity_id"],
                    a["activity_name"],
                    a.get("category", ""),
                    a.get("incharge_teacher", "Not Assigned")
                )
            )

        # ---------------- RIGHT CLICK MENU ----------------
        menu = tk.Menu(self.content, tearoff=0)

        def rc_view_assigned():
            selected = table.selection()
            if not selected:
                return
            activity_id = table.item(selected[0])["values"][0]
            self.load_assigned_students(activity_id)

        def rc_edit_activity():
            selected = table.selection()
            if not selected:
                return
            activity_id = table.item(selected[0])["values"][0]
            self.load_edit_activity(activity_id)

        def rc_delete_activity():
            selected = table.selection()
            if not selected:
                return

            activity_id = table.item(selected[0])["values"][0]

            confirm = messagebox.askyesno(
                "Confirm Delete",
                "Are you sure you want to delete this activity?"
            )
            if not confirm:
                return

            try:
                res = requests.delete(
                    f"{BASE_API_URL}/activities/{activity_id}"
                )
                if res.status_code == 200:
                    messagebox.showinfo(
                        "Deleted",
                        "Activity deleted successfully"
                    )
                    self.load_view_activity()
                else:
                    messagebox.showerror("Error", res.text)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        menu.add_command(label="View Assigned Students", command=rc_view_assigned)
        menu.add_command(label="Edit Activity", command=rc_edit_activity)
        menu.add_separator()
        menu.add_command(label="Delete Activity", command=rc_delete_activity)

        def show_context_menu(event):
            row_id = table.identify_row(event.y)
            if row_id:
                table.selection_set(row_id)
                menu.tk_popup(event.x_root, event.y_root)

        table.bind("<Button-3>", show_context_menu)


    def load_add_activity(self, activity_data=None):
        self.clear_content()

        # Title
        tk.Label(
            self.content,
            text="Add Extra Curricular Activity",
            font=("Arial", 22, "bold"),
            bg="#ECF0F1"
        ).pack(pady=20)

        # Form Frame
        form_frame = tk.Frame(self.content, bg="#ECF0F1")
        form_frame.pack(pady=10)

        # Activity Name
        tk.Label(
            form_frame,
            text="Activity Name",
            font=("Arial", 12),
            bg="#ECF0F1"
        ).grid(row=0, column=0, sticky="w", pady=8)

        self.activity_name_entry = tk.Entry(form_frame, width=40)
        self.activity_name_entry.grid(row=0, column=1, padx=10, pady=8)

        # Category
        tk.Label(
            form_frame,
            text="Category",
            font=("Arial", 12),
            bg="#ECF0F1"
        ).grid(row=1, column=0, sticky="w", pady=8)

        self.activity_category_entry = tk.Entry(form_frame, width=40)
        self.activity_category_entry.grid(row=1, column=1, padx=10, pady=8)

        # In-charge Teacher Dropdown
        tk.Label(
            form_frame,
            text="In-charge Teacher",
            font=("Arial", 12),
            bg="#ECF0F1"
        ).grid(row=2, column=0, sticky="w", pady=8)

        teachers = fetch_teachers()

        teacher_list = ["None"] + [
            f"{t['teacher_id']} - {t['full_name']}" for t in teachers
        ]

        self.teacher_map = {
            f"{t['teacher_id']} - {t['full_name']}": t['teacher_id']
            for t in teachers
        }

        self.selected_teacher = tk.StringVar()
        self.selected_teacher.set("None")

        self.teacher_dropdown = ttk.Combobox(
            form_frame,
            textvariable=self.selected_teacher,
            values=teacher_list,
            state="readonly",
            width=37
        )
        self.teacher_dropdown.grid(row=2, column=1, padx=10, pady=8)

        # Description
        tk.Label(
            form_frame,
            text="Description",
            font=("Arial", 12),
            bg="#ECF0F1"
        ).grid(row=3, column=0, sticky="nw", pady=8)

        self.activity_description_text = tk.Text(
            form_frame,
            width=30,
            height=4
        )
        self.activity_description_text.grid(row=3, column=1, padx=10, pady=8)

        # Buttons
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="Save Activity",
            width=15,
            command=self.save_activity  
        ).grid(row=0, column=0, padx=10)

        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=20)

        self.create_back_button(
            parent=btn_frame,
            go_back_callback=self.load_view_activity,
            form_frame=form_frame
        )

        # If editing existing activity
        if activity_data:
            self.activity_name_entry.insert(0, activity_data["activity_name"])
            self.activity_category_entry.insert(0, activity_data["category"] or "")
            self.activity_description_text.insert( "1.0", activity_data["description"] or "")

            if activity_data["incharge_teacher_id"]:
                teacher_map_reverse = { v: k for k, v in self.teacher_map.items()}
                for label, tid in self.teacher_map.items():
                    if tid == activity_data["incharge_teacher_id"]:
                        self.selected_teacher.set(label)
                        break

            self.edit_activity_id = activity_data["activity_id"]
        else:
            self.edit_activity_id = None


    def load_assign_students(self, activity_id):
        self.clear_content()

        # TITLE
        tk.Label(
            self.content,
            text="Assign Students to Activity",
            font=("Arial", 22, "bold"),
            bg="#ECF0F1"
        ).pack(pady=20)

        # FETCH STUDENTS
        students = fetch_students()
        if not students:
            messagebox.showinfo("Info", "No students found")
            return

        # TABLE
        table = ttk.Treeview(
            self.content,
            columns=("ID", "Name", "Class"),
            show="headings",
            height=15
        )
        table.pack(fill="both", expand=True, padx=20, pady=10)

        table.heading("ID", text="ID")
        table.heading("Name", text="Name")
        table.heading("Class", text="Class")

        table.column("ID", width=80, anchor="center")
        table.column("Name", width=220)
        table.column("Class", width=150)

        # INSERT STUDENTS
        for s in students:
            table.insert(
                "",
                "end",
                values=(
                    s["student_id"],
                    s["full_name"],
                    f'{s["class_name"]} {s["section"]}'
                )
            )

        # ASSIGN BUTTON
        def assign_selected_students():
            selected = table.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select at least one student")
                return

            student_ids = [
                table.item(i)["values"][0] for i in selected
            ]

            payload = {
                "activity_id": activity_id,
                "student_ids": student_ids
            }

            try:
                res = requests.post(
                    f"{BASE_API_URL}/activities/assign-students",
                    json=payload
                )

                if res.status_code == 200:
                    messagebox.showinfo(
                        "Success",
                        "Students assigned successfully"
                    )
                    self.load_view_activity()
                else:
                    messagebox.showerror("Error", res.text)

            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(
            self.content,
            text="Assign Selected Students",
            font=("Arial", 12),
            width=25,
            command=assign_selected_students
        ).pack(pady=15)


    def load_assigned_students(self, activity_id):
        self.clear_content()

        # TITLE
        tk.Label(
            self.content,
            text="Assigned Students",
            font=("Arial", 22, "bold"),
            bg="#ECF0F1"
        ).pack(pady=20)

        # BACK BUTTON 
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)

        self.create_back_button(
            parent=back_frame,
            go_back_callback=self.load_view_activity,
            form_frame=None
        )

        # FETCH ASSIGNED STUDENTS
        try:
            res = requests.get(
                f"{BASE_API_URL}/activities/{activity_id}/students"
            )
            students = res.json() if res.status_code == 200 else []
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        # TABLE FRAME
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        if students:
            table = ttk.Treeview(
                table_frame,
                columns=("ID", "Name", "Class"),
                show="headings",
                height=15
            )
            table.pack(fill="both", expand=True)

            table.heading("ID", text="ID")
            table.heading("Name", text="Name")
            table.heading("Class", text="Class")

            table.column("ID", width=80, anchor="center")
            table.column("Name", width=220, anchor="center")
            table.column("Class", width=150, anchor="center")

            for s in students:
                table.insert(
                    "",
                    "end",
                    values=(
                        s["student_id"],
                        s["full_name"],
                        f'{s["class_name"]} {s["section"]}'
                    )
                )
        else:
            tk.Label(
                table_frame,
                text="No students assigned yet",
                font=("Arial", 12),
                bg="#ECF0F1"
            ).pack(pady=10)

        def assign_student_by_id():
            student_id = simpledialog.askinteger(
                "Assign Student",
                "Enter Student ID:"
            )

            if student_id is None:
                return

            try:
                res = requests.post(
                    f"{BASE_API_URL}/activities/{activity_id}/assign-students",
                    json=[student_id]
                )

                if res.status_code == 200:
                    messagebox.showinfo(
                        "Success",
                        "Student assigned successfully"
                    )
                    self.load_assigned_students(activity_id)
                else:
                    messagebox.showerror("Error", res.text)

            except Exception as e:
                messagebox.showerror("Error", str(e))


        # ASSIGN STUDENT BUTTON
        action_frame = tk.Frame(self.content, bg="#ECF0F1")
        action_frame.pack(pady=15)

        tk.Button(
            action_frame,
            text="Assign Student",
            font=("Arial", 12),
            width=18,
            command=assign_student_by_id
        ).pack()


    def save_activity(self):
        activity_name = self.activity_name_entry.get().strip()
        category = self.activity_category_entry.get().strip()
        description = self.activity_description_text.get("1.0", "end").strip()

        # Validation
        if not activity_name:
            messagebox.showerror("Error", "Activity name is required")
            return

        # Teacher mapping
        teacher_label = self.selected_teacher.get()
        incharge_teacher_id = (
            self.teacher_map.get(teacher_label)
            if teacher_label != "None"
            else None
        )

        payload = {
            "activity_name": activity_name,
            "category": category or None,
            "description": description or None,
            "incharge_teacher_id": incharge_teacher_id
        }

        try:
            # EDIT mode
            if getattr(self, "edit_activity_id", None):
                url = f"http://127.0.0.1:8000/admin/activities/{self.edit_activity_id}"
                response = requests.put(url, json=payload)
            else:
                # CREATE mode
                url = "http://127.0.0.1:8000/admin/activities/"
                response = requests.post(url, json=payload)

            if response.status_code in (200, 201):
                messagebox.showinfo(
                    "Success",
                    "Activity saved successfully"
                )
                self.edit_activity_id = None
                self.load_view_activity()
            else:
                messagebox.showerror("Error", response.text)

        except Exception as e:
            messagebox.showerror("Error", str(e))


    def load_edit_activity(self, activity_id):

        try:
            res = requests.get(f"http://127.0.0.1:8000/admin/activities/{activity_id}")
        except Exception as e:
            messagebox.showerror("Error", "Unable to connect to server.")
            return

        if res.status_code != 200:
            messagebox.showerror("Error", "Unable to fetch activity details.")
            return

        activity_data = res.json()

        # Reuse Add Activity screen with pre-filled data
        self.load_add_activity(activity_data)


    def _rc_view_assigned(self, table):
        selected = table.selection()
        if not selected:
            return

        activity_id = table.item(selected[0])["values"][0]
        self.load_assigned_students(activity_id)


    def _rc_edit_activity(self, table):
        selected = table.selection()
        if not selected:
            return

        activity_id = table.item(selected[0])["values"][0]
        self.load_edit_activity(activity_id)


    def _rc_delete_activity(self, table):
        selected = table.selection()
        if not selected:
            return

        activity_id = table.item(selected[0])["values"][0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this activity?"
        )
        if not confirm:
            return

        try:
            res = requests.delete(
                f"{BASE_API_URL}/activities/{activity_id}"
            )
            if res.status_code == 200:
                messagebox.showinfo("Deleted", "Activity deleted successfully")
                self.load_view_activity()
            else:
                messagebox.showerror("Error", res.text)
        except Exception as e:
            messagebox.showerror("Error", str(e))



    # ==============================================================================
    # ----- TEACHER ONBOARDING BUTTONS -----
    # ----- Button to Create Onboardings -----
    def load_create_onboarding_screen(self):
        self.clear_content()

        tk.Label(
        self.content,
        text="Teacher Onboarding Form",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        fields = [
        ("Full Name", "full_name"),
        ("Gender (M/F/O)", "gender"),
        ("Date of Birth", "date_of_birth"),
        ("Address", "address"),
        ("Subject ID", "subject_id"),
        ("Qualification", "qualification"),
        ("Experience (Years)", "experience_years"),
        ("Email", "email"),
        ("Phone", "phone"),
        ]

        vars = {}

        for i, (label, key) in enumerate(fields):

            tk.Label(form, text=f"{label}:", font=("Arial", 14), bg="#ECF0F1") \
            .grid(row=i, column=0, padx=10, pady=6)

            vars[key] = tk.StringVar()

            # calendar for dob
            if key == "date_of_birth":
                entry = tk.Entry(form, textvariable=vars[key], font=("Arial", 14), width=28)
                entry.grid(row=i, column=1, padx=5, pady=6)

                tk.Button(
                form,
                text="Calendar",
                font=("Arial", 12),
                bg="white",
                command=lambda v=vars[key], b=entry: self.open_calendar_popup(b, v)
                ).grid(row=i, column=2, padx=5)

            else:
                entry = tk.Entry(form, textvariable=vars[key], font=("Arial", 14), width=30)
                entry.grid(row=i, column=1, padx=10, pady=6)

        # Submit Button
        submit_btn = tk.Label(
        form,
        text="Submit",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20, pady=10,
        width=20,
        cursor="arrow",
        relief="ridge"
        )
        submit_btn.grid(row=len(fields), columnspan=2, pady=20)

        def validate():
            if all(v.get().strip() for v in vars.values()):
                submit_btn.config(bg="#000000", fg="white", cursor="arrow")
                submit_btn.bind("<Button-1>", lambda e: submit())
            else:
                submit_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                submit_btn.unbind("<Button-1>")

        for v in vars.values():
            v.trace_add("write", lambda *args: validate())

        def submit():
            data = {k: v.get().strip() for k, v in vars.items()}

            # Gender check
            gender = data["gender"].upper()
            if gender not in ["M", "F", "O"]:
                return self.show_popup("Invalid Gender", "Gender must be M/F/O only!", "warning")

            # Subject ID must be int
            if not data["subject_id"].isdigit():
                return self.show_popup("Invalid Subject ID", "Subject ID must be numeric!", "warning")

            # Experience must be int
            if not data["experience_years"].isdigit():
                 return self.show_popup("Invalid Experience", "Experience must be a number!", "warning")

            # email auto-format
            if "@school.com" not in data["email"]:
                data["email"] = data["email"].lower().replace(" ", "") + "@school.com"

            # phone validation
            if not data["phone"].isdigit() or len(data["phone"]) != 10:
                return self.show_popup("Invalid Phone", "Phone must be 10 digits!", "warning")

            # POST request
            try:
                import requests
                res = requests.post("http://127.0.0.1:8000/admin/teachers/onboardings/create", json=data)

                if res.status_code == 200:
                    self.show_popup("Success", "Teacher Onboarding Submitted!", "info")
                    self.change_screen("Onboarding Submitted!", add_callback=self.load_create_onboarding_screen)
                else:
                    msg = res.json().get("detail", "Error occurred")
                    self.show_popup("Failed", msg, "error")

            except:
                self.show_popup("Server Error", "Backend not reachable", "error")


    # ==============================================================================
    # ----- Button to View all Onboardings in Queue ------
    def load_view_onboarding_queue_screen(self):
        self.clear_content()

        # -------- TITLE --------
        tk.Label(
        self.content,
        text="Teacher Onboarding Queue",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # -------- BACK BUTTON --------
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)
        self.create_back_button(back_frame, self.load_dashboard, None)

        # -------- TABLE WRAPPER --------
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        cols = (
        "onboarding_id", "full_name", "date_of_birth", "gender", "address",
        "email", "phone", "subject_id", "qualification", "experience_years"
        )
        # Filter Bar
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=10)

        tk.Label(
        filter_frame,
        text="Sort By:",
        font=("Arial", 12, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).grid(row=0, column=0, padx=5)

        filter_var = tk.StringVar()
        filter_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=list(cols),
        state="readonly",
        width=20
        )
        filter_dropdown.grid(row=0, column=1, padx=10)

        filter_val_var = tk.StringVar()
        filter_val_entry = tk.Entry(
        filter_frame,
        textvariable=filter_val_var,
        font=("Arial", 12),
        width=25
        )
        filter_val_entry.grid(row=0, column=2, padx=10)

        # Button styling
        def style_btn(btn):
            btn.config(
            bg="#000000",
            fg="white",
            padx=15,
            pady=5,
            width=10,
            relief="raised",
            cursor="arrow",
            font=("Arial", 12, "bold")
            )
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

        load_btn = tk.Label(filter_frame, text="Load")
        style_btn(load_btn)
        load_btn.grid(row=0, column=3, padx=10)

        load_all_btn = tk.Label(filter_frame, text="Load All")
        style_btn(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

        # Table Scrollbars
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        self.teacher_onboarding_tree = ttk.Treeview(
        table_frame,
        columns=cols,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
        )
        self.teacher_onboarding_tree.pack(fill="both", expand=True)
 
        y_scroll.config(command=self.teacher_onboarding_tree.yview)
        x_scroll.config(command=self.teacher_onboarding_tree.xview)

        for col in cols:
            self.teacher_onboarding_tree.heading(col, text=col.replace("_", " ").title())
            self.teacher_onboarding_tree.column(col, width=180, anchor="center")

        # Backend Fetch
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admin/teachers/onboardings/all")
            self.all_teacher_onboardings = res.json() if res.status_code == 200 else []

            self.column_values = {
            "onboarding_id": [str(r["onboarding_id"]) for r in self.all_teacher_onboardings],
            "full_name": [r["full_name"] for r in self.all_teacher_onboardings],
            "date_of_birth": [r["date_of_birth"] for r in self.all_teacher_onboardings],
            "gender": [r["gender"] for r in self.all_teacher_onboardings],
            "address": [r["address"] for r in self.all_teacher_onboardings],
            "email": [r["email"] for r in self.all_teacher_onboardings],
            "phone": [r["phone"] for r in self.all_teacher_onboardings],
            "subject_id": [str(r["subject_id"]) for r in self.all_teacher_onboardings],
            "qualification": [r["qualification"] for r in self.all_teacher_onboardings],
            "experience_years": [str(r["experience_years"]) for r in self.all_teacher_onboardings],
            }
        except:
            self.all_teacher_onboardings = []

        # ----------- UPDATE TABLE -----------
        def update_table(data):
            for row in self.teacher_onboarding_tree.get_children():
                self.teacher_onboarding_tree.delete(row)

            for row in data:
                self.teacher_onboarding_tree.insert(
                "",
                "end",
                values=(
                    row["onboarding_id"],
                    row["full_name"],
                    row["date_of_birth"],
                    row["gender"],
                    row["address"],
                    row["email"],
                    row["phone"],
                    row["subject_id"],
                    row["qualification"],
                    row["experience_years"]
                )
            )

        # ----------- FILTER HANDLER -----------
        def load_filtered():
            col = filter_var.get().strip()
            val = filter_val_var.get().strip().lower()

            if not col or not val:
                return

            valid_lower = [str(v).lower() for v in self.column_values.get(col, [])]

            if val not in valid_lower:
                self.show_popup(
                "Invalid Search",
                f"'{val}' not found in {col.replace('_', ' ').title()}",
                "warning"
                )
                filter_val_var.set("")
                return

            filtered = [
            r for r in self.all_teacher_onboardings
            if str(r[col]).lower() == val
            ]
            update_table(filtered)

        load_btn.bind("<Button-1>", lambda e: load_filtered())
        load_all_btn.bind("<Button-1>", lambda e: update_table(self.all_teacher_onboardings))

        # INITIAL LOAD
        update_table(self.all_teacher_onboardings)


    # ==============================================================================
    # ----- Button to Approve Onboardings -----
    def load_approve_teacher_onboarding_screen(self):
        self.clear_content()

        # ---------------- TITLE ----------------
        tk.Label(
        self.content,
        text="Approve Teacher Onboarding",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=25)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # ---------------- INPUT FIELD ----------------
        tk.Label(form, text="Onboarding ID:", font=("Arial", 14), bg="#ECF0F1")\
        .grid(row=0, column=0, padx=10, pady=10)

        onboard_id_var = tk.StringVar()
        onboard_id_entry = tk.Entry(form, textvariable=onboard_id_var,
                                font=("Arial", 14), width=25)
        onboard_id_entry.grid(row=0, column=1, padx=10, pady=10)

        # ---------------- LOAD BUTTON ----------------
        load_btn = tk.Label(
        form,
        text="Load",
        font=("Arial", 12, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=15,
        pady=5,
        width=12,
        relief="ridge",
        cursor="arrow"
        )
        load_btn.grid(row=0, column=2, padx=10)

        # ENABLE LOAD BUTTON ON VALID INPUT
        def validate_load(*args):
            if onboard_id_var.get().strip():
                load_btn.config(bg="#000000", fg="white", cursor="hand2")
                load_btn.bind("<Enter>", lambda e: load_btn.config(bg="#222222"))
                load_btn.bind("<Leave>", lambda e: load_btn.config(bg="#000000"))
                load_btn.bind("<Button-1>", lambda e: load_teacher_onboarding())
            else:
                load_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                load_btn.unbind("<Enter>")
                load_btn.unbind("<Leave>")
                load_btn.unbind("<Button-1>")

        onboard_id_var.trace_add("write", validate_load)

        # ---------------- OUTPUT PANEL ----------------
        output_frame = tk.Frame(self.content, bg="#ECF0F1")
        output_frame.pack(pady=20)

        fields = [
        "full_name", "date_of_birth", "gender", "address",
        "email", "phone", "subject_id", "qualification", "experience_years"
        ]

        vars_dict = {}

        for i, field in enumerate(fields):
            tk.Label(output_frame, text=f"{field}:",
                 font=("Arial", 14), bg="#ECF0F1").grid(
            row=i, column=0, padx=10, pady=6, sticky="w"
            )

            var = tk.StringVar()
            entry = tk.Entry(
            output_frame,
            textvariable=var,
            font=("Arial", 14),
            width=30,
            state="disabled",
            disabledbackground="#F2F3F4",
            disabledforeground="black"
            )
            entry.grid(row=i, column=1, padx=10, pady=6)
            vars_dict[field] = var

        # ---------------- BACK BUTTON ----------------
        btn_row = tk.Frame(self.content, bg="#ECF0F1")
        btn_row.pack(pady=30)

        self.create_back_button(
        parent=btn_row,
        go_back_callback=self.load_dashboard,
        form_frame=form
        )

        self.content.update_idletasks()

        # ---------------- APPROVE BUTTON ----------------
        approve_btn = tk.Label(
        self.content,
        text="Approve Onboarding",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=10,
        width=18,
        relief="ridge",
        cursor="arrow"
        )
        approve_btn.pack(pady=20)

        # ENABLE / DISABLE APPROVE BUTTON
        def enable_approve():
            approve_btn.config(bg="#000000", fg="white", cursor="arrow")
            approve_btn.bind("<Enter>", lambda e: approve_btn.config(bg="#222222"))
            approve_btn.bind("<Leave>", lambda e: approve_btn.config(bg="#000000"))
            approve_btn.bind("<Button-1>", lambda e: approve_onboarding())

        def disable_approve():
            approve_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            approve_btn.unbind("<Enter>")
            approve_btn.unbind("<Leave>")
            approve_btn.unbind("<Button-1>")

        disable_approve()

        # ---------------- LOAD DATA FUNCTION ----------------
        def load_teacher_onboarding():
            oid = onboard_id_var.get().strip()

            if not oid.isdigit() or int(oid) <= 0:
                self.show_popup("Failed", "Onboarding ID must be a positive number!", "warning")
                return

            import requests

            try:
                res = requests.get(f"http://127.0.0.1:8000/admin/teachers/onboardings/{oid}")

                if res.status_code != 200:
                    self.show_popup("Not Found", "No onboarding record found!", "info")
                    disable_approve()
                    for v in vars_dict.values():
                        v.set("")
                    return

                data = res.json()

                vars_dict["full_name"].set(data["full_name"])
                vars_dict["date_of_birth"].set(data["date_of_birth"])
                vars_dict["gender"].set(data["gender"])
                vars_dict["address"].set(data["address"])
                vars_dict["email"].set(data["email"])
                vars_dict["phone"].set(data["phone"])
                vars_dict["subject_id"].set(data["subject_id"])
                vars_dict["qualification"].set(data["qualification"])
                vars_dict["experience_years"].set(data["experience_years"])

                enable_approve()

            except:
                self.show_popup("Error", "Error fetching onboarding record!", "error")

        # ---------------- APPROVE FUNCTION ----------------
        def approve_onboarding():
            oid = onboard_id_var.get().strip()

            import requests

            try:
                res = requests.post(
                f"http://127.0.0.1:8000/admin/teachers/onboardings/approve/{oid}"
                )

                if res.status_code == 200:
                    teacher_id = res.json().get("teacher_id")
                    self.show_popup("Success", f"Teacher Onboarding Approved!\nTeacher ID: {teacher_id}", "success")
                    self.change_screen(
                    f"Teacher Onboarding Approved!\nTeacher ID: {teacher_id}",
                    add_callback=self.load_approve_teacher_onboarding_screen
                    )
                else:
                    self.show_popup("Failed", "Approval failed!", "error")

            except:
                self.show_popup("Error", "Error approving onboarding!", "error")

    
    # ==============================================================================
    # ----- STAFF ONNBOARDINGS ------
    # ----- Button to Create Staff Onboardings ------
    def load_create_staff_onboarding_screen(self):
        self.clear_content()

        tk.Label(
        self.content,
        text="Staff Onboarding Form",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        fields = [
        ("Full Name", "full_name"),
        ("Date of Birth", "date_of_birth"),
        ("Gender (M/F/O)", "gender"),
        ("Address", "address"),
        ("Department", "department"),
        ("Role", "role"),
        ("Email", "email"),
        ("Phone", "phone"),
        ("Experience (Years)", "experience_years")
        ]

        vars = {}

        for i, (label, key) in enumerate(fields):

            tk.Label(form, text=f"{label}:", font=("Arial", 14), bg="#ECF0F1") \
            .grid(row=i, column=0, padx=10, pady=6)

            vars[key] = tk.StringVar()

            # calendar for dob
            if key == "date_of_birth":
                entry = tk.Entry(form, textvariable=vars[key], font=("Arial", 14), width=28)
                entry.grid(row=i, column=1, padx=5, pady=6)

                tk.Button(
                form,
                text="Calendar",
                font=("Arial", 12),
                bg="white",
                command=lambda v=vars[key], b=entry: self.open_calendar_popup(b, v)
                ).grid(row=i, column=2, padx=5)

            else:
                entry = tk.Entry(form, textvariable=vars[key], font=("Arial", 14), width=30)
                entry.grid(row=i, column=1, padx=10, pady=6)

        # Submit Button
        submit_btn = tk.Label(
        form,
        text="Submit",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20, pady=10,
        width=20,
        cursor="arrow",
        relief="ridge"
        )
        submit_btn.grid(row=len(fields), columnspan=2, pady=20)

        def validate():
            if all(v.get().strip() for v in vars.values()):
                submit_btn.config(bg="#000000", fg="white", cursor="arrow")
                submit_btn.bind("<Button-1>", lambda e: submit())
            else:
                submit_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                submit_btn.unbind("<Button-1>")

        for v in vars.values():
            v.trace_add("write", lambda *args: validate())

        def submit():
            data = {k: v.get().strip() for k, v in vars.items()}

            # Gender check
            gender = data["gender"].upper()
            if gender not in ["M", "F", "O"]:
                return self.show_popup("Invalid Gender", "Gender must be M/F/O only!", "warning")

            # Experience must be int
            if not data["experience_years"].isdigit():
                return self.show_popup("Invalid Experience", "Experience must be a number!", "warning")

            # email auto-format
            if "@school.com" not in data["email"]:
                data["email"] = data["email"].lower().replace(" ", "") + "@school.com"

            # phone validation
            if not data["phone"].isdigit() or len(data["phone"]) != 10:
                return self.show_popup("Invalid Phone", "Phone must be 10 digits!", "warning")

            # POST request
            try:
                import requests
                res = requests.post("http://127.0.0.1:8000/admin/staff/onboardings/create", json=data)

                if res.status_code == 200:
                    self.show_popup("Success", "Staff Onboarding Submitted!", "info")
                    self.change_screen("Onboarding Submitted!", add_callback=self.load_create_staff_onboarding_screen)
                else:
                    msg = res.json().get("detail", "Error occurred")
                    self.show_popup("Failed", msg, "error")

            except:
                self.show_popup("Server Error", "Backend not reachable", "error")


    # ==============================================================================
    # ----- Button to View all staff Onboardings in Queue -----
    def load_view_staff_onboarding_queue_screen(self):
        self.clear_content()

        # -------- TITLE --------
        tk.Label(
        self.content,
        text="Staff Onboarding Queue",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # -------- BACK BUTTON --------
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)
        self.create_back_button(back_frame, self.load_dashboard, None)

        # -------- TABLE WRAPPER --------
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        cols = (
        "onboarding_id", "full_name", "date_of_birth", "gender", "address",
        "email", "phone", "department", "role", "experience_years"
        )
        # Filter Bar
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=10)

        tk.Label(
        filter_frame,
        text="Sort By:",
        font=("Arial", 12, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).grid(row=0, column=0, padx=5)

        filter_var = tk.StringVar()
        filter_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=list(cols),
        state="readonly",
        width=20
        )
        filter_dropdown.grid(row=0, column=1, padx=10)

        filter_val_var = tk.StringVar()
        filter_val_entry = tk.Entry(
        filter_frame,
        textvariable=filter_val_var,
        font=("Arial", 12),
        width=25
        )
        filter_val_entry.grid(row=0, column=2, padx=10)

        # Button styling
        def style_btn(btn):
            btn.config(
            bg="#000000",
            fg="white",
            padx=15,
            pady=5,
            width=10,
            relief="raised",
            cursor="arrow",
            font=("Arial", 12, "bold")
            )
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

        load_btn = tk.Label(filter_frame, text="Load")
        style_btn(load_btn)
        load_btn.grid(row=0, column=3, padx=10)

        load_all_btn = tk.Label(filter_frame, text="Load All")
        style_btn(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

        # Table Scrollbars
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        self.staff_onboarding_tree = ttk.Treeview(
        table_frame,
        columns=cols,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
        )
        self.staff_onboarding_tree.pack(fill="both", expand=True)
 
        y_scroll.config(command=self.staff_onboarding_tree.yview)
        x_scroll.config(command=self.staff_onboarding_tree.xview)

        for col in cols:
            self.staff_onboarding_tree.heading(col, text=col.replace("_", " ").title())
            self.staff_onboarding_tree.column(col, width=180, anchor="center")

        # Backend Fetch
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admin/staff/onboardings/all")
            self.all_staff_onboardings = res.json() if res.status_code == 200 else []

            self.column_values = {
            "onboarding_id": [str(r["onboarding_id"]) for r in self.all_staff_onboardings],
            "full_name": [r["full_name"] for r in self.all_staff_onboardings],
            "date_of_birth": [r["date_of_birth"] for r in self.all_staff_onboardings],
            "gender": [r["gender"] for r in self.all_staff_onboardings],
            "address": [r["address"] for r in self.all_staff_onboardings],
            "email": [r["email"] for r in self.all_staff_onboardings],
            "phone": [r["phone"] for r in self.all_staff_onboardings],
            "department": [r["department"] for r in self.all_staff_onboardings],
            "role": [r["role"] for r in self.all_staff_onboardings],
            "experience_years": [str(r["experience_years"]) for r in self.all_staff_onboardings],
            }
        except:
            self.all_staff_onboardings = []

        # ----------- UPDATE TABLE -----------
        def update_table(data):
            for row in self.staff_onboarding_tree.get_children():
                self.staff_onboarding_tree.delete(row)

            for row in data:
                self.staff_onboarding_tree.insert(
                "",
                "end",
                values=(
                    row["onboarding_id"],
                    row["full_name"],
                    row["date_of_birth"],
                    row["gender"],
                    row["address"],
                    row["email"],
                    row["phone"],
                    row["department"],
                    row["role"],
                    row["experience_years"]
                )
            )

        # ----------- FILTER HANDLER -----------
        def load_filtered():
            col = filter_var.get().strip()
            val = filter_val_var.get().strip().lower()

            if not col or not val:
                return

            valid_lower = [str(v).lower() for v in self.column_values.get(col, [])]

            if val not in valid_lower:
                self.show_popup(
                "Invalid Search",
                f"'{val}' not found in {col.replace('_', ' ').title()}",
                "warning"
                )
                filter_val_var.set("")
                return

            filtered = [
            r for r in self.all_staff_onboardings
            if str(r[col]).lower() == val
            ]
            update_table(filtered)

        load_btn.bind("<Button-1>", lambda e: load_filtered())
        load_all_btn.bind("<Button-1>", lambda e: update_table(self.all_staff_onboardings))

        # INITIAL LOAD
        update_table(self.all_staff_onboardings)

    
    # ==============================================================================
    # ----- Button to Approve Staff Onboardings ------
    def load_approve_staff_onboarding_screen(self):
        self.clear_content()

        # ---------------- TITLE ----------------
        tk.Label(
        self.content,
        text="Approve Staff Onboarding",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=25)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # ---------------- INPUT FIELD ----------------
        tk.Label(form, text="Onboarding ID:", font=("Arial", 14), bg="#ECF0F1")\
        .grid(row=0, column=0, padx=10, pady=10)

        onboard_id_var = tk.StringVar()
        onboard_id_entry = tk.Entry(form, textvariable=onboard_id_var,
                                font=("Arial", 14), width=25)
        onboard_id_entry.grid(row=0, column=1, padx=10, pady=10)

        # ---------------- LOAD BUTTON ----------------
        load_btn = tk.Label(
        form,
        text="Load",
        font=("Arial", 12, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=15,
        pady=5,
        width=12,
        relief="ridge",
        cursor="arrow"
        )
        load_btn.grid(row=0, column=2, padx=10)

        # ENABLE LOAD BUTTON ON VALID INPUT
        def validate_load(*args):
            if onboard_id_var.get().strip():
                load_btn.config(bg="#000000", fg="white", cursor="arrow")
                load_btn.bind("<Enter>", lambda e: load_btn.config(bg="#222222"))
                load_btn.bind("<Leave>", lambda e: load_btn.config(bg="#000000"))
                load_btn.bind("<Button-1>", lambda e: load_staff_onboarding())
            else:
                load_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                load_btn.unbind("<Enter>")
                load_btn.unbind("<Leave>")
                load_btn.unbind("<Button-1>")

        onboard_id_var.trace_add("write", validate_load)

        # ---------------- OUTPUT PANEL ----------------
        output_frame = tk.Frame(self.content, bg="#ECF0F1")
        output_frame.pack(pady=20)

        fields = [
        "full_name", "date_of_birth", "gender", "address", "department", "role",
        "email", "phone", "experience_years"
         ]

        vars_dict = {}

        for i, field in enumerate(fields):
            tk.Label(output_frame, text=f"{field}:",
                 font=("Arial", 14), bg="#ECF0F1").grid(
            row=i, column=0, padx=10, pady=6, sticky="w"
            )

            var = tk.StringVar()
            entry = tk.Entry(
            output_frame,
            textvariable=var,
            font=("Arial", 14),
            width=30,
            state="disabled",
            disabledbackground="#F2F3F4",
            disabledforeground="black"
            )
            entry.grid(row=i, column=1, padx=10, pady=6)
            vars_dict[field] = var

        # ---------------- BACK BUTTON ----------------
        btn_row = tk.Frame(self.content, bg="#ECF0F1")
        btn_row.pack(pady=30)

        self.create_back_button(
        parent=btn_row,
        go_back_callback=self.load_dashboard,
        form_frame=form
        )

        self.content.update_idletasks()

        # ---------------- APPROVE BUTTON ----------------
        approve_btn = tk.Label(
        self.content,
        text="Approve Onboarding",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=10,
        width=18,
        relief="ridge",
        cursor="arrow"
        )
        approve_btn.pack(pady=20)

        # ENABLE / DISABLE APPROVE BUTTON
        def enable_approve():
            approve_btn.config(bg="#000000", fg="white", cursor="arrow")
            approve_btn.bind("<Enter>", lambda e: approve_btn.config(bg="#222222"))
            approve_btn.bind("<Leave>", lambda e: approve_btn.config(bg="#000000"))
            approve_btn.bind("<Button-1>", lambda e: approve_onboarding())

        def disable_approve():
            approve_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            approve_btn.unbind("<Enter>")
            approve_btn.unbind("<Leave>")
            approve_btn.unbind("<Button-1>")

        disable_approve()

        # ---------------- LOAD DATA FUNCTION ----------------
        def load_staff_onboarding():
            oid = onboard_id_var.get().strip()

            if not oid.isdigit() or int(oid) <= 0:
                self.show_popup("Failed", "Onboarding ID must be a positive number!", "warning")
                return

            import requests

            try:
                res = requests.get(f"http://127.0.0.1:8000/admin/staff/onboardings/{oid}")

                if res.status_code != 200:
                    self.show_popup("Not Found", "No onboarding record found!", "info")
                    disable_approve()
                    for v in vars_dict.values():
                        v.set("")
                    return

                data = res.json()

                vars_dict["full_name"].set(data["full_name"])
                vars_dict["date_of_birth"].set(data["date_of_birth"])
                vars_dict["gender"].set(data["gender"])
                vars_dict["address"].set(data["address"])
                vars_dict["email"].set(data["email"])
                vars_dict["phone"].set(data["phone"])
                vars_dict["department"].set(data["department"])
                vars_dict["role"].set(data["role"])
                vars_dict["experience_years"].set(data["experience_years"])

                enable_approve()

            except:
                self.show_popup("Error", "Error fetching onboarding record!", "error")

        # ---------------- APPROVE FUNCTION ----------------
        def approve_onboarding():
            oid = onboard_id_var.get().strip()

            import requests

            try:
                res = requests.post(
                f"http://127.0.0.1:8000/admin/staff/onboardings/approve/{oid}"
                )

                if res.status_code == 200:
                    staff_id = res.json().get("staff_id")
                    self.show_popup("Success", f"Staff Onboarding Approved!\nStaff ID: {staff_id}", "success")
                    self.change_screen(
                    f"Staff Onboarding Approved!\nStaff ID: {staff_id}",
                    add_callback=self.load_approve_staff_onboarding_screen
                    )
                else:
                    self.show_popup("Failed", "Approval failed!", "error")

            except:
                self.show_popup("Error", "Error approving onboarding!", "error")


    # ==============================================================================
    # ------ TEACHER OFFBOARDINGS/TRANSFERS/SEPERATIONS ------
    # ----- Button to Issue Separation to a Teacher ------
    def load_issue_teacher_separation_screen(self):
        self.clear_content()

        # ---------- TITLE ----------
        tk.Label(
        self.content,
        text="Issue Teacher Separation",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
    ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=20)

    # ---------- FIELDS ----------
        fields = [
        ("Teacher ID", "teacher_id"),
        ("Reason", "reason"),
        ("Remarks", "remarks"),
        ("Last Working Date (YYYY-MM-DD)", "separation_date")
    ]

        vars = {}

        for i, (label, key) in enumerate(fields):

            tk.Label(
            form, text=f"{label}:", font=("Arial", 14), bg="#ECF0F1"
        ).grid(row=i, column=0, padx=10, pady=8)

            vars[key] = tk.StringVar()

        # --- Calendar for separation date ---
            if key == "separation_date":
                entry = tk.Entry(form, textvariable=vars[key], font=("Arial", 14), width=28)
                entry.grid(row=i, column=1, padx=10, pady=6)

                tk.Button(
                form,
                text="Calendar",
                font=("Arial", 12),
                bg="white",
                relief="flat",
                command=lambda v=vars[key], b=entry: self.open_calendar_popup(b, v)
            ).grid(row=i, column=2, padx=5)
            else:
                entry = tk.Entry(form, textvariable=vars[key], font=("Arial", 14), width=30)
                entry.grid(row=i, column=1, padx=10, pady=6)

    # ---------- BACK BUTTON ----------
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,
        form_frame=form
    )

    # ---------- SUBMIT BUTTON ----------
        submit_btn = tk.Label(
        form,
        text="Issue Separation",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=10,
        width=20,
        cursor="arrow",
        relief="ridge"
    )
        submit_btn.grid(row=len(fields), column=0, columnspan=3, pady=20)

    # ---------- VALIDATION ----------
        def validate(*args):
            if all(vars[k].get().strip() for k in vars):
                submit_btn.config(bg="#000000", fg="white", cursor="arrow")
                submit_btn.bind("<Enter>", lambda e: submit_btn.config(bg="#222222"))
                submit_btn.bind("<Leave>", lambda e: submit_btn.config(bg="#000000"))
                submit_btn.bind("<Button-1>", lambda e: issue_separation())
            else:
                submit_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                submit_btn.unbind("<Enter>")
                submit_btn.unbind("<Leave>")
                submit_btn.unbind("<Button-1>")

        for v in vars.values():
            v.trace_add("write", validate)

    # ---------- SUBMIT FUNCTION ----------
        def issue_separation():

        # date format validation
            import re
            date_str = vars["separation_date"].get().strip()
            if not re.match(r"\d{4}-\d{2}-\d{2}$", date_str):
                self.show_popup("Invalid Date", "Date must be YYYY-MM-DD format!", "warning")
                return

            payload = {
            "teacher_id": int(vars["teacher_id"].get().strip()),
            "reason": vars["reason"].get().strip(),
            "remarks": vars["remarks"].get().strip(),
            "separation_date": date_str
        }

        # ---- send to backend ----
            import requests
            res = requests.post("http://127.0.0.1:8000/admin/teachers/separation/issue", json=payload)

            if res.status_code == 200:
                self.show_popup("Success", "Separation Issued Successfully!", "info")
                self.change_screen("Teacher Separation Issued!", add_callback=self.load_issue_teacher_separation_screen)
            else:
                msg = res.json().get("detail", "Error issuing separation")
                self.show_popup("Failed", msg, "error")


    # ==============================================================================
    # ----- Button to View all Separation Requests -----
    def load_view_all_teacher_separation_screen(self):
        self.clear_content()

    # ---------- TITLE ----------
        tk.Label(
        self.content,
        text="All Teacher Separation Requests",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
    ).pack(pady=20)

    # ---------- BACK BUTTON ----------
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)

        self.create_back_button(
        parent=back_frame,
        go_back_callback=self.load_dashboard,
        form_frame=None
    )

    # ---------- TABLE FRAME ----------
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # ------- TABLE COLUMNS -------
        cols = ("sep_id", "teacher_id", "separation_date", "reason", "status")

    # ------- FILTER BAR -------
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=10)

        tk.Label(
        filter_frame,
        text="Sort By:",
        font=("Arial", 12, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
    ).grid(row=0, column=0, padx=5)

        filter_var = tk.StringVar()
        filter_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=list(cols),
        state="readonly",
        width=20
    )
        filter_dropdown.grid(row=0, column=1, padx=10)

        filter_val_var = tk.StringVar()
        filter_val = tk.Entry(
        filter_frame,
        textvariable=filter_val_var,
        font=("Arial", 12),
        width=25
    )
        filter_val.grid(row=0, column=2, padx=10)

    # ----- Black Button Styling -----
        def style_button(btn):
            btn.config(
            bg="#000000",
            fg="white",
            padx=15,
            pady=5,
            width=10,
            relief="raised",
            cursor="arrow",
            font=("Arial", 12, "bold")
        )
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

        load_btn = tk.Label(filter_frame, text="Load")
        style_button(load_btn)
        load_btn.grid(row=0, column=3, padx=10)

        load_all_btn = tk.Label(filter_frame, text="Load All")
        style_button(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

    # ---------- SCROLLBARS ----------
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

    # ---------- TREEVIEW TABLE ----------
        self.sep_tree = ttk.Treeview(
        table_frame,
        columns=cols,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
    )
        self.sep_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.sep_tree.yview)
        x_scroll.config(command=self.sep_tree.xview)

        for col in cols:
            self.sep_tree.heading(col, text=col.replace("_", " ").title())
            self.sep_tree.column(col, width=180, anchor="center")

    # ---------- FETCH DATA FROM BACKEND ----------
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admin/teachers/separation/all")
            self.all_separations = res.json() if res.status_code == 200 else []

        # Structure for validation
            self.sep_column_values = {
            "sep_id": [str(r["sep_id"]) for r in self.all_separations],
            "teacher_id": [str(r["teacher_id"]) for r in self.all_separations],
            "separation_date": [r["separation_date"] for r in self.all_separations],
            "reason": [r["reason"] for r in self.all_separations],
            "status": [1 if r["status"] else 0 for r in self.all_separations]
        }
        except:
            self.all_separations = []

        # ---------- UPDATE TABLE ----------
        def update_table(data):
            for row in self.sep_tree.get_children():
                self.sep_tree.delete(row)

            for row in data:
                self.sep_tree.insert(
                "",
                "end",
                values=(
                    row["sep_id"],
                    row["teacher_id"],
                    row["separation_date"],
                    row["reason"],
                    1 if row["status"] else 0
                )
            )

        # ---------- FILTER FUNCTION ----------
        def load_filtered():
            col = filter_var.get().strip()
            val = filter_val.get().strip().lower()

            if not col or not val:
                return

            valid_list = self.sep_column_values.get(col, [])
            valid_lower = [str(v).lower() for v in valid_list]

            if val not in valid_lower:
                self.show_popup(
                "Invalid Search",
                f"'{val}' not found in '{col}'.",
                "warning"
            )
                filter_val_var.set("")
                return

            filtered = [
            r for r in self.all_separations
            if str(r[col]).lower() == val
        ]
            update_table(filtered)

        def load_all():
            update_table(self.all_separations)

        load_btn.bind("<Button-1>", lambda e: load_filtered())
        load_all_btn.bind("<Button-1>", lambda e: load_all())

    # INITIAL LOAD
        update_table(self.all_separations)
    

    # ==============================================================================
    # ----- Button to Approve Separation of a Teacher -----
    def load_approve_teacher_separation_screen(self):
        self.clear_content()
 
        # ---------- TITLE ----------
        tk.Label(
        self.content,
        text="Approve Teacher Separation",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=25)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # ---------- SEPARATION ID INPUT ----------
        tk.Label(
        form,
        text="Separation ID:",
        font=("Arial", 14),
        bg="#ECF0F1"
        ).grid(row=0, column=0, padx=10, pady=10)

        sep_id_var = tk.StringVar()
        sep_entry = tk.Entry(form, textvariable=sep_id_var, font=("Arial", 14), width=25)
        sep_entry.grid(row=0, column=1, padx=10, pady=10)

        # ---------- LOAD BUTTON ----------
        load_btn = tk.Label(
        form,
        text="Load",
        font=("Arial", 12, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=15, pady=5,
        width=12,
        relief="ridge",
        cursor="arrow"
        )
        load_btn.grid(row=0, column=2, padx=10)

        # Enable/Disable Load Button
        def validate_load(*args):
            if sep_id_var.get().strip():
                load_btn.config(bg="#000000", fg="white", cursor="hand2")
                load_btn.bind("<Enter>", lambda e: load_btn.config(bg="#222222"))
                load_btn.bind("<Leave>", lambda e: load_btn.config(bg="#000000"))
                load_btn.bind("<Button-1>", lambda e: load_separation())
            else:
                load_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                load_btn.unbind("<Enter>")
                load_btn.unbind("<Leave>")
                load_btn.unbind("<Button-1>")

        sep_id_var.trace_add("write", validate_load)

        # ---------- OUTPUT PANEL ----------
        output_frame = tk.Frame(self.content, bg="#ECF0F1")
        output_frame.pack(pady=20)

        fields = ["teacher_id", "separation_date", "reason", "remarks", "status"]
        vars_dict = {}

        for i, label in enumerate(fields):
            tk.Label(
            output_frame,
            text=f"{label.replace('_',' ').title()}:",
            font=("Arial", 14),
            bg="#ECF0F1"
            ).grid(row=i, column=0, padx=10, pady=6, sticky="w")

            var = tk.StringVar()
            entry = tk.Entry(
            output_frame,
            textvariable=var,
            font=("Arial", 14),
            width=30,
            state="disabled",
            disabledbackground="#F2F3F4",
            disabledforeground="black"
            )
            entry.grid(row=i, column=1, padx=10, pady=6)
            vars_dict[label] = var

        # ---------- BUTTON ROW ----------
        btn_row = tk.Frame(self.content, bg="#ECF0F1")
        btn_row.pack(pady=30)

        self.create_back_button(btn_row, self.load_dashboard, form)

        # ---------- APPROVE BUTTON ----------
        approve_btn = tk.Label(
        self.content,
        text="Approve Separation",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=10,
        width=18,
        relief="ridge",
        cursor="arrow"
        )
        approve_btn.pack(pady=20)

        def enable_approve():
            approve_btn.config(bg="#000000", fg="white", cursor="hand2")
            approve_btn.bind("<Enter>", lambda e: approve_btn.config(bg="#222222"))
            approve_btn.bind("<Leave>", lambda e: approve_btn.config(bg="#000000"))
            approve_btn.bind("<Button-1>", lambda e: approve_separation())

        def disable_approve():
            approve_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            approve_btn.unbind("<Enter>")
            approve_btn.unbind("<Leave>")
            approve_btn.unbind("<Button-1>")

        disable_approve()

        # ---------- LOAD SEPARATION DETAILS ----------
        def load_separation():
            sep_id = sep_id_var.get().strip()

            if not sep_id.isdigit() or int(sep_id) <= 0:
                self.show_popup("Invalid ID", "Separation ID must be a positive number!", "warning")
                return

            import requests
            try:
                res = requests.get(f"http://127.0.0.1:8000/admin/teachers/separation/{sep_id}")

                if res.status_code != 200:
                    self.show_popup("Not Found", "Separation record not found!", "info")
                    disable_approve()
                    for v in vars_dict.values():
                        v.set("")
                    return

                data = res.json()

                # set values
                vars_dict["teacher_id"].set(data["teacher_id"])
                vars_dict["separation_date"].set(data["separation_date"])
                vars_dict["reason"].set(data["reason"])
                vars_dict["status"].set("1" if data["status"] else "0")

                enable_approve()

            except Exception:
                self.show_popup("Error", "Server not reachable!", "error")

        # ---------- APPROVE SEPARATION ----------
        def approve_separation():
            sep_id = sep_id_var.get().strip()

            import requests
            try:
                res = requests.post(f"http://127.0.0.1:8000/admin/teachers/separation/approve/{sep_id}")

                if res.status_code == 200:
                    msg = "Teacher Separation Approved Successfully!"
                    self.show_popup("Success", msg, "info")
                    self.change_screen(msg, add_callback=self.load_approve_teacher_separation_screen)
                else:
                    self.show_popup("Failed", "Approval failed!", "error")

            except Exception:
                self.show_popup("Error", "Unable to approve separation!", "error")
    

    # ==============================================================================
    # ----- Button to Create a Transfer Request for Teacher -----
    def load_create_teacher_transfer_screen(self):
        self.clear_content()

        # ---- TITLE ----
        tk.Label(
        self.content,
        text="Create Teacher Transfer Request",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # ---- FORM FRAME ----
        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=15)

        fields = [
        ("Teacher ID", "teacher_id"),
        ("New Department", "new_department"),
        ("New Subject ID", "new_subject_id"),
        ("New Class ID", "new_class_id"),
        ("Request Date (YYYY-MM-DD)", "request_date"),
        ]

        self.tf_vars = {}

        for i, (label, key) in enumerate(fields):

            tk.Label(
            form, text=f"{label}:", font=("Arial", 14), bg="#ECF0F1"
            ).grid(row=i, column=0, padx=10, pady=8, sticky="e")
 
            var = tk.StringVar()
            self.tf_vars[key] = var

            entry = tk.Entry(
            form, textvariable=var, font=("Arial", 14), width=28
            )
            entry.grid(row=i, column=1, padx=10, pady=8)

            # Calendar only for request_date
            if key == "request_date":
                tk.Button(
                form,
                text="Calendar",
                font=("Arial", 12),
                bg="white",
                relief="ridge",
                command=lambda e=entry, v=var: self.open_calendar_popup(e, v)
                ).grid(row=i, column=2, padx=5)

        # ---- BACK BUTTON ----
        btn_row = tk.Frame(self.content, bg="#ECF0F1")
        btn_row.pack(pady=20)

        self.create_back_button(
        parent=btn_row,
        go_back_callback=self.load_dashboard,
        form_frame=form
        )

        # ---- SUBMIT BUTTON ----
        submit_btn = tk.Label(
        self.content,
        text="Create Transfer Request",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=12,
        width=22,
        relief="ridge",
        cursor="arrow"
        )
        submit_btn.pack(pady=20)

        # ---------- ENABLE/DISABLE ----------
        def enable():
            submit_btn.config(bg="#000000", fg="white", cursor="hand2")
            submit_btn.bind("<Enter>", lambda e: submit_btn.config(bg="#222222"))
            submit_btn.bind("<Leave>", lambda e: submit_btn.config(bg="#000000"))
            submit_btn.bind("<Button-1>", lambda e: submit_request())

        def disable():
            submit_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            submit_btn.unbind("<Enter>")
            submit_btn.unbind("<Leave>")
            submit_btn.unbind("<Button-1>")

        disable()

        # ---------- VALIDATION ----------
        import re
        def validate(*args):
            data = {k: v.get().strip() for k, v in self.tf_vars.items()}

            if not data["teacher_id"].isdigit():
                disable()
                return

            if data["new_subject_id"] and not data["new_subject_id"].isdigit():
                disable()
                return
            
            if data["new_class_id"] and not data["new_class_id"].isdigit():
                disable()
                return
            
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", data["request_date"]):
                disable()
                return

            enable()

        for v in self.tf_vars.values():
            v.trace_add("write", validate)

        # ---------- SUBMIT FUNCTION ----------
        def submit_request():
            data = {k: v.get().strip() for k, v in self.tf_vars.items()}

            # Required fields
            if not data["teacher_id"] or not data["request_date"]:
                self.show_popup("Missing Data", "Teacher ID and Request Date are required", "warning")
                return

            payload = {
            "teacher_id": int(data["teacher_id"]),
            "new_department": data["new_department"] if data["new_department"] else None,
            "new_subject_id": int(data["new_subject_id"]) if data["new_subject_id"] else None,
            "new_class_id": int(data["new_class_id"]) if data["new_class_id"] else None,
            "request_date": data["request_date"]
            }

            import requests
            try:
                res = requests.post(
                "http://127.0.0.1:8000/admin/teacher-transfer/request",
                json=payload
                )

                if res.status_code == 200:
                    self.show_popup("Success", "Transfer Request Added to Queue!", "info")
                    self.change_screen(
                    "Transfer Request Created!",
                    add_callback=self.load_create_teacher_transfer_screen
                    )
                else:
                    msg = res.json().get("detail", "Error occurred")
                    self.show_popup("Failed", msg, "error")

            except Exception as e:
                self.show_popup("Error", str(e), "error")


    # ==============================================================================
    # ----- Button to View all Transfer Requests in Queue for Teacher -----
    def load_view_all_teacher_transfers_screen(self):
        self.clear_content()

        # ----- TITLE -----
        tk.Label(
        self.content,
        text="All Teacher Transfer Requests",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
    ).pack(pady=20)

        # -------- BACK BUTTON --------
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)
        self.create_back_button(back_frame, self.load_dashboard, None)

        # -------- TABLE FRAME --------
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # ---- TABLE COLUMNS (MATCHING TeacherTransfer MODEL) ----
        cols = (
        "transfer_id",
        "teacher_id",
        "old_department",
        "old_subject_id",
        "new_department",
        "new_subject_id",
        "request_date",
        "status"
    )

        # ====== FILTER BAR ======
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=10)

        tk.Label(
        filter_frame,
        text="Sort By:",
        font=("Arial", 12, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
    ).grid(row=0, column=0, padx=5)

        filter_var = tk.StringVar()
        filter_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=list(cols),
        state="readonly",
        width=20
    )
        filter_dropdown.grid(row=0, column=1, padx=10)

        filter_val_var = tk.StringVar()
        filter_val = tk.Entry(
        filter_frame,
        textvariable=filter_val_var,
        font=("Arial", 12),
        width=25
    )
        filter_val.grid(row=0, column=2, padx=10)

        # ---- Button Styling ----
        def style_button(btn):
            btn.config(
            bg="#000000",
            fg="white",
            padx=15,
            pady=5,
            width=10,
            relief="raised",
            cursor="arrow",
            font=("Arial", 12, "bold")
        )
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

        load_btn = tk.Label(filter_frame, text="Load")
        style_button(load_btn)
        load_btn.grid(row=0, column=3, padx=10)

        load_all_btn = tk.Label(filter_frame, text="Load All")
        style_button(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

        # ------ TABLE + SCROLLBARS ------
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        self.transfer_tree = ttk.Treeview(
        table_frame,
        columns=cols,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
    )
        self.transfer_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.transfer_tree.yview)
        x_scroll.config(command=self.transfer_tree.xview)

        for col in cols:
            self.transfer_tree.heading(col, text=col.replace("_", " ").title())
            self.transfer_tree.column(col, width=180, anchor="center")

        # ----- BACKEND FETCH ------
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admin/teacher-transfer/all")
            self.all_transfers = res.json() if res.status_code == 200 else []

            # For filter validation:
            self.transfer_column_values = {
            "transfer_id": [str(r["transfer_id"]) for r in self.all_transfers],
            "teacher_id": [str(r["teacher_id"]) for r in self.all_transfers],
            "old_department": [str(r["old_department"]) for r in self.all_transfers],
            "old_subject_id": [str(r["old_subject_id"]) for r in self.all_transfers],
            "new_department": [str(r["new_department"]) for r in self.all_transfers],
            "new_subject_id": [str(r["new_subject_id"]) for r in self.all_transfers],
            "request_date": [r["request_date"] for r in self.all_transfers],
            "status": [1 if r["status"] else 0 for r in self.all_transfers]
        }

        except:
            self.all_transfers = []

        # ------- UPDATE TABLE -------
        def update_table(data):
            for row in self.transfer_tree.get_children():
                self.transfer_tree.delete(row)

            for row in data:
                self.transfer_tree.insert(
                "",
                "end",
                values=(
                    row["transfer_id"],
                    row["teacher_id"],
                    row["old_department"],
                    row["old_subject_id"],
                    row["new_department"],
                    row["new_subject_id"],
                    row["request_date"],
                    1 if row["status"] else 0
                )
            )

        # ------- FILTER FUNCTION -------
        def load_filtered():
            col = filter_var.get().strip()
            val = filter_val_var.get().strip().lower()

            if not col or not val:
                return

            valid_list = self.transfer_column_values.get(col, [])
            valid_lower = [str(v).lower() for v in valid_list]

            if val not in valid_lower:
                self.show_popup(
                "Invalid Search",
                f"'{val}' not found in column '{col}'.",
                "warning"
            )
                filter_val_var.set("")
                return

            filtered = [
                r for r in self.all_transfers
                if str(r[col]).lower() == val
            ]
            update_table(filtered)

        def load_all():
            update_table(self.all_transfers)

        load_btn.bind("<Button-1>", lambda e: load_filtered())
        load_all_btn.bind("<Button-1>", lambda e: load_all())

        # INITIAL LOAD
        update_table(self.all_transfers)


    # ==============================================================================
    # ----- Button to Approve a Transfer Request for a Teacher -----
    def load_approve_teacher_transfer_screen(self):
        self.clear_content()

        # ----- TITLE -----
        tk.Label(
        self.content,
        text="Approve Teacher Transfer Request",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
    ).pack(pady=25)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # ---------- TRANSFER ID INPUT ----------
        tk.Label(form, text="Transfer ID:", font=("Arial", 14), bg="#ECF0F1").grid(
        row=0, column=0, padx=10, pady=10
        )

        transfer_id_var = tk.StringVar()
        transfer_id_entry = tk.Entry(form, textvariable=transfer_id_var,
                                 font=("Arial", 14), width=25)
        transfer_id_entry.grid(row=0, column=1, padx=10, pady=10)

        # ---------- LOAD BUTTON ----------
        load_btn = tk.Label(
        form,
        text="Load",
        font=("Arial", 12, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=15, pady=5,
        width=12,
        relief="ridge",
        cursor="arrow"
    )
        load_btn.grid(row=0, column=2, padx=10)

        # Enable/Disable LOAD button
        def validate_load(*args):
            if transfer_id_var.get().strip():
                load_btn.config(bg="#000000", fg="white", cursor="hand2")
                load_btn.bind("<Enter>", lambda e: load_btn.config(bg="#222222"))
                load_btn.bind("<Leave>", lambda e: load_btn.config(bg="#000000"))
                load_btn.bind("<Button-1>", lambda e: load_transfer())
            else:
                load_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                load_btn.unbind("<Enter>")
                load_btn.unbind("<Leave>")
                load_btn.unbind("<Button-1>")

        transfer_id_var.trace_add("write", validate_load)

        # ---------- OUTPUT PANEL ----------
        output_frame = tk.Frame(self.content, bg="#ECF0F1")
        output_frame.pack(pady=20)

        fields = [
        "teacher_id",
        "old_department", "new_department",
        "old_subject_id", "new_subject_id",
        "old_class_id", "new_class_id",
        "request_date", "status"
        ]
    
        vars_dict = {}

        for i, label in enumerate(fields):
            tk.Label(
            output_frame,
            text=f"{label.replace('_',' ').title()}:",
            font=("Arial", 14),
            bg="#ECF0F1"
            ).grid(row=i, column=0, padx=10, pady=6, sticky="w")

            var = tk.StringVar()
            entry = tk.Entry(
            output_frame,
            textvariable=var,
            font=("Arial", 14),
            width=30,
            state="disabled",
            disabledbackground="#F2F3F4",
            disabledforeground="black"
            )
            entry.grid(row=i, column=1, padx=10, pady=6)
            vars_dict[label] = var

        # ---------- BACK BUTTON ----------
        btn_row = tk.Frame(self.content, bg="#ECF0F1")
        btn_row.pack(pady=30)

        self.create_back_button(
        parent=btn_row,
        go_back_callback=self.load_dashboard,
        form_frame=form
    )

        # ---------- APPROVE BUTTON ----------
        approve_btn = tk.Label(
        self.content,
        text="Approve Transfer",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=10,
        width=18,
        relief="ridge",
        cursor="arrow"
    )
        approve_btn.pack(pady=20)

        def enable_approve():
            approve_btn.config(bg="#000000", fg="white", cursor="hand2")
            approve_btn.bind("<Enter>", lambda e: approve_btn.config(bg="#222222"))
            approve_btn.bind("<Leave>", lambda e: approve_btn.config(bg="#000000"))
            approve_btn.bind("<Button-1>", lambda e: approve_transfer())

        def disable_approve():
            approve_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            approve_btn.unbind("<Enter>")
            approve_btn.unbind("<Leave>")
            approve_btn.unbind("<Button-1>")

        disable_approve()

        # ---------- LOAD TRANSFER DETAILS ----------
        def load_transfer():
            tid = transfer_id_var.get().strip()

            if not tid.isdigit() or int(tid) <= 0:
                self.show_popup("Invalid ID", "Transfer ID must be a positive number!", "warning")
                return

            import requests
            try:
                res = requests.get(f"http://127.0.0.1:8000/admin/teacher-transfer/{tid}")

                if res.status_code != 200:
                    self.show_popup("Not Found", "No record found for this Transfer ID!", "info")
                    disable_approve()
                    for v in vars_dict.values():
                        v.set("")
                    return

                data = res.json()

                # Fill UI
                for key in vars_dict:
                    vars_dict[key].set(data.get(key))

                # status formatting
                vars_dict["status"].set("1" if data["status"] else "0")

                enable_approve()

            except:
                self.show_popup("Error", "Server not reachable!", "error")

        # ---------- APPROVE TRANSFER ----------
        def approve_transfer():
            tid = transfer_id_var.get().strip()
            import requests

            try:
                res = requests.post(
                f"http://127.0.0.1:8000/admin/teacher-transfer/approve/{tid}"
            )

                if res.status_code == 200:
                    self.show_popup("Success", "Transfer Approved Successfully!", "info")
                    self.change_screen(
                    "Transfer Approved Successfully!",
                    add_callback=self.load_approve_teacher_transfer_screen
                )
                else:
                    msg = res.json().get("detail", "Approval failed!")
                    self.show_popup("Failed", msg, "error")

            except:
                self.show_popup("Error", "Unable to approve transfer!", "error")
    

    # ==============================================================================
    # ------ STAFF OFFBOARDINGS/TRANSFERS/SEPERATIONS ------
    # ----- Button to Issue Separation to a staff -----
    def load_issue_staff_separation_screen(self):
        self.clear_content()

        # ---------- TITLE ----------
        tk.Label(
        self.content,
        text="Issue Staff Separation",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=20)

        # ---------- FIELDS ----------
        fields = [
        ("Staff ID", "staff_id"),
        ("Reason", "reason"),
        ("Remarks", "remarks"),
        ("Last Working Date (YYYY-MM-DD)", "separation_date")
        ]

        vars = {}

        for i, (label, key) in enumerate(fields):

            tk.Label(
            form, text=f"{label}:", font=("Arial", 14), bg="#ECF0F1"
            ).grid(row=i, column=0, padx=10, pady=8)

            vars[key] = tk.StringVar()

            # --- Calendar for separation date ---
            if key == "separation_date":
                entry = tk.Entry(form, textvariable=vars[key], font=("Arial", 14), width=28)
                entry.grid(row=i, column=1, padx=10, pady=6)

                tk.Button(
                form,
                text="Calendar",
                font=("Arial", 12),
                bg="white",
                relief="flat",
                command=lambda v=vars[key], b=entry: self.open_calendar_popup(b, v)
                ).grid(row=i, column=2, padx=5)
            else:
                entry = tk.Entry(form, textvariable=vars[key], font=("Arial", 14), width=30)
                entry.grid(row=i, column=1, padx=10, pady=6)

        # ---------- BACK BUTTON ----------
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,
        form_frame=form
        )

        # ---------- SUBMIT BUTTON ----------
        submit_btn = tk.Label(
        form,
        text="Issue Separation",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=10,
        width=20,
        cursor="arrow",
        relief="ridge"
        )
        submit_btn.grid(row=len(fields), column=0, columnspan=3, pady=20)

        # ---------- VALIDATION ----------
        def validate(*args):
            if all(vars[k].get().strip() for k in vars):
                submit_btn.config(bg="#000000", fg="white", cursor="arrow")
                submit_btn.bind("<Enter>", lambda e: submit_btn.config(bg="#222222"))
                submit_btn.bind("<Leave>", lambda e: submit_btn.config(bg="#000000"))
                submit_btn.bind("<Button-1>", lambda e: issue_separation())
            else:
                submit_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                submit_btn.unbind("<Enter>")
                submit_btn.unbind("<Leave>")
                submit_btn.unbind("<Button-1>")

        for v in vars.values():
            v.trace_add("write", validate)

        # ---------- SUBMIT FUNCTION ----------
        def issue_separation():

            # date format validation
            import re
            date_str = vars["separation_date"].get().strip()
            if not re.match(r"\d{4}-\d{2}-\d{2}$", date_str):
                self.show_popup("Invalid Date", "Date must be YYYY-MM-DD format!", "warning")
                return

            payload = {
            "staff_id": int(vars["staff_id"].get().strip()),
            "reason": vars["reason"].get().strip(),
            "remarks": vars["remarks"].get().strip(),
            "separation_date": date_str
            }

            # ---- send to backend ----
            import requests
            res = requests.post("http://127.0.0.1:8000/admin/staff/separation/issue", json=payload)

            if res.status_code == 200:
                self.show_popup("Success", "Separation Issued Successfully!", "info")
                self.change_screen("Staff Separation Issued!", add_callback=self.load_issue_staff_separation_screen)
            else:
                msg = res.json().get("detail", "Error issuing separation")
                self.show_popup("Failed", msg, "error")

    # ==============================================================================
    # ----- Button to View all Separations in Queue -----
    def load_view_all_staff_separation_screen(self):
        self.clear_content()

        # ---------- TITLE ----------
        tk.Label(
        self.content,
        text="All Staff Separation Requests",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # ---------- BACK BUTTON ----------
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)

        self.create_back_button(
        parent=back_frame,
        go_back_callback=self.load_dashboard,
        form_frame=None
        )

        # ---------- TABLE FRAME ----------
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # ------- TABLE COLUMNS -------
        cols = ("sep_id", "staff_id", "separation_date", "reason", "status")

        # ------- FILTER BAR -------
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=10)

        tk.Label(
        filter_frame,
        text="Sort By:",
        font=("Arial", 12, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).grid(row=0, column=0, padx=5)

        filter_var = tk.StringVar()
        filter_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=list(cols),
        state="readonly",
        width=20
        )
        filter_dropdown.grid(row=0, column=1, padx=10)

        filter_val_var = tk.StringVar()
        filter_val = tk.Entry(
        filter_frame,
        textvariable=filter_val_var,
        font=("Arial", 12),
        width=25
        )
        filter_val.grid(row=0, column=2, padx=10)

        # ----- Black Button Styling -----
        def style_button(btn):
            btn.config(
            bg="#000000",
            fg="white",
            padx=15,
            pady=5,
            width=10,
            relief="raised",
            cursor="arrow",
            font=("Arial", 12, "bold")
            )
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

        load_btn = tk.Label(filter_frame, text="Load")
        style_button(load_btn)
        load_btn.grid(row=0, column=3, padx=10)

        load_all_btn = tk.Label(filter_frame, text="Load All")
        style_button(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

        # ---------- SCROLLBARS ----------
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        # ---------- TREEVIEW TABLE ----------
        self.sep_tree = ttk.Treeview(
        table_frame,
        columns=cols,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
        )
        self.sep_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.sep_tree.yview)
        x_scroll.config(command=self.sep_tree.xview)

        for col in cols:
            self.sep_tree.heading(col, text=col.replace("_", " ").title())
            self.sep_tree.column(col, width=180, anchor="center")

        # ---------- FETCH DATA FROM BACKEND ----------
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admin/staff/separation/all")
            self.all_separations = res.json() if res.status_code == 200 else []

            # Structure for validation
            self.sep_column_values = {
            "sep_id": [str(r["sep_id"]) for r in self.all_separations],
            "staff_id": [str(r["staff_id"]) for r in self.all_separations],
            "separation_date": [r["separation_date"] for r in self.all_separations],
            "reason": [r["reason"] for r in self.all_separations],
            "status": [1 if r["status"] else 0 for r in self.all_separations]
            }
        except:
            self.all_separations = []

        # ---------- UPDATE TABLE ----------
        def update_table(data):
            for row in self.sep_tree.get_children():
                self.sep_tree.delete(row)

            for row in data:
                self.sep_tree.insert(
                "",
                "end",
                values=(
                    row["sep_id"],
                    row["staff_id"],
                    row["separation_date"],
                    row["reason"],
                    1 if row["status"] else 0
                )
            )

        # ---------- FILTER FUNCTION ----------
        def load_filtered():
            col = filter_var.get().strip()
            val = filter_val.get().strip().lower()

            if not col or not val:
                return

            valid_list = self.sep_column_values.get(col, [])
            valid_lower = [str(v).lower() for v in valid_list]

            if val not in valid_lower:
                self.show_popup(
                "Invalid Search",
                f"'{val}' not found in '{col}'.",
                "warning"
                )
                filter_val_var.set("")
                return

            filtered = [
            r for r in self.all_separations
            if str(r[col]).lower() == val
            ]
            update_table(filtered)

        def load_all():
            update_table(self.all_separations)

        load_btn.bind("<Button-1>", lambda e: load_filtered())
        load_all_btn.bind("<Button-1>", lambda e: load_all())

        # INITIAL LOAD
        update_table(self.all_separations)
    

    # ==============================================================================
    # ----- Button to Approve Separations by ID -----
    def load_approve_staff_separation_screen(self):
        self.clear_content()
 
        # ---------- TITLE ----------
        tk.Label(
        self.content,
        text="Approve Staff Separation",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=25)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # ---------- SEPARATION ID INPUT ----------
        tk.Label(
        form,
        text="Separation ID:",
        font=("Arial", 14),
        bg="#ECF0F1"
        ).grid(row=0, column=0, padx=10, pady=10)

        sep_id_var = tk.StringVar()
        sep_entry = tk.Entry(form, textvariable=sep_id_var, font=("Arial", 14), width=25)
        sep_entry.grid(row=0, column=1, padx=10, pady=10)

        # ---------- LOAD BUTTON ----------
        load_btn = tk.Label(
        form,
        text="Load",
        font=("Arial", 12, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=15, pady=5,
        width=12,
        relief="ridge",
        cursor="arrow"
        )
        load_btn.grid(row=0, column=2, padx=10)

        # Enable/Disable Load Button
        def validate_load(*args):
            if sep_id_var.get().strip():
                load_btn.config(bg="#000000", fg="white", cursor="hand2")
                load_btn.bind("<Enter>", lambda e: load_btn.config(bg="#222222"))
                load_btn.bind("<Leave>", lambda e: load_btn.config(bg="#000000"))
                load_btn.bind("<Button-1>", lambda e: load_separation())
            else:
                load_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                load_btn.unbind("<Enter>")
                load_btn.unbind("<Leave>")
                load_btn.unbind("<Button-1>")

        sep_id_var.trace_add("write", validate_load)

        # ---------- OUTPUT PANEL ----------
        output_frame = tk.Frame(self.content, bg="#ECF0F1")
        output_frame.pack(pady=20)

        fields = ["staff_id", "separation_date", "reason", "remarks", "status"]
        vars_dict = {}

        for i, label in enumerate(fields):
            tk.Label(
            output_frame,
            text=f"{label.replace('_',' ').title()}:",
            font=("Arial", 14),
            bg="#ECF0F1"
            ).grid(row=i, column=0, padx=10, pady=6, sticky="w")

            var = tk.StringVar()
            entry = tk.Entry(
            output_frame,
            textvariable=var,
            font=("Arial", 14),
            width=30,
            state="disabled",
            disabledbackground="#F2F3F4",
            disabledforeground="black"
            )
            entry.grid(row=i, column=1, padx=10, pady=6)
            vars_dict[label] = var

        # ---------- BUTTON ROW ----------
        btn_row = tk.Frame(self.content, bg="#ECF0F1")
        btn_row.pack(pady=30)

        self.create_back_button(btn_row, self.load_dashboard, form)

        # ---------- APPROVE BUTTON ----------
        approve_btn = tk.Label(
        self.content,
        text="Approve Separation",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=10,
        width=18,
        relief="ridge",
        cursor="arrow"
        )
        approve_btn.pack(pady=20)

        def enable_approve():
            approve_btn.config(bg="#000000", fg="white", cursor="hand2")
            approve_btn.bind("<Enter>", lambda e: approve_btn.config(bg="#222222"))
            approve_btn.bind("<Leave>", lambda e: approve_btn.config(bg="#000000"))
            approve_btn.bind("<Button-1>", lambda e: approve_separation())

        def disable_approve():
            approve_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            approve_btn.unbind("<Enter>")
            approve_btn.unbind("<Leave>")
            approve_btn.unbind("<Button-1>")

        disable_approve()

        # ---------- LOAD SEPARATION DETAILS ----------
        def load_separation():
            sep_id = sep_id_var.get().strip()

            if not sep_id.isdigit() or int(sep_id) <= 0:
                self.show_popup("Invalid ID", "Separation ID must be a positive number!", "warning")
                return

            import requests
            try:
                res = requests.get(f"http://127.0.0.1:8000/admin/staff/separation/{sep_id}")

                if res.status_code != 200:
                    self.show_popup("Not Found", "Separation record not found!", "info")
                    disable_approve()
                    for v in vars_dict.values():
                        v.set("")
                    return

                data = res.json()

                # set values
                vars_dict["staff_id"].set(data["staff_id"])
                vars_dict["separation_date"].set(data["separation_date"])
                vars_dict["reason"].set(data["reason"])
                vars_dict["status"].set("1" if data["status"] else "0")

                enable_approve()

            except Exception:
                self.show_popup("Error", "Server not reachable!", "error")

        # ---------- APPROVE SEPARATION ----------
        def approve_separation():
            sep_id = sep_id_var.get().strip()

            import requests
            try:
                res = requests.post(f"http://127.0.0.1:8000/admin/staff/separation/approve/{sep_id}")

                if res.status_code == 200:
                    msg = "Staff Separation Approved Successfully!"
                    self.show_popup("Success", msg, "info")
                    self.change_screen(msg, add_callback=self.load_approve_staff_separation_screen)
                else:
                    self.show_popup("Failed", "Approval failed!", "error")

            except Exception:
                self.show_popup("Error", "Unable to approve separation!", "error")

    # ==============================================================================
    # ----- Button Create a Transfer Request for a staff Member -----
    def load_create_staff_transfer_screen(self):
        self.clear_content()

        # ---- TITLE ----
        tk.Label(
        self.content,
        text="Create Staff Transfer Request",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # ---- FORM FRAME ----
        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=15)

        fields = [
        ("Staff ID", "staff_id"),
        ("New Department", "new_department"),
        ("New Role", "new_role"),
        ("Request Date (YYYY-MM-DD)", "request_date"),
        ]

        self.tf_vars = {}

        for i, (label, key) in enumerate(fields):

            tk.Label(
            form, text=f"{label}:", font=("Arial", 14), bg="#ECF0F1"
            ).grid(row=i, column=0, padx=10, pady=8, sticky="e")
 
            var = tk.StringVar()
            self.tf_vars[key] = var

            entry = tk.Entry(
            form, textvariable=var, font=("Arial", 14), width=28
            )
            entry.grid(row=i, column=1, padx=10, pady=8)

            # Calendar only for request_date
            if key == "request_date":
                tk.Button(
                form,
                text="Calendar",
                font=("Arial", 12),
                bg="white",
                relief="ridge",
                command=lambda e=entry, v=var: self.open_calendar_popup(e, v)
                ).grid(row=i, column=2, padx=5)

        # ---- BACK BUTTON ----
        btn_row = tk.Frame(self.content, bg="#ECF0F1")
        btn_row.pack(pady=20)

        self.create_back_button(
        parent=btn_row,
        go_back_callback=self.load_dashboard,
        form_frame=form
        )

        # ---- SUBMIT BUTTON ----
        submit_btn = tk.Label(
        self.content,
        text="Create Transfer Request",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=12,
        width=22,
        relief="ridge",
        cursor="arrow"
        )
        submit_btn.pack(pady=20)

        # ---------- ENABLE/DISABLE ----------
        def enable():
            submit_btn.config(bg="#000000", fg="white", cursor="hand2")
            submit_btn.bind("<Enter>", lambda e: submit_btn.config(bg="#222222"))
            submit_btn.bind("<Leave>", lambda e: submit_btn.config(bg="#000000"))
            submit_btn.bind("<Button-1>", lambda e: submit_request())

        def disable():
            submit_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            submit_btn.unbind("<Enter>")
            submit_btn.unbind("<Leave>")
            submit_btn.unbind("<Button-1>")

        disable()

        # ---------- VALIDATION ----------
        import re
        def validate(*args):
            data = {k: v.get().strip() for k, v in self.tf_vars.items()}

            if not data["staff_id"].isdigit():
                disable()
                return
            
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", data["request_date"]):
                disable()
                return

            enable()

        for v in self.tf_vars.values():
            v.trace_add("write", validate)

        # ---------- SUBMIT FUNCTION ----------
        def submit_request():
            data = {k: v.get().strip() for k, v in self.tf_vars.items()}

            # Required fields
            if not data["staff_id"] or not data["request_date"]:
                self.show_popup("Missing Data", "Staff ID and Request Date are required", "warning")
                return

            payload = {
            "staff_id": int(data["staff_id"]),
            "new_department": data["new_department"] if data["new_department"] else None,
            "new_role": data["new_role"] if data["new_role"] else None,
            "request_date": data["request_date"]
            }

            import requests
            try:
                res = requests.post(
                "http://127.0.0.1:8000/admin/staff-transfer/request",
                json=payload
                )

                if res.status_code == 200:
                    self.show_popup("Success", "Transfer Request Added to Queue!", "info")
                    self.change_screen(
                    "Transfer Request Created!",
                    add_callback=self.load_create_staff_transfer_screen
                    )
                else:
                    msg = res.json().get("detail", "Error occurred")
                    self.show_popup("Failed", msg, "error")

            except Exception as e:
                self.show_popup("Error", str(e), "error")


    # ==============================================================================
    # ----- Button to View all Transfer Requests in Queue -----
    def load_view_all_staff_transfers_screen(self):
        self.clear_content()

        # ----- TITLE -----
        tk.Label(
        self.content,
        text="All Staff Transfer Requests",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # -------- BACK BUTTON --------
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)
        self.create_back_button(back_frame, self.load_dashboard, None)

        # -------- TABLE FRAME --------
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # ---- TABLE COLUMNS (MATCHING StaffTransfer MODEL) ----
        cols = (
        "transfer_id",
        "staff_id",
        "old_department",
        "old_role",
        "new_department",
        "new_role",
        "request_date",
        "status"
        )

        # ====== FILTER BAR ======
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=10)

        tk.Label(
        filter_frame,
        text="Sort By:",
        font=("Arial", 12, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).grid(row=0, column=0, padx=5)

        filter_var = tk.StringVar()
        filter_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=list(cols),
        state="readonly",
        width=20
        )
        filter_dropdown.grid(row=0, column=1, padx=10)

        filter_val_var = tk.StringVar()
        filter_val = tk.Entry(
        filter_frame,
        textvariable=filter_val_var,
        font=("Arial", 12),
        width=25
        )
        filter_val.grid(row=0, column=2, padx=10)

        # ---- Button Styling ----
        def style_button(btn):
            btn.config(
            bg="#000000",
            fg="white",
            padx=15,
            pady=5,
            width=10,
            relief="raised",
            cursor="arrow",
            font=("Arial", 12, "bold")
            )
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

        load_btn = tk.Label(filter_frame, text="Load")
        style_button(load_btn)
        load_btn.grid(row=0, column=3, padx=10)

        load_all_btn = tk.Label(filter_frame, text="Load All")
        style_button(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

        # ------ TABLE + SCROLLBARS ------
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        self.transfer_tree = ttk.Treeview(
        table_frame,
        columns=cols,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
        )
        self.transfer_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.transfer_tree.yview)
        x_scroll.config(command=self.transfer_tree.xview)

        for col in cols:
            self.transfer_tree.heading(col, text=col.replace("_", " ").title())
            self.transfer_tree.column(col, width=180, anchor="center")

        # ----- BACKEND FETCH ------
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admin/staff-transfer/all")
            self.all_transfers = res.json() if res.status_code == 200 else []

            # For filter validation:
            self.transfer_column_values = {
            "transfer_id": [str(r["transfer_id"]) for r in self.all_transfers],
            "staff_id": [str(r["staff_id"]) for r in self.all_transfers],
            "old_department": [str(r["old_department"]) for r in self.all_transfers],
            "old_role": [str(r["old_role"]) for r in self.all_transfers],
            "new_department": [str(r["new_department"]) for r in self.all_transfers],
            "new_role": [str(r["new_role"]) for r in self.all_transfers],
            "request_date": [r["request_date"] for r in self.all_transfers],
            "status": [1 if r["status"] else 0 for r in self.all_transfers]
            }

        except:
            self.all_transfers = []

        # ------- UPDATE TABLE -------
        def update_table(data):
            for row in self.transfer_tree.get_children():
                self.transfer_tree.delete(row)

            for row in data:
                self.transfer_tree.insert(
                "",
                "end",
                values=(
                    row["transfer_id"],
                    row["staff_id"],
                    row["old_department"],
                    row["old_role"],
                    row["new_department"],
                    row["new_role"],
                    row["request_date"],
                    1 if row["status"] else 0
                )
            )

        # ------- FILTER FUNCTION -------
        def load_filtered():
            col = filter_var.get().strip()
            val = filter_val_var.get().strip().lower()

            if not col or not val:
                return

            valid_list = self.transfer_column_values.get(col, [])
            valid_lower = [str(v).lower() for v in valid_list]

            if val not in valid_lower:
                self.show_popup(
                "Invalid Search",
                f"'{val}' not found in column '{col}'.",
                "warning"
                )
                filter_val_var.set("")
                return

            filtered = [
                r for r in self.all_transfers
                if str(r[col]).lower() == val
            ]
            update_table(filtered)

        def load_all():
            update_table(self.all_transfers)

        load_btn.bind("<Button-1>", lambda e: load_filtered())
        load_all_btn.bind("<Button-1>", lambda e: load_all())

        # INITIAL LOAD
        update_table(self.all_transfers)

    # ==============================================================================  
    # ----- Button to Approve a Transfer Request of a Staff Member -----
    def load_approve_staff_transfer_screen(self):
        self.clear_content()

        # ----- TITLE -----
        tk.Label(
        self.content,
        text="Approve Staff Transfer Request",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=25)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # ---------- TRANSFER ID INPUT ----------
        tk.Label(form, text="Transfer ID:", font=("Arial", 14), bg="#ECF0F1").grid(
        row=0, column=0, padx=10, pady=10
        )

        transfer_id_var = tk.StringVar()
        transfer_id_entry = tk.Entry(form, textvariable=transfer_id_var,
                                 font=("Arial", 14), width=25)
        transfer_id_entry.grid(row=0, column=1, padx=10, pady=10)

        # ---------- LOAD BUTTON ----------
        load_btn = tk.Label(
        form,
        text="Load",
        font=("Arial", 12, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=15, pady=5,
        width=12,
        relief="ridge",
        cursor="arrow"
        )
        load_btn.grid(row=0, column=2, padx=10)

        # Enable/Disable LOAD button
        def validate_load(*args):
            if transfer_id_var.get().strip():
                load_btn.config(bg="#000000", fg="white", cursor="hand2")
                load_btn.bind("<Enter>", lambda e: load_btn.config(bg="#222222"))
                load_btn.bind("<Leave>", lambda e: load_btn.config(bg="#000000"))
                load_btn.bind("<Button-1>", lambda e: load_transfer())
            else:
                load_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                load_btn.unbind("<Enter>")
                load_btn.unbind("<Leave>")
                load_btn.unbind("<Button-1>")

        transfer_id_var.trace_add("write", validate_load)

        # ---------- OUTPUT PANEL ----------
        output_frame = tk.Frame(self.content, bg="#ECF0F1")
        output_frame.pack(pady=20)

        fields = [
        "staff_id",
        "old_department", "new_department",
        "old_role", "new_role",
        "request_date", "status"
        ]
    
        vars_dict = {}

        for i, label in enumerate(fields):
            tk.Label(
            output_frame,
            text=f"{label.replace('_',' ').title()}:",
            font=("Arial", 14),
            bg="#ECF0F1"
            ).grid(row=i, column=0, padx=10, pady=6, sticky="w")

            var = tk.StringVar()
            entry = tk.Entry(
            output_frame,
            textvariable=var,
            font=("Arial", 14),
            width=30,
            state="disabled",
            disabledbackground="#F2F3F4",
            disabledforeground="black"
            )
            entry.grid(row=i, column=1, padx=10, pady=6)
            vars_dict[label] = var

        # ---------- BACK BUTTON ----------
        btn_row = tk.Frame(self.content, bg="#ECF0F1")
        btn_row.pack(pady=30)

        self.create_back_button(
        parent=btn_row,
        go_back_callback=self.load_dashboard,
        form_frame=form
        )

        # ---------- APPROVE BUTTON ----------
        approve_btn = tk.Label(
        self.content,
        text="Approve Transfer",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=10,
        width=18,
        relief="ridge",
        cursor="arrow"
        )
        approve_btn.pack(pady=20)

        def enable_approve():
            approve_btn.config(bg="#000000", fg="white", cursor="hand2")
            approve_btn.bind("<Enter>", lambda e: approve_btn.config(bg="#222222"))
            approve_btn.bind("<Leave>", lambda e: approve_btn.config(bg="#000000"))
            approve_btn.bind("<Button-1>", lambda e: approve_transfer())

        def disable_approve():
            approve_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            approve_btn.unbind("<Enter>")
            approve_btn.unbind("<Leave>")
            approve_btn.unbind("<Button-1>")

        disable_approve()

        # ---------- LOAD TRANSFER DETAILS ----------
        def load_transfer():
            tid = transfer_id_var.get().strip()

            if not tid.isdigit() or int(tid) <= 0:
                self.show_popup("Invalid ID", "Transfer ID must be a positive number!", "warning")
                return

            import requests
            try:
                res = requests.get(f"http://127.0.0.1:8000/admin/staff-transfer/{tid}")

                if res.status_code != 200:
                    self.show_popup("Not Found", "No record found for this Transfer ID!", "info")
                    disable_approve()
                    for v in vars_dict.values():
                        v.set("")
                    return

                data = res.json()

                # Fill UI
                for key in vars_dict:
                    vars_dict[key].set(data.get(key))

                # status formatting
                vars_dict["status"].set("1" if data["status"] else "0")

                enable_approve()

            except:
                self.show_popup("Error", "Server not reachable!", "error")

        # ---------- APPROVE TRANSFER ----------
        def approve_transfer():
            tid = transfer_id_var.get().strip()
            import requests

            try:
                res = requests.post(
                f"http://127.0.0.1:8000/admin/staff-transfer/approve/{tid}"
                )

                if res.status_code == 200:
                    self.show_popup("Success", "Transfer Approved Successfully!", "info")
                    self.change_screen(
                    "Transfer Approved Successfully!",
                    add_callback=self.load_approve_staff_transfer_screen
                    )
                else:
                    msg = res.json().get("detail", "Approval failed!")
                    self.show_popup("Failed", msg, "error")

            except:
                self.show_popup("Error", "Unable to approve transfer!", "error")
    
    # ==============================================================================
    # ====== STAFF's ATTENDANCE ======
    # ----- Button to View all Staff's Attendance ------
    def load_view_all_staff_attendance(self):
        self.clear_content()

        # ---- Title ----
        tk.Label(
        self.content,
        text="All Staff Attendance Records",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # ---- Back Button ----
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)
        self.create_back_button(back_frame, self.load_dashboard, None)

        # ---- Table Frame ----
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Columns
        cols = ("record_id", "staff_id", "date", "status", "remarks")

        # ----- FILTER BAR (Dropdown + Entry + Black Buttons) -----
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=10)

        tk.Label(
        filter_frame,
        text="Sort By:",
        font=("Arial", 12, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).grid(row=0, column=0, padx=5)

        filter_var = tk.StringVar()
        filter_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=list(cols),
        state="readonly",
        width=18
        )
        filter_dropdown.grid(row=0, column=1, padx=10)

        filter_value_var = tk.StringVar()
        filter_value = tk.Entry(
            filter_frame,
            textvariable=filter_value_var,
            font=("Arial", 12),
             width=20
        )
        filter_value.grid(row=0, column=2, padx=10)

        # ---------- Button Style ----------
        def style_button(btn):
            btn.config(
            bg="#000000",
            fg="white",
            padx=15,
            pady=5,
            width=10,
            relief="raised",
            cursor="hand2",
            font=("Arial", 12, "bold")
            )
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

        # LOAD Button
        load_btn = tk.Label(filter_frame, text="Load")
        style_button(load_btn)
        load_btn.grid(row=0, column=3, padx=10)

        # LOAD ALL Button
        load_all_btn = tk.Label(filter_frame, text="Load All")
        style_button(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

        # ---- Scrollbars ----
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        # ---- TABLE ----
        self.staff_tree = ttk.Treeview(
        table_frame,
        columns=cols,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set,
        height=18
        )
        self.staff_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.staff_tree.yview)
        x_scroll.config(command=self.staff_tree.xview)

        # Column Widths
        widths = {
        "record_id": 120,
        "staff_id": 120,
        "date": 150,
        "status": 100,
        "remarks": 220,
        }

        for col in cols:
            self.staff_tree.heading(col, text=col.replace("_", " ").title())
            self.staff_tree.column(col, width=widths[col], anchor="center")

        # ---- FETCH BACKEND DATA ----
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admin/attendance/staff")
            self.all_staff_att = res.json() if res.status_code == 200 else []
            self.column_values_staff_att = {
                "record_id":   [str(r["record_id"]) for r in self.all_staff_att],
                "staff_id":  [str(r["staff_id"]) for r in self.all_staff_att],
                "date":        [r["date"] for r in self.all_staff_att],
                "status":      [r["status"] for r in self.all_staff_att],
                "remarks":     [r["remarks"] for r in self.all_staff_att],
            }
        except:
            self.all_staff_att = []

        # ---- UPDATE TABLE ----
        def update_table(data):
            for r in self.staff_tree.get_children():
                self.staff_tree.delete(r)

            for row in data:
                self.staff_tree.insert(
                "",
                "end",
                values=(
                    row["record_id"],
                    row["staff_id"],
                    row["date"],
                    row["status"],
                    row.get("remarks", "")
                )
            )

        # ---- FILTER LOGIC ----
        def load_filtered():
            col = filter_var.get().strip()
            val = filter_value.get().strip()

            if not col or not val:
                return
            valid_list = self.column_values_staff_att.get(col, [])
            valid_lower = [str(v).lower() for v in valid_list]

            if val not in valid_lower:
                self.show_popup(
                "Invalid Search Value",
                f"'{val}' not found in column '{col}'.",
                "warning"
            )
                filter_value_var.set("")
                return
            filtered = [
            r for r in self.all_staff_att
            if str(r[col]).lower() == val.lower()
            ]
            update_table(filtered)

        def load_all():
            update_table(self.all_staff_att)

        load_btn.bind("<Button-1>", lambda e: load_filtered())
        load_all_btn.bind("<Button-1>", lambda e: load_all())

    # ---- INITIAL LOAD ----
        update_table(self.all_staff_att)

    # ==============================================================================
    # ----- Button to View Staff Attendance by ID -----
    def load_view_staff_attendance_by_id(self):
        self.clear_content()

        title = tk.Label(
        self.content,
        text="View Staff Attendance by Record ID",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        )
        title.pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=20)

        # ===== record ID input =====
        tk.Label(form, text="Record ID:", font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=0, padx=10, pady=8)

        rec_var = tk.StringVar()
        rec_entry = tk.Entry(form, textvariable=rec_var, font=("Arial", 14), width=25)
        rec_entry.grid(row=0, column=1, padx=10, pady=8)
        
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

        # Back Button from global function
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,    
        form_frame=form                          
        )
        # ===== Search Button (Label style) =====
        search_btn = tk.Label(
        form,
        text="Search",
        font=("Arial", 12, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=15,
        pady=5,
        width=12,
        relief="ridge",
        cursor="arrow"
        )
        search_btn.grid(row=0, column=2, padx=10)

        # ====== Output fields ======
        tk.Label(form, text="Staff ID:", font=("Arial", 14), bg="#ECF0F1").grid(row=1, column=0, padx=10, pady=8)
        tk_id = tk.Entry(form, font=("Arial", 14), width=25, state="disabled")
        tk_id.grid(row=1, column=1, padx=10, pady=8)

        tk.Label(form, text="Date:", font=("Arial", 14), bg="#ECF0F1").grid(row=2, column=0, padx=10, pady=8)
        date_entry = tk.Entry(form, font=("Arial", 14), width=25, state="disabled")
        date_entry.grid(row=2, column=1, padx=10, pady=8)

        tk.Label(form, text="Status:", font=("Arial", 14), bg="#ECF0F1").grid(row=3, column=0, padx=10, pady=8)
        status_entry = tk.Entry(form, font=("Arial", 14), width=25, state="disabled")
        status_entry.grid(row=3, column=1, padx=10, pady=8)

        tk.Label(form, text="Remarks:", font=("Arial", 14), bg="#ECF0F1").grid(row=4, column=0, padx=10, pady=8)
        remarks_entry = tk.Entry(form, font=("Arial", 14), width=25, state="disabled")
        remarks_entry.grid(row=4, column=1, padx=10, pady=8)

        tk.Label(form, text="Record ID:", font=("Arial", 14), bg="#ECF0F1").grid(row=5, column=0, padx=10, pady=8)
        rec_id_entry = tk.Entry(form, font=("Arial", 14), width=25, state="disabled")
        rec_id_entry.grid(row=5, column=1, padx=10, pady=8)

        # ===== ENABLE / DISABLE SEARCH BUTTON =====
        def validate_search_btn(*args):
            if rec_var.get().strip():
                search_btn.config(bg="#000000", fg="white", cursor="hand2")
                search_btn.bind("<Enter>", lambda e: search_btn.config(bg="#222222"))
                search_btn.bind("<Leave>", lambda e: search_btn.config(bg="#000000"))

                search_btn.bind("<Button-1>", lambda e: fetch_attendance())
            else:
                search_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                search_btn.unbind("<Enter>")
                search_btn.unbind("<Leave>")
                search_btn.unbind("<Button-1>")

        rec_var.trace_add("write", validate_search_btn)

        # ===== FETCH DATA FROM BACKEND =====
        def fetch_attendance():
            record_id = rec_var.get().strip()
            if not record_id:
                self.show_popup(
                    "Missing Input",
                    "Please enter a Record ID.",
                    "warning"
                )
                return
            if not record_id.isdigit() or int(record_id) <= 0:
                self.show_popup(
                    "Invalid Record ID",
                    "Record ID must be a positive number.",
                    "warning"
                )
                return
            import requests
            try:
                res = requests.get(f"http://127.0.0.1:8000/admin/attendance/staff/{record_id}")

                if res.status_code == 200:
                    data = res.json()

                    # Enable all entries
                    for box in (tk_id, date_entry, status_entry, remarks_entry, rec_id_entry):
                        box.config(state="normal")

                    # Clear previous values
                    tk_id.delete(0, "end")
                    date_entry.delete(0, "end")
                    status_entry.delete(0, "end")
                    remarks_entry.delete(0, "end")
                    rec_id_entry.delete(0, "end")

                    # Fill new data
                    tk_id.insert(0, data["staff_id"])
                    date_entry.insert(0, data["date"])
                    status_entry.insert(0, data["status"])
                    remarks_entry.insert(0, data.get("remarks", ""))
                    rec_id_entry.insert(0, data.get("record_id", ""))

                    # Disable them again
                    for box in (tk_id, date_entry, status_entry, remarks_entry, rec_id_entry):
                        box.config(state="disabled")

                else:
                    self.show_popup(
                        "Not Found",
                        f"No attendance record found for ID {record_id}.",
                        "error"
                    )
                    return

            except Exception as e:
                self.show_popup(
                    "Backend Error",
                    f"Something went wrong.\nError: {e}",
                    "error"
                )
                return

    # ==============================================================================
    # ----- Button to View Summary of Staff Attendance by Staff ID -----
    def load_staff_attendance_summary_screen(self):
        self.clear_content()

        title = tk.Label(
        self.content,
        text="Staff Attendance Summary",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        )
        title.pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # ===== Inputs =====
        tk.Label(form, text="Staff ID:", font=("Arial", 14), bg="#ECF0F1")\
            .grid(row=0, column=0, padx=10, pady=8)
        sid_var = tk.StringVar()
        sid_entry = tk.Entry(form, textvariable=sid_var, font=("Arial", 14), width=25)
        sid_entry.grid(row=0, column=1, padx=10, pady=8)

        # ---- FROM DATE ----
        tk.Label(
            form,
            text="From Date (YYYY-MM-DD):",
            font=("Arial", 14),
            bg="#ECF0F1"
            ).grid(row=1, column=0, padx=10, pady=8)

        from_var = tk.StringVar()
        from_entry = tk.Entry(form, textvariable=from_var, font=("Arial", 14), width=20)
        from_entry.grid(row=1, column=1, padx=5, pady=8)

        tk.Button(
            form,
            text="Calendar",
            font=("Arial", 12),
            bg="white",
            relief="flat",
            command=lambda v=from_var, e=from_entry: self.open_calendar_popup(e, v)
        ).grid(row=1, column=2, padx=5)


        # ---- TO DATE ----
        tk.Label(
            form,
            text="To Date (YYYY-MM-DD):",
            font=("Arial", 14),
            bg="#ECF0F1"
        ).grid(row=2, column=0, padx=10, pady=8)

        to_var = tk.StringVar()
        to_entry = tk.Entry(form, textvariable=to_var, font=("Arial", 14), width=20)
        to_entry.grid(row=2, column=1, padx=5, pady=8)

        tk.Button(
            form,
            text="Calendar",
            font=("Arial", 12),
            bg="white",
            relief="flat",
            command=lambda v=to_var, e=to_entry: self.open_calendar_popup(e, v)
        ).grid(row=2, column=2, padx=5)

        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

        # Back Button from global function
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,    
        form_frame=form                          
        )
        # ===== Submit Button =====
        summary_btn = tk.Label(
        form,
        text="Get Summary",
        font=("Arial", 12, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        relief="ridge",
        padx=15,
        pady=5,
        width=14,
        cursor="arrow"
        )
        summary_btn.grid(row=3, column=1, pady=15)

        # ===== OUTPUT FRAME =====
        output = tk.Frame(self.content, bg="#ECF0F1")
        output.pack(pady=20)

        labels = {}
        for i, field in enumerate(["Staff ID", "Total Days", "Present", "Absent", "Leave", "Percentage"]):
            labels[field] = tk.Label(output, text=f"{field}: -", font=("Arial", 16), bg="#ECF0F1", fg="#2C3E50")
            labels[field].pack(anchor="w", padx=30, pady=3)

        # ===== Enable Button on Input =====
        def validate_btn(*args):
            if sid_var.get().strip() and from_var.get().strip() and to_var.get().strip():
                summary_btn.config(bg="#000000", fg="white", cursor="hand2")
                summary_btn.bind("<Enter>", lambda e: summary_btn.config(bg="#222222"))
                summary_btn.bind("<Leave>", lambda e: summary_btn.config(bg="#000000"))
                summary_btn.bind("<Button-1>", lambda e: fetch_summary())
            else:
                summary_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                summary_btn.unbind("<Enter>")
                summary_btn.unbind("<Leave>")
                summary_btn.unbind("<Button-1>")

        sid_var.trace_add("write", validate_btn)
        from_var.trace_add("write", validate_btn)
        to_var.trace_add("write", validate_btn)

        # ===== BACKEND CALL =====
        def fetch_summary():
            staff_id = sid_var.get().strip()
            date_from = from_var.get().strip()
            date_to = to_var.get().strip()
            if not staff_id:
                self.show_popup(
                    "Missing Input",
                    "Staff ID cannot be empty.",
                    "warning"
                )
                return

            # Staff ID must be a positive integer
            if not staff_id.isdigit() or int(staff_id) <= 0:
                self.show_popup(
                    "Invalid Staff ID",
                    "Staff ID must be a positive number.",
                    "warning"
                )
                return

            # Date From empty
            if not date_from:
                self.show_popup(
                    "Missing Date",
                    "Please enter a 'From' date.",
                    "warning"
                )
                return

            # Date To empty
            if not date_to:
                self.show_popup(
                    "Missing Date",
                    "Please enter a 'To' date.",
                    "warning"
                )
                return

            # Date format validation
            import re
            date_pattern = r"^\d{4}-\d{2}-\d{2}$"

            if not re.match(date_pattern, date_from):
                self.show_popup(
                    "Invalid Date Format",
                    "From Date must be in YYYY-MM-DD format.",
                    "error"
                )
                return

            import requests
            url = (
                f"http://127.0.0.1:8000/admin/attendance/staff/summary/{staff_id}"
                f"?date_from={date_from}"
                f"&date_to={date_to}"
            )

            try:
                res = requests.get(url)     
                if res.status_code != 200:
                    res = requests.get(url)
                    self.show_popup(
                            "Not Found",
                            "Staff member not found or no summary available for given date range.",
                            "error"
                    )
                    return
                data = res.json()
                
                labels["Staff ID"].config(text=f"Staff ID: {data['staff_id']}")
                labels["Total Days"].config(text=f"Total Days: {data['total_days']}")
                labels["Present"].config(text=f"Present: {data['present']}")
                labels["Absent"].config(text=f"Absent: {data['absent']}")
                labels["Leave"].config(text=f"Leave: {data['leave']}")
                labels["Percentage"].config(text=f"Percentage: {data['percentage']}%")

            except Exception as e:
                self.show_popup(
                    "Backend Error",
                    f"Failed to fetch summary.\nError: {e}",
                    "error"
                )
                return

    # ==============================================================================
    # ----- Button to Update Staff's Attendance -----
    def load_update_staff_attendance_screen(self):
        self.clear_content()

        title = tk.Label(
        self.content,
        text="Update Staff Attendance",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        )
        title.pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=20)

        # ====== INPUT FIELDS ======
        tk.Label(form, text="Record ID:", font=("Arial", 14), bg="#ECF0F1")\
            .grid(row=0, column=0, padx=10, pady=8)
        record_var = tk.StringVar()
        record_entry = tk.Entry(form, textvariable=record_var, font=("Arial", 14), width=25)
        record_entry.grid(row=0, column=1, padx=10, pady=8)

        # ----- Load Button -----
        load_btn = tk.Label(
        form,
        text="Load",
        font=("Arial", 12, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        relief="ridge",
        width=12,
        padx=10, pady=5,
        cursor="arrow"
        )
        load_btn.grid(row=0, column=2, padx=12)

        # ==== Fields that get filled AFTER load ====
        fields = {
        "Staff ID": tk.StringVar(),
        "Date": tk.StringVar(),
        "Status": tk.StringVar(),
        "Remarks": tk.StringVar()
        }
        row_index = 1
        entries = {}
        for label, var in fields.items():

            tk.Label(
                form,
                text=f"{label}:",
                font=("Arial", 14),
                bg="#ECF0F1"
            ).grid(row=row_index, column=0, padx=10, pady=8)

            # ---- DATE FIELD GETS SPECIAL TREATMENT ----
            if label == "Date":
                ent = tk.Entry(
                    form,
                    textvariable=var,
                    font=("Arial", 14),
                    width=20,
                    state="disabled"
                )
                ent.grid(row=row_index, column=1, padx=5, pady=8)

                # Calendar button
                cal_btn = tk.Button(
                    form,
                    text="Calendar",
                    font=("Arial", 12),
                    bg="white",
                    relief="flat",
                    command=lambda v=var, e=ent: self.open_calendar_popup(e, v)
                )
                cal_btn.grid(row=row_index, column=2, padx=5)

            else:
                # ---- NORMAL DISABLED ENTRY ----
                ent = tk.Entry(
                    form,
                    textvariable=var,
                    font=("Arial", 14),
                    width=25,
                    state="disabled"
                )
                ent.grid(row=row_index, column=1, padx=10, pady=8)

            entries[label] = ent
            row_index += 1
        
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

        # Back Button from global function
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,    
        form_frame=form                          
        )
        self.content.update_idletasks()

        # ====== UPDATE BUTTON ======
        update_btn = tk.Label(
        self.content,
        text="Update Attendance",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        relief="ridge",
        padx=20, pady=10,
        width=20,
        cursor="arrow"
        )
        update_btn.pack(pady=25)

        # ===== VALIDATION FOR LOAD BUTTON =====
        def validate_load(*args):
            if record_var.get().strip():
                load_btn.config(bg="#000000", fg="white", cursor="arrow")
                load_btn.bind("<Enter>", lambda e: load_btn.config(bg="#222222"))
                load_btn.bind("<Leave>", lambda e: load_btn.config(bg="#000000"))
                load_btn.bind("<Button-1>", lambda e: load_record())
            else:
                load_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                load_btn.unbind("<Enter>")
                load_btn.unbind("<Leave>")
                load_btn.unbind("<Button-1>")

        record_var.trace_add("write", validate_load)

        # ===== LOAD EXISTING RECORD =====
        def load_record():
            rec_id = record_var.get().strip()
            if not rec_id:
                self.show_popup("Missing Input", "Record ID cannot be empty!", "warning")
                return

            # Must be positive integer
            if not rec_id.isdigit() or int(rec_id) <= 0:
                self.show_popup("Invalid Record ID", "Record ID must be a positive number.", "warning")
                return

            import requests
            try:
                res = requests.get(f"http://127.0.0.1:8000/admin/attendance/staff/{rec_id}")
                if res.status_code != 200:
                    self.show_popup(
                        "Not Found",
                        f"No attendance record found for ID {rec_id}.",
                        "error"
                    )
                    return
                data = res.json()

                # Enable all input fields
                for ent in entries.values():
                    ent.config(state="normal")

                # Fill values
                fields["Staff ID"].set(data["staff_id"])
                fields["Date"].set(data["date"])
                fields["Status"].set(data["status"])
                fields["Remarks"].set(data.get("remarks", ""))

                enable_update_validation()

            except Exception as e:
                self.show_popup(
                    "Backend Error",
                    f"Could not fetch staff attendance.\nError: {e}",
                    "error"
                )

        # ===== VALIDATE ALL FIELDS BEFORE UPDATE =====
        def enable_update_validation():

            def validate_all(*args):
                if all(v.get().strip() for v in fields.values()):
                    update_btn.config(
                    bg="#000000", fg="white",
                    cursor="arrow"
                    )
                    update_btn.bind("<Enter>", lambda e: update_btn.config(bg="#222222"))
                    update_btn.bind("<Leave>", lambda e: update_btn.config(bg="#000000"))
                    update_btn.bind("<Button-1>", lambda e: submit_update())
                else:
                    update_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                    update_btn.unbind("<Enter>")
                    update_btn.unbind("<Leave>")
                    update_btn.unbind("<Button-1>")

            # Track all fields live
            for var in fields.values():
                var.trace_add("write", validate_all)

        # ===== SUBMIT UPDATE TO BACKEND =====
        def submit_update():
            rec_id = record_var.get().strip()

            if not rec_id:
                self.show_popup("Missing Record ID", "Please enter a Record ID!", "warning")
                return

            if not rec_id.isdigit() or int(rec_id) <= 0:
                self.show_popup("Invalid Record ID", "Record ID must be a positive number.", "warning")
                return
            
            staff_raw = fields["Staff ID"].get().strip()
            if not staff_raw.isdigit() or int(staff_raw) <= 0:
                self.show_popup("Invalid Staff ID", "Staff ID must be a positive number.", "warning")
                return
            staff_id = int(staff_raw)

            # Date
            date_val = fields["Date"].get().strip()
            import re
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_val):
                self.show_popup("Invalid Date", "Date must be in YYYY-MM-DD format!", "error")
                return

            # Status
            status_val = fields["Status"].get().strip().upper()
            if status_val not in ["P", "A", "L"]:
                self.show_popup("Invalid Status", "Status must be P, A, or L only!", "warning")
                return
            
            remarks_val = fields["Remarks"].get().strip()

            payload = {
            "staff_id": staff_id,
            "date": date_val,
            "status": status_val,
            "remarks": remarks_val
            }

            import requests
            rec_id = record_var.get().strip()
            try:
                res = requests.put(f"http://127.0.0.1:8000/admin/attendance/staff/update/{rec_id}", json=payload)
                if res.status_code == 200:
                    self.show_popup("Success", "Staff Attendance Updated Successfully!", "info")
                    self.change_screen("Staff Attendance Updated Successfully",
                            add_callback=self.load_update_staff_attendance_screen)   
                else:
                    msg = res.json().get("detail", "Update failed!")
                    self.show_popup("Error", msg, "error")
    
            except Exception as e:
                self.show_popup("Backend Error", f"Error updating data:\n{e}", "error")


    # ==============================================================================
    # ----- Button to Delete Staff's Attendance -----
    def load_delete_staff_attendance_screen(self):
        self.clear_content()

        title = tk.Label(
        self.content,
        text="Delete Staff Attendance",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        )
        title.pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=20)

        # ---- RECORD ID INPUT ----
        tk.Label(form, text="Record ID:", font=("Arial", 14), bg="#ECF0F1")\
            .grid(row=0, column=0, padx=10, pady=8)

        record_var = tk.StringVar()
        record_entry = tk.Entry(form, textvariable=record_var, font=("Arial", 14), width=25)
        record_entry.grid(row=0, column=1, padx=10, pady=8)

        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

        # Back Button from global function
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,    
        form_frame=form                          
        )
        self.content.update_idletasks()

        # ---- DELETE BUTTON ----
        delete_btn = tk.Label(
        self.content,
        text="Delete Attendance",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        relief="ridge",
        padx=20, pady=10,
        width=20,
        cursor="arrow"
        )
        delete_btn.pack(pady=25)

       # ===== VALIDATE DELETE BUTTON (Enable / Disable) =====
        def validate_delete(*args):
            if record_var.get().strip():
                delete_btn.config(bg="#000000", fg="white", cursor="arrow")

                # Hover
                delete_btn.bind("<Enter>", lambda e: delete_btn.config(bg="#222222"))
                delete_btn.bind("<Leave>", lambda e: delete_btn.config(bg="#000000"))

                # Click
                delete_btn.bind("<Button-1>", lambda e: submit_delete())

            else:
                delete_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                delete_btn.unbind("<Enter>")
                delete_btn.unbind("<Leave>")
                delete_btn.unbind("<Button-1>")

        record_var.trace_add("write", validate_delete)

        # ===== DELETE REQUEST TO BACKEND =====
        def submit_delete():
            rec_id = record_var.get().strip()
            if not rec_id:
                self.show_popup("Missing Record ID", "Please enter Record ID!", "warning")
                return

            if not rec_id.isdigit() or int(rec_id) <= 0:
                self.show_popup("Invalid Record ID",
                        "Record ID must be a positive number.",
                        "warning")
                return

            import requests
            try:
                url = f"http://127.0.0.1:8000/admin/attendance/staff/delete/{rec_id}"
                res = requests.delete(url)

                if res.status_code == 200:
                    self.show_popup("Success",
                            "Staff Attendance Deactivated Successfully!",
                            "info")
                    self.change_screen("Staff Attendance Deactivated Successfully",
                                       add_callback=self.load_delete_staff_attendance_screen)
                else:
                    msg = res.json().get("detail", "Record Not Found")
                    self.show_popup("Delete Failed", msg, "error")
                    return

            except Exception as e:
                self.show_popup("Backend Error",
                        f"Unable to delete record.\n{e}",
                        "error")


    # ==============================================================================
    # ===== STUDENT'S EXAMS/MARKS/RESULTS =====
    # ----- Button to Create an Exam Type -----
    def load_create_exam_type_screen(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="Create Exam Type",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # ---------- FORM FIELDS ----------
        fields = [
        ("Exam Name", "exam_name"),
        ("Description", "description"),
        ("Exam Date (YYYY-MM-DD)", "exam_date")
        ]

        vars = {}

        for i, (label, key) in enumerate(fields):
            tk.Label(
            form,
            text=f"{label}:",
            bg="#ECF0F1",
            font=("Arial", 14)
            ).grid(row=i, column=0, padx=10, pady=8, sticky="w")

            vars[key] = tk.StringVar()

            # Date field → calendar
            if key == "exam_date":
                entry = tk.Entry(form, textvariable=vars[key], font=("Arial", 14), width=28)
                entry.grid(row=i, column=1, padx=10, pady=6)

                tk.Button(
                form,
                text="Calendar",
                font=("Arial", 12),
                bg="white",
                relief="ridge",
                command=lambda v=vars[key], b=entry: self.open_calendar_popup(b, v)
            ).grid(row=i, column=2, padx=5)

            else:
                entry = tk.Entry(form, textvariable=vars[key], font=("Arial", 14), width=30)
                entry.grid(row=i, column=1, padx=10, pady=6)

        # ========== BACK BUTTON ==========
        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,
        form_frame=form
    )

        # ===== SUBMIT BUTTON =====
        submit_btn = tk.Label(
        self.content,
        text="Create Exam",
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

        # ---------- ENABLE / DISABLE ----------
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
   
        disable()

        # ---------- VALIDATION ----------
        import re

        def validate(*args):
            name = vars["exam_name"].get().strip()
            desc = vars["description"].get().strip()
            date = vars["exam_date"].get().strip()

            if not name or not desc:
                disable()
                return

            # Date format check
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
                disable()
                return

            enable()

        for v in vars.values():
            v.trace_add("write", validate)

        # ---------- SUBMIT FUNCTION ----------
        def submit():
            payload = {
            "exam_name": vars["exam_name"].get().strip(),
            "description": vars["description"].get().strip(),
            "exam_date": vars["exam_date"].get().strip(),
            }

            import requests
            try:
                res = requests.post(
                "http://127.0.0.1:8000/admin/exams/create",
                json=payload
            )

                if res.status_code == 200 or res.status_code == 201:
                    self.show_popup("Success", "Exam Created Successfully!", "info")
                    self.change_screen("Exam Created!", add_callback=self.load_create_exam_type_screen)
                else:
                    self.show_popup("Error", res.text, "error")

            except Exception as e:
                self.show_popup("Server Error", str(e), "error")

    
    # ==============================================================================
    # ----- Button to View all Exam Types -----
    def load_view_all_exams_screen(self):
        self.clear_content()

        # ----- TITLE -----
        tk.Label(
        self.content,
        text="All Exams",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # -------- BACK BUTTON --------
        back_frame = tk.Frame(self.content, bg="#ECF0F1")
        back_frame.pack(anchor="w", padx=20)
        self.create_back_button(back_frame, self.load_dashboard, None)

        # -------- TABLE FRAME --------
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # ---- EXAM TABLE COLUMNS ----
        cols = ("exam_id", "exam_name", "description", "exam_date")

        # ------ TABLE + SCROLLBARS ------
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        self.exam_tree = ttk.Treeview(
        table_frame,
        columns=cols,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
    )
        self.exam_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.exam_tree.yview)
        x_scroll.config(command=self.exam_tree.xview)

        for col in cols:
            self.exam_tree.heading(col, text=col.replace("_", " ").title())
            self.exam_tree.column(col, width=200, anchor="center")
        
        # ===== FILTER BAR AT BOTTOM =====
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=12)

        tk.Label(
        filter_frame,
        text="Sort By:",
        font=("Arial", 12, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).grid(row=0, column=0, padx=5)

        filter_var = tk.StringVar()
        sort_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=list(cols),
        state="readonly",
        width=18
    )
        sort_dropdown.grid(row=0, column=1, padx=10)

        filter_val_var = tk.StringVar()
        filter_val = tk.Entry(filter_frame, textvariable=filter_val_var,
                          font=("Arial", 12), width=25)
        filter_val.grid(row=0, column=2, padx=10)

        # BUTTON STYLE
        def style_button(btn):
            btn.config(
            bg="#000000",
            fg="white",
            padx=15,
            pady=5,
            width=10,
            relief="raised",
            cursor="arrow",
            font=("Arial", 12, "bold")
        )
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

        # LOAD BUTTON
        load_btn = tk.Label(filter_frame, text="Load")
        style_button(load_btn)
        load_btn.grid(row=0, column=3, padx=10)

        # LOAD ALL BUTTON
        load_all_btn = tk.Label(filter_frame, text="Load All")
        style_button(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

        # ----- FETCH FROM BACKEND -----
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admin/exams/all")
            self.exams = res.json() if res.status_code == 200 else []
        except:
            self.exams = []
            self.show_popup("Error", "Unable to load exams from server!", "error")

        # ------- FUNCTION TO UPDATE TABLE -------
        def update_table(data):
            for row in self.exam_tree.get_children():
                self.exam_tree.delete(row)

            for row in data:
                self.exam_tree.insert(
                "",
                "end",
                values=(
                    row["exam_id"],
                    row["exam_name"],
                    row["description"],
                    row["exam_date"]
                )
            )
        
        # ===== FILTER FUNCTION =====
        def load_filtered():
            col = filter_var.get().strip()
            val = filter_val.get().strip().lower()
            if not col or not val:
                return

            filtered = [
            r for r in self.exams
            if val in str(r[col]).lower()
        ]

            update_table(filtered)

        load_btn.bind("<Button-1>", lambda e: load_filtered())
        load_all_btn.bind("<Button-1>", lambda e: update_table(self.exams))

        update_table(self.exams)

        # INITIAL TABLE LOAD
        update_table(self.exams)

    # ==============================================================================
    # ----- Button to Update Exam by ID -----
    def load_update_exam_screen(self):
        self.clear_content()

        # ----- TITLE -----
        tk.Label(
        self.content,
        text="Update Exam Details",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=25)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # ================== INPUT → EXAM ID ====================
        tk.Label(form, text="Exam ID:", font=("Arial", 14), bg="#ECF0F1")\
        .grid(row=0, column=0, padx=10, pady=10)

        exam_id_var = tk.StringVar()
        exam_id_entry = tk.Entry(form, textvariable=exam_id_var, font=("Arial", 14), width=25)
        exam_id_entry.grid(row=0, column=1, padx=10)

        # ---------- LOAD BUTTON ----------
        load_btn = tk.Label(
        form,
        text="Load",
        font=("Arial", 12, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=15, pady=5,
        width=12,
        relief="ridge",
        cursor="arrow"
    )
        load_btn.grid(row=0, column=2, padx=10)

        # ---------- OUTPUT FIELDS ----------
        fields = ["exam_name", "description", "exam_date"]
        vars_dict = {}

        output_frame = tk.Frame(self.content, bg="#ECF0F1")
        output_frame.pack(pady=20)

        for i, label in enumerate(fields):
            tk.Label(
            output_frame,
            text=f"{label.replace('_',' ').title()}:",
            font=("Arial", 14),
            bg="#ECF0F1"
        ).grid(row=i, column=0, padx=10, pady=6, sticky="w")

            var = tk.StringVar()
            entry = tk.Entry(output_frame, textvariable=var, font=("Arial", 14), width=30)
            entry.grid(row=i, column=1, padx=10, pady=6)

            vars_dict[label] = var

        # Calendar button for exam_date
        tk.Button(
        output_frame,
        text="Calendar",
        font=("Arial", 12),
        bg="white",
        relief="ridge",
        command=lambda: self.open_calendar_popup(
            output_frame.grid_slaves(row=2, column=1)[0],
            vars_dict["exam_date"]
        )
    ).grid(row=2, column=2, padx=6)

        # ---------- BACK BUTTON ----------
        back_row = tk.Frame(self.content, bg="#ECF0F1")
        back_row.pack(pady=10)
        self.create_back_button(back_row, self.load_dashboard, form)

        # ---------- UPDATE BUTTON ----------
        update_btn = tk.Label(
        self.content,
        text="Update Exam",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=10,
        width=18,
        relief="ridge",
        cursor="arrow"
    )
        update_btn.pack(pady=15)

        # Disable button initially
        def disable_update():
            update_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            update_btn.unbind("<Enter>")
            update_btn.unbind("<Leave>")
            update_btn.unbind("<Button-1>")

        def enable_update():
            update_btn.config(bg="#000000", fg="white", cursor="hand2")
            update_btn.bind("<Enter>", lambda e: update_btn.config(bg="#222222"))
            update_btn.bind("<Leave>", lambda e: update_btn.config(bg="#000000"))
            update_btn.bind("<Button-1>", lambda e: update_exam())

        disable_update()

        # ---------- LOAD EXAM DETAILS ----------
        def load_exam():
            exam_id = exam_id_var.get().strip()

            if not exam_id.isdigit():
                self.show_popup("Invalid Input", "Exam ID must be a number!", "warning")
                disable_update()
                return

            import requests
            res = requests.get(f"http://127.0.0.1:8000/admin/exams/{exam_id}")

            if res.status_code != 200:
                self.show_popup("Not Found", "No exam found!", "info")
                disable_update()
                for v in vars_dict.values():
                    v.set("")
                return

            data = res.json()

            vars_dict["exam_name"].set(data["exam_name"])
            vars_dict["description"].set(data["description"])
            vars_dict["exam_date"].set(data["exam_date"])

            enable_update()

        # Bind to Load button
        def validate_load(*args):
            if exam_id_var.get().strip():
                load_btn.config(bg="#000000", fg="white", cursor="hand2")
                load_btn.bind("<Enter>", lambda e: load_btn.config(bg="#222222"))
                load_btn.bind("<Leave>", lambda e: load_btn.config(bg="#000000"))
                load_btn.bind("<Button-1>", lambda e: load_exam())
            else:
                load_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                load_btn.unbind("<Enter>")
                load_btn.unbind("<Leave>")
                load_btn.unbind("<Button-1>")

        exam_id_var.trace_add("write", validate_load)

        # ---------- UPDATE REQUEST ----------
        def update_exam():
            exam_id = exam_id_var.get().strip()

            payload = {
            "exam_name": vars_dict["exam_name"].get().strip(),
            "description": vars_dict["description"].get().strip(),
            "exam_date": vars_dict["exam_date"].get().strip()
        }

            import re
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", payload["exam_date"]):
                self.show_popup("Invalid Date", "Date must be YYYY-MM-DD!", "warning")
                return

            import requests
            res = requests.put(
            f"http://127.0.0.1:8000/admin/exams/update/{exam_id}",
            json=payload
        )

            if res.status_code == 200:
                self.show_popup("Success", "Exam Updated Successfully!", "info")
                self.change_screen(
                "Exam Updated Successfully!",
                add_callback=self.load_update_exam_screen
            )
            else:
                self.show_popup("Error", "Failed to update exam!", "error")

    # ==============================================================================
    # ----- Button to Delete Exam Type -----
    def load_delete_exam_screen(self):
        self.clear_content()

        # Title
        tk.Label(
        self.content,
        text="Delete Exam Type",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
    ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # Exam ID input
        tk.Label(
        form, text="Exam ID:", font=("Arial", 14), bg="#ECF0F1"
    ).grid(row=0, column=0, padx=10, pady=10)

        exam_id_var = tk.StringVar()
        tk.Entry(
        form, textvariable=exam_id_var, font=("Arial", 14), width=25
    ).grid(row=0, column=1, padx=10, pady=10)

        # Back button
        btn_row = tk.Frame(self.content, bg="#ECF0F1")
        btn_row.pack(pady=20)
        self.create_back_button(btn_row, self.load_dashboard, form)

        # Delete button
        delete_btn = tk.Label(
        self.content,
        text="Delete Exam",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=10,
        width=18,
        relief="ridge",
        cursor="arrow"
    )
        delete_btn.pack(pady=20)

        # Enable / Disable logic
        def validate(*args):
            if exam_id_var.get().strip().isdigit():
                enable()
            else:
                disable()

        def enable():
            delete_btn.config(bg="#000000", fg="white", cursor="hand2")
            delete_btn.bind("<Enter>", lambda e: delete_btn.config(bg="#222222"))
            delete_btn.bind("<Leave>", lambda e: delete_btn.config(bg="#000000"))
            delete_btn.bind("<Button-1>", lambda e: delete_exam())

        def disable():
            delete_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            delete_btn.unbind("<Enter>")
            delete_btn.unbind("<Leave>")
            delete_btn.unbind("<Button-1>")

        exam_id_var.trace_add("write", validate)
        disable()

        # Delete call
        def delete_exam():
            exam_id = exam_id_var.get().strip()

            try:
                import requests
                res = requests.delete(
                f"http://127.0.0.1:8000/admin/exams/delete/{exam_id}"
            )

                if res.status_code == 200:
                    self.show_popup("Success", "Exam Deleted Successfully!", "info")
                    self.change_screen(
                    "Exam Deleted!",
                    add_callback=self.load_delete_exam_screen
                )
                else:
                    msg = res.json().get("detail", "Failed to delete exam")
                    self.show_popup("Error", msg, "error")

            except Exception as e:
                self.show_popup("Server Error", str(e), "error")

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

    # ==============================================================================
    # ----- MASTER TABLES -----
    # ----- Button to View Student Master Table -----
    def load_student_master(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="Student Master",
        font=("Arial", 26, "bold"),
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

        cols = [
            ("student_id", "Student Id"),
            ("roll_no", "Roll No"),
            ("full_name", "Full Name"),
            ("date_of_birth", "Date Of Birth"),
            ("gender", "Gender"),
            ("address", "Address"),
            ("previous_school", "Previous School"),
            ("father_name", "Father Name"),
            ("mother_name", "Mother Name"),
            ("parent_phone", "Parent Phone"),
            ("parent_email", "Parent Email"),
            ("class_id", "Class Id"),
            ("is_active", "Is Active")
        ]


        # ===== SCROLLBARS =====
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")
 
        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        column_keys = [c[0] for c in cols]

        self.student_tree = ttk.Treeview(
            table_frame,
            columns=column_keys,
            show="headings",
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )

        self.student_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.student_tree.yview)
        x_scroll.config(command=self.student_tree.xview)

        # HEADINGS
        for key, label in cols:
            self.student_tree.heading(key, text=label)
            self.student_tree.column(key, width=180, anchor="center")

        # ===== FILTER BAR AT BOTTOM =====
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=12)

        tk.Label(
        filter_frame,
        text="Sort By:",
        font=("Arial", 12, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).grid(row=0, column=0, padx=5)

        filter_var = tk.StringVar()
        sort_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=[label for _, label in cols],
        state="readonly",
        width=18
    )
        sort_dropdown.grid(row=0, column=1, padx=10)

        filter_val_var = tk.StringVar()
        filter_val = tk.Entry(filter_frame, textvariable=filter_val_var,
                          font=("Arial", 12), width=25)
        filter_val.grid(row=0, column=2, padx=10)

        # BUTTON STYLE
        def style_button(btn):
            btn.config(
            bg="#000000",
            fg="white",
            padx=15,
            pady=5,
            width=10,
            relief="raised",
            cursor="arrow",
            font=("Arial", 12, "bold")
        )
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

        # LOAD BUTTON
        load_btn = tk.Label(filter_frame, text="Load")
        style_button(load_btn)
        load_btn.grid(row=0, column=3, padx=10)

        # LOAD ALL BUTTON
        load_all_btn = tk.Label(filter_frame, text="Load All")
        style_button(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

        # ===== BACKEND FETCH =====
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admin/master/students")
            self.all_students = res.json() if res.status_code == 200 else []
        except:
            self.all_students = []

        # ===== UPDATE TABLE FUNCTION =====
        def update_table(data):
            for row in self.student_tree.get_children():
                self.student_tree.delete(row)

            for r in data:
                values = [r.get(key, "") for key, _ in cols]
                self.student_tree.insert("", "end", values=values)


        # ===== FILTER FUNCTION =====
        label_to_key = {label: key for key, label in cols}

        def load_filtered():
            label = filter_var.get().strip()
            val = filter_val.get().strip().lower()
            if not label or not val:
                return

            key = label_to_key[label]

            filtered = [
                r for r in self.all_students
                if val in str(r.get(key, "")).lower()
                ]
            update_table(filtered)

        load_btn.bind("<Button-1>", lambda e: load_filtered())
        load_all_btn.bind("<Button-1>", lambda e: update_table(self.all_students))

        update_table(self.all_students)


    # ==============================================================================
    # ----- Button to View Class Master Table -----
    def load_class_master(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="Class Master",
        font=("Arial", 26, "bold"),
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

        cols = [
            ("class_id", "Class ID"),
            ("class_name", "Class Name"),
            ("section", "Section")
            ]

        # ===== SCROLLBARS =====
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")
 
        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        column_keys = [c[0] for c in cols]

        self.class_tree = ttk.Treeview(
        table_frame,
        columns=column_keys,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
    )
        self.class_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.class_tree.yview)
        x_scroll.config(command=self.class_tree.xview)

        # HEADINGS
        for key, label in cols:
            self.class_tree.heading(key, text=label)
            self.class_tree.column(key, width=180, anchor="center")

        # ===== FILTER BAR AT BOTTOM =====
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=12)

        tk.Label(
        filter_frame,
        text="Sort By:",
        font=("Arial", 12, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).grid(row=0, column=0, padx=5)

        filter_var = tk.StringVar()
        sort_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=[label for _, label in cols],
        state="readonly",
        width=18
    )
        sort_dropdown.grid(row=0, column=1, padx=10)

        filter_val_var = tk.StringVar()
        filter_val = tk.Entry(filter_frame, textvariable=filter_val_var,
                          font=("Arial", 12), width=25)
        filter_val.grid(row=0, column=2, padx=10)

        # BUTTON STYLE
        def style_button(btn):
            btn.config(
            bg="#000000",
            fg="white",
            padx=15,
            pady=5,
            width=10,
            relief="raised",
            cursor="arrow",
            font=("Arial", 12, "bold")
        )
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

        # LOAD BUTTON
        load_btn = tk.Label(filter_frame, text="Load")
        style_button(load_btn)
        load_btn.grid(row=0, column=3, padx=10)

        # LOAD ALL BUTTON
        load_all_btn = tk.Label(filter_frame, text="Load All")
        style_button(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

        # ===== BACKEND FETCH =====
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admin/master/classes")
            self.all_classes = res.json() if res.status_code == 200 else []
        except:
            self.all_classes = []

        # ===== UPDATE TABLE FUNCTION =====
        def update_table(data):
            for row in self.class_tree.get_children():
                self.class_tree.delete(row)

            for r in data:
                values = [r.get(key, "") for key, _ in cols]
                self.class_tree.insert("", "end", values=values)


        # ===== FILTER FUNCTION =====
        label_to_key = {label: key for key, label in cols}

        def load_filtered():
            label = filter_var.get().strip()
            val = filter_val.get().strip().lower()
            if not label or not val:
                return

            key = label_to_key[label]

            filtered = [
                r for r in self.all_classes
                if val in str(r.get(key, "")).lower()
                ]
            update_table(filtered)

        load_btn.bind("<Button-1>", lambda e: load_filtered())
        load_all_btn.bind("<Button-1>", lambda e: update_table(self.all_classes))

        update_table(self.all_classes)

    # ==============================================================================
    # ----- Button to View Teacher Master Table -----
    def load_teacher_master(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="Teacher Master",
        font=("Arial", 26, "bold"),
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

        cols = [
        ("teacher_id", "Teacher ID"),
        ("full_name", "Full Name"),
        ("subject_id", "Subject ID"),
        ("email", "Email"),
        ("phone", "Phone"), 
        ("date_of_birth", "Date of Birth"),
        ("gender", "Gender"),
        ("address", "Address"),
        ("class_id", "Class ID"),
        ("is_active", "Is Active"),
        ("department", "Department"),
        ("qualification", "Qualification"),
        ("experience_years", "Experience Years")
        ]

        # ===== SCROLLBARS =====
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")
 
        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")
        
        column_keys = [c[0] for c in cols]

        self.teacher_tree = ttk.Treeview(
        table_frame,
        columns=column_keys,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
    )
        self.teacher_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.teacher_tree.yview)
        x_scroll.config(command=self.teacher_tree.xview)

        # HEADINGS
        for key, label in cols:
            self.teacher_tree.heading(key, text=label)
            self.teacher_tree.column(key, width=180, anchor="center")

        # ===== FILTER BAR AT BOTTOM =====
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=12)

        tk.Label(
        filter_frame,
        text="Sort By:",
        font=("Arial", 12, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).grid(row=0, column=0, padx=5)

        filter_var = tk.StringVar()
        sort_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=[label for _, label in cols],
        state="readonly",
        width=18
    )
        sort_dropdown.grid(row=0, column=1, padx=10)

        filter_val_var = tk.StringVar()
        filter_val = tk.Entry(filter_frame, textvariable=filter_val_var,
                          font=("Arial", 12), width=25)
        filter_val.grid(row=0, column=2, padx=10)

        # BUTTON STYLE
        def style_button(btn):
            btn.config(
            bg="#000000",
            fg="white",
            padx=15,
            pady=5,
            width=10,
            relief="raised",
            cursor="arrow",
            font=("Arial", 12, "bold")
        )
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

        # LOAD BUTTON
        load_btn = tk.Label(filter_frame, text="Load")
        style_button(load_btn)
        load_btn.grid(row=0, column=3, padx=10)

        # LOAD ALL BUTTON
        load_all_btn = tk.Label(filter_frame, text="Load All")
        style_button(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

        # ===== BACKEND FETCH =====
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admin/master/teachers")
            self.all_teachers = res.json() if res.status_code == 200 else []
        except:
            self.all_teachers = []

        # ===== UPDATE TABLE FUNCTION =====
        def update_table(data):
            for row in self.teacher_tree.get_children():
                self.teacher_tree.delete(row)

            for r in data:
                values = [r.get(key, "") for key, _ in cols]
                self.teacher_tree.insert("", "end", values=values)

        # ===== FILTER FUNCTION =====
        label_to_key = {label: key for key, label in cols}

        def load_filtered():
            label = filter_var.get().strip()
            val = filter_val.get().strip().lower()
            if not label or not val:
                return

            key = label_to_key[label]

            filtered = [
                r for r in self.all_teachers
                if val in str(r.get(key, "")).lower()
                ]
            update_table(filtered)

        load_btn.bind("<Button-1>", lambda e: load_filtered())
        load_all_btn.bind("<Button-1>", lambda e: update_table(self.all_teachers))

        update_table(self.all_teachers)

    # ==============================================================================
    # ----- Button to View Subject Master Table -----
    def load_subject_master(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="Subject Master",
        font=("Arial", 26, "bold"),
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

        cols = [
            ("subject_id", "Student ID"),
            ("subject_name", "Subject Name")
            ]

        # ===== SCROLLBARS =====
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")
 
        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")
        
        column_keys = [c[0] for c in cols]

        self.subject_tree = ttk.Treeview(
        table_frame,
        columns=column_keys,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
    )
        self.subject_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.subject_tree.yview)
        x_scroll.config(command=self.subject_tree.xview)

        # HEADINGS
        for key, label in cols:
            self.subject_tree.heading(key, text=label)
            self.subject_tree.column(key, width=180, anchor="center")

        # ===== FILTER BAR AT BOTTOM =====
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=12)

        tk.Label(
        filter_frame,
        text="Sort By:",
        font=("Arial", 12, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).grid(row=0, column=0, padx=5)

        filter_var = tk.StringVar()
        sort_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=[label for _, label in cols],
        state="readonly",
        width=18
    )
        sort_dropdown.grid(row=0, column=1, padx=10)

        filter_val_var = tk.StringVar()
        filter_val = tk.Entry(filter_frame, textvariable=filter_val_var,
                          font=("Arial", 12), width=25)
        filter_val.grid(row=0, column=2, padx=10)

        # BUTTON STYLE
        def style_button(btn):
            btn.config(
            bg="#000000",
            fg="white",
            padx=15,
            pady=5,
            width=10,
            relief="raised",
            cursor="arrow",
            font=("Arial", 12, "bold")
        )
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

        # LOAD BUTTON
        load_btn = tk.Label(filter_frame, text="Load")
        style_button(load_btn)
        load_btn.grid(row=0, column=3, padx=10)

        # LOAD ALL BUTTON
        load_all_btn = tk.Label(filter_frame, text="Load All")
        style_button(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

        # ===== BACKEND FETCH =====
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admin/master/subjects")
            self.all_subjects = res.json() if res.status_code == 200 else []
        except:
            self.all_subjects = []

        # ===== UPDATE TABLE FUNCTION =====
        def update_table(data):
            for row in self.subject_tree.get_children():
                self.subject_tree.delete(row)

            for r in data:
                values = [r.get(key, "") for key, _ in cols]
                self.subject_tree.insert("", "end", values=values)

        # ===== FILTER FUNCTION =====
        label_to_key = {label: key for key, label in cols}

        def load_filtered():
            label = filter_var.get().strip()
            val = filter_val.get().strip().lower()
            if not label or not val:
                return

            key = label_to_key[label]

            filtered = [
                r for r in self.all_subjects
                if val in str(r.get(key, "")).lower()
                ]
            update_table(filtered)

        load_btn.bind("<Button-1>", lambda e: load_filtered())
        load_all_btn.bind("<Button-1>", lambda e: update_table(self.all_subjects))

        update_table(self.all_subjects)
    
    # ==============================================================================
    # ----- Button to View Fee Master Table -----
    def load_fee_master(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="Fee Master",
        font=("Arial", 26, "bold"),
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

        cols = [
            ("fee_id", "Fee ID"),
            ("class_id", "Class ID"),
            ("fee_type", "Fee Type"),
            ("amount", "Amount"),
            ("currency", "Currency"), 
            ("effective_from", "Effective_from"),
            ("effective_to", "Effective_to"),
            ("is_active", "Is_active"), 
            ("notes", "Notes")
            ]

        # ===== SCROLLBARS =====
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")
 
        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")
        
        column_keys = [c[0] for c in cols]

        self.fee_tree = ttk.Treeview(
        table_frame,
        columns=column_keys,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
    )
        self.fee_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.fee_tree.yview)
        x_scroll.config(command=self.fee_tree.xview)

        # HEADINGS
        for key, label in cols:
            self.fee_tree.heading(key, text=label)
            self.fee_tree.column(key, width=180, anchor="center")

        # ===== FILTER BAR AT BOTTOM =====
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=12)

        tk.Label(
        filter_frame,
        text="Sort By:",
        font=("Arial", 12, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).grid(row=0, column=0, padx=5)

        filter_var = tk.StringVar()
        sort_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=[label for _, label in cols],
        state="readonly",
        width=18
    )
        sort_dropdown.grid(row=0, column=1, padx=10)

        filter_val_var = tk.StringVar()
        filter_val = tk.Entry(filter_frame, textvariable=filter_val_var,
                          font=("Arial", 12), width=25)
        filter_val.grid(row=0, column=2, padx=10)

        # BUTTON STYLE
        def style_button(btn):
            btn.config(
            bg="#000000",
            fg="white",
            padx=15,
            pady=5,
            width=10,
            relief="raised",
            cursor="arrow",
            font=("Arial", 12, "bold")
        )
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

        # LOAD BUTTON
        load_btn = tk.Label(filter_frame, text="Load")
        style_button(load_btn)
        load_btn.grid(row=0, column=3, padx=10)

        # LOAD ALL BUTTON
        load_all_btn = tk.Label(filter_frame, text="Load All")
        style_button(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

        # ===== BACKEND FETCH =====
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admin/master/fees")
            self.all_fees = res.json() if res.status_code == 200 else []
        except:
            self.all_fees = []

        # ===== UPDATE TABLE FUNCTION =====
        def update_table(data):
            for row in self.fee_tree.get_children():
                self.fee_tree.delete(row)

            for r in data:
                values = [r.get(key, "") for key, _ in cols]
                self.fee_tree.insert("", "end", values=values)

        # ===== FILTER FUNCTION =====
        label_to_key = {label: key for key, label in cols}

        def load_filtered():
            label = filter_var.get().strip()
            val = filter_val.get().strip().lower()
            if not label or not val:
                return

            key = label_to_key[label]

            filtered = [
                r for r in self.all_fees
                if val in str(r.get(key, "")).lower()
                ]
            update_table(filtered)

        load_btn.bind("<Button-1>", lambda e: load_filtered())
        load_all_btn.bind("<Button-1>", lambda e: update_table(self.all_fees))

        update_table(self.all_fees)

    # ==============================================================================
    # ----- Button to View Exam Master Table -----
    def load_exam_master(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="Exam Master",
        font=("Arial", 26, "bold"),
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

        cols = [
            ("exam_id", "Exam ID"),
            ("exam_name", "Exam Name"),
            ("description", "Description"),
            ("exam_date", "Exam Date"),
            ("is_active", "Is Active")
            ]

        # ===== SCROLLBARS =====
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")
 
        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")
        
        column_keys = [c[0] for c in cols]

        self.exam_tree = ttk.Treeview(
        table_frame,
        columns=column_keys,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
    )
        self.exam_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.exam_tree.yview)
        x_scroll.config(command=self.exam_tree.xview)

        # HEADINGS
        for key, label in cols:
            self.exam_tree.heading(key, text=label)
            self.exam_tree.column(key, width=180, anchor="center")

        # ===== FILTER BAR AT BOTTOM =====
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=12)

        tk.Label(
        filter_frame,
        text="Sort By:",
        font=("Arial", 12, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).grid(row=0, column=0, padx=5)

        filter_var = tk.StringVar()
        sort_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=[label for _, label in cols],
        state="readonly",
        width=18
    )
        sort_dropdown.grid(row=0, column=1, padx=10)

        filter_val_var = tk.StringVar()
        filter_val = tk.Entry(filter_frame, textvariable=filter_val_var,
                          font=("Arial", 12), width=25)
        filter_val.grid(row=0, column=2, padx=10)

        # BUTTON STYLE
        def style_button(btn):
            btn.config(
            bg="#000000",
            fg="white",
            padx=15,
            pady=5,
            width=10,
            relief="raised",
            cursor="arrow",
            font=("Arial", 12, "bold")
        )
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

        # LOAD BUTTON
        load_btn = tk.Label(filter_frame, text="Load")
        style_button(load_btn)
        load_btn.grid(row=0, column=3, padx=10)

        # LOAD ALL BUTTON
        load_all_btn = tk.Label(filter_frame, text="Load All")
        style_button(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

        # ===== BACKEND FETCH =====
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admin/master/exams")
            self.all_exams = res.json() if res.status_code == 200 else []
        except:
            self.all_exams = []

        # ===== UPDATE TABLE FUNCTION =====
        def update_table(data):
            for row in self.exam_tree.get_children():
                self.exam_tree.delete(row)

            for r in data:
                values = [r.get(key, "") for key, _ in cols]
                self.exam_tree.insert("", "end", values=values)

        # ===== FILTER FUNCTION =====
        label_to_key = {label: key for key, label in cols}

        def load_filtered():
            label = filter_var.get().strip()
            val = filter_val.get().strip().lower()
            if not label or not val:
                return

            key = label_to_key[label]

            filtered = [
                r for r in self.all_exams
                if val in str(r.get(key, "")).lower()
                ]
            update_table(filtered)

        load_btn.bind("<Button-1>", lambda e: load_filtered())
        load_all_btn.bind("<Button-1>", lambda e: update_table(self.all_exams))

        update_table(self.all_exams)

    # ==============================================================================
    # ----- Button to View Result Master Table -----
    def load_result_master(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="Result Master",
        font=("Arial", 26, "bold"),
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

        cols = [
            ("result_id", "Result ID"),
            ("student_id", "Student ID"),
            ("exam_id", "Exam ID"),
            ("total_marks", "Total Marks"), 
            ("obtained_marks", "Obtained Marks"),
            ("percentage", "Percentage"),
            ("grade", "Grade"),
            ("result_status", "Result Status")
            ]

        # ===== SCROLLBARS =====
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")
 
        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")
        
        column_keys = [c[0] for c in cols]

        self.result_tree = ttk.Treeview(
        table_frame,
        columns=column_keys,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
    )
        self.result_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.result_tree.yview)
        x_scroll.config(command=self.result_tree.xview)

        # HEADINGS
        for key, label in cols:
            self.result_tree.heading(key, text=label)
            self.result_tree.column(key, width=180, anchor="center")

        # ===== FILTER BAR AT BOTTOM =====
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=12)

        tk.Label(
        filter_frame,
        text="Sort By:",
        font=("Arial", 12, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).grid(row=0, column=0, padx=5)

        filter_var = tk.StringVar()
        sort_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=[label for _, label in cols],
        state="readonly",
        width=18
    )
        sort_dropdown.grid(row=0, column=1, padx=10)

        filter_val_var = tk.StringVar()
        filter_val = tk.Entry(filter_frame, textvariable=filter_val_var,
                          font=("Arial", 12), width=25)
        filter_val.grid(row=0, column=2, padx=10)

        # BUTTON STYLE
        def style_button(btn):
            btn.config(
            bg="#000000",
            fg="white",
            padx=15,
            pady=5,
            width=10,
            relief="raised",
            cursor="arrow",
            font=("Arial", 12, "bold")
        )
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

        # LOAD BUTTON
        load_btn = tk.Label(filter_frame, text="Load")
        style_button(load_btn)
        load_btn.grid(row=0, column=3, padx=10)

        # LOAD ALL BUTTON
        load_all_btn = tk.Label(filter_frame, text="Load All")
        style_button(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

        # ===== BACKEND FETCH =====
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admin/master/results")
            self.all_results = res.json() if res.status_code == 200 else []
        except:
            self.all_results = []

        # ===== UPDATE TABLE FUNCTION =====
        def update_table(data):
            for row in self.result_tree.get_children():
                self.result_tree.delete(row)

            for r in data:
                values = [r.get(key, "") for key, _ in cols]
                self.result_tree.insert("", "end", values=values)

        # ===== FILTER FUNCTION =====
        label_to_key = {label: key for key, label in cols}

        def load_filtered():
            label = filter_var.get().strip()
            val = filter_val.get().strip().lower()
            if not label or not val:
                return

            key = label_to_key[label]

            filtered = [
                r for r in self.all_results
                if val in str(r.get(key, "")).lower()
                ]
            update_table(filtered)

        load_btn.bind("<Button-1>", lambda e: load_filtered())
        load_all_btn.bind("<Button-1>", lambda e: update_table(self.all_results))

        update_table(self.all_results)

    # ==============================================================================
    # ----- Button to View Staff Master Table -----
    def load_staff_master(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="Staff Master",
        font=("Arial", 26, "bold"),
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

        cols = [
            ("staff_id", "Staff ID"),
            ("full_name", "Full Name"),
            ("date_of_birth", "Date of Birth"),
            ("gender", "Gender"),
            ("address", "Address"),
            ("department", "Department"), 
            ("role", "Role"),
            ("email", "Email"),
            ("phone", "Phone"),
            ("experience_years", "Experience Years")
            ]
        
        # ===== SCROLLBARS =====
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")
 
        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")
        
        column_keys = [c[0] for c in cols]

        self.staff_tree = ttk.Treeview(
        table_frame,
        columns=column_keys,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
    )
        self.staff_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.staff_tree.yview)
        x_scroll.config(command=self.staff_tree.xview)

        # HEADINGS
        for key, label in cols:
            self.staff_tree.heading(key, text=label)
            self.staff_tree.column(key, width=180, anchor="center")

        # ===== FILTER BAR AT BOTTOM =====
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=12)

        tk.Label(
        filter_frame,
        text="Sort By:",
        font=("Arial", 12, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).grid(row=0, column=0, padx=5)

        filter_var = tk.StringVar()
        sort_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=[label for _, label in cols],
        state="readonly",
        width=18
    )
        sort_dropdown.grid(row=0, column=1, padx=10)

        filter_val_var = tk.StringVar()
        filter_val = tk.Entry(filter_frame, textvariable=filter_val_var,
                          font=("Arial", 12), width=25)
        filter_val.grid(row=0, column=2, padx=10)

        # BUTTON STYLE
        def style_button(btn):
            btn.config(
            bg="#000000",
            fg="white",
            padx=15,
            pady=5,
            width=10,
            relief="raised",
            cursor="arrow",
            font=("Arial", 12, "bold")
        )
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

        # LOAD BUTTON
        load_btn = tk.Label(filter_frame, text="Load")
        style_button(load_btn)
        load_btn.grid(row=0, column=3, padx=10)

        # LOAD ALL BUTTON
        load_all_btn = tk.Label(filter_frame, text="Load All")
        style_button(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

        # ===== BACKEND FETCH =====
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admin/master/staff")
            self.all_staff = res.json() if res.status_code == 200 else []
        except:
            self.all_staff = []

        # ===== UPDATE TABLE FUNCTION =====
        def update_table(data):
            for row in self.staff_tree.get_children():
                self.staff_tree.delete(row)

            for r in data:
                values = [r.get(key, "") for key, _ in cols]
                self.staff_tree.insert("", "end", values=values)

        # ===== FILTER FUNCTION =====
        label_to_key = {label: key for key, label in cols}

        def load_filtered():
            label = filter_var.get().strip()
            val = filter_val.get().strip().lower()
            if not label or not val:
                return

            key = label_to_key[label]

            filtered = [
                r for r in self.all_staff
                if val in str(r.get(key, "")).lower()
                ]
            update_table(filtered)

        load_btn.bind("<Button-1>", lambda e: load_filtered())
        load_all_btn.bind("<Button-1>", lambda e: update_table(self.all_staff))

        update_table(self.all_staff)

    # ==============================================================================
    # ----- Button to View Salary Master Table -----
    def load_salary_master(self):
        self.clear_content()

        # ===== TITLE =====
        tk.Label(
        self.content,
        text="Salary Master",
        font=("Arial", 26, "bold"),
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

        cols = [
            ("salary_id", "Salary ID"),
            ("role", "Role"),
            ("base_salary", "Base Salary"),
            ("bonus_percentage", "Bonus Percentage"),
            ("is_active", "Is Active")
            ]

        # ===== SCROLLBARS =====
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")
 
        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")
        
        column_keys = [c[0] for c in cols]

        self.salary_tree = ttk.Treeview(
        table_frame,
        columns=column_keys,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
    )
        self.salary_tree.pack(fill="both", expand=True)

        y_scroll.config(command=self.salary_tree.yview)
        x_scroll.config(command=self.salary_tree.xview)

        # HEADINGS
        for key, label in cols:
            self.salary_tree.heading(key, text=label)
            self.salary_tree.column(key, width=180, anchor="center")

        # ===== FILTER BAR AT BOTTOM =====
        filter_frame = tk.Frame(self.content, bg="#ECF0F1")
        filter_frame.pack(pady=12)

        tk.Label(
        filter_frame,
        text="Sort By:",
        font=("Arial", 12, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).grid(row=0, column=0, padx=5)

        filter_var = tk.StringVar()
        sort_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=[label for _, label in cols],
        state="readonly",
        width=18
    )
        sort_dropdown.grid(row=0, column=1, padx=10)

        filter_val_var = tk.StringVar()
        filter_val = tk.Entry(filter_frame, textvariable=filter_val_var,
                          font=("Arial", 12), width=25)
        filter_val.grid(row=0, column=2, padx=10)

        # BUTTON STYLE
        def style_button(btn):
            btn.config(
            bg="#000000",
            fg="white",
            padx=15,
            pady=5,
            width=10,
            relief="raised",
            cursor="arrow",
            font=("Arial", 12, "bold")
        )
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))

        # LOAD BUTTON
        load_btn = tk.Label(filter_frame, text="Load")
        style_button(load_btn)
        load_btn.grid(row=0, column=3, padx=10)

        # LOAD ALL BUTTON
        load_all_btn = tk.Label(filter_frame, text="Load All")
        style_button(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

        # ===== BACKEND FETCH =====
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admin/master/salary")
            self.all_salaries = res.json() if res.status_code == 200 else []
        except:
            self.all_salaries = []

        # ===== UPDATE TABLE FUNCTION =====
        def update_table(data):
            for row in self.salary_tree.get_children():
                self.salary_tree.delete(row)

            for r in data:
                values = [r.get(key, "") for key, _ in cols]
                self.salary_tree.insert("", "end", values=values)

        # ===== FILTER FUNCTION =====
        label_to_key = {label: key for key, label in cols}

        def load_filtered():
            label = filter_var.get().strip()
            val = filter_val.get().strip().lower()
            if not label or not val:
                return

            key = label_to_key[label]

            filtered = [
                r for r in self.all_salaries
                if val in str(r.get(key, "")).lower()
                ]
            update_table(filtered)

        load_btn.bind("<Button-1>", lambda e: load_filtered())
        load_all_btn.bind("<Button-1>", lambda e: update_table(self.all_salaries))

        update_table(self.all_salaries)

    # ==============================================================================
    # ===== DASHBOARD PAGE ======
    def load_dashboard(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        tk.Label(
            self.content,
            text="Admin Dashboard",
            font=("Arial", 26, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(pady=20)

        box = tk.Frame(self.content, bg="white", bd=2, relief="groove")
        box.pack(pady=60)

        tk.Label(
            box,
            text="Welcome to the Admin Panel!",
            font=("Arial", 16),
            bg="white"
        ).pack(padx=40, pady=30)


# ======== RUN UI ========
if __name__ == "__main__":
    root = tk.Tk()
    app = AdminUI(root)
    root.mainloop()

