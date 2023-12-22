from flask import flash, redirect, url_for
from flask_login import current_user


def login_required(view):
    def inner(*args, **kwargs):
        if current_user.is_authenticated:
            return view(*args, **kwargs)
        flash("You have to login first")
        return redirect(url_for("login"))

    inner.__name__ = view.__name__
    return inner


def verified_email_required(view):
    def inner(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.email_verified:
                return view(*args, **kwargs)
            return redirect(url_for("verify_email_request"))
        flash("You have to login first")
        return redirect(url_for("login"))

    inner.__name__ = view.__name__
    return inner


def admin_required(view):
    def inner(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.role == "admin":
                return view(*args, **kwargs)
            flash("Only admin can access the page you requested")
            return redirect(url_for("dashboard"))
        flash("Only admin can access the page you requested")
        return redirect(url_for("login"))

    inner.__name__ = view.__name__
    return inner


def active_account_required(view):
    def inner(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.state == "active":
                return view(*args, **kwargs)
            flash("Your account is not active, please contact the admin")
            return redirect(url_for("contact"))
        flash("You have to login first")
        return redirect(url_for("login"))

    inner.__name__ = view.__name__
    return inner


def shop_owner_required(view):
    def inner(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.role == "shop_owner":
                if current_user.state == "active":
                    return view(*args, **kwargs)
                flash("Your account is not active, please contact the admin")
                return redirect(url_for("contact"))
            flash("Only A Shop Owner can access the page you requested")
            return redirect(url_for("dashboard"))
        flash("Only A Shop Owner can access the page you requested")
        return redirect(url_for("login"))

    inner.__name__ = view.__name__
    return inner
