# Assignment 4: Simple CRUD System Using Django

A student management app matching `assignment4.mp4`: a **Student Lists** table,
**Add New**, **Create Student**, **Edit Student**, **Back**, **Submit**, and
**Delete** with an **Are you sure?** prompt. Fields are Name, Email, Gender
(Male/Female/Other), and Phone. Records persist in a local SQLite database.
Bootstrap CSS is bundled locally, so the design works without internet after setup.
The table numbers the displayed students from 1 and renumbers them after deletion.
Database IDs remain unchanged for editing and deleting records.

Python runs this app directly; no separate C/C++ compiler, Live Server, or database
server is needed. Python, Django, VS Code, and its Python/Debugger extensions are
already installed on this computer.

## Run in VS Code on Windows

1. Open **`D:\ncc python assignment-4`** using VS Code's **File > Open Folder**.
2. Install the recommended **Python** and **Python Debugger** extensions if prompted.
3. For first-time setup, open **Terminal > Run Task > Django: Setup**.
   Python 3.10 or later and internet access for the dependency download are required.
4. Select **Django: Student CRUD** in the Run and Debug panel.
5. Choose **Run > Run Without Debugging** (**Ctrl+F5**), or **Run > Start Debugging** (**F5**).
6. The app starts and opens automatically in your browser. Stop it with **Ctrl+C** in the terminal, or **Shift+F5** when debugging.

You can also open **run.py** and click the top-right **Run Python File** button.
If VS Code asks for an interpreter, choose `.venv\Scripts\python.exe`.
Stop any existing server before starting another run.

### Terminal alternative

Setup is already complete on this computer. Run this single command in VS Code's terminal:

```powershell
.\run.cmd
```

If an old server is still running, press **Ctrl+C** before using this command.
On a new computer, run `powershell -NoProfile -ExecutionPolicy Bypass -File .\setup.ps1` once first.

Setup is safe to repeat: it installs requirements and applies database migrations
without deleting existing students. The app starts with an empty student list,
as shown at the beginning of the demo.

## Try the demo flow

Click **Add New**, enter Alex / alex@gmail.com / Female / 258963, and **Submit**.
Add Bob and Charle, then edit Bob's details. Click **Delete** on Alex and cancel
to keep the row; click again and confirm to remove it. Refresh or restart the
server to confirm that saved changes persist.

## Test

Use **Terminal > Run Task > Django: Test**, or:

```powershell
.\.venv\Scripts\python.exe manage.py test
```

Tests cover the complete CRUD flow, invalid input, leading zeroes in phone
numbers, missing records, CSRF protection, escaping, and POST-only deletion.

## Project structure

- `config/`: Django settings and root routes.
- `students/models.py`: Student database model.
- `students/forms.py`: Input fields and validation.
- `students/views.py` and `urls.py`: CRUD request handling and routes.
- `students/migrations/`: Database schema.
- `templates/`: Bootstrap list and form pages.
- `static/`: Bundled Bootstrap CSS, small layout adjustments, delete prompt.
- `.vscode/`: Interpreter, task, and debugger settings.
- `setup.ps1`: First-time setup.
- `run.cmd`, `run.ps1`, and `run.py`: One-command launch with automatic browser opening.

This is a local assignment app with development settings. The student screens
do not require a login. Optional Django admin is available at `/admin/` after
running `.\.venv\Scripts\python.exe manage.py createsuperuser`.

Reference documentation: [Django 5.2](https://docs.djangoproject.com/en/5.2/)
and [Bootstrap 5.3](https://getbootstrap.com/docs/5.3/).
