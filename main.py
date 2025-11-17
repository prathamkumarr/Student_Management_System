import tkinter as tk
from tkinter import messagebox
from Frontend.timetable_ui import TimetableUI
from Frontend.work_ui import WorkModule


class StudentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 Student Management System")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f4f4f4")

        # ---------- Title ----------
        title = tk.Label(
            self.root,
            text="🎓 Student Management System - Admin Panel",
            font=("Arial", 24, "bold"),
            bg="navy", fg="white", pady=10
        )
        title.pack(side=tk.TOP, fill=tk.X)

        # ---------- Frame ----------
        main_frame = tk.Frame(self.root, bg="#f4f4f4")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ---------- Sidebar ----------
        sidebar = tk.Frame(main_frame, bg="#002b5b", width=220)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(
            sidebar, text="📚 Modules",
            bg="#002b5b", fg="white", font=("Arial", 14, "bold"), pady=15
        ).pack(fill=tk.X)

        # ---------- Buttons ----------
        tk.Button(
            sidebar, text="📅 Timetable", font=("Arial", 12, "bold"),
            bg="#004b87", fg="white", relief="flat", cursor="hand2",
            command=self.open_timetable
        ).pack(fill=tk.X, padx=10, pady=5)

        tk.Button(
            sidebar, text="📘 Work Management", font=("Arial", 12, "bold"),
            bg="#004b87", fg="white", relief="flat", cursor="hand2",
            command=self.open_work
        ).pack(fill=tk.X, padx=10, pady=5)

        tk.Button(
            sidebar, text="🚪 Exit", font=("Arial", 12, "bold"),
            bg="red", fg="white", relief="flat", cursor="hand2",
            command=self.exit_app
        ).pack(fill=tk.X, padx=10, pady=20)

        # ---------- Main Area ----------
        self.display_label = tk.Label(
            main_frame,
            text="Select a module from the sidebar",
            font=("Arial", 16), bg="#f4f4f4", fg="#333"
        )
        self.display_label.pack(pady=150)

    # ---------- Module Openers ----------
    def open_timetable(self):
        """Open Timetable UI window"""
        new_window = tk.Toplevel(self.root)
        TimetableUI(new_window)

    def open_work(self):
        """Open Work Management UI window"""
        new_window = tk.Toplevel(self.root)
        WorkModule(new_window)

    def exit_app(self):
        """Exit confirmation"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementApp(root)
    root.mainloop()
