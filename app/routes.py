from flask import Blueprint, render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os

from .models import User, Job, Application
from .forms import RegistrationForm, LoginForm, JobForm
from . import db

main = Blueprint('main', __name__)

@main.app_context_processor
def inject_user():
    return dict(current_user=current_user)


@main.route('/')
def home():
    return render_template('home.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.jobs'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

@main.route('/jobs')
def jobs():
    keyword = request.args.get('keyword')
    location = request.args.get('location')
    jobs = Job.query
    if keyword:
        jobs = jobs.filter(Job.title.ilike(f"%{keyword}%"))
    if location:
        jobs = jobs.filter(Job.location.ilike(f"%{location}%"))
    return render_template('jobs.html', jobs=jobs.all())

@main.route('/apply/<int:job_id>', methods=['GET', 'POST'])
@login_required
def apply(job_id):
    job = Job.query.get_or_404(job_id)
    if request.method == 'POST':
        resume = request.files['resume']
        if resume:
            filename = secure_filename(resume.filename)
            save_path = os.path.join('resumes', filename)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            resume.save(save_path)
            application = Application(user_id=current_user.id, job_id=job.id, resume_filename=filename)
            db.session.add(application)
            db.session.commit()
            flash("Application submitted!", "success")
            return redirect(url_for('main.jobs'))
    return render_template('apply.html', job=job)

@main.route('/post_job', methods=['GET', 'POST'])
@login_required
def post_job():
    form = JobForm()
    if form.validate_on_submit():
        job = Job(
            title=form.title.data,
            company=form.company.data,
            description=form.description.data,
            salary=form.salary.data,
            location=form.location.data,
            employer_id=current_user.id
        )
        db.session.add(job)
        db.session.commit()
        flash("Job posted successfully!", "success")
        return redirect(url_for('main.employer_dashboard'))
    return render_template('post_job.html', form=form)

@main.route('/employer_dashboard')
@login_required
def employer_dashboard():
    jobs = Job.query.filter_by(employer_id=current_user.id).all()
    return render_template('employer_dashboard.html', jobs=jobs)

@main.route('/delete_job/<int:job_id>', methods=['POST'])
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.employer_id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for('main.employer_dashboard'))
    db.session.delete(job)
    db.session.commit()
    flash("Job deleted successfully.", "success")
    return redirect(url_for('main.employer_dashboard'))
