import google.oauth2.credentials
import google_auth_oauthlib.flow
import requests
from flask import Flask, session, abort, redirect, request
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests
import os
from models import User


# Initialize Flask app
app = Flask('Google Login')
app.secret_key = 'dev'
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


# Google API Client ID and client_secrets
GOOGLE_CLIENT_ID = '991740828482-gia7dp4kjbd107ipto7od9luup9eq4bg.apps.googleusercontent.com'
client_secrets_file = "/home/shanks31/Downloads/client_secret.json"


# Create an oauthlib flow object that will handle the talking between our app and Google API
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(\
        client_secrets_file,\
        scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"])

flow.redirect_uri = "http://127.0.0.1:5000/callback"


# Decorator to put before pages accessible to authenticated users only
def login_is_required(function):
    def wrapper_function(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        else: return function()

    return wrapper_function


# Login page
@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)


# Callback to execute after the user authenticates
@app.route("/callback")
def callback():
    # Fetch an identification token
    flow.fetch_token(authorization_response=request.url)

    # Abort if intercepted
    if not session['state'] == request.args['state']:
        abort(500)

    # Retrieve user info from obtained credentials
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token = credentials._id_token,
        request = token_request,
        audience = GOOGLE_CLIENT_ID
    )

    # Store user info into current session
    session['google_id'] = id_info.get('sub')
    session['name'] = id_info.get('name')
    
    return redirect('/protected_area')


# Take authenticated user to private space
@app.route("/protected_area")
@login_is_required
def protected_area():
    return f"<p>Welcome to Golden Opportunities, {session['name']}! <br/> <a href='/logout'> <button>Logout</button></a>"

# Logout page
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# Base route
# Omit in production
@app.route('/')
def index():
    return"<h1>LOGIN PAGE</h1><br><a href='/login'><button>Login</button></a>"


if __name__ == "__main__":
    app.run(debug=True)
