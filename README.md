# Kanban Board App

App developed by [Noufal Rahman](mailto:21f1005287@student.onlinedegree.iitm.ac.in) (21f1005287)

Made with care using HTML, Flask, Bootstrap
____

## Steps to run this app
- Create a Virtual environment in the same directory
  - `python -m venv env` for Windows.
  - `virtualenv env` for Linux or MacOS.
- Activate the Virtual environment
  - `env\Scripts\activate` for Windows.
  - `source env/bin/activate` for Linux or MacOS.
- Run the app `python app.py`
- Don't forget to deactivate the Virtual environment when you're done exploring
  - `env\Scripts/deactivate` for Windows.
  - `source env/bin/deactivate` for Linux or MacOS.
___

## Folder Structure

- ### /apis
  - [/card.py](apis/card.py) - Contains API calls to get, put, delete a card, get cards from a list and add a card to list.
  - [/list.py](apis/list.py) - Contains API calls to get, put, delete a list, get lists of a user and add a card for a user.
  - [/user.py](apis/user.py) - Contains API calls for all CRUD operations on user.
  - [/validation.py](apis/validations.py) - Contains validation error classes for APIs.

- ### /application
  - [/db.py](application/db.py) - Configuration of database.
  - [/models.py](application/models.py) - Contains Database schemas.

- ### /routes
  - [/auth.py](routes/auth.py) - Route for login, logout and signup pages.
  - [/card.py](routes/card.py) - Route to create, view, delete and edit a card.
  - [/list.py](routes/card.py) - Route to create, edit, delete and view the lists.
  - [/route.py](routes/route.py) - Checks the session for user login.
  - [/summary.py](routes/summary.py) - Route for summary page.

- ### /static
  - [/style.css](static/style.css) - Stylesheet.
  - [/bg.webp](static/bg.webp) - Background Image.
  - [/<user_id>_summary.png](static/noufal_summary.png) - Image of a bar graph for the completed and pending tasks of a user. It is automatically generated when a user navigates to the /<user_id>/summary

- ### /templates
  - [/list.html](templates/lists.html) - Template for Lists page.
  - [/login.html](templates/login.html) - Template for Login page.
  - [/signup.html](templates/signup.html) - Template for Signup page.
  - [/summary.html](templates/summary.html) - Template for Summary page

- ### [/app.py](app.py) - Configuration of Application.
- ### [/db.sqlite3](db.sqlite3) - Database.
- ### [/CHECKLIST.md](CHECKLIST.md) - Checklist for Project Submission.
- ### [/README.md](README.md)
- ### [/Kanban Board App Report.pdf](Kanban%20Board%20App%20Report.pdf) - Project Report.
- ### [/kanban-app.yaml](kanban-app.yaml) - YAML file for API description.
- ### [/requirements.txt](requirements.txt) - Packages required
- ### [Video](https://drive.google.com/file/d/133s0CWlGhgB99Dfh2z4UBJFbN9w23jEb/view?usp=sharing)
___