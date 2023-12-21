from threading import Thread
from time import time

import jwt
from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user
from flask_mail import Message

from myapp import app, db, mail
from myapp.forms import LoginForm, ResetPasswordForm, ResetPasswordRequestForm
from myapp.models import User


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, text_body, html_body):
    msg = Message(subject, sender=app.config["MAIL_USERNAME"], recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def get_reset_password_token(user_id, expires_in=600):
    return jwt.encode(
        {"reset_password": user_id, "exp": time() + expires_in},
        app.config["SECRET_KEY"],
        algorithm="HS256",
    )


def verify_reset_password_token(token):
    try:
        id = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])[
            "reset_password"
        ]
    except:
        return
    return db.session.get(User, id)


def send_password_reset_email(user):
    token = get_reset_password_token(user.id)
    send_email(
        "[Golden Opinions] Reset Your Password",
        recipients=[user.email],
        text_body=render_template("email/reset_password.txt", user=user, token=token),
        html_body=render_template("email/reset_password.html", user=user, token=token),
    )


@app.route("/reset_password", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        logout_user()
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = db.session.scalar(db.select(User).where(User.email == form.email.data))
        if not user:
            flash(f"No account is associated with {form.email.data}", "error")
            return redirect(url_for("reset_password_request"))
        send_password_reset_email(user)
        flash("Check your email for the instructions to reset your password")
        return redirect(url_for("login"))
    return render_template("reset-password-request.html", form=form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    user = verify_reset_password_token(token)
    if not user:
        flash("Invalid or expired token for password reset", category="error")
        return redirect(url_for("login"))
    if current_user == user:
        logout_user()
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset.")
        return redirect(url_for("login"))
    return render_template("reset-password.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(db.select(User).filter_by(username=form.username.data))
        if user is None:
            flash("Invalid username")
            return redirect(url_for("login"))
        elif not user.check_password(form.password.data):
            flash("Wrong password")
            return redirect(url_for("login"))
        login_user(user, force=True)
        return redirect(url_for("dashboard"))
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))
