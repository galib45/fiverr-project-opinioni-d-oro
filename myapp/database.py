import sqlite3
from sys import stderr

if __name__ == '__main__':
	from models import User, Store, Customer
else:
	from myapp.models import User, Store, Customer

class Database:
	def __init__(self, filename):
		# Connect to the database & Create a cursor
		self.connection = sqlite3.connect('database.db', check_same_thread=False)
		self.cursor = self.connection.cursor()
		self.schema_users_table = """(
			id INTEGER PRIMARY KEY,
			username TEXT NOT NULL UNIQUE,
			email TEXT NOT NULL UNIQUE,
			password_hash TEXT NOT NULL,
			email_verified INTEGER
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
		create_table_sql = f'CREATE TABLE IF NOT EXISTS {table_name} {schema}'
		self.cursor.execute(create_table_sql)
		self.connection.commit()

	def create_default_tables(self):
		# Create the default tables
		self.create_table('users', self.schema_users_table)
		self.create_table('stores', self.schema_stores_table)
		
	def add_user(self, user):
		try:
			if not hasattr(user, 'password_hash'): 
				raise SystemExit(f'No password was set for "{user.username}"\nuse user.set_password(password)')
			self.cursor.execute("""
				INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)
			""", (user.username, user.email, user.password_hash))
			self.connection.commit()
		except Exception as e:
			print(e, file=stderr)

	def get_user_by_username(self, username):
		try: 
			select_user_sql = f'SELECT * FROM users WHERE username = ?'
			self.cursor.execute(select_user_sql, (username,))
			data = self.cursor.fetchone()
			if data: return User.from_db(*data)
			return data
		except Exception as e:
			print(e, file=stderr)

	def get_user_by_id(self, id):
		try: 
			select_user_sql = f'SELECT * FROM users WHERE id = ?'
			self.cursor.execute(select_user_sql, (id,))
			data = self.cursor.fetchone()
			if data: return User.from_db(*data)
			return data
		except Exception as e:
			print(e, file=stderr)

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
	user_admin = User('admin', 'admin@opinionidoro.com')
	user_admin.set_password('password')
	db.add_user(user_admin)
	db.close()
