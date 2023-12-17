from flask import flash, redirect, url_for
from flask_login import current_user


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
