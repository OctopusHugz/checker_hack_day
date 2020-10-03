#!/usr/bin/env python3
from cwd import pid_from_cwd
from sys import argv
from settings import auth_token
import requests
checks_dict = {}
payload = {'Content-Type': 'application/json'}


def request_correction():
    """Requests a correction given a task ID"""
    project_id = pid_from_cwd()
    task_url = 'https://intranet.hbtn.io/projects/{}.json?auth_token={}'.format(project_id,
                                                                                auth_token)
    project = requests.get(task_url, params=payload).json()
    tasks = project.get('tasks')
    for task in tasks:
        task_id = task.get('id')
        task_file = task.get('github_file')
        if task_file in argv:
            correction_url = 'https://intranet.hbtn.io/tasks/{}/start_correction.json?auth_token={}'.format(
                task_id, auth_token)
            correction_res_id = requests.post(
                correction_url, params=payload).json().get('id')
            if not correction_res_id:
                print('Too many requests...please respect the rate limits!')
                exit(1)
            # correction_result_url = 'https://intranet.hbtn.io/correction_requests/{:d}.json?auth_token={}'.format(
            #     correction_res_id, auth_token)
            correction_result_url = 'https://intranet.hbtn.io/correction_requests/3592580.json?auth_token={}'.format(
                auth_token)
            update_checks_dict(correction_result_url, task_id)
    print(checks_dict)


def update_checks_dict(correction_result_url, task_id):
    print("Waiting on correction result...")
    correction_result = requests.get(
        correction_result_url, params=payload).json()
    checks = correction_result.get('result_display').get('checks')
    checks_dict.update({task_id: checks})
