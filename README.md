# 🧑‍💼 Job Portal Web Application

A Flask-based job portal that allows Job Seekers to find and apply for jobs, Employers to post and manage listings, and Admins to oversee users and job data.

## 📌 Features

### 👥 User Roles
- **Job Seeker:** Register, login, browse jobs, apply, upload resume.
- **Employer:** Post jobs, view and manage listings, view applicants.
- **Admin:** View all users and job postings.

### ⚙️ Functionalities
- User registration and login
- Role-based dashboards
- Job search and filtering
- Resume upload and download (PDF/DOCX)
- Admin panel (with job & user management)

## 🛠️ Tech Stack

- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite (default), compatible with PostgreSQL
- **Extensions:** Flask-Login, Flask-WTF, SQLAlchemy

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.8+
- pip
- Git (optional, for cloning)

### 📁 Setup

```bash
# Clone the repo or download as ZIP
git clone https://github.com/your-username/job-portal.git
cd job-portal

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Setup the database
python setup.py

# Run the app
python run.py
