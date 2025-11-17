import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import os
import shutil

# Import backend functions
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

        # ---------- Title ----------
        title = tk.Label(self.root, text="📘 Work Management (Classwork / Homework / Assignment)",
                         font=("Arial", 22, "bold"), bg="navy", fg="white", pady=8)
        title.pack(side=tk.TOP, fill=tk.X)

        # ---------- Layout ----------
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # ---------- Left Panel ----------
        form_frame = tk.LabelFrame(main_frame, text="Add / Edit Work", font=("Arial", 12, "bold"), bd=2, relief=tk.RIDGE)
        form_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        # Form fields
        self.create_form_fields(form_frame)

        # Buttons
        self.create_buttons(form_frame)

        # ---------- Table ----------
        self.create_table(main_frame)

        # Load dropdown data
        self.load_combobox_data()
        self.fetch_records()

    # ---------- UI Components ----------
    def create_form_fields(self, form_frame):
        tk.Label(form_frame, text="Class:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.class_combo = ttk.Combobox(form_frame, textvariable=self.var_class, font=("Arial", 12), state="readonly", width=18)
        self.class_combo.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Type:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.type_combo = ttk.Combobox(form_frame, textvariable=self.var_type, font=("Arial", 12), state="readonly", width=18)
        self.type_combo["values"] = ("Classwork", "Homework", "Assignment")
        self.type_combo.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Subject:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.subject_combo = ttk.Combobox(form_frame, textvariable=self.var_subject, font=("Arial", 12), state="readonly", width=18)
        self.subject_combo.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Title:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(form_frame, textvariable=self.var_title, font=("Arial", 12), width=20).grid(row=3, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Description:", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(form_frame, textvariable=self.var_desc, font=("Arial", 12), width=20).grid(row=4, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Due Date:", font=("Arial", 12)).grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.due_entry = DateEntry(form_frame, textvariable=self.var_due, font=("Arial", 12),
                                   width=18, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
        self.due_entry.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Teacher:", font=("Arial", 12)).grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.teacher_combo = ttk.Combobox(form_frame, textvariable=self.var_teacher, font=("Arial", 12), state="readonly", width=18)
        self.teacher_combo.grid(row=6, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="PDF File:", font=("Arial", 12)).grid(row=7, column=0, padx=10, pady=5, sticky="w")
        tk.Entry(form_frame, textvariable=self.var_file_path, font=("Arial", 10), width=20, state="readonly").grid(row=7, column=1, padx=10, pady=5)
        tk.Button(form_frame, text="Browse", command=self.browse_file, bg="#004b87", fg="white", font=("Arial", 10, "bold")).grid(row=7, column=2, padx=5)

    def create_buttons(self, form_frame):
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=8, column=0, columnspan=3, pady=15)
        buttons = [
            ("Add", "green", self.add_record),
            ("Update", "blue", self.update_record),
            ("Delete", "red", self.delete_record),
            ("Clear", "gray", self.clear_fields),
            ("Show", "orange", self.fetch_records),
        ]
        for i, (text, color, cmd) in enumerate(buttons):
            tk.Button(btn_frame, text=text, bg=color, fg="white", font=("Arial", 12, "bold"), command=cmd).grid(row=0, column=i, padx=5)

    def create_table(self, main_frame):
        table_frame = tk.LabelFrame(main_frame, text="Work Records", font=("Arial", 12, "bold"), bd=2, relief=tk.RIDGE)
        table_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        columns = ("id", "class", "type", "subject", "title", "due_date", "teacher", "file", "description")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.table.yview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.pack(fill=tk.BOTH, expand=True)
        for col in columns:
            self.table.heading(col, text=col.capitalize())
            self.table.column(col, anchor="center", stretch=True)
        self.table.bind("<ButtonRelease-1>", self.get_selected_row)

    # ---------- Logic ----------
    def browse_file(self):
        path = filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF Files", "*.pdf")])
        if path:
            self.var_file_path.set(path)

    def load_combobox_data(self):
        try:
            classes = work_backend.get_class_data()
            self.class_map = {row["class_name"]: row["class_id"] for row in classes}
            self.class_combo["values"] = list(self.class_map.keys())

            teachers = work_backend.get_teacher_data()
            self.teacher_map = {row["name"]: row["teacher_id"] for row in teachers}
            self.teacher_combo["values"] = list(self.teacher_map.keys())

            subjects = work_backend.get_subject_data()
            self.subject_combo["values"] = subjects
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data:\n{e}", parent=self.root)

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
            messagebox.showinfo("Success", "Work added successfully!", parent=self.root)
            self.fetch_records()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add record:\n{e}", parent=self.root)

    def update_record(self):
        if not self.selected_id:
            messagebox.showwarning("Warning", "Select a record to update.", parent=self.root)
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
            messagebox.showinfo("Updated", "Record updated successfully.", parent=self.root)
            self.fetch_records()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Update failed:\n{e}", parent=self.root)

    def delete_record(self):
        if not self.selected_id:
            messagebox.showwarning("Warning", "Select a record to delete.", parent=self.root)
            return
        try:
            work_backend.delete_work_record(self.selected_id)
            messagebox.showinfo("Deleted", "Record deleted successfully.", parent=self.root)
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
                    row["title"], row["due_date"], row["teacher"], row["file_path"], row["description"]
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data:\n{e}", parent=self.root)

    def get_selected_row(self, event):
        selected = self.table.focus()
        values = self.table.item(selected, "values")
        if values:
            self.selected_id = values[0]
            self.var_class.set(values[1])
            self.var_type.set(values[2])
            self.var_subject.set(values[3])
            self.var_title.set(values[4])
            self.var_due.set(values[5])
            self.var_teacher.set(values[6])
            self.var_file_path.set(values[7])
            self.var_desc.set(values[8])

    def clear_fields(self):
        for var in [self.var_class, self.var_type, self.var_subject, self.var_title,
                    self.var_teacher, self.var_due, self.var_desc, self.var_file_path]:
            var.set("")
        self.selected_id = None


if __name__ == "__main__":
    root = tk.Tk()
    app = WorkModule(root)
    root.mainloop()
