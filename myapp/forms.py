from flask_wtf import FlaskForm
from myapp import db
from myapp.models import User
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import ValidationError


def check_if_username_exists(form, field):
    if db.session.scalar(db.select(User).filter_by(username=form.username.data)):
        raise ValidationError("A store with this username already exists!")


class AddStoreForm(FlaskForm):
    username = StringField("Username", validators=[check_if_username_exists])
    email = StringField("Email")
    password = PasswordField("Password")
    confirm_password = PasswordField("Confirm Password")
    name = StringField("Store Name")
    phone_number = StringField("Phone Number")
    address = StringField("Address")
    google_map_url = StringField("Google Map URL")
    place_id = StringField("Place ID")
    hex_id = StringField("Hex ID")
    submit = SubmitField("Add Store")


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Login")


class RegisterCustomerForm(FlaskForm):
    email = StringField("Email")
    name = StringField("Name")
    phone_number = StringField("Phone Number")
    privacy_policy = BooleanField()
    submit = SubmitField("Register")
