from werkzeug.security import generate_password_hash

class User:
	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = generate_password_hash(password)

class Store:
    def __init__(self, username, name, address, business_page_link):
        self.username = username
        self.name = name
        self.address = address
        self.business_page_link = business_page_link


class Customer:
    def __init__(self, email, phone):
        self.email = CharField(max_length=80, primary_key=True, unique=True)
        self.phone = CharField(max_length=20, unique=True)
        self.email_verified = 0
        self.phone_verified = 0
        self.review_count = 0
        self.unique_sentence = None
        self.coupon_code = None
        self.coupon_code_timestamp = None
