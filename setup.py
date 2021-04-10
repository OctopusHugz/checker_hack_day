#!/usr/bin/env python3
""" Setup script for the check_task program """
from os import getenv
import re
import mmap


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
            f.write(f'check_task_dir = "{check_task_dir}"\n')
            f.write(f'settings_path = "{settings_path}"\n')
            f.write(f'email = "{email}"\n')
            f.write(f'pwd = "{pwd}"\n')
            f.write(f'api_key = "{api_key}"\n')
            f.write(f'auth_token = "{auth_token}"\n')
        home = getenv("HOME")
        need_to_write_alias = 1
        with open(f'{home}/.bashrc', "r+") as f:
            data = mmap.mmap(f.fileno(), 0).read()
            alias_exists = re.search('alias ct=', data.decode('utf-8'))
            if alias_exists is not None:
                need_to_write_alias = 0
        if need_to_write_alias:
            with open(f'{home}/.bashrc', "a") as f:
                f.write("\n# check_task aliases\n")
                f.write(f'alias ct="{check_task_dir}/check_task.py"\n')


if __name__ == "__main__":
    setup_func()
