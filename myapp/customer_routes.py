import json
import os

import cachecontrol
import google.auth.transport.requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
import requests
from flask import abort, redirect, render_template, request, session, url_for
from google.oauth2 import id_token
from myapp import app, db
from myapp.forms import RegisterCustomerForm
from myapp.models import Customer, Store

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

client_secrets_file = "google-api-credentials.json"

with open(client_secrets_file) as file:
    data = json.load(file)

GOOGLE_CLIENT_ID = data["web"]["client_id"]

# Create an oauthlib flow object that will handle the talking between our app and Google API
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    client_secrets_file,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
    ],
)

flow.redirect_uri = "http://127.0.0.1:5000/google/callback"  # "https://goldenopinions.duckdns.org/google/callback"
if app.config["ENVIRONMENT"] == "production":
    flow.redirect_uri = "https://goldenopinions.duckdns.org/google/callback"


# Login page
@app.route("/google/login")
def google_login():
    if "store_id" not in session:
        abort(403)
    if "customer_google_account_id" in session:
        return redirect(url_for("give_review", store_id=session["store_id"]))
    else:
        authorization_url, state = flow.authorization_url()
        session["state"] = state
        return redirect(authorization_url)


# Callback to execute after the user authenticates
@app.route("/google/callback")
def google_callback():
    # Fetch an identification token
    flow.fetch_token(authorization_response=request.url)

    # Abort if intercepted
    if not session["state"] == request.args["state"]:
        abort(500)

    # Retrieve user info from obtained credentials
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token, request=token_request, audience=GOOGLE_CLIENT_ID
    )

    # Store user info into current session
    session["customer_google_account_id"] = id_info.get("sub")
    session["customer_name"] = id_info.get("name")
    session["customer_email"] = id_info.get("email")
    return redirect(url_for("give_review", store_id=session["store_id"]))


# Logout page
@app.route("/google/logout")
def google_logout():
    if "store_id" not in session:
        abort(403)
    del session["customer_google_account_id"]
    del session["customer_name"]
    del session["customer_email"]
    return redirect(url_for("google_login"))


@app.route("/store/<store_id>/review")
def give_review(store_id):
    store = db.session.get(Store, store_id)
    session["store_id"] = store_id
    if store:
        if "customer_google_account_id" in session and "customer_email" in session:
            customer = db.session.scalar(
                db.select(Customer).filter_by(email=session["customer_email"])
            )
            if customer:
                return render_template(
                    "give_review.html", customer=customer, store=store
                )
            else:
                return redirect(url_for("registercustomer", store_id=store_id))
        else:
            return redirect(url_for("google_login"))
    else:
        abort(404)


@app.route("/store/<store_id>/register", methods=["GET", "POST"])
def registercustomer(store_id):
    store = db.session.get(Store, store_id)
    if store:
        if "customer_name" in session:
            customer = db.session.scalar(
                db.select(Customer).filter_by(email=session["customer_email"])
            )
            if customer:
                return redirect(url_for("give_review", store_id=store_id))
            else:
                form = RegisterCustomerForm()
                if form.validate_on_submit():
                    customer = Customer(
                        email=form.email.data,
                        name=form.name.data,
                        phone_number=form.phone_number.data,
                        account_id=session["customer_google_account_id"],
                    )
                    db.session.add(customer)
                    store.customers.append(customer)
                    db.session.commit()
                    return redirect(url_for("give_review", store_id=store_id))
                return render_template(
                    "registercustomer.html", store=store, session=session, form=form
                )
        else:
            return redirect(url_for("google_login"))
    else:
        abort(404)


@app.route("/review_url/<store_id>")
def review_url(store_id):
    store = db.session.get(Store, store_id)
    if store:
        url = f"https://search.google.com/local/writereview?placeid={store.place_id}"
        return redirect(url)
    else:
        abort(404)
