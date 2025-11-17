import tkinter as tk
from tkinter import ttk, messagebox
from Backend.Admin import timetable_backend
from config import connect_db


class TimetableUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📅 Timetable Management")

        try:
            self.root.state("zoomed")
        except tk.TclError:
            self.root.attributes("-zoomed", True)

        self.root.minsize(1000, 650)

        # ---------- Variables ----------
        self.var_class = tk.StringVar()
        self.var_day = tk.StringVar()
        self.var_subject = tk.StringVar()
        self.var_teacher = tk.StringVar()
        self.var_start = tk.StringVar()
        self.var_end = tk.StringVar()

        self.selected_id = None  # timetable_id (hidden)

        self.class_map = {}
        self.teacher_map = {}

        # ---------- Title ----------
        title = tk.Label(
            self.root,
            text="📅 Timetable Management",
            font=("Arial", 22, "bold"),
            bg="navy",
            fg="white",
            pady=8,
        )
        title.pack(side=tk.TOP, fill=tk.X)

        # ---------- Layout ----------
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Left Form
        form_frame = tk.LabelFrame(
            main_frame,
            text="Add / Edit Timetable",
            font=("Arial", 12, "bold"),
            bd=2,
            relief=tk.RIDGE,
        )
        form_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        self.create_form_fields(form_frame)
        self.create_buttons(form_frame)
        self.create_table(main_frame)

        # Load dropdowns + table
        self.load_combobox_data()
        self.fetch_records()

    # ------------------------------------------------------------
    # FORM
    # ------------------------------------------------------------
    def create_form_fields(self, form_frame):
        # Class Dropdown
        tk.Label(form_frame, text="Class:", font=("Arial", 12)).grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )
        self.class_combo = ttk.Combobox(
            form_frame, textvariable=self.var_class,
            font=("Arial", 12), state="readonly", width=18
        )
        self.class_combo.grid(row=0, column=1, padx=10, pady=5)

        # Day Dropdown
        tk.Label(form_frame, text="Day:", font=("Arial", 12)).grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        self.day_combo = ttk.Combobox(
            form_frame, textvariable=self.var_day,
            font=("Arial", 12), state="readonly", width=18
        )
        self.day_combo["values"] = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday")
        self.day_combo.grid(row=1, column=1, padx=10, pady=5)

        # Subject Dropdown
        tk.Label(form_frame, text="Subject:", font=("Arial", 12)).grid(
            row=2, column=0, padx=10, pady=5, sticky="w"
        )
        self.subject_combo = ttk.Combobox(
            form_frame, textvariable=self.var_subject,
            font=("Arial", 12), state="readonly", width=18
        )
        self.subject_combo.grid(row=2, column=1, padx=10, pady=5)

        # Teacher Dropdown
        tk.Label(form_frame, text="Teacher:", font=("Arial", 12)).grid(
            row=3, column=0, padx=10, pady=5, sticky="w"
        )
        self.teacher_combo = ttk.Combobox(
            form_frame, textvariable=self.var_teacher,
            font=("Arial", 12), state="readonly", width=18
        )
        self.teacher_combo.grid(row=3, column=1, padx=10, pady=5)
        self.teacher_combo.bind("<<ComboboxSelected>>", self.auto_fill_subject)

        # Start Time
        tk.Label(form_frame, text="Start Time:", font=("Arial", 12)).grid(
            row=4, column=0, padx=10, pady=5, sticky="w"
        )
        tk.Entry(form_frame, textvariable=self.var_start, font=("Arial", 12), width=20).grid(
            row=4, column=1, padx=10, pady=5
        )

        # End Time
        tk.Label(form_frame, text="End Time:", font=("Arial", 12)).grid(
            row=5, column=0, padx=10, pady=5, sticky="w"
        )
        tk.Entry(form_frame, textvariable=self.var_end, font=("Arial", 12), width=20).grid(
            row=5, column=1, padx=10, pady=5
        )

    # ------------------------------------------------------------
    # BUTTONS
    # ------------------------------------------------------------
    def create_buttons(self, form_frame):
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=15)

        buttons = [
            ("Add", "green", self.add_record),
            ("Update", "blue", self.update_record),
            ("Delete", "red", self.delete_record),
            ("Clear", "gray", self.clear_fields),
            ("Show", "orange", self.fetch_records),
        ]

        for i, (text, color, cmd) in enumerate(buttons):
            tk.Button(
                btn_frame, text=text,
                bg=color, fg="white",
                font=("Arial", 12, "bold"),
                command=cmd
            ).grid(row=0, column=i, padx=5)

    # ------------------------------------------------------------
    # TABLE (with hidden ID)
    # ------------------------------------------------------------
    def create_table(self, main_frame):
        table_frame = tk.LabelFrame(
            main_frame,
            text="Timetable Records",
            font=("Arial", 12, "bold"),
            bd=2,
            relief=tk.RIDGE,
        )
        table_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # ✔ We include timetable_id as first column but hide it
        self.table = ttk.Treeview(
            table_frame,
            columns=("timetable_id", "class_name", "day", "subject", "teacher", "start_time", "end_time"),
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        self.table.pack(fill=tk.BOTH, expand=True)

        scroll_y.config(command=self.table.yview)
        scroll_x.config(command=self.table.xview)

        # Table headings
        self.table.heading("timetable_id", text="", anchor="center")
        self.table.column("timetable_id", width=0, stretch=False)  # HIDDEN COLUMN

        for col in ("class_name", "day", "subject", "teacher", "start_time", "end_time"):
            self.table.heading(col, text=col.capitalize())
            self.table.column(col, anchor="center", stretch=True)

        self.table.bind("<ButtonRelease-1>", self.get_selected_row)

    # ------------------------------------------------------------
    # LOAD DROPDOWNS
    # ------------------------------------------------------------
    def load_combobox_data(self):
        try:
            classes = timetable_backend.get_class_data()
            self.class_map = {row["class_name"]: row["class_id"] for row in classes}
            self.class_combo["values"] = list(self.class_map.keys())

            teachers = timetable_backend.get_teacher_data()
            self.teacher_map = {row["name"]: row["teacher_id"] for row in teachers}
            self.teacher_combo["values"] = list(self.teacher_map.keys())

            subjects = timetable_backend.get_subject_data()
            self.subject_combo["values"] = subjects

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load dropdowns:\n{e}", parent=self.root)

    # Auto-fill subject when teacher selected
    def auto_fill_subject(self, event):
        teacher_name = self.var_teacher.get()
        con = connect_db()
        cur = con.cursor()
        cur.execute("SELECT subject FROM teachers WHERE name=%s", (teacher_name,))
        row = cur.fetchone()
        con.close()
        if row:
            self.var_subject.set(row["subject"])

    # ------------------------------------------------------------
    # CRUD LOGIC
    # ------------------------------------------------------------
    def add_record(self):
        try:
            timetable_backend.add_timetable_record(
                self.class_map[self.var_class.get()],
                self.var_day.get(),
                self.var_subject.get(),
                self.teacher_map.get(self.var_teacher.get(), None),
                self.var_start.get(),
                self.var_end.get(),
            )
            messagebox.showinfo("Success", "Timetable added successfully!", parent=self.root)
            self.fetch_records()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add record:\n{e}", parent=self.root)

    def update_record(self):
        if not self.selected_id:
            messagebox.showwarning("Select a record first.", parent=self.root)
            return

        try:
            timetable_backend.update_timetable_record(
                self.selected_id,
                self.class_map[self.var_class.get()],
                self.var_day.get(),
                self.var_subject.get(),
                self.teacher_map.get(self.var_teacher.get(), None),
                self.var_start.get(),
                self.var_end.get(),
            )
            messagebox.showinfo("Updated", "Record updated!", parent=self.root)
            self.fetch_records()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update:\n{e}", parent=self.root)

    def delete_record(self):
        if not self.selected_id:
            messagebox.showwarning("Select a record first.", parent=self.root)
            return

        try:
            timetable_backend.delete_timetable_record(self.selected_id)
            messagebox.showinfo("Deleted", "Record deleted!", parent=self.root)
            self.fetch_records()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete:\n{e}", parent=self.root)

    # ------------------------------------------------------------
    # FILTER / SHOW RECORDS
    # ------------------------------------------------------------
    def fetch_records(self):
        try:
            rows = timetable_backend.fetch_timetable_records(
                class_id=self.class_map.get(self.var_class.get(), None),
                teacher_id=self.teacher_map.get(self.var_teacher.get(), None),
                subject=self.var_subject.get() or None,
                day=self.var_day.get() or None
            )

            self.table.delete(*self.table.get_children())

            if not rows:
                messagebox.showinfo("No Records", "No records found.", parent=self.root)
                return

            for row in rows:
                self.table.insert("", tk.END, values=(
                    row["timetable_id"],
                    row["class_name"],
                    row["day"],
                    row["subject"],
                    row["teacher"],
                    row["start_time"],
                    row["end_time"],
                ))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch:\n{e}", parent=self.root)

    # ------------------------------------------------------------
    # GET SELECTED ROW (Correct Mapping)
    # ------------------------------------------------------------
    def get_selected_row(self, event):
        selected = self.table.focus()
        if not selected:
            return

        values = self.table.item(selected, "values")
        if not values:
            return

        self.selected_id = values[0]  # hidden column

        # Fill form using correct order
        self.var_class.set(values[1])
        self.var_day.set(values[2])
        self.var_subject.set(values[3])
        self.var_teacher.set(values[4])
        self.var_start.set(values[5])
        self.var_end.set(values[6])

    # ------------------------------------------------------------
    # CLEAR FIELDS
    # ------------------------------------------------------------
    def clear_fields(self):
        self.var_class.set("")
        self.var_day.set("")
        self.var_subject.set("")
        self.var_teacher.set("")
        self.var_start.set("")
        self.var_end.set("")
        self.selected_id = None
        self.fetch_records()


if __name__ == "__main__":
    root = tk.Tk()
    app = TimetableUI(root)
    root.mainloop()
