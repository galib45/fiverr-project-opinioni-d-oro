from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from myapp import db
from myapp.utils import get_id_from_url

store_customer = db.Table(
    "store_customer",
    db.Column("store_id", db.Integer, db.ForeignKey("store.id")),
    db.Column("customer_id", db.Integer, db.ForeignKey("customer.id")),
)

campaign_customer = db.Table(
    "campaign_customer",
    db.Column("campaign_id", db.Integer, db.ForeignKey("campaign.id")),
    db.Column("customer_id", db.Integer, db.ForeignKey("customer.id")),
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(255))
    email_verified = db.Column(db.Boolean, default=False)
    policies_accepted = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(10), default="shop_owner")
    state = db.Column(db.String(10), default="active")
    stores = db.relationship("Store", backref="owner", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User(username='{self.username}', email='{self.email}', email_verified={self.email_verified})"


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    phone_number = db.Column(db.String(20))
    google_map_url = db.Column(db.String(50))
    place_id = db.Column(db.String(50))
    hex_id = db.Column(db.String(50))
    date_created = db.Column(db.DateTime())
    upto_timestamp = db.Column(db.DateTime())
    general_coupon_offer = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    package = db.Column(db.String, default="basic")
    customers = db.relationship("Customer", secondary="store_customer", backref="store")
    campaigns = db.relationship("Campaign", backref="store", lazy="dynamic")
    coupons = db.relationship("Coupon", backref="store", lazy="dynamic")
    reviews = db.relationship("Review", backref="store", lazy="dynamic")
    coupons_generated = db.Column(db.Integer, default=0)
    coupons_redeemed = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"Store(name='{self.name}', address='{self.address}', phone_number='{self.phone_number}')"


class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    offer = db.Column(db.String)
    code = db.Column(db.String(10))
    date_created = db.Column(db.DateTime())
    expire_date = db.Column(db.DateTime())
    category = db.Column(db.String(10), default="general")
    status = db.Column(db.String(10), default="pending")
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"))
    customers = db.relationship(
        "Customer", secondary="campaign_customer", backref="campaign"
    )

    def __repr__(self):
        return f"Campaign(name='{self.name}', offer='{self.offer}', code='{self.code}', expire_date='{self.expire_date}')"


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String)
    data = db.Column(db.String)
    date_created = db.Column(db.DateTime())

    def __repr__(self):
        return f"Action(category='{self.category}')"


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String(50), unique=True)
    phone_number = db.Column(db.String(20))
    account_id = db.Column(db.String)
    phone_verified = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(10))
    got_coupon_date = db.Column(db.DateTime())
    coupons = db.relationship("Coupon", backref="customer", lazy="dynamic")
    reviews = db.relationship("Review", backref="customer", lazy="dynamic")

    def __repr__(self):
        return f"Customer(name='{self.name}', email='{self.email}', phone_number='{self.phone_number}')"


class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10))
    expire_date = db.Column(db.DateTime())
    offer = db.Column(db.String)
    email_sent = db.Column(db.Boolean)
    sms_sent = db.Column(db.Boolean)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"))
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))

    def __repr__(self):
        return f"Coupon(code='{self.code}', expire_date='{self.expire_date}')"


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"))
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    updates = db.relationship("Update", backref="review", lazy="dynamic")


class Update(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    text = db.Column(db.String)
    timestamp = db.Column(db.String)
    review_id = db.Column(db.Integer, db.ForeignKey("review.id"))
    photos = db.relationship("Photo", backref="update", lazy="dynamic")

    def __repr__(self):
        return f"Update(rating='{self.rating}', 'text='{self.text}', timestamp='{self.timestamp}')"


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    updated_at = db.Column(db.DateTime())


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    update_id = db.Column(db.Integer, db.ForeignKey("update.id"))

    def __repr__(self):
        return f"Store(url='{self.url}')"
