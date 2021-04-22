#!/usr/bin/env python3
from cwd import pid_from_cwd
from sys import argv
from settings import auth_token
from time import sleep
import requests
from colorama import Fore, init
checks_dict = {}
payload = {'Content-Type': 'application/json'}
init(autoreset=True)


def request_correction():
    """Requests a correction given a task ID"""
    if len(argv) > 2:
        print(Fore.RED + "Try running with no arguments, or a single task number!")
        exit(1)
    project_id = pid_from_cwd()
    if project_id is None:
        print(Fore.RED + "Whoops! No checker for you today. Try a manual review instead!")
        exit(1)
    task_url = 'https://intranet.hbtn.io/projects/{}.json?auth_token={}'.format(project_id,
                                                                                auth_token)
    project = requests.get(task_url, params=payload).json()
    tasks = project.get('tasks')
    if not tasks:
        print('Something went wrong...Please try again')
        exit(1)
    task_list = []
    task_files = []
    non_zero_start = False
    one_arg_given = True if len(argv) == 2 else False
    for task in tasks:
        task_list.append(task)
        task_files.append(task.get('github_file'))
    if one_arg_given:
        try:
            task_number = int(argv[1])
        except Exception:
            print(Fore.RED + "Try passing in a task number instead!")
            exit(1)
    checker_available_list = [task.get("checker_available") for task in tasks]
    if True not in checker_available_list:
        print(
            Fore.RED + 'This project has no checker. Please find a peer for a manual review!')
        exit(1)

    if task_list[0].get('position') != 0:
        non_zero_start = True

    if one_arg_given:
        if checker_available_list[task_number]:
            # try:
            correct_task(task_list[task_number].get("id"),
                         task_list[task_number].get("title"),
                         task_number)
            # except Exception:
            #     print(
            #         Fore.RED + "Looks like this task has no checker! Please find a peer for a manual review!")
        else:
            print(
                Fore.RED + "Looks like this task has no checker! Please find a peer for a manual review!")

    for task in task_list:
        task_id = task.get('id')
        task_title = task.get('title')
        task_position = task.get('position')
        if task_position < 100 and non_zero_start:
            task_position -= 1
        if len(argv) == 1 and task.get("checker_available"):
            correct_task(task_id, task_title, task_position)


def correct_task(task_id, task_title, task_position):
    correction_url = 'https://intranet.hbtn.io/tasks/{}/start_correction.json?auth_token={}'.format(
        task_id, auth_token)
    correction_res_id = requests.post(
        correction_url, params=payload).json().get('id')
    if not correction_res_id:
        # or could be manual review?!
        # breaking when running ct only and manual review in middle of autos?
        print('Too many requests...Please respect the rate limits!')
        exit(1)
    print("Waiting on correction result for task: " + Fore.BLUE + "{}. {}".format(
        task_position, task_title))
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
        # turn this sleep into async/await or something more robust?
        sleep(2)
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
    print(req_color + f'Requirement Checks: {req_dict_passed}/{len(req_dict)}')
    print(code_color + f'Code Checks: {code_dict_passed}/{len(code_dict)}')
