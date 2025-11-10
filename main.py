import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
import os

# Import your Timetable module
from Backend.Students.timetable import TimetableModule


class StudentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 Student Management System")
        self.root.geometry("900x500")
        self.root.resizable(True, True)

        # ---------- Title ----------
        title = tk.Label(
            self.root,
            text="🎓 Student Management System",
            font=("Arial", 24, "bold"),
            bg="navy", fg="white", pady=10
        )
        title.pack(side=tk.TOP, fill=tk.X)

        # ---------- Frame ----------
        main_frame = tk.Frame(self.root, bg="#f2f2f2")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ---------- Sidebar ----------
        sidebar = tk.Frame(main_frame, bg="#002b5b", width=220)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(
            sidebar,
            text="📚 Modules",
            bg="#002b5b", fg="white",
            font=("Arial", 14, "bold"), pady=15
        ).pack(fill=tk.X)

        # Buttons for modules
        tk.Button(
            sidebar, text="📅 Timetable", font=("Arial", 12, "bold"),
            bg="#004b87", fg="white", relief="flat", cursor="hand2",
            command=self.open_timetable
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
            font=("Arial", 16),
            bg="#f2f2f2", fg="#444"
        )
        self.display_label.pack(pady=150)

    # ---------- Functions ----------
    def open_timetable(self):
        """Open the Timetable Module in a new window"""
        new_window = tk.Toplevel(self.root)
        TimetableModule(new_window)

    def exit_app(self):
        """Confirm before closing"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()
            sys.exit(0)


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementApp(root)
    root.mainloop()
