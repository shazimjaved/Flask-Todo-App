# 📝 Flask ToDo App

![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)  
![Flask](https://img.shields.io/badge/flask-2.0%2B-green.svg)  
![Bootstrap](https://img.shields.io/badge/bootstrap-5-blueviolet.svg)  
![License](https://img.shields.io/badge/license-MIT-orange.svg)  
![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)  

A simple and elegant **ToDo Web Application** built with **Flask, Bootstrap, SQLAlchemy, and JavaScript**.  
Manage tasks, track progress, and view live stats with an interactive dashboard.

---

## 🚀 Features
- 🔐 User authentication (login & signup)  
- 🕒 Live clock and date on dashboard  
- 💡 Motivational quotes under navbar  
- ✅ Add, edit, mark as done, delete tasks  
- 📊 Statistics page with bar charts (completed vs. pending)  
- 🎨 Responsive UI with Bootstrap  

---

## 🛠️ Tech Stack
- **Backend:** Flask, SQLAlchemy, Flask-WTF, Flask-Login, Flask-Migrate  
- **Frontend:** Bootstrap, CSS, JavaScript  
- **Database:** SQL (via SQLAlchemy ORM)  

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/shazimjaved/flask-todo-app.git
cd flask-todo-app

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables (in .env file)
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key

# Run migrations
flask db init
flask db migrate
flask db upgrade

# Start the app
flask run
