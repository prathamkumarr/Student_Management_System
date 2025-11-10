import tkinter as tk
from tkinter import ttk, messagebox
from config import connect_db


class TimetableModule:
    def __init__(self, root):
        self.root = root
        self.root.title("Timetable Management")

        # ---------- Fullscreen + minsize ----------
        try:
            self.root.state("zoomed")  # Windows
        except tk.TclError:
            self.root.attributes("-zoomed", True)  # Linux fallback

        self.root.minsize(1000, 650)
        self.root.resizable(True, True)

        # ---------- Title ----------
        title = tk.Label(
            self.root,
            text="📅 Timetable Manager",
            font=("Arial", 22, "bold"),
            bg="navy",
            fg="white",
            pady=8,
        )
        title.pack(side=tk.TOP, fill=tk.X)

        # ---------- Variables ----------
        self.var_class = tk.StringVar()
        self.var_day = tk.StringVar()
        self.var_subject = tk.StringVar()
        self.var_teacher = tk.StringVar()
        self.var_start = tk.StringVar()
        self.var_end = tk.StringVar()
        self.selected_id = None

        self.class_map = {}
        self.teacher_map = {}
        self.subjects_list = []

        # ---------- Layout ----------
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # ---------- Left: Add/Edit ----------
        form_frame = tk.LabelFrame(
            main_frame,
            text="Add / Edit Timetable",
            font=("Arial", 12, "bold"),
            bd=2,
            relief=tk.RIDGE,
        )
        form_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        form_frame.config(width=400)

        # Class
        tk.Label(form_frame, text="Class:", font=("Arial", 12)).grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )
        self.class_combo = ttk.Combobox(
            form_frame, textvariable=self.var_class,
            font=("Arial", 12), state="readonly", width=18
        )
        self.class_combo.grid(row=0, column=1, padx=10, pady=5)

        # Day
        tk.Label(form_frame, text="Day:", font=("Arial", 12)).grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        self.day_combo = ttk.Combobox(
            form_frame, textvariable=self.var_day,
            font=("Arial", 12), state="readonly", width=18
        )
        self.day_combo["values"] = (
            "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
        )
        self.day_combo.set("")
        self.day_combo.grid(row=1, column=1, padx=10, pady=5)

        # Subject
        tk.Label(form_frame, text="Subject:", font=("Arial", 12)).grid(
            row=2, column=0, padx=10, pady=5, sticky="w"
        )
        # ✅ Subject ComboBox (auto-fills from DB)
        self.subject_combo = ttk.Combobox(
            form_frame, textvariable=self.var_subject,
            font=("Arial", 12), state="readonly", width=18
        )
        self.subject_combo.grid(row=2, column=1, padx=10, pady=5)

        # Teacher
        tk.Label(form_frame, text="Teacher:", font=("Arial", 12)).grid(
            row=3, column=0, padx=10, pady=5, sticky="w"
        )
        self.teacher_combo = ttk.Combobox(
            form_frame, textvariable=self.var_teacher,
            font=("Arial", 12), state="readonly", width=18
        )
        self.teacher_combo.grid(row=3, column=1, padx=10, pady=5)

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

        # ---------- Buttons ----------
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=15)

        tk.Button(btn_frame, text="Add", bg="green", fg="white", font=("Arial", 12, "bold"),
                  command=self.add_record).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update", bg="blue", fg="white", font=("Arial", 12, "bold"),
                  command=self.update_record).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete", bg="red", fg="white", font=("Arial", 12, "bold"),
                  command=self.delete_record).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Clear", bg="gray", fg="white", font=("Arial", 12, "bold"),
                  command=self.clear_fields).grid(row=0, column=3, padx=5)

        # ✅ Show button for filters
        tk.Button(btn_frame, text="Show", bg="orange", fg="black",
                  font=("Arial", 12, "bold"),
                  command=self.filter_records).grid(row=0, column=4, padx=5)

        # ---------- Right: Table ----------
        table_frame = tk.LabelFrame(
            main_frame, text="Timetable Records",
            font=("Arial", 12, "bold"), bd=2, relief=tk.RIDGE
        )
        table_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)

        columns = ("id", "class", "day", "subject", "teacher", "start_time", "end_time")
        self.table = ttk.Treeview(
            table_frame, columns=columns,
            show="headings", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set
        )
        scroll_y.config(command=self.table.yview)
        scroll_x.config(command=self.table.xview)

        self.table.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        for col in columns:
            self.table.heading(col, text=col.capitalize())
            self.table.column(col, anchor="center", stretch=True)

        self.table.bind("<ButtonRelease-1>", self.get_selected_row)

        # ---------- Load Data ----------
        self.load_combobox_data()
        self.fetch_records()

    # ---------- Load Dropdown Data ----------
    def load_combobox_data(self):
        con = connect_db()
        if con is None:
            return
        cur = con.cursor()
        try:
            # Classes
            cur.execute("SELECT class_id, class_name FROM classes ORDER BY LENGTH(class_name), class_name")
            classes = cur.fetchall()
            self.class_map = {row["class_name"]: row["class_id"] for row in classes}
            self.class_combo["values"] = list(self.class_map.keys())

            # Teachers
            cur.execute("SELECT teacher_id, name FROM teachers ORDER BY name")
            teachers = cur.fetchall()
            self.teacher_map = {row["name"]: row["teacher_id"] for row in teachers}
            self.teacher_combo["values"] = list(self.teacher_map.keys())

            # ✅ Subjects (auto-load unique subject names)
            cur.execute("SELECT DISTINCT subject FROM timetable ORDER BY subject")
            subjects = cur.fetchall()
            self.subjects_list = [row["subject"] for row in subjects if row["subject"]]
            self.subject_combo["values"] = self.subjects_list
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load dropdown data:\n{e}", parent=self.root)
        finally:
            con.close()

    # ---------- Add ----------
    def add_record(self):
        if not self.var_class.get() or not self.var_teacher.get():
            messagebox.showwarning("Warning", "Class and Teacher must be selected.", parent=self.root)
            return
        con = connect_db()
        cur = con.cursor()
        try:
            cur.execute("""
                INSERT INTO timetable (class_id, day, subject, teacher_id, start_time, end_time)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                self.class_map[self.var_class.get()],
                self.var_day.get(),
                self.var_subject.get(),
                self.teacher_map[self.var_teacher.get()],
                self.var_start.get(),
                self.var_end.get()
            ))
            con.commit()
            messagebox.showinfo("Success", "Timetable record added successfully.", parent=self.root)
            self.fetch_records()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add record:\n{e}", parent=self.root)
        finally:
            con.close()

    # ---------- Filter / Show ----------
    def filter_records(self):
        selected_class = self.var_class.get()
        selected_teacher = self.var_teacher.get()
        selected_day = self.var_day.get()
        selected_subject = self.var_subject.get().strip()

        if not (selected_class or selected_teacher or selected_day or selected_subject):
            messagebox.showwarning(
                "Warning",
                "Select at least one filter (Class, Teacher, Day, or Subject).",
                parent=self.root
            )
            return

        con = connect_db()
        cur = con.cursor()
        try:
            query = """
                SELECT t.timetable_id, c.class_name, t.day, t.subject, tr.name AS teacher,
                       t.start_time, t.end_time
                FROM timetable t
                JOIN classes c ON t.class_id = c.class_id
                LEFT JOIN teachers tr ON t.teacher_id = tr.teacher_id
                WHERE 1=1
            """
            params = []

            if selected_class:
                query += " AND c.class_id = %s"
                params.append(self.class_map[selected_class])
            if selected_teacher:
                query += " AND tr.teacher_id = %s"
                params.append(self.teacher_map[selected_teacher])
            if selected_day:
                query += " AND t.day = %s"
                params.append(selected_day)
            if selected_subject:
                query += " AND t.subject LIKE %s"
                params.append(f"%{selected_subject}%")

            query += " ORDER BY FIELD(t.day,'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'), t.start_time"

            cur.execute(query, tuple(params))
            rows = cur.fetchall()

            self.table.delete(*self.table.get_children())
            if rows:
                for row in rows:
                    self.table.insert("", tk.END, values=(
                        row["timetable_id"], row["class_name"], row["day"],
                        row["subject"], row["teacher"], row["start_time"], row["end_time"]
                    ))
            else:
                # ✅ Fixed: Does NOT close the window anymore
                messagebox.showinfo("Info", "No matching records found.", parent=self.root)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to filter records:\n{e}", parent=self.root)
        finally:
            con.close()

    # ---------- Fetch All ----------
    def fetch_records(self):
        con = connect_db()
        if con is None:
            return
        cur = con.cursor()
        try:
            cur.execute("""
                SELECT t.timetable_id, c.class_name, t.day, t.subject, tr.name AS teacher,
                       t.start_time, t.end_time
                FROM timetable t
                JOIN classes c ON t.class_id = c.class_id
                LEFT JOIN teachers tr ON t.teacher_id = tr.teacher_id
                ORDER BY c.class_name, FIELD(t.day,'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'), t.start_time
            """)
            rows = cur.fetchall()
            self.table.delete(*self.table.get_children())
            for row in rows:
                self.table.insert("", tk.END, values=(
                    row["timetable_id"], row["class_name"], row["day"],
                    row["subject"], row["teacher"], row["start_time"], row["end_time"]
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data:\n{e}", parent=self.root)
        finally:
            con.close()

    # ---------- Other CRUD ----------
    def get_selected_row(self, event):
        selected = self.table.focus()
        values = self.table.item(selected, "values")
        if values:
            self.selected_id = values[0]
            self.var_class.set(values[1])
            self.var_day.set(values[2])
            self.var_subject.set(values[3])
            self.var_teacher.set(values[4])
            self.var_start.set(values[5])
            self.var_end.set(values[6])

    def update_record(self):
        if not self.selected_id:
            messagebox.showwarning("Warning", "Select a record to update.", parent=self.root)
            return
        con = connect_db()
        cur = con.cursor()
        try:
            cur.execute("""
                UPDATE timetable 
                SET class_id=%s, day=%s, subject=%s, teacher_id=%s, start_time=%s, end_time=%s
                WHERE timetable_id=%s
            """, (
                self.class_map[self.var_class.get()],
                self.var_day.get(),
                self.var_subject.get(),
                self.teacher_map[self.var_teacher.get()],
                self.var_start.get(),
                self.var_end.get(),
                self.selected_id
            ))
            con.commit()
            messagebox.showinfo("Updated", "Record updated successfully.", parent=self.root)
            self.fetch_records()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update record:\n{e}", parent=self.root)
        finally:
            con.close()

    def delete_record(self):
        if not self.selected_id:
            messagebox.showwarning("Warning", "Select a record to delete.", parent=self.root)
            return
        con = connect_db()
        cur = con.cursor()
        try:
            cur.execute("DELETE FROM timetable WHERE timetable_id=%s", (self.selected_id,))
            con.commit()
            messagebox.showinfo("Deleted", "Record deleted successfully.", parent=self.root)
            self.fetch_records()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete record:\n{e}", parent=self.root)
        finally:
            con.close()

    def clear_fields(self):
        self.var_class.set("")
        self.var_day.set("")
        self.var_subject.set("")
        self.var_teacher.set("")
        self.var_start.set("")
        self.var_end.set("")
        self.selected_id = None


if __name__ == "__main__":
    root = tk.Tk()
    app = TimetableModule(root)
    root.mainloop()
