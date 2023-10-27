from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user
from myapp import app, db, login
from myapp.forms import LoginForm

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/favicon.ico')
# def favicon():
#     return redirect(url_for('static', filename='favicon.ico'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.get_user_by_username(form.username.data)
        if user is None or not user.check_password(form.password.data):
            if user is None: flash('Invalid username')
            else: flash('Wrong password')
            return redirect(url_for('login'))
        login_user(user, force=True)
        return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    if current_user.is_authenticated:
        return render_template('dashboard.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
