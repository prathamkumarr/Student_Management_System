import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry

from Backend.Admin import work_backend


class WorkModule:
    def __init__(self, root):
        self.root = root
        self.root.title("📘 Work Management")

        try:
            self.root.state("zoomed")
        except tk.TclError:
            self.root.attributes("-zoomed", True)

        self.root.minsize(1000, 650)

        # ---------- Variables ----------
        self.var_class = tk.StringVar()
        self.var_type = tk.StringVar()
        self.var_subject = tk.StringVar()
        self.var_title = tk.StringVar()
        self.var_teacher = tk.StringVar()
        self.var_due = tk.StringVar()
        self.var_desc = tk.StringVar()
        self.var_file_path = tk.StringVar()

        self.selected_id = None
        self.class_map = {}
        self.teacher_map = {}

        # ---------- TITLE ----------
        tk.Label(
            self.root,
            text="📘 Work Management (Classwork / Homework / Assignment)",
            font=("Arial", 22, "bold"),
            bg="navy", fg="white", pady=8
        ).pack(fill=tk.X)

        # ---------- MAIN LAYOUT ----------
        main = tk.Frame(self.root)
        main.pack(fill=tk.BOTH, expand=True)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)

        # ---------- LEFT FORM ----------
        form = tk.LabelFrame(main, text="Add / Edit Work", font=("Arial", 12, "bold"), bd=2)
        form.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        # ---- Create fields using a loop ----
        self._make_label(form, "Class:", 0)
        self.class_combo = self._make_combo(form, self.var_class, 0)

        self._make_label(form, "Type:", 1)
        self.type_combo = self._make_combo(form, self.var_type, 1, values=("Classwork", "Homework", "Assignment"))

        self._make_label(form, "Subject:", 2)
        self.subject_combo = self._make_combo(form, self.var_subject, 2)

        self._make_label(form, "Title:", 3)
        tk.Entry(form, textvariable=self.var_title, font=("Arial", 12), width=20).grid(row=3, column=1, padx=10, pady=5)

        self._make_label(form, "Description:", 4)
        tk.Entry(form, textvariable=self.var_desc, font=("Arial", 12), width=20).grid(row=4, column=1, padx=10, pady=5)

        self._make_label(form, "Due Date:", 5)
        self.due_entry = DateEntry(form, textvariable=self.var_due, font=("Arial", 12),
                                   width=18, date_pattern="yyyy-mm-dd")
        self.due_entry.grid(row=5, column=1, padx=10, pady=5)

        self._make_label(form, "Teacher:", 6)
        self.teacher_combo = self._make_combo(form, self.var_teacher, 6)

        # PDF File
        self._make_label(form, "PDF File:", 7)
        tk.Entry(form, textvariable=self.var_file_path, font=("Arial", 10), width=20,
                 state="readonly").grid(row=7, column=1, padx=10, pady=5)
        tk.Button(
            form, text="Browse", command=self.browse_file,
            bg="#004b87", fg="white", font=("Arial", 10, "bold")
        ).grid(row=7, column=2, padx=5)

        # ---------- BUTTONS ----------
        btn_frame = tk.Frame(form)
        btn_frame.grid(row=8, column=0, columnspan=3, pady=15)

        btns = [
            ("Add", "green", self.add_record),
            ("Update", "blue", self.update_record),
            ("Delete", "red", self.delete_record),
            ("Clear", "gray", self.clear_fields),
            ("Show", "orange", self.fetch_records)
        ]

        for i, (name, color, cmd) in enumerate(btns):
            tk.Button(btn_frame, text=name, bg=color, fg="white",
                      font=("Arial", 12, "bold"), command=cmd).grid(row=0, column=i, padx=5)

        # ---------- TABLE ----------
        self._create_table(main)

        # Load dropdown data
        self.load_combobox_data()
        self.fetch_records()

    # -------------------------------------------------------
    # HELPERS
    # -------------------------------------------------------

    def _make_label(self, parent, text, row):
        tk.Label(parent, text=text, font=("Arial", 12)).grid(
            row=row, column=0, padx=10, pady=5, sticky="w"
        )

    def _make_combo(self, parent, var, row, values=None):
        combo = ttk.Combobox(parent, textvariable=var, font=("Arial", 12),
                             width=18, state="readonly")
        if values:
            combo["values"] = values
        combo.grid(row=row, column=1, padx=10, pady=5)
        return combo

    def _create_table(self, parent):
        table_frame = tk.LabelFrame(parent, text="Work Records", font=("Arial", 12, "bold"))
        table_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)

        columns = ("id", "class", "type", "subject", "title",
                   "due_date", "teacher", "file", "description")

        self.table = ttk.Treeview(
            table_frame, columns=columns, show="headings",
            yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set
        )

        scroll_y.config(command=self.table.yview)
        scroll_x.config(command=self.table.xview)

        self.table.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        for col in columns:
            self.table.heading(col, text=col.capitalize())
            self.table.column(col, width=150, minwidth=120, anchor="center")

        self.table.bind("<ButtonRelease-1>", self.get_selected_row)

    # -------------------------------------------------------
    # DATA LOADERS
    # -------------------------------------------------------

    def browse_file(self):
        path = filedialog.askopenfilename(
            title="Select PDF", filetypes=[("PDF Files", "*.pdf")]
        )
        if path:
            self.var_file_path.set(path)

    def load_combobox_data(self):
        try:
            classes = work_backend.get_class_data()
            teachers = work_backend.get_teacher_data()
            subjects = work_backend.get_subject_data()

            self.class_map = {row["class_name"]: row["class_id"] for row in classes}
            self.teacher_map = {row["name"]: row["teacher_id"] for row in teachers}

            self.class_combo["values"] = list(self.class_map.keys())
            self.teacher_combo["values"] = list(self.teacher_map.keys())
            self.subject_combo["values"] = subjects

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load dropdown data:\n{e}", parent=self.root)

    # -------------------------------------------------------
    # CRUD OPERATIONS 
    # -------------------------------------------------------

    def add_record(self):
        try:
            work_backend.add_work_record(
                self.class_map[self.var_class.get()],
                self.var_subject.get(),
                self.var_type.get(),
                self.var_title.get(),
                self.var_desc.get(),
                self.var_due.get(),
                self.teacher_map.get(self.var_teacher.get(), None),
                self.var_file_path.get()
            )
            messagebox.showinfo("Success", "Work added!", parent=self.root)
            self.fetch_records()
            self.clear_fields()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add:\n{e}", parent=self.root)

    def update_record(self):
        if not self.selected_id:
            messagebox.showwarning("Select a record first", parent=self.root)
            return
        try:
            work_backend.update_work_record(
                self.selected_id,
                self.class_map[self.var_class.get()],
                self.var_subject.get(),
                self.var_type.get(),
                self.var_title.get(),
                self.var_desc.get(),
                self.var_due.get(),
                self.teacher_map.get(self.var_teacher.get(), None),
                self.var_file_path.get()
            )
            messagebox.showinfo("Updated", "Record updated!", parent=self.root)
            self.fetch_records()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Update failed:\n{e}", parent=self.root)

    def delete_record(self):
        if not self.selected_id:
            messagebox.showwarning("Select a record first", parent=self.root)
            return
        try:
            work_backend.delete_work_record(self.selected_id)
            messagebox.showinfo("Deleted", "Record removed!", parent=self.root)
            self.fetch_records()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Delete failed:\n{e}", parent=self.root)

    def fetch_records(self):
        try:
            rows = work_backend.fetch_work_records()
            self.table.delete(*self.table.get_children())

            for row in rows:
                self.table.insert("", tk.END, values=(
                    row["work_id"], row["class_name"], row["type"], row["subject"],
                    row["title"], row["due_date"], row["teacher"],
                    row["file_path"], row["description"]
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch:\n{e}", parent=self.root)

    # -------------------------------------------------------
    # TABLE SELECTION + CLEAR 
    # -------------------------------------------------------

    def get_selected_row(self, event):
        item = self.table.focus()
        values = self.table.item(item, "values")

        if values:
            self.selected_id = values[0]
            vars_list = [
                self.var_class, self.var_type, self.var_subject, self.var_title,
                self.var_due, self.var_teacher, self.var_file_path, self.var_desc
            ]
            for var, val in zip(vars_list, values[1:]):
                var.set(val)

    def clear_fields(self):
        for v in [
            self.var_class, self.var_type, self.var_subject, self.var_title,
            self.var_teacher, self.var_due, self.var_desc, self.var_file_path
        ]:
            v.set("")
        self.selected_id = None


if __name__ == "__main__":
    root = tk.Tk()
    WorkModule(root)
    root.mainloop()
