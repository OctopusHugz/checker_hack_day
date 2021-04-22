#!/usr/bin/env python3
from os import getcwd, path
from projects import (low_list, high_list, sedo_list,
                      interview_list, web_front_end_list, web_back_end_list)


def pid_from_cwd():
    """Returns a project's ID based on the current working directory"""
    cwd = path.basename(getcwd())
    projects = {
        "low": low_list,
        "high": high_list,
        "sedo": sedo_list,
        "interview": interview_list,
        "web_front_end": web_front_end_list,
        "web_back_end": web_back_end_list
    }
    all_projects = list(projects.values())
    # all projects is list of list of dicts where each dict is a project
    for track in all_projects:
        # track is a list of dicts where each dict is a project in that track
        for project in track:
            project_dir = list(project.values())[0]
            project_id = list(project.keys())[0]
            if cwd == project_dir:
                return project_id


def parent_from_cwd():
    """Returns the parent directory based on the current working directory"""
    parent = getcwd().split('/')[-2]
    return parent
