from datetime import datetime, timedelta, timezone

from flask import abort, flash, redirect, render_template, request, send_file, url_for
from flask.json import dumps, jsonify, loads
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message
from werkzeug.exceptions import HTTPException

from myapp import app, cli_commands, customer_routes, db, login, mail
from myapp.forms import AddStoreForm, LoginForm
from myapp.models import *
from myapp.utils import get_id_from_url, log_error, log_info


@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    return f"""<div style="display: flex;flex-direction: column;align-items: center;font-family:sans-serif;">
    <h1 style="font-size: 5em;margin: 0;">{e.code}</h1>
    <h3 style="font-size: 1.5em;margin: 0;">{e.name}</h3>
    <div style="max-width: 300px;text-align: center;">{e.description}</div>
    </div>"""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/settings")
def settings():
    if current_user.is_authenticated:
        if current_user.username == "admin":
            return render_template("settings-admin.html")
        else:
            store = current_user.stores[0]
            if not store.settings:
                store.settings = '{"coupon_offer": ""}'
                db.session.commit()
            settings = loads(store.settings)
            return render_template("settings.html", settings=settings)
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(db.select(User).filter_by(username=form.username.data))
        if user is None:
            flash("Invalid username")
            return redirect(url_for("login"))
        elif not user.check_password(form.password.data):
            flash("Wrong password")
            return redirect(url_for("login"))
        login_user(user, force=True)
        return redirect(url_for("dashboard"))
    return render_template("login.html", form=form)


@app.route("/dashboard")
def dashboard():
    if current_user.is_authenticated:
        if current_user.username == "admin":
            stores = db.session.scalars(db.select(Store)).all()
            return render_template("dashboard-admin-overview.html", stores=stores)
        else:
            store = current_user.stores[0]
            customers = store.customers
            data = {}
            data["updates"] = {customer.id: 0 for customer in customers}
            data["num_redeems"] = [coupon.redeemed for coupon in store.coupons].count(
                True
            )
            for review in store.reviews:
                data[review.customer.id] = review.updates.count()
            return render_template(
                "dashboard-analytics.html", store=current_user.stores[0], data=data
            )
    return redirect(url_for("login"))


@app.route("/dashboard/customers")
def dashboard_customers():
    if current_user.is_authenticated:
        if current_user.username != "admin":
            store = current_user.stores[0]
            data = {}
            for review in store.reviews:
                data[review.customer.id] = review.updates.count()
            return render_template("dashboard-customers.html", store=store, data=data)
        return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("login"))


@app.route("/dashboard/campaigns")
def dashboard_campaigns():
    if current_user.is_authenticated:
        if current_user.username != "admin":
            return render_template("dashboard-campaigns.html")
        return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("login"))


@app.route("/dashboard/qrcode")
def dashboard_qrcode():
    if current_user.is_authenticated:
        if current_user.username != "admin":
            return render_template("dashboard-qrcode.html")
        return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("login"))


@app.route("/chartdata")
def chartdata():
    if current_user.is_authenticated and current_user.username != "admin":
        store = current_user.stores[0]
        data = {}
        updates = []
        for review in store.reviews:
            for update in review.updates:
                updates.append(
                    {"rating": update.rating, "timestamp": float(update.timestamp)}
                )
        data["updates"] = updates
        data["store_created"] = store.date_created.timestamp()
        return jsonify(data)
    else:
        return jsonify({})


@app.route("/addstore", methods=["GET", "POST"])
def addstore():
    if current_user.is_authenticated and current_user.username == "admin":
        form = AddStoreForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            timestamp_now = datetime.utcnow()

            store = Store(
                name=form.name.data,
                address=form.address.data,
                phone_number=form.phone_number.data,
                google_map_url=form.google_map_url.data,
                place_id=form.place_id.data,
                hex_id=form.hex_id.data,
                date_created=timestamp_now,
                upto_timestamp=timestamp_now - timedelta(days=1),
                owner=user,
            )
            db.session.add(store)
            db.session.commit()
            return redirect(url_for("dashboard"))
        return render_template("addstore.html", form=form)
    else:
        return redirect(url_for("index"))


@app.route("/delstore/<store_id>")
def delstore(store_id):
    if current_user.is_authenticated:
        if current_user.username == "admin":
            store = db.session.get(Store, store_id)
            if store:
                owner = store.owner
                store_count = owner.stores.count()
                if store_count <= 1:
                    db.session.delete(owner)
                    flash(f"Removed user [{owner.username}] successfully")
                db.session.delete(store)
                flash(f"Removed store [{store.name}] successfully")
                db.session.commit()
            return redirect(url_for("dashboard"))
        else:
            flash("Only admin can access the page you requested")
            return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/getid/<google_map_url_id>")
def getid(google_map_url_id):
    url = f"https://maps.app.goo.gl/{google_map_url_id}"
    log_info(url)
    place_id, hex_id = get_id_from_url(url)
    return jsonify(place_id=place_id, hex_id=hex_id)
