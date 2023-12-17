from flask import render_template

from myapp import app, db


@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html", error=error), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("500.html", error=error), 500