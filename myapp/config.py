from dotenv import dotenv_values


class Config:
    env = dotenv_values(".env")
    ENVIRONMENT = env.get("ENVIRONMENT")
    SECRET_KEY = env.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = env.get("SQLALCHEMY_DATABASE_URI")
    MAIL_SERVER = env.get("MAIL_SERVER")
    MAIL_PORT = env.get("MAIL_PORT")
    MAIL_USE_TLS = env.get("MAIL_USE_TLS")
    MAIL_USERNAME = env.get("MAIL_USERNAME")
    MAIL_PASSWORD = env.get("MAIL_PASSWORD")
    ADMINS = ["yamisukehirobulls@gmail.com"]
