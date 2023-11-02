from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from myapp.utils import get_id_from_url
from myapp import db


store_customer = db.Table(
    'store_customer',
    db.Column('store_id', db.Integer, db.ForeignKey('store.id')),
    db.Column('customer_id', db.Integer, db.ForeignKey('customer.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(255))
    email_verified = db.Column(db.Boolean, default=False)
    stores = db.relationship('Store', backref='owner', lazy='dynamic')

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
    coupon_offer = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    customers = db.relationship('Customer', secondary='store_customer', backref='store')
    coupons = db.relationship('Coupon', backref='store', lazy='dynamic')

    def __repr__(self):
        return f"Store(name='{self.name}', address='{self.address}', phone_number='{self.phone_number}')"


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String(50), unique=True)
    phone_number = db.Column(db.String(20))
    email_verified = db.Column(db.Boolean, default=False)
    phone_verified = db.Column(db.Boolean, default=False)
    coupons = db.relationship('Coupon', backref='customer', lazy='dynamic')

    def __repr__(self):
        return f"Customer(email='{self.email}', phone='{self.phone}', email_verified={self.email_verified}, phone_verified={self.phone_verified}, review_count={self.review_count}, unique_sentence='{self.unique_sentence}', coupon_code='{self.coupon_code}', coupon_code_timestamp='{self.coupon_code_timestamp}')"


class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10))
    expire_date = db.Column(db.DateTime())
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
