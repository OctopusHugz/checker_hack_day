#!/usr/bin/env python3
from setup import setup_func
from os import path
import requests
auth_url = 'https://intranet.hbtn.io/users/auth_token.json'


def settings_auth_test():
    from settings import settings_path
    """Checks for settings file and runs tests to see if auth_token is valid"""
    if not path.exists(settings_path):
        setup_func()
    authorized = check_auth()
    if authorized:
        return True
    else:
        print('Unauthorized request. Getting new auth_token now...')
        try:
            setup_func()
            print('New auth_token stored successfully!')
            authorized = check_auth()
            if authorized:
                return True
        except Exception:
            print("Failed auth test! Double check config and try again!")
            return False


def check_auth():
    """Check if auth_token is valid or not"""
    try:
        from settings import auth_token
    except Exception:
        return 0
    payload = {'Content-Type': 'application/json'}
    url = 'https://intranet.hbtn.io/users/me.json?auth_token={}'.format(
        auth_token)
    response = requests.get(url, params=payload)
    if response.status_code != 200:
        return 0
    return 1


def get_auth(api_key="", email="", pwd=""):
    """Given Holberton credentials, returns an auth_token"""
    if not api_key or not email or not pwd:
        from settings import api_key, email, pwd
    holb_creds = {"api_key": api_key, "email": email,
                  "password": pwd, "scope": "checker"}
    return requests.post(
        auth_url, params=holb_creds).json().get('auth_token')
