#!/usr/bin/python3
import requests
from sys import argv

project_id = argv[1]
task_id = argv[2]
auth_token = argv[3]
checks_list = []
check_dict = {}
count = 0
task_url = 'https://intranet.hbtn.io/projects/{}.json?auth_token={}'.format(
    project_id, auth_token)
payload = {'Content-Type': 'application/json'}
project = requests.get(task_url, params=payload).json()
tasks = project.get('tasks')
correction_res_list = []
for task in tasks:
    position = str(task.get('position'))
    task_file = task.get('github_file')
    if position == task_id:
        correction_url = 'https://intranet.hbtn.io/tasks/{}/start_correction.json?auth_token={}'.format(
            task.get('id'), auth_token)
        correction_res_id = requests.post(
            correction_url, params=payload).json().get('id')
        print(correction_res_id)
        correction_res_list.append(correction_res_id)
    for cor_id in correction_res_list:
        correction_result_url = 'https://intranet.hbtn.io/correction_requests/{}.json?auth_token={}'.format(cor_id, auth_token)
        correction_result = requests.get(correction_result_url, params=payload).json()
        checks_list = correction_result.get('result_display').get('checks')
        print(checks_list)
        for check in checks_list:
            label = check.get('check_label')
            passed = check.get('passed')
            check_dict.update({label + '_check ' + str(count) : passed})
            count += 1
        print(check_dict)
        if False in check_dict.values():
            print("You've made some mistakes in {}, but that's ok. We can fix them together!".format(
                task.get('title')))
        else:
            print("Good job, you've passed all the checks for: {}. {}!".format(position,
                task.get('title')))
        correction_res_list.remove(cor_id)
