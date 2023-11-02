import sqlite3
from sys import stderr
from myapp.models import User, Store, Customer
from myapp.utils import log_info, log_error

class Database:
	def __init__(self, filename):
		# Connect to the database & Create a cursor
		self.database_file = filename
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
			phone_number TEXT NOT NULL,
			google_map_link TEXT NOT NULL,
			place_id TEXT,
			unique_hex_id TEXT
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

	def execute_sql(self, sql, params=()):
		connection = sqlite3.connect(self.database_file)
		cursor = connection.cursor()
		cursor.execute(sql, params)
		connection.commit()
		connection.close()

	def execute_sql_fetchone(self, sql, params=()):
		connection = sqlite3.connect(self.database_file)
		cursor = connection.cursor()
		cursor.execute(sql, params)
		data = cursor.fetchone()
		connection.commit()
		connection.close()
		return data

	def execute_sql_fetchall(self, sql, params=()):
		connection = sqlite3.connect(self.database_file)
		cursor = connection.cursor()
		cursor.execute(sql, params)
		data = cursor.fetchall()
		connection.commit()
		connection.close()
		return data

	def create_table(self, table_name, schema):
		log_info(f'creating table {table_name}')
		create_table_sql = f'CREATE TABLE IF NOT EXISTS {table_name} {schema}'
		self.execute_sql(create_table_sql)	

	def create_default_tables(self):
		# Create the default tables
		self.create_table('users', self.schema_users_table)
		self.create_table('stores', self.schema_stores_table)
		
	def add_user(self, user):
		error = None
		try:
			if not hasattr(user, 'password_hash'): 
				raise SystemExit(f'No password was set for "{user.username}"\nuse user.set_password(password)')
			log_info(f'adding user {user}')
			self.execute_sql("""
				INSERT INTO users (username, email, password_hash, email_verified) VALUES (?, ?, ?, ?)
			""", (user.username, user.email, user.password_hash, user.email_verified))
		except Exception as e:
			log_error(e)
			error = e
		return error

	def get_user_by_username(self, username):
		try: 
			select_user_sql = f'SELECT * FROM users WHERE username = ?'
			data = self.execute_sql_fetchone(select_user_sql, (username,))
			if data: return User.from_db(*data)
			return data
		except Exception as e:
			log_error(e)

	def get_user_by_id(self, id):
		try: 
			select_user_sql = f'SELECT * FROM users WHERE id = ?'
			data = self.execute_sql_fetchone(select_user_sql, (id,))
			if data: return User.from_db(*data)
			return data
		except Exception as e:
			log_error(e)

	def add_store(self, store):
		error = None
		log_info(f'adding store {store}')
		try:
			self.execute_sql("""
				INSERT INTO stores (username, name, address, phone_number, google_map_link, place_id, unique_hex_id) 
				VALUES (?, ?, ?, ?, ?, ?, ?)
			""", (store.username, store.name, store.address, 
				store.phone_number, store.google_map_link, 
				store.place_id, store.unique_hex_id)
			)
		except Exception as e:
			log_error(e)
			error = e
		return error
	# def add_store(self, table_name, customer):
	# 	self.execute_sql("""
	# 		INSERT INTO users (username, name, address, business_page_link) VALUES (?, ?, ?)
	# 	""", (store.username, store.name, store.address, store.business_page_link))


if __name__ == '__main__':
	from models import User, Store, Customer
	db = Database('database.db')
	db.create_default_tables()
	user_admin = User('admin', 'admin@opinionidoro.com', 1)
	user_admin.set_password('password')
	db.add_user(user_admin)
