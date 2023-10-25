import sqlite3

class Database:
	def __init__(self, filename):
		# Connect to the database & Create a cursor
		self.connection = sqlite3.connect('database.db')
		self.cursor = self.connection.cursor()
		self.schema_users_table = """(
			username TEXT PRIMARY KEY NOT NULL UNIQUE,
			email TEXT NOT NULL UNIQUE,
			password TEXT NOT NULL
		)"""
		self.schema_stores_table = """(
			username TEXT PRIMARY KEY NOT NULL UNIQUE,
			name TEXT NOT NULL,
			address TEXT NOT NULL,
			business_page_link TEXT NOT NULL
		)"""
		self.schema_customers_table = """(
			email TEXT PRIMARY KEY NOT NULL UNIQUE,
			phone TEXT NOT NULL UNIQUE,
			email_verified INTEGER,
			phone_verified INTEGER,
			unique_sentence TEXT UNIQUE,
			review_count INTEGER,
			coupon_code TEXT,
			coupon_code_timestamp TEXT
		)"""
		
	def close(self):
		self.connection.close()

	def create_table(self, table_name, schema):
		create_table_sql = 'CREATE TABLE IF NOT EXISTS ' + table_name + ' ' + schema
		self.cursor.execute(create_table_sql)
		self.connection.commit()

	def create_default_tables(self):
		# Create the default tables
		self.create_table('users', self.schema_users_table)
		self.create_table('stores', self.schema_stores_table)
		
	def add_user(self, user):
		self.cursor.execute("""
			INSERT INTO users (username, email, password) VALUES (?, ?, ?)
		""", (user.username, user.email, user.password))
		self.connection.commit()

	def add_store(self, store):
		self.cursor.execute("""
			INSERT INTO users (username, name, address, business_page_link) VALUES (?, ?, ?)
		""", (store.username, store.name, store.address, store.business_page_link))
		self.connection.commit()

	def add_store(self, table_name, customer):
		self.cursor.execute("""
			INSERT INTO users (username, name, address, business_page_link) VALUES (?, ?, ?)
		""", (store.username, store.name, store.address, store.business_page_link))
		self.connection.commit()


if __name__ == '__main__':
	from models import User, Store, Customer
	db = Database('database.db')
	db.create_default_tables()
	db.create_table('pizzaburg_customers', db.schema_customers_table)
	user_admin = User('admin', 'admin@opinionidoro.com', 'password')
	db.add_user(user_admin)
	db.close()
