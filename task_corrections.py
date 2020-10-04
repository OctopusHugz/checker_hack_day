#!/usr/bin/env python3
from cwd import pid_from_cwd
from sys import argv
from settings import auth_token
import requests
import time
from colorama import Fore, init
checks_dict = {}
payload = {'Content-Type': 'application/json'}
init(autoreset=True)


def request_correction():
    """Requests a correction given a task ID"""
    project_id = pid_from_cwd()
    task_url = 'https://intranet.hbtn.io/projects/{}.json?auth_token={}'.format(project_id,
                                                                                auth_token)
    project = requests.get(task_url, params=payload).json()
    tasks = project.get('tasks')
    if not tasks:
        print('Something went wrong...Please try again')
        exit(1)
    task_list = []
    for task in tasks:
        task_id = task.get('id')
        task_file = task.get('github_file')
        task_position = task.get('position')
        if task_position < 100:
            task_position -= 1
        task_list.append(task)
        if task_file in argv:
            correction_url = 'https://intranet.hbtn.io/tasks/{}/start_correction.json?auth_token={}'.format(
                task_id, auth_token)
            correction_res_id = requests.post(
                correction_url, params=payload).json().get('id')
            if not correction_res_id:
                print('Too many requests...Please respect the rate limits!')
                exit(1)
            print("Waiting on correction result for task: " + Fore.BLUE + "{}. {}".format(
                task_position, task.get('title')))
            correction_result_url = 'https://intranet.hbtn.io/correction_requests/{:d}.json?auth_token={}'.format(
                correction_res_id, auth_token)
            update_checks_dict(correction_result_url, task_id)
    if len(argv) == 1:
        for task in task_list:
            task_id = task.get('id')
            task_file = task.get('github_file')
            task_position = task.get('position')
            if task_position < 100:
                task_position -= 1
            correction_url = 'https://intranet.hbtn.io/tasks/{}/start_correction.json?auth_token={}'.format(
                task_id, auth_token)
            correction_res_id = requests.post(
                correction_url, params=payload).json().get('id')
            if not correction_res_id:
                print('Too many requests...Please respect the rate limits!')
                exit(1)
            print("Waiting on correction result for task: " + Fore.BLUE + "{}. {}".format(
                task_position, task.get('title')))
            correction_result_url = 'https://intranet.hbtn.io/correction_requests/{:d}.json?auth_token={}'.format(
                correction_res_id, auth_token)
            update_checks_dict(correction_result_url, task_id)


def update_checks_dict(correction_result_url, task_id):
    check_dict = {}
    req_dict = {}
    code_dict = {}
    count = 0
    correction_result = requests.get(
        correction_result_url, params=payload).json()
    status = correction_result.get('status')
    while status == 'Sent':
        time.sleep(2.5)
        correction_result = requests.get(
            correction_result_url, params=payload).json()
        status = correction_result.get('status')
    checks = correction_result.get('result_display').get('checks')
    checks_dict.update({task_id: checks})
    for check in checks:
        label = check.get('check_label')
        passed = check.get('passed')
        title = check.get('title')
        if label == 'requirement':
            req_dict.update(
                {label + '_' + title.lower().replace(' ', '_'): passed})
        else:
            code_dict.update(
                {label + '_' + title.lower().replace(' ', '_'): passed})
        check_dict.update({label + '_check ' + str(count): passed})
        count += 1
    req_dict_passed = list(req_dict.values()).count(True)
    code_dict_passed = list(code_dict.values()).count(True)
    if req_dict_passed == len(req_dict):
        req_color = Fore.GREEN
    else:
        req_color = Fore.RED
    if code_dict_passed == len(code_dict):
        code_color = Fore.GREEN
    else:
        code_color = Fore.RED
    print(req_color +
          'Requirement Checks: {:d}/{:d}'.format(req_dict_passed, len(req_dict)))
    print(code_color +
          'Code Checks: {:d}/{:d}'.format(code_dict_passed, len(code_dict)))
