from flask import render_template, flash, redirect, url_for, request, send_file
from flask.json import jsonify
from flask_login import current_user, login_user, login_required, logout_user
from myapp import app, db, login
from myapp.forms import LoginForm, AddStoreForm
from myapp.models import User, Store
from myapp.utils import log_info, log_error, get_id_from_url

@app.route('/')
def index():
    return render_template('index.html')

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
        user = db.session.scalar(db.select(User).filter_by(username=form.username.data))
        if user is None:
            flash('Invalid username')
            return redirect(url_for('login'))
        elif not user.check_password(form.password.data):
            flash('Wrong password')
            return redirect(url_for('login'))
        login_user(user, force=True)
        return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    if current_user.is_authenticated:
        if current_user.username == 'admin':
            stores = db.session.scalars(db.select(Store)).all()
            return render_template('dashboard-admin.html', stores=stores)
        else:
            return render_template('dashboard.html')
    return redirect(url_for('login'))

@app.route('/addstore', methods=['GET', 'POST'])
def addstore():
    if current_user.is_authenticated and current_user.username == 'admin':
        form = AddStoreForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            store = Store(
                name=form.name.data, address=form.address.data, 
                phone_number=form.phone_number.data, google_map_url=form.google_map_url.data,
                place_id=form.place_id.data, hex_id=form.hex_id.data,
                owner=user
            )
            db.session.add(store)
            db.session.commit()
            return redirect(url_for('dashboard'))
        return render_template('addstore.html', form=form)
    else:
        return redirect(url_for('index'))

@app.route('/delstore/<username>')
def delstore(username):
    if current_user.is_authenticated:
        if current_user.username == 'admin':
            db.execute_sql('DELETE from users WHERE username=?', (username,))
            db.execute_sql('DELETE from stores WHERE username=?', (username,))
            flash(f'Store of [{username}] deleted successfully')
            return redirect(url_for('dashboard'))
        else:
            flash('Only admin can access the page you requested')
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/getid/<google_map_url_id>')
def getid(google_map_url_id):
    url = f'https://maps.app.goo.gl/{google_map_url_id}'
    log_info(url)
    place_id, hex_id = get_id_from_url(url)
    return jsonify(place_id=place_id, hex_id=hex_id)
