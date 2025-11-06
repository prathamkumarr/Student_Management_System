# Student Management System
Welcome!
This document explains how to set up, collaborate, and contribute to our Student Management System project step-by-step.

---

# Clone the Repository
Open VS Code or your terminal and run:
```bash
git clone https://github.com/prathamkumarr/Student_Management_System.git

# Branch Naming 
Always work on your own branch — not directly on main.

git checkout -b feat/<your_module_name>

Examples:
feat/student_module
feat/teacher_dashboard
fix/attendance_bug

# Commit, push/pull
Before coding:

git pull origin main


After making changes:

git add .
git commit -m "feat: your short commit message"
git push -u origin feat/<your_module_name>

Then go to GitHub : create a Pull Request (PR)
- target branch: main

-- If someone merges new code into main:

git checkout main
git pull origin main
git checkout feat/<your_branch>
git merge main

-- Pull Request Rules

One feature = one PR
Add clear title & short description
Do not merge your own PR — another teammate must review it
Delete branch after merge

# commit message format
Follow this syntax:

<type>: <short description>


Allowed types:

feat : new feature
fix : bug fix
docs : documentation
refactor : code improvement

Example:

git add .
git commit --amend -m "feat: implemented complete student module"

