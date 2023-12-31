from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import ValidationError

from myapp import db
from myapp.models import User


def check_if_username_exists(form, field):
    if db.session.scalar(db.select(User).filter_by(username=form.username.data)):
        raise ValidationError("A store with this username already exists!")


def check_if_email_exists(form, field):
    if db.session.scalar(db.select(User).filter_by(email=form.email.data)):
        raise ValidationError("A store with this email already exists!")


class NewCampaignForm(FlaskForm):
    name = StringField("Name of the Campaign")
    description = TextAreaField("Short Description")
    offer = StringField("Campaign Offer")
    expire_date = StringField("Expire Date")
    category = RadioField('Target Audience', 
        choices=[('general','All Customers'),('custom','A Few Selected Customers')], 
        default='general'
    )
    submit = SubmitField("Create Campaign")


class AddArticleForm(FlaskForm):
    title = StringField("Title of the Article")
    content = StringField("Content")
    submit = SubmitField("Add Article")


class AddStoreForm(FlaskForm):
    username = StringField("Username", validators=[check_if_username_exists])
    email = StringField("Email", validators=[check_if_email_exists])
    password = PasswordField("Password")
    confirm_password = PasswordField("Confirm Password")
    name = StringField("Store Name")
    phone_number = StringField("Phone Number")
    address = StringField("Address")
    google_map_url = StringField("Google Map URL")
    place_id = StringField("Place ID")
    hex_id = StringField("Hex ID")
    submit = SubmitField("Add Store")


class EditStoreForm(FlaskForm):
    name = StringField("Store Name")
    phone_number = StringField("Phone Number")
    address = StringField("Address")
    google_map_url = StringField("Google Map URL")
    place_id = StringField("Place ID")
    hex_id = StringField("Hex ID")
    submit = SubmitField("Save")


class AdminSettingsForm(FlaskForm):
    email = StringField("Email")
    submit = SubmitField("Save")

class ShopOwnerSettingsForm(FlaskForm):
    email = StringField("Email")
    general_coupon_offer = StringField("General Coupon Offer")
    submit = SubmitField("Save")

class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Login")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("New Password")
    confirm_password = PasswordField("Confirm New Password")
    submit = SubmitField("Submit")


class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Email")
    submit = SubmitField("Submit")


class RegisterCustomerForm(FlaskForm):
    email = StringField("Email")
    name = StringField("Name")
    phone_number = StringField("Phone Number")
    privacy_policy = BooleanField()
    submit = SubmitField("Register")
