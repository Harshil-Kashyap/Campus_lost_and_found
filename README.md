# Campus Lost & Found System

A simple desktop application for college students to report lost or found items, search for items, and submit claims. An admin can review claims.

## Features

- Student registration and login
- Report lost or found items
- Search items
- Submit and track claims
- Manage personal reports
- Admin approval or rejection of claims
- Basic dashboard
- SQLite database

## Technologies

- Python
- Tkinter
- SQLite
- unittest

No extra Python packages are required.

## How to Run

### Windows

```text
py app.py
```

You can also run `run.py`.

### Other Systems

```text
python3 app.py
```

## Demo Accounts

**Student**
- Email: `student@campus.local`
- Password: `student123`

**Admin**
- Email: `admin@campus.local`
- Password: `admin123`

## Tests

Run this from the project folder:

```text
python -m unittest discover -s tests -v
```

The tests use a temporary database, so the main database is not affected.

## Project Structure

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
```
