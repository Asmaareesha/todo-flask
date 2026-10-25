# To-Do List (Web App)

A to-do list website built with Python and Flask. Tasks have priorities
and due dates, and everything is saved automatically.

![Screenshot](screenshot.png)

## Features

- Add tasks with a priority (High, Medium, Low) and an optional due date
- Color-coded tasks, with overdue tasks highlighted
- Edit, complete, undo, and delete tasks
- Search tasks by keyword
- Progress counter showing completed and overdue tasks
- Tasks are saved automatically to tasks.json

## How to run it

1. Install Python from python.org
2. Download this project and open a terminal in its folder
3. Install Flask: python -m pip install -r requirements.txt
4. Start the app: python app.py
5. Open http://127.0.0.1:5000 in your browser

## Project structure

- app.py: the Flask application (routes and logic)
- templates/index.html: the page layout
- static/style.css: the styling

## What I learned

Building a web app with Flask, routes and HTML forms, Jinja templates,
redirects, validating user input, working with dates, and saving data
to JSON.
