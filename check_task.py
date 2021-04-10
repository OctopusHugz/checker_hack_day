#!/usr/bin/env python3
"""This module runs the gitcheck program"""
if __name__ == "__main__":
    from auth_test import settings_auth_test
    authorized = settings_auth_test()
    if authorized:
        from task_corrections import request_correction
        request_correction()
