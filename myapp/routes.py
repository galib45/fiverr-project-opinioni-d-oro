from datetime import datetime, timezone, timedelta
from flask import abort, render_template, flash, redirect, url_for, request, send_file
from flask.json import jsonify
from flask_login import current_user, login_user, login_required, logout_user
from myapp import app, db, login
from myapp.forms import LoginForm, AddStoreForm
from myapp.models import User, Store, Customer, Photo, Update, Review, Coupon
from myapp.utils import log_info, log_error, get_id_from_url
from werkzeug.exceptions import HTTPException
from myapp import customer_routes

@app.cli.command("fetch-reviews")
def fetch_reviews():
    from myapp.utils import get_review_list, generate_random_code
    stores = db.session.scalars(db.select(Store)).all()
    timestamp_now = datetime.utcnow()
    for store in stores:
        account_id_list = [customer.account_id for customer in store.customers]
        review_list = get_review_list(store.hex_id, datetime.timestamp(store.upto_timestamp))
        for review in review_list:
            account_id, timestamp, rating, text, photos = review
            print(account_id, end='')
            if account_id in account_id_list:
                customer = db.session.scalar(db.select(Customer).filter_by(account_id=review[0]))
                review = Review()
                update = Update(rating=rating, text=text, timestamp=timestamp)
                for item in photos:
                    photo = Photo(url=f'https://lh5.googleusercontent.com/p/{item}')
                    update.photos.append(photo)
                review.updates.append(update)
                
                if review.updates.count() == 1:
                    if customer.coupons.count() > 0:
                        days_after_last_coupon = (timestamp_now - customer.got_coupon_date).days
                        if days_after_last_coupon < 15:
                            # generate coupon
                            coupon = Coupon(code=generate_random_code(), expire_date=timestamp_now+timedelta(days=30))
                            customer.coupons.append(coupon)
                            customer.got_coupon_date = timestamp_now
                            store.coupons.append(coupon)
                    else:
                        # generate coupon
                        coupon = Coupon(code=generate_random_code(), expire_date=timestamp_now+timedelta(days=30))
                        customer.coupons.append(coupon)
                        customer.got_coupon_date = timestamp_now
                        store.coupons.append(coupon)
                customer.reviews.append(review)
                store.reviews.append(review)
                print(' - registered')
            else: print(' - not registered')
            store.upto_timestamp = timestamp_now
            db.session.commit()

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    return f'''<div style="display: flex;flex-direction: column;align-items: center;font-family:sans-serif;">
    <h1 style="font-size: 5em;margin: 0;">{e.code}</h1>
    <h3 style="font-size: 1.5em;margin: 0;">{e.name}</h3>
    <div style="max-width: 300px;text-align: center;">{e.description}</div>
    </div>'''

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
            return render_template('dashboard.html', store=current_user.stores[0])
    return redirect(url_for('login'))

@app.route('/addstore', methods=['GET', 'POST'])
def addstore():
    if current_user.is_authenticated and current_user.username == 'admin':
        form = AddStoreForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            timestamp_now = datetime.utcnow()
            
            store = Store(
                name=form.name.data, address=form.address.data, 
                phone_number=form.phone_number.data, google_map_url=form.google_map_url.data,
                place_id=form.place_id.data, hex_id=form.hex_id.data,
                date_created=timestamp_now, upto_timestamp=timestamp_now-timedelta(days=1),
                owner=user
            )
            db.session.add(store)
            db.session.commit()
            return redirect(url_for('dashboard'))
        return render_template('addstore.html', form=form)
    else:
        return redirect(url_for('index'))

@app.route('/delstore/<store_id>')
def delstore(store_id):
    if current_user.is_authenticated:
        if current_user.username == 'admin':
            store = db.session.get(Store, store_id)
            if store:
                owner = store.owner
                store_count = owner.stores.count()
                if store_count <= 1: 
                    db.session.delete(owner)
                    flash(f'Removed user [{owner.username}] successfully')
                db.session.delete(store)
                flash(f'Removed store [{store.name}] successfully')
                db.session.commit()
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

