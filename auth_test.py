#!/usr/bin/env python3
import requests
from os import path
auth_url = 'https://intranet.hbtn.io/users/auth_token.json'


def settings_auth_test():
    """Checks for settings file and runs tests to see if auth_token is valid"""
    if not path.exists('/home/vagrant/utils/checker_hack_day/settings.py'):
        create_settings_file()
    authorized = check_auth()
    if authorized:
        return True
    else:
        print('Unauthorized request. Getting new auth_token now...')
        auth_token = get_auth()
        create_settings_file(auth_token)
        print('New auth_token stored successfully!')
        return False


def check_auth():
    """Check if auth_token is valid or not"""
    try:
        from settings import auth_token
    except:
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


def create_settings_file(auth_token=""):
    """Sets Holberton credentials to settings.py file"""
    if not auth_token:
        email = input('Enter Holberton email: ')
        pwd = input('Enter Holberton password: ')
        api_key = input('Enter Holberton API key: ')
        auth_token = get_auth(api_key, email, pwd)
    else:
        from settings import api_key, email, pwd
    write_to_file(api_key, email, pwd, auth_token)


def write_to_file(api_key, email, pwd, auth_token):
    """Writes the Holberton credentials to settings.py file"""
    with open('/home/vagrant/utils/checker_hack_day/settings.py', 'w+') as f:
        f.write('#!/usr/bin/env python3\n')
        f.write('email = "' + email + '"\n')
        f.write('pwd = "' + pwd + '"\n')
        f.write('api_key = "' + api_key + '"\n')
        f.write('auth_token = "' + auth_token + '"\n')
