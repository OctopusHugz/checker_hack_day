#!/usr/bin/python3
# from projects import pid_from_cwd
import requests
from sys import argv
from os import path
from settings import auth_token


# project_id = pid_from_cwd()
task_url = 'https://intranet.hbtn.io/projects/281.json?auth_token={}'.format(auth)
payload = {'Content-Type': 'application/json'}
project = requests.get(task_url, params=payload).json()
tasks = project.get('tasks')
# mand_tasks = {}
# adv_tasks = {}
# correction_res_list = []
# checks_dict = {}
# count = 0
# for task in tasks:
#     task_id = task.get('id')
#     task_file = task.get('github_file')
#     if task.get('position') < 100:
#         mand_tasks.update({task_id: task_file})
#     else:
#         adv_tasks.update({task_id: task_file})
# for t_id in mand_tasks.keys():
#     correction_url = 'https://intranet.hbtn.io/tasks/{}/start_correction.json?auth_token={}'.format(
#         t_id, auth_token)
#     correction_res_id = requests.post(
#         correction_url, params=payload).json().get('id')
#     correction_res_list.append(correction_res_id)
# for cor_id in correction_res_list:
#     correction_result_url = 'https://intranet.hbtn.io/correction_requests/{}.json?auth_token={}'.format(cor_id,
#                                                                                                         auth_token)
#     correction_result = requests.get(
#         correction_result_url, params=payload).json()
#     checks_dict.update(
#         {task_id: correction_result.get('result_display').get('checks')})
# print(checks_dict)
# for check in checks_list:
#     label = check.get('check_label')
#     passed = check.get('passed')
#     check_dict.update({label + '_check ' + str(count) : passed})
#     count += 1


# if False in check_dict.values():
#     print("You've made some mistakes, but that's ok. We can fix them together!")
# else:
#     print("Good job, you've passed all the checks for: {}!".format(tasks[0].get('title')))
