#  Teacher Management System (TMS)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2%2B-092e20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Deployment](https://img.shields.io/badge/Deployment-Render-46E3B7?logo=render&logoColor=white)](https://render.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

A robust and simple **Teacher Management System** built with Django, designed for academic institutions to manage teacher records, track performance, and handle user authentication seamlessly.

---

##  Overview

The **Teacher Management System (TMS)** is a web application that allows administrators to register, update, and manage teacher profiles efficiently. The system provides a secure environment with user-level authentication and a dynamic dashboard for easy accessibility.

##  Key Features

-    **User Authentication**: Secure Login/Registration for system admins.
-    **Dashboard**: Overview of current system status and quick access to management tools.
-    **Teacher Records (CRUD)**:
    -    **Add Teachers**: Record teaching details, qualifications, and contacts.
    -    **View Records**: Dynamic table view of all registered teachers.
    -    **Update Records**: Edit existing teacher information.
    -    **Delete Records**: Remove teachers from the system.
-    **User Management**: Admin control to view and manage registered users.
-    **Modern UI**: Clean and professional design with responsive layouts.

##  Technology Stack

-   **Backend**: Python, [Django Framework](https://www.djangoproject.com/)
-   **Frontend**: HTML5, CSS3, JavaScript
-   **Database**: SQLite (Development), PostgreSQL/dj-database-url (Production ready)
-   **Static Assets**: WhiteNoise (Production serving)
-   **Production Server**: Gunicorn

---

##  Project Structure

```bash
teacher_mng_system/
├── mypro/                   # Root Django project
│   ├── mypro/               # Project settings and core files
│   │   ├── settings.py      # Configuration for local & production
│   │   ├── urls.py          # Main URL routing
│   │   └── wsgi.py          # Entry point for production servers
│   ├── tms/                 # Primary Application app
│   │   ├── models.py        # Database models (Teacher, User)
│   │   ├── views.py         # Business logic & routing
│   │   ├── static/          # CSS, JS, and image assets
│   │   └── templates/       # HTML view templates
│   ├── manage.py            # Django management CLI
│   └── db.sqlite3           # Local development database
├── requirements.txt         # Project dependencies
└── README.md                # Documentation (Current file)
```

---

##  Setup and Installation

Follow these steps to get the project up and running locally:

### 1. Clone the repository
```bash
git clone <repository_url>
cd teacher_mng_system
```

### 2. Create a virtual environment
```bash
python3 -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
cd mypro
python3 manage.py makemigrations
python3 manage.py migrate
```

### 5. Create a Superuser (Admin Dashboard access)
```bash
# Ensure you are in the mypro directory
cd mypro
python3 manage.py createsuperuser
```

### 6. Start the Development Server
```bash
# Ensure you are in the mypro directory
cd mypro
python3 manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser to see the application!

---

## Deployment (Render)

This project is pre-configured for deployment on **Render**. It uses `dj-database-url` and `WhiteNoise` for efficient serving in production.

- **URL**: `https://teacher_mng_system.onrender.com`
- **Steps**:
    1. Connect the repository to Render.
    2. Set `DEBUG` to `False` in environment variables.
    3. Use `gunicorn mypro.wsgi` as the Start Command.

#
