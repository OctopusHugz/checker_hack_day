#!/usr/bin/env python3
"""This module runs the gitcheck program"""
if __name__ == "__main__":
    from auth_test import settings_auth_test
    from task_corrections import request_correction
    settings_auth_test()
    request_correction()
