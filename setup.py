#!/usr/bin/env python3
""" Setup script for the check_task program """


def setup_func():
    """ Imports variables or gets input from user to store in settings.py """
    from auth_test import get_auth
    try:
        from settings import api_key, email, pwd, check_task_dir, settings_path
        auth_token = get_auth(api_key, email, pwd)
    except Exception:
        from os import getcwd
        email = input('Enter Holberton email: ')
        pwd = input('Enter Holberton password: ')
        api_key = input('Enter Holberton API key: ')
        auth_token = get_auth(api_key, email, pwd)
        check_task_dir = getcwd()
        settings_path = check_task_dir + "/settings.py"
    finally:
        with open(settings_path, 'w+') as f:
            f.write('#!/usr/bin/env python3\n')
            f.write('check_task_dir = "' + check_task_dir + '"\n')
            f.write('settings_path = "' + settings_path + '"\n')
            f.write('email = "' + email + '"\n')
            f.write('pwd = "' + pwd + '"\n')
            f.write('api_key = "' + api_key + '"\n')
            f.write('auth_token = "' + auth_token + '"\n')


if __name__ == "__main__":
    setup_func()
