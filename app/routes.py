from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, TODO
from .forms import TODOForm, SignupForm, LoginForm
from . import db
from datetime import datetime, timedelta

# Define the blueprint
todo_bp = Blueprint('todo', __name__)

@todo_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists.', 'danger')
            return render_template('signup.html', form=form)
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered.', 'danger')
            return render_template('signup.html', form=form)
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('todo.login'))
    return render_template('signup.html', form=form)

@todo_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f'Welcome, {user.username}!', 'success')
            flash('Logged in successfully!', 'success')
            return redirect(url_for('todo.index'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@todo_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('todo.login'))

# Protect TODO routes
@todo_bp.route('/')
@login_required
def index():
    todos = TODO.query.order_by(TODO.due_date).all()
    return render_template('todo/list.html', todos=todos)

@todo_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_todo():
    form = TODOForm()
    if form.validate_on_submit():
        todo = TODO(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            status=form.status.data
        )
        db.session.add(todo)
        db.session.commit()
        flash('TODO added successfully!', 'success')
        return redirect(url_for('todo.index'))
    return render_template('todo/form.html', form=form, action='Add')

@todo_bp.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
@login_required
def edit_todo(todo_id):
    todo = TODO.query.get_or_404(todo_id)
    form = TODOForm(obj=todo)
    if form.validate_on_submit():
        todo.title = form.title.data
        todo.description = form.description.data
        todo.due_date = form.due_date.data
        todo.status = form.status.data
        db.session.commit()
        flash('TODO updated successfully!', 'success')
        return redirect(url_for('todo.index'))
    return render_template('todo/form.html', form=form, action='Edit')

@todo_bp.route('/delete/<int:todo_id>', methods=['POST'])
@login_required
def delete_todo(todo_id):
    todo = TODO.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash('TODO deleted successfully!', 'success')
    return redirect(url_for('todo.index'))

@todo_bp.route('/complete/<int:todo_id>', methods=['POST'])
@login_required
def complete_todo(todo_id):
    todo = TODO.query.get_or_404(todo_id)
    todo.status = 'Completed'
    db.session.commit()
    flash('TODO marked as completed!', 'success')
    return redirect(url_for('todo.index'))

@todo_bp.route('/your-stats')
def your_stats():
    total_tasks = TODO.query.count()
    completed_tasks = TODO.query.filter_by(status='Completed').count()
    pending_tasks = TODO.query.filter_by(status='Pending').count()

    # Weekly progress: count completed tasks per day for the last 7 days
    today = datetime.utcnow().date()
    week_dates = [today - timedelta(days=i) for i in range(6, -1, -1)]
    week_labels = [d.strftime('%a') for d in week_dates]
    week_counts = []
    for d in week_dates:
        count = TODO.query.filter_by(status='Completed', due_date=d).count()
        week_counts.append(count)

    return render_template(
        'your_stats.html',
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        week_labels=week_labels,
        week_counts=week_counts
    ) 