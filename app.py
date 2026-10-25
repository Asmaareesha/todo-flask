import json
from datetime import date, datetime

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

FILENAME = "tasks.json"
PRIORITIES = ["High", "Medium", "Low"]


# ---------- Saving and loading ----------

def load_tasks():
    try:
        with open(FILENAME, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(tasks):
    with open(FILENAME, "w") as file:
        json.dump(tasks, file)


# ---------- Helpers ----------

def is_valid_date(text):
    try:
        datetime.strptime(text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def is_overdue(task):
    due = task.get("due")
    if task["done"] or not due:
        return False
    return datetime.strptime(due, "%Y-%m-%d").date() < date.today()


# ---------- Pages ----------

@app.route("/")
def index():
    tasks = load_tasks()
    keyword = request.args.get("q", "").strip()
    error = request.args.get("error", "")
    edit_id = request.args.get("edit", type=int)

    shown = []
    for task_id, task in enumerate(tasks):
        if keyword.lower() not in task["title"].lower():
            continue

        if task["done"]:
            status = "done"
        elif is_overdue(task):
            status = "overdue"
        else:
            status = task.get("priority", "Medium").lower()

        shown.append({
            "id": task_id,
            "title": task["title"],
            "done": task["done"],
            "priority": task.get("priority", "Medium"),
            "due": task.get("due"),
            "status": status,
        })

    editing = None
    if edit_id is not None and 0 <= edit_id < len(tasks):
        task = tasks[edit_id]
        editing = {
            "id": edit_id,
            "title": task["title"],
            "priority": task.get("priority", "Medium"),
            "due": task.get("due") or "",
        }

    done_count = sum(1 for task in tasks if task["done"])
    overdue_count = sum(1 for task in tasks if is_overdue(task))

    return render_template(
        "index.html",
        tasks=shown,
        editing=editing,
        keyword=keyword,
        error=error,
        total=len(tasks),
        done_count=done_count,
        overdue_count=overdue_count,
    )


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    priority = request.form.get("priority", "Medium")
    due = request.form.get("due", "").strip()

    if title == "":
        return redirect(url_for("index", error="Please type a task first."))
    if due != "" and not is_valid_date(due):
        return redirect(url_for("index", error="Please use a valid date."))
    if priority not in PRIORITIES:
        priority = "Medium"

    tasks = load_tasks()
    tasks.append({
        "title": title,
        "done": False,
        "priority": priority,
        "due": due or None,
    })
    save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/update/<int:task_id>", methods=["POST"])
def update(task_id):
    tasks = load_tasks()
    if not 0 <= task_id < len(tasks):
        return redirect(url_for("index", error="That task no longer exists."))

    title = request.form.get("title", "").strip()
    priority = request.form.get("priority", "Medium")
    due = request.form.get("due", "").strip()

    if title == "":
        return redirect(url_for("index", edit=task_id,
                                error="The task can't be empty."))
    if due != "" and not is_valid_date(due):
        return redirect(url_for("index", edit=task_id,
                                error="Please use a valid date."))
    if priority not in PRIORITIES:
        priority = "Medium"

    tasks[task_id]["title"] = title
    tasks[task_id]["priority"] = priority
    tasks[task_id]["due"] = due or None
    save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]["done"] = not tasks[task_id]["done"]
        save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)