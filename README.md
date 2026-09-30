# Campus Lost & Found System

This is a simple desktop application for use by college students. The software allows them to report lost or found items, search for items, and make claims. An admin can approve or reject claims.

## Features

Students can register and login to the system.
Users can report lost and found items and search for items. They can also make and view claims and manage their reports. The admin approves or rejects claims. There is also a simple dashboard and a SQLite database.

## Technologies

The following technologies are used in this project:
- Python
- Tkinter
- SQLite
- unittest
No other python libraries are needed.
## Getting started
For windows:

```text

py app.py
```
you can also use the file run.py.
For other systems:
```text
python3 app.py
```
## Demo Accounts
Student:
- Email: student@campus.local
- Password: student123
Admin:
- Email: admin@campus.local
- Password: admin123
## Tests
To run the tests, navigate to the project directory and run the following command:
```text
python -m unittest discover -s tests -v
```
This script runs tests using a temporary database. The tests should not modify the main database.
## Folder Structure
The following is the folder structure:
```text
campus_lost_found/
├── app.py
├── auth.py
├── claims.py
├── db.py
├── items.py
├── reports.py
├── ui.py
├── run.py
├── run.bat
├── requirements.txt
├── README.md
├── statement.md
├── data/
├── docs/
└── tests/
