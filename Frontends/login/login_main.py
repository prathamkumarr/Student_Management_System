import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
from tkinter import ttk

from Frontends.login.login_utils import validate_admin, parse_login_email, LoginError


class LoginUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("School ERP Login")
        self.root.geometry("820x600")
        self.root.configure(bg="#ECF0F1")
        self.root.resizable(True, True)

        self.saved_credentials = {}
        self.load_saved_credentials()

        self.build_ui()

    # =============================================================
    def apply_glass(self, widget):
        widget.config(
        bg="#FFFFFF",
        highlightbackground="#D0D3D4",
        highlightthickness=1,
        bd=0
    )

    # =============================================================
    def load_saved_credentials(self):
        self.saved_credentials = {}
        try:
            with open(".saved_credentials", "r") as f:
                for line in f:
                    if "=" in line:
                        email, pwd = line.strip().split("=")
                        self.saved_credentials[email] = pwd
        except:
            pass

    # =============================================================
    def delete_saved_email(self):

        email = self.email_var.get().strip()

        if not email:
            return

        if email not in self.saved_credentials:
            messagebox.showwarning("Not Found", "Email not saved!")
            return

        confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete '{email}' ?"
        )

        if not confirm:
            return
  
        # remove email
        del self.saved_credentials[email]

        # rewrite file
        with open(".saved_credentials", "w") as f:
            for e, p in self.saved_credentials.items():
                f.write(f"{e}={p}\n")

        # update UI
        self.email_box["values"] = list(self.saved_credentials.keys())
        self.email_var.set("")
        self.pass_var.set("")

    # =============================================================
    def update_delete_button(self, *args):

        if self.email_var.get().strip():
            # entry filled → black delete icon active
            self.delete_btn.config(
            bg="#000000",
            fg="white",
            cursor="hand2"
        )
        else:
            # entry empty → disabled light button
            self.delete_btn.config(
            bg="#D5D8DC",
            fg="#7B7D7D",
            cursor="arrow"
        )

    # =============================================================
    def build_ui(self):

        tk.Label(
            self.root,
            text="School ERP Login",
            font=("Arial", 32, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50"
        ).pack(pady=45)

        card = tk.Frame(
            self.root,
            bg="white",
            width=600,
            height=350,
            highlightbackground="#BDC3C7",
            highlightthickness=2
        )
        card.pack()
        card.pack_propagate(False)

        form = tk.Frame(card, bg="white")
        form.pack(pady=20)

        self.delete_btn = tk.Label(
        form,
        text="✕",
        font=("Arial", 14, "bold"),
        bg="#000000",
        fg="white",
        width=2,
        padx=6,
        pady=2,
        cursor="hand2",
        bd=3,
        relief="raised",
        )
        self.delete_btn.grid(row=0, column=2, sticky="w", padx=6)

        self.delete_btn.bind("<Enter>", lambda e: self.delete_btn.config(bg="#222222"))
        self.delete_btn.bind("<Leave>", lambda e: self.delete_btn.config(bg="#000000"))

        self.delete_btn.bind("<Button-1>", lambda e: self.delete_saved_email())
        self.delete_btn.grid_remove()


        # EMAIL -------------------------
        tk.Label(
            form, text="Login ID",
            font=("Arial", 15),
            bg="white",
            fg="#2C3E50"
        ).grid(row=0, column=0, sticky="w", padx=15, pady=8)

        self.email_var = tk.StringVar()

        self.email_box = ttk.Combobox(
            form,
            textvariable=self.email_var,
            font=("Arial", 15),
            width=30,
            state="normal"
        )
        self.email_box.grid(row=0, column=1, pady=8, sticky="w")

        # populate dropdown email list
        self.email_box["values"] = list(self.saved_credentials.keys())


        # when dropdown selected : fill password
        def on_email_select(event):
            email = self.email_var.get().strip()
            if email in self.saved_credentials:
                self.pass_var.set(self.saved_credentials[email])
            else:
                self.pass_var.set("")

        self.email_box.bind("<<ComboboxSelected>>", on_email_select)


        # PASSWORD -------------------------
        tk.Label(
            form,
            text="Password",
            font=("Arial", 15),
            bg="white",
            fg="#2C3E50"
        ).grid(row=1, column=0, sticky="w", padx=15, pady=8)

        self.pass_var = tk.StringVar()

        self.password_entry = tk.Entry(
            form,
            textvariable=self.pass_var,
            show="*",
            font=("Arial", 15),
            width=30
        )
        self.password_entry.grid(row=1, column=1, pady=8, sticky="w")


        # PASSWORD SHOW / HIDE BTN
        self.show_pass = False

        def toggle_password():
            self.show_pass = not self.show_pass
            if self.show_pass:
                self.password_entry.config(show="")
                toggle_btn.config(text="Hide")
            else:
                self.password_entry.config(show="*")
                toggle_btn.config(text="Show")

        toggle_btn = tk.Button(
            form,
            text="Show",
            font=("Arial", 11, "bold"),
            bg="#ECF0F1",
            fg="#2C3E50",
            width=6,
            command=toggle_password
        )
        toggle_btn.grid(row=1, column=3, padx=8)



        # REMEMBER ME -------------------------
        self.remember_var = tk.BooleanVar()

        tk.Checkbutton(
            form, text="Remember Me",
            variable=self.remember_var,
            bg="white", font=("Arial", 11)
        ).grid(row=2, column=1, sticky="w", pady=4)


        # LOGIN BUTTON -------------------------
        self.login_btn = tk.Label(
            card,
            text="Login",
            font=("Arial", 18, "bold"),
            width=13
        )
        self.login_btn.pack(pady=25)

        self.style_login_btn_disabled()

        self.login_btn.bind("<Button-1>", lambda e: self.login())


        # enable logic
        self.email_var.trace_add("write", self.check_enable_login)
        self.pass_var.trace_add("write", self.check_enable_login)

        self.email_var.trace_add("write", self.update_delete_button)
        self.update_delete_button()  # initial state


    # =============================================================
    def style_login_btn_active(self):

        self.login_btn.config(
            bg="#000000",
            fg="white",
            padx=20,
            pady=8,
            relief="raised",
            cursor="hand2"
        )

        self.login_btn.bind("<Enter>", lambda e: self.login_btn.config(bg="#222222"))
        self.login_btn.bind("<Leave>", lambda e: self.login_btn.config(bg="#000000"))


    # =============================================================
    def style_login_btn_disabled(self):

        self.login_btn.config(
            bg="#AEB6BF",
            fg="white",
            padx=20,
            pady=8,
            relief="flat",
            cursor="arrow"
        )


    # =============================================================
    def check_enable_login(self, *args):

        email = self.email_var.get().strip()

        # LOGIN BUTTON ENABLE RULE
        if email and self.pass_var.get().strip():
            self.style_login_btn_active()
        else:
            self.style_login_btn_disabled()

        # DELETE BUTTON SHOW/HIDE RULE
        if hasattr(self, "delete_btn"):
            if email:
                self.delete_btn.grid()   
            else:
                self.delete_btn.grid_remove()  


    # =============================================================
    def login(self):

        email = self.email_var.get().strip()
        password = self.pass_var.get().strip()

        if not email or not password:
            messagebox.showwarning("Empty Fields", "Please enter both Email & Password")
            return

        # ============ REMEMBER USER SAVE ============
        if self.remember_var.get():
            self.saved_credentials[email] = password
            with open(".saved_credentials", "w") as f:
                for e, p in self.saved_credentials.items():
                    f.write(f"{e}={p}\n")


        # ============ ADMIN LOGIN CHECK ============
        if validate_admin(email, password):
            self.root.destroy()
            subprocess.Popen([
                sys.executable,
                "Frontends/Frontend_admin/admin_main.py"
            ])
            return

        # ============ NORMAL USER LOGIN ============
        import requests

        try:
            res = requests.post(
            "http://127.0.0.1:8000/auth/login",
            params={"email": email, "password": password}
            )

            if res.status_code != 200:
                raise Exception()

            data = res.json()
            role = data["role"]
            user_id = data["user_id"]
 
        except:
            messagebox.showerror(
            "Login Failed",
            "Invalid Email or Password!"
        )
            return

        # ======= ROLE BASED REDIRECTION =======

        try:
            if role == "student":
                subprocess.Popen([
                sys.executable,
                "Frontends/Frontend_student/student_main.py",
                str(user_id)
            ])

            elif role == "teacher":
                subprocess.Popen([
                sys.executable,
                "Frontends/Frontend_teacher/teacher_main.py",
                str(user_id)
            ])

            elif role == "staff":
                subprocess.Popen([
                sys.executable,
                "Frontends/Frontend_staff/staff_main.py",
                str(user_id)
            ])

            self.root.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Error launching dashboard:\n{e}")


    # =============================================================
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    LoginUI().run()
