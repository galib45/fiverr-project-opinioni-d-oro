from datetime import datetime, timedelta

from flask import abort, flash, redirect, render_template, request, send_file, url_for
from flask.json import dumps, jsonify, loads
from flask_login import current_user, login_user, logout_user
from flask_mail import Message
from slugify import slugify

from myapp import (
    app,
    campaign_routes,
    cli_commands,
    customer_routes,
    db,
    decorators,
    errorhandlers,
    login,
    mail,
)
from myapp.forms import AddArticleForm, AddStoreForm, EditStoreForm, LoginForm
from myapp.models import *
from myapp.utils import get_id_from_url, log_error, log_info


@app.after_request
def after_request(response):
    response.headers["Content-Security-Policy"] = (
        ""
        + "font-src https://fonts.googleapis.com/ https://fonts.gstatic.com;"
        + "style-src-elem 'self' https://fonts.googleapis.com/ https://cdn.quilljs.com 'nonce-golden';"
        + "script-src-elem 'self' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net https://cdn.quilljs.com https://esm.sh 'nonce-golden'"
    )
    return response


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
        if current_user.role == "admin":
            stores = db.session.scalars(db.select(Store)).all()
            return render_template("dashboard-admin-overview.html", stores=stores)
        else:
            if current_user.state == "active":
                store = current_user.stores[0]
                customers = store.customers
                data = {}
                data["updates"] = {customer.id: 0 for customer in customers}
                data["num_redeems"] = [
                    coupon.redeemed for coupon in store.coupons
                ].count(True)
                for review in store.reviews:
                    data[review.customer.id] = review.updates.count()
                return render_template(
                    "dashboard-analytics.html", store=current_user.stores[0], data=data
                )
            flash("Your account is not active, please contact the admin")
            return redirect(url_for("contact"))
    return redirect(url_for("login"))


@app.route("/dashboard/customers")
@decorators.shop_owner_required
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


@app.route("/dashboard/qrcode")
@decorators.shop_owner_required
def dashboard_qrcode():
    if current_user.is_authenticated:
        if current_user.username != "admin":
            store = current_user.stores[0]
            store_slug = f"{store.id}-{slugify(store.name)}"
            return render_template("dashboard-qrcode.html", store_slug=store_slug)
        return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("login"))


@app.route("/chartdata")
@decorators.shop_owner_required
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
@decorators.admin_required
def addstore():
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


@app.route("/delstore/<store_id>")
@decorators.admin_required
def delstore(store_id):
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


@app.route("/editstore/<store_id>", methods=["GET", "POST"])
@decorators.admin_required
def editstore(store_id):
    store = db.session.get(Store, store_id)
    if store:
        form = EditStoreForm()
        if form.validate_on_submit():
            store.name = form.name.data
            store.phone_number = form.phone_number.data
            store.address = form.address.data
            store.google_map_url = form.google_map_url.data
            store.place_id = form.place_id.data
            store.hex_id = form.hex_id.data
            try:
                db.session.commit()
            except Exception as e:
                flash(f"Error occurred - {e}")
            return redirect(url_for("dashboard"))
        return render_template("editstore.html", store=store, form=form)
    else:
        abort(404)


@app.route("/editstore/<store_id>/extras", methods=["POST"])
@decorators.admin_required
def editstore_extras(store_id):
    data = request.json
    store = db.session.get(Store, store_id)
    if not store:
        abort(404)
    if "state" in data:
        store.owner.state = data["state"]
    if "package" in data:
        store.package = data["package"]
    try:
        db.session.commit()
    except:
        return jsonify(status="error")
    return jsonify(status="success")


@app.route("/help")
def helpcenter():
    articles = db.session.scalars(db.select(Article)).all()
    return render_template("helpcenter.html", articles=articles, slugify=slugify)


@app.route("/help/<slug>")
def help_article(slug):
    try:
        id, title = slug.split("-", 1)
    except:
        abort(404)
    article = db.session.get(Article, id)
    if not article:
        abort(404)
    if slugify(title) != slugify(article.title):
        abort(404)
    if title != slugify(title):
        abort(404)
    return render_template("help-article.html", article=article)


@app.route("/articles")
@decorators.admin_required
def articles():
    articles = db.session.scalars(db.select(Article)).all()
    return render_template("articles.html", articles=articles)


@app.route("/articles/add", methods=["GET", "POST"])
@decorators.admin_required
def add_article():
    form = AddArticleForm()
    if form.validate_on_submit():
        article = Article(
            title=form.title.data,
            content=form.content.data,
            updated_at=datetime.utcnow(),
        )
        db.session.add(article)
        db.session.commit()
        flash("new article created successfully")
    return render_template("add-article.html", form=form)


@app.route("/articles/<id>/edit", methods=["GET", "POST"])
@decorators.admin_required
def edit_article(id):
    article = db.session.get(Article, id)
    form = AddArticleForm()
    if form.validate_on_submit():
        article.title = form.title.data
        article.content = form.content.data
        article.updated_at = datetime.utcnow()
        db.session.commit()
        flash("article updated successfully")
        return redirect(url_for("articles"))
    return render_template("edit-article.html", form=form, article=article)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/getid/<google_map_url_id>")
def getid(google_map_url_id):
    url = f"https://maps.app.goo.gl/{google_map_url_id}"
    log_info(url)
    place_id, hex_id = get_id_from_url(url)
    return jsonify(place_id=place_id, hex_id=hex_id)
