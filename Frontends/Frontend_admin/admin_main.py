import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import datetime

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
            width=20,
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


    # ===== SIDEBAR BUILD =====
    def build_sidebar(self):

        tk.Label(
            self.sidebar,
            text="ADMIN PANEL",
            bg="#1E2A38",
            fg="white",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        # Main Buttons
        admission_btn = self.add_btn("Manage Admissions")
        self.build_admission_dropdown(admission_btn)

        att_btn = self.add_btn("Manage Attendances")
        self.build_attendance_dropdown(att_btn)

        fee_btn = self.add_btn("Manage Fees")
        self.build_fees_dropdown(fee_btn)

        tc_btn = self.add_btn("Manage TCs")
        self.build_tc_dropdown(tc_btn)
    
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
    
    # =========================================
    def build_fees_dropdown(self, parent_label):
        menu = tk.Menu(self.root, tearoff=0)

        menu.add_command(label="Create Fee", command=lambda: self.load_create_fee_screen())
        menu.add_command(label="Assign Fee", command=lambda: self.load_assign_fee_screen())
        menu.add_command(label="View Fees", command=lambda: self.load_view_fees_screen())
        menu.add_command(label="Update Fee", command=lambda: self.load_update_fee_screen())
        menu.add_command(label="Delete Fee", command=lambda: self.load_delete_fee_screen())
        menu.add_command(label="Fee History", command=lambda: self.load_fee_history_screen())
        menu.add_command(label="Upload Receipt", command=lambda: self.load_upload_receipt_screen())

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

    def build_tc_dropdown(self, parent_label):
        menu = tk.Menu(self.root, tearoff=0)

        menu.add_command(label="Apply TC", command=self.load_issue_tc_screen)
        menu.add_command(label="View TC", command=self.load_view_all_tc_screen)
        menu.add_command(label="Delete TC", command=self.load_approve_tc_screen)

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
                    self.show_popup("Failed", "Failed to Assign Fees!", "error")

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


    # ===== button to Upload Receipt in DB =====
    def load_upload_receipt_screen(self):
        self.clear_content()

        tk.Label(
        self.content,
        text="Upload Fee Receipt",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # Variables
        student_var = tk.StringVar()
        fee_var = tk.StringVar()
        file_var = tk.StringVar()

        # Form Fields
        tk.Label(form, text="Student ID:", bg="#ECF0F1", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
        student_entry = tk.Entry(form, textvariable=student_var, font=("Arial", 14), width=25)
        student_entry.grid(row=0, column=1, padx=10)

        tk.Label(form, text="Fee ID:", bg="#ECF0F1", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10)
        fee_entry = tk.Entry(form, textvariable=fee_var, font=("Arial", 14), width=25)
        fee_entry.grid(row=1, column=1, padx=10)

        tk.Label(form, text="Select File:", bg="#ECF0F1", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=10)

        file_display = tk.Entry(form, textvariable=file_var, font=("Arial", 12), width=25, state="disabled")
        file_display.grid(row=2, column=1, padx=10)
 
        # Browse button
        def browse_file():
            from tkinter import filedialog
            file_path = filedialog.askopenfilename(
                title="Select Receipt File",
                filetypes=[("Image/PDF Files", "*.png *.jpg *.jpeg *.pdf")]
            )
            if file_path:
                file_var.set(file_path)
                validate_upload_btn()

        browse_btn = tk.Label(
        form,
        text="Browse",
        font=("Arial", 12, "bold"),
        bg="#95A5A6",
        fg="white",
        padx=15,
        pady=6,
        cursor="arrow",
        relief="ridge"
        )
        browse_btn.grid(row=2, column=2, padx=10)
        browse_btn.bind("<Enter>", lambda e: browse_btn.config(bg="#7F8C8D"))
        browse_btn.bind("<Leave>", lambda e: browse_btn.config(bg="#95A5A6"))
        browse_btn.bind("<Button-1>", lambda e: browse_file())

        btn_frame = tk.Frame(self.content, bg="#ECF0F1")
        btn_frame.pack(pady=25)

        # Back Button from global function
        self.create_back_button(
        parent=btn_frame,
        go_back_callback=self.load_dashboard,    
        form_frame=form                          
        )
        self.content.update_idletasks()
        
        # Upload Button (Disabled initially)
        upload_btn = tk.Label(
        self.content,
        text="Upload",
        font=("Arial", 16, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=25,
        pady=12,
        width=12,
        borderwidth=1,
        relief="solid",
        cursor="arrow",
        )
        upload_btn.pack(pady=30)

        # ======= VALIDATION (Enable on all filled) =======
        def validate_upload_btn(*args):
            if student_var.get().strip() and fee_var.get().strip() and file_var.get().strip():
                upload_btn.config(bg="#000000", fg="white", cursor="hand2")

                upload_btn.bind("<Enter>", lambda e: upload_btn.config(bg="#222222"))
                upload_btn.bind("<Leave>", lambda e: upload_btn.config(bg="#000000"))
                upload_btn.bind("<Button-1>", lambda e: upload_receipt())
            else:
                upload_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                upload_btn.unbind("<Enter>")
                upload_btn.unbind("<Leave>")
                upload_btn.unbind("<Button-1>")

        # Trace input changes
        student_var.trace_add("write", validate_upload_btn)
        fee_var.trace_add("write", validate_upload_btn)
        file_var.trace_add("write", validate_upload_btn)

        # ====== Upload Function ======
        def upload_receipt(self, invoice_id):
            import requests
            import os
      
    # ---- READ ENTRIES ----
            student_id = student_var["student_id"].get().strip()
            fee_id = fee_var["fee_id"].get().strip()
            file_path = file_var["file"].get().strip()

    # ---- VALIDATE STUDENT ID ----
            if not student_id.isdigit() or int(student_id) <= 0:
                self.show_popup("Invalid Student ID", "Student ID must be a positive number.", "warning")
                return

    # ---- VALIDATE FEE ID ----
            if not fee_id.isdigit() or int(fee_id) <= 0:
               self.show_popup("Invalid Fee ID", "Fee ID must be a positive number.", "warning")
               return

    # ---- VALIDATE FILE SELECTION ----
            if not os.path.exists(file_path):
                self.show_popup("Invalid File", "Please select a valid receipt file.", "warning")
                return
    # ---- EVERYTHING VALID → START UPLOAD ----
            try:
                with open(file_path, "rb") as f:
                    files = {"file": f}

                    res = requests.post(
                f"http://127.0.0.1:8000/admin/fees/receipt/upload/{invoice_id}",
                files=files
            )

                if res.status_code in (200, 201):
                    self.change_screen(
                "Receipt Uploaded Successfully!",
                add_callback=self.load_upload_receipt_screen
            )
                else:
                    self.show_popup("Upload Failed", res.text, "error")

            except Exception as e:
                self.show_popup("Upload Error", str(e), "error")


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
                fields["Date"].set(data["on_date"])
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
            "on_date": date_val,
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
                disabledforeground="black"      # <-- TEXT COLOR BLACK
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
            adm_id = str(adm_id_var).get().strip()

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
    # ======== Button Issue Tc ========
    def load_issue_tc_screen(self):
        self.clear_content()

        tk.Label(
        self.content, text="Issue Transfer Certificate",
        font=("Arial", 26, "bold"), bg="#ECF0F1", fg="#2C3E50"
    ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=20)

    # ---------------- FIELDS ----------------
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
                command=lambda v=vars[key], b=entry: self.open_calendar_popup(b, v)
            )
                cal_btn.grid(row=i, column=2, padx=5)
            else:
                tk.Entry(form, textvariable=vars[key], font=("Arial", 14), width=30)\
                .grid(row=i, column=1, padx=10)

    # ---------------- BUTTON ----------------
        submit = tk.Label(
        form, text="Issue TC", font=("Arial", 16, "bold"),
        bg="#D5D8DC", fg="#AEB6BF",
        padx=20, pady=10, width=15,
        cursor="arrow"
    )
        submit.grid(row=len(fields), columnspan=3, pady=20)

    # ---------------- VALIDATION ----------------
        def validate(*args):
            if all(vars[k].get().strip() for k in vars):
                submit.config(bg="#000", fg="white", cursor="hand2")
                submit.bind("<Enter>", lambda e: submit.config(bg="#222"))
                submit.bind("<Leave>", lambda e: submit.config(bg="#000"))
                submit.bind("<Button-1>", lambda e: issue_tc())
            else:
                submit.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
                submit.unbind("<Enter>")
                submit.unbind("<Leave>")
                submit.unbind("<Button-1>")

        for v in vars.values():
            v.trace_add("write", validate)

    # ---------------- SUBMIT ----------------
        def issue_tc():
            sid = vars["student_id"].get().strip()
            if not sid.isdigit():
                self.show_popup("Invalid ID", "Student ID must be numeric!", "warning")
                return

            import re
            date_str = vars["issue_date"].get().strip()
            if not re.match(r"\d{4}-\d{2}-\d{2}", date_str):
                self.show_popup("Invalid Date", "Date must be YYYY-MM-DD!", "warning")
                return

            payload = {k: v.get().strip() for k, v in vars.items()}

            import requests
            res = requests.post("http://127.0.0.1:8000/admin/tc/issue", json=payload)

            if res.status_code == 200:
                self.show_popup("Success", "TC Issued Successfully!", "info")
                self.change_screen("TC Issued!", add_callback=self.load_issue_tc_screen)
            else:
                self.show_popup("Error", "Failed to Issue TC!", "error")

    # ============================================
    def load_view_all_tc_screen(self):
        self.clear_content()

    # -------- TITLE --------
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
        self.create_back_button(back_frame, self.load_tc_menu, None)

    # -------- TABLE FRAME --------
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # ---- TC TABLE COLUMNS ----
        cols = (
        "tc_id", "student_id", "issue_date",
        "reason", "status"
    )

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
            cursor="hand2",
            font=("Arial", 12, "bold")
        )
            btn.bind("<Enter>", lambda e: btn.config(bg="#222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000"))

        load_btn = tk.Label(filter_frame, text="Load")
        style_button(load_btn)
        load_btn.grid(row=0, column=3, padx=10)

        load_all_btn = tk.Label(filter_frame, text="Load All")
        style_button(load_all_btn)
        load_all_btn.grid(row=0, column=4, padx=10)

    # ======================================================
    #               TABLE + SCROLLBARS
    # ======================================================
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

    # ======================================================
    #                 BACKEND FETCH
    # ======================================================
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
            "status": [r["status"] for r in self.all_tc],
        }

        except:
            self.all_tc = []

    # ----------- UPDATE TABLE FUNCTION -----------
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
                    row["status"]
                )
            )

    # ----------- FILTER FUNCTION -----------
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


    # =======================================
    def load_approve_tc_screen(self):
        self.clear_content()

    # ===== TITLE =====
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
        go_back_callback=self.load_tc_menu,
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
                vars_dict["status"].set(data["status"])

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


# RUN UI
if __name__ == "__main__":
    root = tk.Tk()
    app = AdminUI(root)
    root.mainloop()

