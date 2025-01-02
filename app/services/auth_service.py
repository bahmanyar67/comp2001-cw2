from flask import current_app
import requests
from app.models import User
from app import flask_app_instance


def basic_auth_wrapper(username, password):
    # Ensure the function runs in an app context
    with flask_app_instance.app_context():
        return basic_auth(username, password)


def basic_auth(username, password):
    # Check if the user exists in the database
    user = User.query.filter_by(user_email=username).first()
    if user is None:
        print("User not found")
        return None

    # Check authentication API
    if authenticate_api(username, password):
        return {"sub": username, "role": user.user_role}
    else:
        return None


def authenticate_api(username, password):
    auth_url = 'https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users'

    credentials = {
        'email': username,
        'password': password
    }

    response = requests.post(auth_url, json=credentials)

    if response.status_code == 200:
        try:
            json_response = response.json()
            if json_response[0] == 'Verified' and json_response[1] == 'True':
                return True
            else:
                print("Authentication failed:", json_response)
                return False
        except requests.JSONDecodeError:
            print("Response is not valid JSON. Raw response content: ")
            return False
    else:
        print(f"Authentication failed with status code {response.status_code}")
        return False
