from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User(username='{self.username}', email='{self.email}', email_verified={self.email_verified})"

    def from_db(id, username, email, password_hash, email_verified):
        user = User(username, email)
        user.id = id
        user.password_hash = password_hash
        user.email_verified = email_verified
        return user

class Store:
    def __init__(self, username, name, address, business_page_link):
        self.username = username
        self.name = name
        self.address = address
        self.business_page_link = business_page_link

    def __repr__(self):
        return f"Store(username='{self.username}', name='{self.name}', address='{self.address}', business_page_link='{self.business_page_link}')"


class Customer:
    def __init__(self, email, phone, email_verified=0, phone_verified=0, review_count=0, unique_sentence=None, coupon_code=None, coupon_code_timestamp=None):
        self.email = email
        self.phone = phone
        self.email_verified = email_verified
        self.phone_verified = phone_verified
        self.review_count = review_count
        self.unique_sentence = unique_sentence
        self.coupon_code = coupon_code
        self.coupon_code_timestamp = coupon_code_timestamp

    def __repr__(self):
        return f"Customer(email='{self.email}', phone='{self.phone}', email_verified={self.email_verified}, phone_verified={self.phone_verified}, review_count={self.review_count}, unique_sentence='{self.unique_sentence}', coupon_code='{self.coupon_code}', coupon_code_timestamp='{self.coupon_code_timestamp}')"

