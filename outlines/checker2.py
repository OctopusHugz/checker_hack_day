#!/usr/bin/python3
import requests
from sys import argv
from os import path


# def check_auth():
#     """Check if auth_token is valid or not. If invalid, get a new auth_token and write to settings.py"""
#     try:
#         from settings import auth_token
#     except:
#         return 0
#     payload = {'Content-Type': 'application/json'}
#     url = 'https://intranet.hbtn.io/users/me.json?auth_token={}'.format(
#         auth_token)
#     response = requests.get(url, params=payload)
#     if response.status_code != 200:
#         return 0
#     return 1


# if path.exists('settings.py'):
#     print('We have settings!')
#     from settings import email
#     from settings import pwd
#     from settings import api_key
#     from settings import auth_token
# else:
#     with open('settings.py', 'w') as f:
#         f.write('# !/usr/bin/env python3\n')
#         email = input('Enter Holberton email: ')
#         f.write('email = "' + email + '"\n')
#         pwd = input('Enter Holberton password: ')
#         f.write('pwd = "' + pwd + '"\n')
#         api_key = input('Enter Holberton API key: ')
#         f.write('api_key = "' + api_key + '"\n')
#     authorized = check_auth()
#     if not authorized:
#         print('Not authorized. Getting auth_token now...')
#         with open('settings.py', 'a') as f:
#             auth_url = 'https://intranet.hbtn.io/users/auth_token.json'
#             holb_creds = {"api_key": api_key, "email": email, "password": pwd, "scope": "checker"}
#             auth_token = requests.post(auth_url, params=holb_creds).json().get('auth_token')
#             f.write('auth_token = "' + auth_token + '"\n')
project_id = argv[1]
auth_token = argv[2]
task_url = 'https://intranet.hbtn.io/projects/{}.json?auth_token={}'.format(
    project_id, auth_token)
payload = {'Content-Type': 'application/json'}
project = requests.get(task_url, params=payload).json()
tasks = project.get('tasks')
print(tasks)
mand_tasks = {}
adv_tasks = {}
correction_res_list = []
checks_dict = {}
count = 0
for task in tasks:
    task_id = task.get('id')
    task_file = task.get('github_file')
    if task.get('position') < 100:
        mand_tasks.update({task_id: task_file})
    else:
        adv_tasks.update({task_id: task_file})
for t_id in mand_tasks.keys():
    correction_url = 'https://intranet.hbtn.io/tasks/{}/start_correction.json?auth_token={}'.format(
        t_id, auth_token)
    correction_res_id = requests.post(
        correction_url, params=payload).json().get('id')
    correction_res_list.append(correction_res_id)
for cor_id in correction_res_list:
    correction_result_url = 'https://intranet.hbtn.io/correction_requests/{}.json?auth_token={}'.format(cor_id,
                                                                                                        auth_token)
    correction_result = requests.get(
        correction_result_url, params=payload).json()
    print(correction_result)
    tid = correction_result.get('task_id')
    checks = correction_result.get('result_display').get('checks')
    checks_dict.update(
        {tid: checks})
print(checks_dict)
# for check in checks_list:
#     label = check.get('check_label')
#     passed = check.get('passed')
#     check_dict.update({label + '_check ' + str(count) : passed})
#     count += 1


if False in check_dict.values():
    print("You've made some mistakes, but that's ok. We can fix them together!")
else:
    print("Good job, you've passed all the checks for: {}!".format(tasks[0].get('title')))
