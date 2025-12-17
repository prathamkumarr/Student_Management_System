import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import datetime

# =============
class StaffUI:
    def __init__(self, root, staff_id = 4):
        self.root = root

        # teacher Logged-In Details (Dummy OR Fetched From Login)
        self.staff_id = staff_id

        self.root.title("School ERP - Staff Panel")
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
            text="STAFF PANEL",
            bg="#1E2A38",
            fg="white",
            font=("Arial", 18, "bold")
            ).pack(pady=20)

        # Main Buttons
        att_btn = self.add_btn("Mark and View Attendance")
        self.build_attendance_dropdown(att_btn)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()


    # ===== DROPDOWN MENUS =====
    # ===============================================
    def build_attendance_dropdown(self, parent_label):
        menu = tk.Menu(self.root, tearoff=0)
  
        menu.add_command(label="Mark Self Attendance", command=self.load_mark_self_attendance)
        menu.add_command(label="View All Attendance", command=self.load_staff_attendance_filter)
        menu.add_command(label="Attendance Summary", command=self.load_staff_attendance_summary_screen)

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
        bg="#000000", fg="white",
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
        # Staff ID (auto-filled, not editable)
        tk.Label(
        form,
        text="Staff ID:",
        font=("Arial", 14),
        bg="#ECF0F1"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        staff_id_var = tk.StringVar(value=str(self.staff_id))
        tk.Entry(
        form, textvariable=staff_id_var, font=("Arial", 14), width=25, state="readonly"
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
    "staff_id": int(staff_id_var.get().strip()),
    "date": date_var.get().strip(),
    "check_in": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    "status": status_var.get(),   # P / A / L
    "remarks": "Self Attendance Marked"
}

            try:
                res = requests.post(
                "http://127.0.0.1:8000/staff/attendance/mark-self",
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
                    self.show_popup("Staff member Not Found", "Invalid Staff ID!", "error")
                    return

                self.show_popup("Error", f"Unexpected Error: {res.text}", "error")

            except Exception as e:
                self.show_popup("Backend Error", f"Error: {e}", "error")


    # ==========================================================================
    # ===== Button to View Filtered Staff Attendance by Date =====
    def load_staff_attendance_filter(self):
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

        # Staff ID (readonly)
        tk.Label(form, text="Staff ID:", font=("Arial", 14), bg="#ECF0F1").grid(row=0, column=0, padx=10, pady=10)
        staff_id_var = tk.StringVar(value=str(self.staff_id))
        tk.Entry(form, textvariable=staff_id_var, font=("Arial", 14), width=25, state="readonly").grid(row=0, column=1)

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
            filter_btn.config(bg="#000000", fg="white", cursor="arrow")
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
            tid = staff_id_var.get()
            d1 = date_from_var.get()
            d2 = date_to_var.get()

            import requests
            try:
                url = f"http://127.0.0.1:8000/staff/attendance/self/{tid}?date_from={d1}&date_to={d2}"
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
    # ===== Button to View Staff Attendance Summary =====
    def load_staff_attendance_summary_screen(self):
        self.clear_content()

        import requests
        import re

        # ---- TITLE ----
        tk.Label(
        self.content,
        text="Staff Attendance Summary",
        font=("Arial", 26, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
        ).pack(pady=20)

        # ---- FORM FRAME ----
        form = tk.Frame(self.content, bg="#ECF0F1")
        form.pack(pady=10)

        # ====== FIELDS ======

        # Staff ID
        tk.Label(
        form,
        text="Staff ID:",
        font=("Arial", 14),
        bg="#ECF0F1"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        staff_id_var = tk.StringVar(value=str(self.staff_id))
        staff_id_entry = tk.Entry(
            form,
            textvariable=staff_id_var,
            font=("Arial", 14),
            width=25,
            state="disabled",
            disabledbackground="#F2F3F4",
            disabledforeground="black"
        )
        staff_id_entry.grid(row=0, column=1, padx=10, pady=10)

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
            submit_btn.config(bg="#000000", fg="white", cursor="arrow")
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

        staff_id_var.trace_add("write", validate)
        date_from_var.trace_add("write", validate)
        date_to_var.trace_add("write", validate)

        # ---- SUMMARY BOX FRAME ----
        summary_frame = tk.Frame(self.content, bg="#ECF0F1")
        summary_frame.pack(pady=20)

        # ---- FETCH SUMMARY FUNCTION ----
        def fetch_summary():
            sid = staff_id_var.get().strip()
            d1 = date_from_var.get().strip()
            d2 = date_to_var.get().strip()

            try:
                url = f"http://127.0.0.1:8000/teacher/attendance/summary/{sid}?date_from={d1}&date_to={d2}"
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
    # ===== DASHBOARD PAGE ======
    def load_dashboard(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        tk.Label(
            self.content,
            text="Staff Dashboard",
            font=("Arial", 26, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
            ).pack(pady=20)

        box = tk.Frame(self.content, bg="white", bd=2, relief="groove")
        box.pack(pady=60)

        tk.Label(
            box,
            text="Welcome to the Staff Panel!",
            font=("Arial", 16),
            bg="white"
            ).pack(padx=40, pady=30)


# ======== RUN UI ========
if __name__ == "__main__":
    root = tk.Tk()
    app = StaffUI(root)
    root.mainloop()