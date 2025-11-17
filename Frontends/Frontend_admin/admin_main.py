import tkinter as tk
from tkinter import ttk

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


    # ===== CHANGE SCREEN VIEW =====
    def change_screen(self, screen_name):
        for widget in self.content.winfo_children():
            widget.destroy()

        tk.Label(
            self.content,
            text=f"{screen_name} Page",
            font=("Arial", 22, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(pady=40)
    
    # ==============================================================================
    # ==== Button to create fee ====
    def load_create_fee_screen(self):
        self.clear_content()

        title = tk.Label(self.content, text="Create Fee", font=("Arial", 26, "bold"),
                        bg="#ECF0F1", fg="#2C3E50")
        title.pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=20)

        labels = ["Class ID", "Fee Type", "Amount"]
        self.entries = {}

        # StringVar storage for auto tracking
        self.vars = {}

        for i, text in enumerate(labels):
            lbl = tk.Label(form, text=text + ":", bg="#ECF0F1", fg="#2C3E50", font=("Arial", 14))
            lbl.grid(row=i, column=0, sticky="e", padx=10, pady=10)

            var = tk.StringVar()
            var.trace_add("write", lambda *args: self.validate_fee_form())

            entry = tk.Entry(form, textvariable=var, font=("Arial", 14), width=25)
            entry.grid(row=i, column=1, padx=10, pady=10)

            self.vars[text] = var
            self.entries[text] = entry

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
        class_id = self.vars["Class ID"].get().strip()
        fee_type = self.vars["Fee Type"].get().strip()
        amount = self.vars["Amount"].get().strip()

        if class_id and fee_type and amount:
            self.enable_submit()
        else:
            self.disable_submit()

    def submit_create_fee(self):
        payload = {
            "class_id": int(self.entries["Class ID"].get()),
            "fee_type": self.entries["Fee Type"].get(),
            "amount": float(self.entries["Amount"].get())
        }

        import requests
        requests.post("http://127.0.0.1:8000/admin/fees/create", json=payload)

        self.change_screen("Fee Created Successfully")

    # ====================
    # button to assign fee
    def load_assign_fee_screen(self):
        self.clear_content()

        tk.Label(
        self.content,
        text="Assign Fee to Student",
        font=("Arial", 22, "bold"),
        bg="#ECF0F1"
        ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # Vars to trace
        sid_var = tk.StringVar()
        fid_var = tk.StringVar()

        sid_var.trace_add("write", lambda *_: self.validate_assign_form(sid_var, fid_var, assign_btn))
        fid_var.trace_add("write", lambda *_: self.validate_assign_form(sid_var, fid_var, assign_btn))

        tk.Label(form, text="Student ID:", font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=0, padx=10, pady=8)
        sid_entry = tk.Entry(form, font=("Arial", 14), textvariable=sid_var)
        sid_entry.grid(row=0, column=1, padx=10)
 
        tk.Label(form, text="Fee ID:", font=("Arial", 14), bg="#ECF0F1").grid(row=1, column=0, padx=10, pady=8)
        fid_entry = tk.Entry(form, font=("Arial", 14), textvariable=fid_var)
        fid_entry.grid(row=1, column=1, padx=10)

        def assign_fee():
            print("ASSIGNING FEE...")
            print("Student:", sid_var.get())
            print("Fee:", fid_var.get())

        assign_btn = tk.Label(
                form,
                text="Assign",
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
        assign_btn.grid(row=2, columnspan=2, pady=15)
    
    # ========================
    def validate_assign_form(self, sid_var, fid_var, btn):
        if sid_var.get().strip() and fid_var.get().strip():
            btn.config(bg="#000000", fg="white", cursor="hand2")
            btn.bind("<Enter>", lambda e: btn.config(bg="#222222"))
            btn.bind("<Leave>", lambda e: btn.config(bg="#000000"))
            btn.bind("<Button-1>", lambda e: print("Assigning Fee..."))
        else:
            btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")
            btn.unbind("<Enter>")
            btn.unbind("<Leave>")
            btn.unbind("<Button-1>")


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

    # ===== button to view all fees from DB =====
    def load_view_fees_screen(self):
        self.clear_content()

        title = tk.Label(self.content, text="All Fees", font=("Arial", 26, "bold"),
                        bg="#ECF0F1", fg="#2C3E50")
        title.pack(pady=20)

        table_frame = tk.Frame(self.content)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Scrollbars
        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")

        self.tree = ttk.Treeview(
            table_frame,
            columns=("fee_id", "class_id", "fee_type", "amount", "from_date", "to_date", "active"),
            show="headings",
        )

        # Define columns
        headers = {
            "fee_id": "Fee ID",
            "class_id": "Class ID",
            "fee_type": "Fee Type",
            "amount": "Amount",
            "from_date": "From",
            "to_date": "To",
            "active": "Active"
        }

        for key, text in headers.items():
            self.tree.heading(key, text=text)
            self.tree.column(key, width=150)

        # Pack Scrollbars
        x_scroll.config(command=self.tree.xview)
        y_scroll.config(command=self.tree.yview)

        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        # ---- FETCH FROM BACKEND ----
        import requests
        try:
            response = requests.get("http://127.0.0.1:8000/admin/fees/all")
            data = response.json()

            for row in data:
                self.tree.insert("", "end", values=(
                    row["fee_id"],
                    row["class_id"],
                    row["fee_type"],
                    row["amount"],
                    row["start_date"],
                    row["end_date"],
                    row["is_active"]
                ))

        except:
            print("Backend not running or wrong URL!")

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
        import requests
        try:
            res = requests.get(f"http://127.0.0.1:8000/admin/fees/{fee_id}")
            if res.status_code != 200:
                self.change_screen("Fee Not Found")
                return

            data = res.json()
            self.show_update_form(data)

        except:
            self.change_screen("Error Fetching Fee Data")
    
    # ===== Button to Update any fee record =====
    def show_update_form(self, data):
        self.clear_content()

        tk.Label(self.content, text="Update Fee",
                font=("Arial", 26, "bold"),
                bg="#ECF0F1", fg="#2C3E50").pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        labels = ["Class ID", "Fee Type", "Amount"]
        fields = ["class_id", "fee_type", "amount"]

        self.update_vars = {}
        self.update_entries = {}

        for i, field in enumerate(fields):
            tk.Label(form, text=labels[i] + ":", font=("Arial", 14),
                    bg="#ECF0F1").grid(row=i, column=0, padx=10, pady=10)

            var = tk.StringVar(value=str(data[field]))
            entry = tk.Entry(form, textvariable=var, font=("Arial", 14), width=25)

            entry.grid(row=i, column=1, padx=10, pady=10)

            self.update_vars[field] = var
            self.update_entries[field] = entry

            # enable update button when entries valid
            var.trace_add("write", lambda *args: self.validate_update_form())

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
    def submit_fee_update(self):
        payload = {
        "class_id": int(self.update_vars["class_id"].get()),
        "fee_type": self.update_vars["fee_type"].get(),
        "amount": float(self.update_vars["amount"].get())
        }

        import requests
        requests.put("http://127.0.0.1:8000/admin/fees/update", json=payload)

        self.change_screen("Fee Updated Successfully!")


    # ===== button to delete a fee using fee_id =====
    def load_delete_fee_screen(self):
        self.clear_content()

        title = tk.Label(
        self.content,
        text="Delete Fee",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        )
        title.pack(pady=25)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=20)

        # Label + input
        tk.Label(
            form, text="Fee ID:", font=("Arial", 16), bg="#ECF0F1"
        ).grid(row=0, column=0, padx=10, pady=10)

        fee_id_var = tk.StringVar()
        fee_id_entry = tk.Entry(form, textvariable=fee_id_var, font=("Arial", 14), width=25)
        fee_id_entry.grid(row=0, column=1, padx=10, pady=10)

        # Delete button (disabled initially)
        delete_btn = tk.Label(
        form,
        text="Delete",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=22,
        pady=10,
        width=12,
        cursor="arrow",
        borderwidth=1,
        relief="solid"
        )
        delete_btn.grid(row=1, columnspan=2, pady=20)

        # ===== Enable / Disable Button =====
        def validate_delete_button(*args):
            fee_id = fee_id_var.get().strip()

            if fee_id:
                delete_btn.config(bg="#000000", fg="white", cursor="hand2")

            # Hover dark
                delete_btn.bind("<Enter>", lambda e: delete_btn.config(bg="#222222"))
                delete_btn.bind("<Leave>", lambda e: delete_btn.config(bg="#000000"))

                delete_btn.bind("<Button-1>",
                    lambda e: self.perform_fee_delete(fee_id)
                )
            else:
                delete_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")

                delete_btn.unbind("<Enter>")
                delete_btn.unbind("<Leave>")
                delete_btn.unbind("<Button-1>")

        # Trigger when user types
        fee_id_var.trace_add("write", validate_delete_button)

    # ===========================
    def perform_fee_delete(self, fee_id):
        import requests
    
        try:
            url = f"http://127.0.0.1:8000/admin/fees/delete/{fee_id}"
            response = requests.delete(url)

            if response.status_code == 200:
                self.change_screen("Fee Deleted Successfully")
            else:
                self.change_screen("Error Deleting Fee")

        except Exception as e:
            print("Error:", e)
            self.change_screen("Backend Error, Try Again!")


    # ===== button to upload receipt =====
    def load_fee_history_screen(self):
        self.clear_content()

        # Title
        tk.Label(
        self.content,
        text="Fee History",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=25)

        # Form frame
        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        tk.Label(
            form, text="Enter Fee ID:", bg="#ECF0F1",
            fg="#2C3E50", font=("Arial", 16)
        ).grid(row=0, column=0, padx=10, pady=10)

        fee_id_var = tk.StringVar()
        fee_id_entry = tk.Entry(form, textvariable=fee_id_var, font=("Arial", 14), width=25)
        fee_id_entry.grid(row=0, column=1, padx=10)

        # Search button (disabled)
        search_btn = tk.Label(
        form,
        text="Search",
        font=("Arial", 14, "bold"),
        bg="#D5D8DC",
        fg="#AEB6BF",
        padx=20,
        pady=10,
        width=12,
        relief="solid",
        borderwidth=1,
        cursor="arrow"
        )
        search_btn.grid(row=1, columnspan=2, pady=20)

        # ------ Enable / Disable Logic -------
        def validate_history_btn(*args):
            fee_id = fee_id_var.get().strip()

            if fee_id:
                search_btn.config(bg="#000000", fg="white", cursor="hand2")

                search_btn.bind("<Enter>", lambda e: search_btn.config(bg="#222222"))
                search_btn.bind("<Leave>", lambda e: search_btn.config(bg="#000000"))

                search_btn.bind("<Button-1>", lambda e: self.fetch_fee_history(fee_id))
            else:
                search_btn.config(bg="#D5D8DC", fg="#AEB6BF", cursor="arrow")

                search_btn.unbind("<Enter>")
                search_btn.unbind("<Leave>")
                search_btn.unbind("<Button-1>")

        fee_id_var.trace_add("write", validate_history_btn)

    # ===== Fetch From Backend (Fee History) =====
    def fetch_fee_history(self, fee_id):
        import requests

        self.clear_content()
 
        tk.Label(
        self.content,
        text=f"Fee History for ID: {fee_id}",
        font=("Arial", 24, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        table_frame = tk.Frame(self.content)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")

        # Table structure
        columns = ("history_id", "fee_id", "old_amount", "new_amount",
                "changed_on", "changed_by")

        tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        xscrollcommand=x_scroll.set,
        yscrollcommand=y_scroll.set
        )

        # Scrollbar binding
        x_scroll.config(command=tree.xview)
        y_scroll.config(command=tree.yview)

        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")
        tree.pack(fill="both", expand=True)

        # Headers
        headers = ["History ID", "Fee ID", "Old Amount", "New Amount",
                "Changed On", "Changed By"]

        for i, col in enumerate(columns):
            tree.heading(col, text=headers[i])
            tree.column(col, width=150)

        # Fetch from backend
        try:
            url = f"http://127.0.0.1:8000/admin/fees/history/{fee_id}"
            res = requests.get(url)

            if res.status_code == 200:
                for row in res.json():
                    tree.insert("", "end", values=(
                        row["history_id"],
                        row["fee_id"],
                        row["old_amount"],
                        row["new_amount"],
                        row["changed_on"],
                        row["changed_by"]
                    ))
            else:
                tk.Label(
                self.content,
                text="No History Found!",
                font=("Arial", 16),
                bg="#ECF0F1",
                fg="red"
                ).pack(pady=20)

        except Exception as e:
            print("Error:", e)
            tk.Label(
            self.content,
            text="Backend Error!",
            font=("Arial", 16),
            bg="#ECF0F1",
            fg="red"
            ).pack(pady=20)

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
        cursor="hand2",
        relief="ridge"
        )
        browse_btn.grid(row=2, column=2, padx=10)
        browse_btn.bind("<Enter>", lambda e: browse_btn.config(bg="#7F8C8D"))
        browse_btn.bind("<Leave>", lambda e: browse_btn.config(bg="#95A5A6"))
        browse_btn.bind("<Button-1>", lambda e: browse_file())

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
        def upload_receipt():
            import requests

            student_id = student_var.get().strip()
            fee_id = fee_var.get().strip()
            file_path = file_var.get()

            try:
                with open(file_path, "rb") as f:
                    files = {"file": f}
                    payload = {"student_id": student_id, "fee_id": fee_id}

                    res = requests.post(
                    "http://127.0.0.1:8000/admin/fees/upload-receipt",
                    data=payload,
                    files=files
                    )

                if res.status_code == 200:
                    self.change_screen("Receipt Uploaded Successfully!")
                else:
                    self.change_screen("Upload Failed!")

            except Exception as e:
                print("UPLOAD ERROR:", e)
                self.change_screen("Error Uploading Receipt!")

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

        tk.Label(form, text="Description:", font=("Arial", 14), bg="#ECF0F1").grid(row=1, column=0, padx=10, pady=10)
        desc_entry = tk.Entry(form, textvariable=desc_var, font=("Arial", 14), width=25)
        desc_entry.grid(row=1, column=1, padx=10)

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
            payload = {
            "method_name": name_var.get().strip(),
            "description": desc_var.get().strip()
            }

            try:
                import requests
                res = requests.post("http://127.0.0.1:8000/admin/payment-methods/add", json=payload)

                if res.status_code == 200:
                    self.change_screen("Payment Method Added!")
                else:
                    self.change_screen("Error Adding Method!")

            except Exception as e:
                print("UPLOAD ERROR:", e)
                self.change_screen("Backend Error!")


    # ===== Button to View Payment Methods =====
    def load_view_methods_screen(self):
        self.clear_content()

        tk.Label(
            self.content, text="Payment Methods",
            font=("Arial", 26, "bold"), bg="#ECF0F1", fg="#2C3E50"
        ).pack(pady=20)

        table_frame = tk.Frame(self.content)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        cols = ("method_id", "method_name", "details")

        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")

        self.method_tree = ttk.Treeview(
        table_frame, columns=cols, show="headings",
        xscrollcommand=x_scroll.set,
        yscrollcommand=y_scroll.set
        )

        # headings
        headers = ["Method ID", "Method Name", "Details"]
        for col_id, col_name in zip(cols, headers):
            self.method_tree.heading(col_id, text=col_name)
            self.method_tree.column(col_id, width=200, anchor="center")

        # Scrollbars
        y_scroll.config(command=self.method_tree.yview)
        x_scroll.config(command=self.method_tree.xview)
 
        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")
        self.method_tree.pack(fill="both", expand=True)

        # Fetch data
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/payment/methods/all")
            data = res.json()

            for row in data:
                self.method_tree.insert("", "end", values=(
                row["method_id"],
                row["method_name"],
                row["details"]
                ))
        except:
            print("Backend error")

    
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

        tk.Label(form, text="Details:", font=("Arial", 14), bg="#ECF0F1").grid(row=2, column=0, padx=10, pady=8)
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
                data = response.json()

                name_entry.config(state="normal")
                details_entry.config(state="normal")

                name_var.set(data["method_name"])
                details_var.set(data["details"])

                print("Loaded:", data)
            else:
                print("Method not found")
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
            payload = {
            "method_name": name_var.get(),
            "details": details_var.get()
            }
            requests.put(
                f"http://127.0.0.1:8000/admin/payment-methods/update/{method_id}",
                json=payload
            )
            self.change_screen("Payment Method Updated Successfully")

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

            import requests
            try:
                res = requests.delete(
                f"http://127.0.0.1:8000/admin/payment-methods/delete/{mid}"
                )

                if res.status_code == 200:
                    self.change_screen("Payment Method Deleted Successfully")
                else:
                    self.change_screen("Failed to Delete Payment Method")

            except Exception as e:
                print("Error deleting method:", e)
                self.change_screen("Backend Error")

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

        # ---- Table Frame ----
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # ---- Scrollbars ----
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        # ---- Treeview ----
        self.att_tree = ttk.Treeview(
            table_frame,
            columns=("attendance_id", "student_id", "subject_id", "class_id",
                   "lecture_date", "status", "remarks"),
            show="headings",
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set,
            height=18
        )

        # Attach scrollbars to treeview
        y_scroll.config(command=self.att_tree.yview)
        x_scroll.config(command=self.att_tree.xview)

        self.att_tree.pack(fill="both", expand=True)

        # ---- Column Setup ----
        cols = {
        "attendance_id": 120,
        "student_id": 100,
        "subject_id": 100,
        "class_id": 100,
        "lecture_date": 150,
        "status": 80,
        "remarks": 200
        }

        for col, width in cols.items():
            self.att_tree.heading(col, text=col.replace("_", " ").title())
            self.att_tree.column(col, width=width)

        # ---- Fetch Data from Backend ----
        import requests
        try:
            response = requests.get("http://127.0.0.1:8000/student")
            data = response.json()

            if not data:
                self.att_tree.insert("", "end", values=("No records found", "", "", "", "", "", ""))
                return

            # Insert rows
            for row in data:
                self.att_tree.insert(
                "",
                "end",
                values=(
                    row["attendance_id"],
                    row["student_id"],
                    row["subject_id"],
                    row["class_id"],
                    row["lecture_date"],
                    row["status"],
                    row["remarks"]
                )
                )

        except Exception as e:
            print("Error fetching student attendance:", e)
            self.att_tree.insert("", "end", values=("Error fetching data", "", "", "", "", "", ""))


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
            import requests

            att_id = att_id_var.get().strip()
            result_box.delete("1.0", "end")

            try:
                res = requests.get(f"http://127.0.0.1:8000/student/{att_id}")

                if res.status_code == 404:
                    result_box.insert("end", "⚠️ Attendance record not found")
                    return

                data = res.json()

                formatted = f"""
                    Attendance ID : {data['attendance_id']}
                    Student ID    : {data['student_id']}
                    Subject ID    : {data['subject_id']}
                    Class ID      : {data['class_id']}
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
        text="Filter Student Attendance",
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

        for i, label in enumerate(labels):
            tk.Label(form, text=label, font=("Arial", 14), bg="#ECF0F1").grid(row=i, column=0, padx=10, pady=8)
            entry = tk.Entry(form, textvariable=vars_list[i], font=("Arial", 14), width=25)
            entry.grid(row=i, column=1, padx=10, pady=8)
            entries.append(entry)

        student_var, from_var, to_var, subject_var = vars_list

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
            from datetime import datetime

            payload = {
            "student_id": int(student_var.get().strip()),
            "date_from": from_var.get().strip(),
            "date_to": to_var.get().strip(),
            "subject_id": int(subject_var.get()) if subject_var.get().strip() else None
            }

            # Clear previous table
            for widget in table_frame.winfo_children():
                widget.destroy()

            try:
                response = requests.post("http://127.0.0.1:8000/student/by-student", json=payload)

                if response.status_code != 200:
                    tk.Label(table_frame, text="❌ No records found", font=("Arial", 14), bg="#ECF0F1", fg="red").pack()
                    return

                records = response.json()

                # ------- TABLE (Treeview) --------
                columns = ["attendance_id", "student_id", "subject_id", "class_id", "lecture_date", "status", "remarks"]

                tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
            
                # Scrollbars
                y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
                tree.configure(yscroll=y_scroll.set)

                y_scroll.pack(side="right", fill="y")
                tree.pack(fill="both", expand=True)

                # Headers
                for col in columns:
                    tree.heading(col, text=col.replace("_", " ").title())
                    tree.column(col, width=150, anchor="center")

                # Insert data
                for rec in records:
                    tree.insert("", "end", values=(
                    rec["attendance_id"],
                    rec["student_id"],
                    rec["subject_id"],
                    rec["class_id"],
                    rec["lecture_date"],
                    rec["status"],
                    rec["remarks"]
                    ))

            except Exception as e:
                tk.Label(table_frame, text=f"❌ Error: {e}", font=("Arial", 14), bg="#ECF0F1", fg="red").pack()


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
            tk.Label(form, text=label_text, bg="#ECF0F1", font=("Arial", 14)).grid(row=i, column=0, padx=10, pady=8)
            tk.Entry(form, textvariable=var, font=("Arial", 14), width=25).grid(row=i, column=1, padx=10, pady=8)

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
            for w in result_frame.winfo_children():
                w.destroy()

            import requests

            student_id = student_var.get().strip()
            date_from = from_var.get().strip()
            date_to = to_var.get().strip()

            url = f"http://127.0.0.1:8000/student/summary/{student_id}?date_from={date_from}&date_to={date_to}"

            try:
                res = requests.get(url)
                data = res.json()

                # Summary Card
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
                    tk.Label(card, text=f"{label_text}: ", font=("Arial", 14, "bold"), bg="white").grid(row=idx, column=0, sticky="w", pady=5)
                    tk.Label(card, text=value, font=("Arial", 14), bg="white").grid(row=idx, column=1, sticky="w", pady=5)

            except Exception as e:
                tk.Label(result_frame, text=f"Error: {e}", bg="#ECF0F1", fg="red", font=("Arial", 14)).pack()


    # ==== Button to update attendance of any student using attendance_id ====
    def load_update_student_attendance_screen(self):
        self.clear_content()

        # ---------- HEADER ----------
        tk.Label(
        self.content,
        text="Update Student Attendance",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # ---------- INPUT: Attendance ID ----------
        tk.Label(form, text="Attendance ID:", font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=0, pady=8)
    
        att_id_var = tk.StringVar()
        att_id_entry = tk.Entry(form, textvariable=att_id_var, font=("Arial", 14), width=25)
        att_id_entry.grid(row=0, column=1, padx=10, pady=8)

        # ---------- LOAD BUTTON ----------
        load_btn = tk.Label(
        form, text="Load", font=("Arial", 12, "bold"),
        bg="#D5D8DC", fg="#AEB6BF", padx=15, pady=7,
        relief="ridge", cursor="arrow", width=12
        )
        load_btn.grid(row=0, column=2, padx=10)

        # ---------- FORM FIELDS (initially disabled) ----------
        labels = ["Student ID", "Class ID", "Subject ID", "Teacher ID", "Date (YYYY-MM-DD)", "Status (P/A/L)", "Remarks"]
        self.update_fields = {}
        self.update_vars = {}

        for i, t in enumerate(labels, start=1):
            tk.Label(form, text=f"{t}:", font=("Arial", 14), bg="#ECF0F1").grid(row=i, column=0, pady=8)
            var = tk.StringVar()
            entry = tk.Entry(form, textvariable=var, font=("Arial", 14), width=25, state="disabled")
            entry.grid(row=i, column=1, padx=10, pady=8)

            self.update_vars[t] = var
            self.update_fields[t] = entry

        # ---------- UPDATE BUTTON ----------
        update_btn = tk.Button(
        self.content,
        text="Update Attendance",
        bg="#D5D8DC", fg="#AEB6BF",
        state="disabled",
        font=("Arial", 14, "bold"),
        padx=20, pady=10
        )
        update_btn.pack(pady=25)

        # ---------- VALIDATION ----------
        def validate_update(*args):
            if all(v.get().strip() for v in self.update_vars.values()):
                update_btn.config(
                state="normal",
                bg="#000000", fg="white",
                activebackground="#111111",
                activeforeground="white",
                relief="flat"
                )
            else:
                update_btn.config(
                state="disabled",
                bg="#D5D8DC", fg="#AEB6BF",
                relief="groove"
                )

        for v in self.update_vars.values():
            v.trace_add("write", validate_update)

        # ---------- LOAD EXISTING ATTENDANCE ----------
        def load_attendance():
            import requests

            att_id = att_id_var.get().strip()
            if not att_id:
                return

            try:
                url = f"http://127.0.0.1:8000/student/{att_id}"
                res = requests.get(url)

                if res.status_code != 200:
                    tk.Label(self.content, text="❌ Attendance not found", fg="red", bg="#ECF0F1").pack()
                    return

                data = res.json()

                # Enable all fields
                for entry in self.update_fields.values():
                    entry.config(state="normal")

                # Fill data
                self.update_vars["Student ID"].set(data["student_id"])
                self.update_vars["Class ID"].set(data["class_id"])
                self.update_vars["Subject ID"].set(data["subject_id"])
                self.update_vars["Teacher ID"].set(data["teacher_id"])
                self.update_vars["Date (YYYY-MM-DD)"].set(data["lecture_date"])
                self.update_vars["Status (P/A/L)"].set(data["status"])
                self.update_vars["Remarks"].set(data.get("remarks", ""))

            except Exception as e:
                print("ERR:", e)

        # Enable load button
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

        # ---------- SUBMIT UPDATE ----------
        def submit_update():
            import requests

            att_id = att_id_var.get().strip()
            payload = {
            "student_id": int(self.update_vars["Student ID"].get()),
            "class_id": int(self.update_vars["Class ID"].get()),
            "subject_id": int(self.update_vars["Subject ID"].get()),
            "teacher_id": int(self.update_vars["Teacher ID"].get()),
            "lecture_date": self.update_vars["Date (YYYY-MM-DD)"].get(),
            "status": self.update_vars["Status (P/A/L)"].get(),
            "remarks": self.update_vars["Remarks"].get(),
            }

            requests.put(f"http://127.0.0.1:8000/student/{att_id}", json=payload)

            self.change_screen("Student Attendance Updated Successfully")

        update_btn.config(command=submit_update)


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

            try:
                url = f"http://127.0.0.1:8000/student/{att_id}"
                response = requests.delete(url)

                if response.status_code == 200:
                    self.change_screen("Attendance Deleted Successfully")
                else:
                    tk.Label(
                    self.content, text="Attendance Not Found",
                    fg="red", bg="#ECF0F1", font=("Arial", 14)
                    ).pack(pady=10)

            except Exception as e:
                tk.Label(
                self.content, text=f"Error: {e}",
                fg="red", bg="#ECF0F1", font=("Arial", 14)
                ).pack(pady=10)
 
    # ===========================================================================
    # --- TEACHERS ATTENDANCE ---
    # ==== Button to View Attendance of teachers ====
    def load_view_all_teacher_attendance(self):
        self.clear_content()

        title = tk.Label(
        self.content,
        text="All Teacher Attendance Records",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        )
        title.pack(pady=20)

        # Table frame
        table_frame = tk.Frame(self.content)
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Scrollbars
        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")

        self.teacher_tree = ttk.Treeview(
        table_frame,
        columns=("record_id", "teacher_id", "date", "status", "remarks"),
        show="headings",
        xscrollcommand=x_scroll.set,
        yscrollcommand=y_scroll.set,
        height=20
        )

        # Scrollbar config
        x_scroll.config(command=self.teacher_tree.xview)
        y_scroll.config(command=self.teacher_tree.yview)

        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")
        self.teacher_tree.pack(fill="both", expand=True)

        # Table headers
        headers = ["Record ID", "Teacher ID", "Date", "Status", "Remarks"]
        for col in headers:
            col_id = col.lower().replace(" ", "_")
            self.teacher_tree.heading(col_id, text=col)
            self.teacher_tree.column(col_id, width=160, anchor="center")

        # ---- Fetch From Backend ----
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admin/attendance/teacher")
            if res.status_code == 200:
                data = res.json()

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
            else:
                print("Error fetching data:", res.text)

        except Exception as e:
            print("Backend error:", e)

    
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

            import requests
            try:
                res = requests.get(f"http://127.0.0.1:8000/admin/attendance/teacher/{record_id}")

                if res.status_code == 200:
                    data = res.json()

                    # enable boxes
                    tk_id.config(state="normal")
                    date_entry.config(state="normal")
                    status_entry.config(state="normal")
                    remarks_entry.config(state="normal")

                    # clear previous
                    tk_id.delete(0, "end")
                    date_entry.delete(0, "end")
                    status_entry.delete(0, "end")
                    remarks_entry.delete(0, "end")

                    # fill values
                    tk_id.insert(0, data["teacher_id"])
                    date_entry.insert(0, data["date"])
                    status_entry.insert(0, data["status"])
                    remarks_entry.insert(0, data.get("remarks", ""))

                    # make them readonly again
                    tk_id.config(state="disabled")
                    date_entry.config(state="disabled")
                    status_entry.config(state="disabled")
                    remarks_entry.config(state="disabled")

                else:
                    print("Record Not Found")

            except Exception as e:
                print("Backend Error:", e)


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

        tk.Label(form, text="From Date (YYYY-MM-DD):", font=("Arial", 14), bg="#ECF0F1")\
            .grid(row=1, column=0, padx=10, pady=8)
        from_var = tk.StringVar()
        from_entry = tk.Entry(form, textvariable=from_var, font=("Arial", 14), width=25)
        from_entry.grid(row=1, column=1, padx=10, pady=8)

        tk.Label(form, text="To Date (YYYY-MM-DD):", font=("Arial", 14), bg="#ECF0F1")\
            .grid(row=2, column=0, padx=10, pady=8)
        to_var = tk.StringVar()
        to_entry = tk.Entry(form, textvariable=to_var, font=("Arial", 14), width=25)
        to_entry.grid(row=2, column=1, padx=10, pady=8)

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
        for i, field in enumerate(["Total Days", "Present", "Absent", "Leave", "Percentage"]):
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

            import requests
            url = f"http://127.0.0.1:8000/admin/attendance/summary/{teacher_id}?date_from={date_from}&date_to={date_to}"

            try:
                res = requests.get(url)
                data = res.json()

                labels["Total Days"].config(text=f"Total Days: {data['total_days']}")
                labels["Present"].config(text=f"Present: {data['present']}")
                labels["Absent"].config(text=f"Absent: {data['absent']}")
                labels["Leave"].config(text=f"Leave: {data['leave']}")
                labels["Percentage"].config(text=f"Percentage: {data['percentage']}%")

            except Exception as e:
                print("Failed to fetch summary:", e)


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
        "Check-in": tk.StringVar(),
        "Check-out": tk.StringVar(),
        "Status": tk.StringVar(),
        "Remarks": tk.StringVar()
        }

        row_index = 1
        entries = {}

        for label, var in fields.items():
            tk.Label(form, text=f"{label}:", font=("Arial", 14), bg="#ECF0F1")\
                .grid(row=row_index, column=0, padx=10, pady=8)

            ent = tk.Entry(form, textvariable=var, font=("Arial", 14), width=25, state="disabled")
            ent.grid(row=row_index, column=1, padx=10, pady=8)

            entries[label] = ent
            row_index += 1

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

            import requests
            try:
                res = requests.get(f"http://127.0.0.1:8000/admin/attendance/teacher/{rec_id}")
                data = res.json()

                # Enable all input fields
                for ent in entries.values():
                    ent.config(state="normal")

                # Fill values
                fields["Teacher ID"].set(data["teacher_id"])
                fields["Date"].set(data["on_date"])
                fields["Check-in"].set(data.get("check_in", ""))
                fields["Check-out"].set(data.get("check_out", ""))
                fields["Status"].set(data["status"])
                fields["Remarks"].set(data.get("remarks", ""))

                enable_update_validation()

            except Exception as e:
                print("Error fetching teacher attendance:", e)

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
            payload = {
            "teacher_id": int(fields["Teacher ID"].get()),
            "on_date": fields["Date"].get(),
            "check_in": fields["Check-in"].get(),
            "check_out": fields["Check-out"].get(),
            "status": fields["Status"].get(),
            "remarks": fields["Remarks"].get()
            }

            import requests
            rec_id = record_var.get().strip()
            try:
                requests.put(f"http://127.0.0.1:8000/admin/attendance/teacher/{rec_id}", json=payload)
                self.change_screen("Teacher Attendance Updated Successfully")
            except:
                print("Failed to update teacher attendance")


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

            import requests
            try:
                url = f"http://127.0.0.1:8000/admin/attendance/teacher/{rec_id}"
                res = requests.delete(url)

                if res.status_code == 200:
                    self.change_screen("Teacher Attendance Deleted Successfully")
                else:
                    print("Error:", res.text)

            except Exception as e:
                print("Failed to delete:", e)

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
        ("Date of Birth (YYYY-MM-DD)", "dob"),
        ("Class Name (e.g. X, IX)", "class_name"),
        ("Address", "address"),
        ("Phone", "phone"),
        ("Email", "email")
        ]

        vars = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(form, text=f"{label}:", font=("Arial", 14), bg="#ECF0F1").grid(row=i, column=0, padx=10, pady=6)
            vars[key] = tk.StringVar()
            tk.Entry(form, textvariable=vars[key], font=("Arial", 14), width=30).grid(row=i, column=1, padx=10, pady=6)

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
            import requests

            data = {k: v.get().strip() for k, v in vars.items()}

            try:
                res = requests.post("http://127.0.0.1:8000/admission/", json=data)
                if res.status_code == 200:
                    self.change_screen("Admission Request Submitted!")
                else:
                    print("Error:", res.text)
            except:
                print("Backend not reachable")

    
    # ====== Button to view all admissions ======
    def load_view_all_admissions_screen(self):
        self.clear_content()

        # Title
        tk.Label(
        self.content,
        text="All Admissions",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # Frame for table + scrollbars
        table_frame = tk.Frame(self.content, bg="#ECF0F1")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Scrollbars
        y_scroll = tk.Scrollbar(table_frame, orient="vertical")
        x_scroll = tk.Scrollbar(table_frame, orient="horizontal")

        # Treeview (table)
        self.admission_tree = ttk.Treeview(
        table_frame,
        columns=("ID", "Full Name", "Gender", "DOB", "Class", "Address", "Phone", "Email"),
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
        )

        y_scroll.config(command=self.admission_tree.yview)
        x_scroll.config(command=self.admission_tree.xview)

        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")
        self.admission_tree.pack(fill="both", expand=True)

        # Set column headings
        columns = ["ID", "Full Name", "Gender", "DOB", "Class", "Address", "Phone", "Email"]

        for col in columns:
            self.admission_tree.heading(col, text=col)
            self.admission_tree.column(col, width=150, anchor="center")

        # Fetch data from backend
        import requests
        try:
            res = requests.get("http://127.0.0.1:8000/admission/")
            data = res.json()

            for row in data:
                self.admission_tree.insert(
                "", "end",
                values=(
                    row["admission_id"],
                    row["full_name"],
                    row["gender"],
                    row["dob"],
                    row["class_name"],
                    row["address"],
                    row["phone"],
                    row["email"]
                    )
                )
        except Exception as e:
            print("Error loading admissions:", e)


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

        labels = ["Full Name", "Gender", "DOB", "Class", "Address", "Phone", "Email"]
        vars_dict = {}

        for i, label in enumerate(labels):
            tk.Label(output_frame, text=f"{label}:", font=("Arial", 14), bg="#ECF0F1").grid(row=i, column=0, padx=10, pady=6)
            var = tk.StringVar()
            entry = tk.Entry(output_frame, textvariable=var, font=("Arial", 14), width=30, state="disabled")
            entry.grid(row=i, column=1, padx=10, pady=6)
            vars_dict[label] = var

        # ---------- FETCH FUNCTION ----------
        def fetch_admission():
            adm_id = adm_id_var.get().strip()

            import requests
            try:
                res = requests.get(f"http://127.0.0.1:8000/admission/{adm_id}")

                if res.status_code != 200:
                    print("Not found")
                    for k in vars_dict.values():
                        k.set("")
                    return

                data = res.json()

                vars_dict["Full Name"].set(data["full_name"])
                vars_dict["Gender"].set(data["gender"])
                vars_dict["DOB"].set(data["dob"])
                vars_dict["Class"].set(data["class_name"])
                vars_dict["Address"].set(data["address"])
                vars_dict["Phone"].set(data["phone"])
                vars_dict["Email"].set(data["email"])

            except Exception as e:
                print("Error fetching admission:", e)

    
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

        fields = ["Full Name", "Gender", "DOB", "Class", "Address", "Phone", "Email"]
        vars_dict = {}

        for i, label in enumerate(fields):
            tk.Label(output_frame, text=f"{label}:", font=("Arial", 14), bg="#ECF0F1").grid(
            row=i, column=0, padx=10, pady=6, sticky="w"
            )
            var = tk.StringVar()
            entry = tk.Entry(output_frame, textvariable=var, font=("Arial", 14),
                            width=35, state="disabled")
            entry.grid(row=i, column=1, padx=10, pady=6)
            vars_dict[label] = var

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
            import requests

            try:
                res = requests.get(f"http://127.0.0.1:8000/admission/{adm_id}")

                if res.status_code != 200:
                    print("Admission Not Found")
                    disable_approve()
                    for v in vars_dict.values():
                        v.set("")
                    return

                data = res.json()

                vars_dict["Full Name"].set(data["full_name"])
                vars_dict["Gender"].set(data["gender"])
                vars_dict["DOB"].set(data["dob"])
                vars_dict["Class"].set(data["class_name"])
                vars_dict["Address"].set(data["address"])
                vars_dict["Phone"].set(data["phone"])
                vars_dict["Email"].set(data["email"])

                enable_approve()

            except Exception as e:
                print("Error:", e)

        # ---------- APPROVE ADMISSION FUNCTION ----------
        def approve_admission():
            adm_id = adm_id_var.get().strip()
            import requests

            try:
                res = requests.post(f"http://127.0.0.1:8000/admission/approve/{adm_id}")

                if res.status_code == 200:
                    self.change_screen(
                        f"Admission Approved Successfully!\nStudent ID: {res.json()['student_id']}"
                    )
                else:
                    print("Approve failed:", res.text)

            except Exception as e:
                print("Error approving admission:", e)


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

