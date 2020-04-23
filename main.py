import time

import requests

from settings import DMOJ_HANDLE, DMOJ_URL, MODE, TARGET_HANDLE, PROBLEM_ID, PROBLEM_CHECK_COUNT, \
    DMOJ_REQUEST_DELAY
from problem import download_subs


def solved_list(user_id):
    return requests.get(f'{DMOJ_URL}api/user/info/{user_id}').json()['solved_problems']


def check_problem(problem_id):
    print(f'Checking problem {problem_id}...')
    info = download_subs(TARGET_HANDLE, problem_id)


if __name__ == '__main__':
    if MODE == 'problem':
        check_problem(PROBLEM_ID)
    elif MODE == 'user':
        print(f'Checking {PROBLEM_CHECK_COUNT} highest point problems of user {TARGET_HANDLE}...')
        print('Note that only problems you already solved will be considered')

        # Get list of problems
        problem_point_dict = dict(
            ((k, v['points']) for k, v in requests.get(f'{DMOJ_URL}api/problem/list').json().items()))
        time.sleep(DMOJ_REQUEST_DELAY)
        you_solved = set(solved_list(DMOJ_HANDLE))
        time.sleep(DMOJ_REQUEST_DELAY)
        solved = sorted(filter(lambda pid: pid in you_solved, solved_list(TARGET_HANDLE)),
                        key=lambda pid: -problem_point_dict[pid])[:PROBLEM_CHECK_COUNT]
        time.sleep(DMOJ_REQUEST_DELAY)

        # Check problem
        print(f'Problems being checked: {solved}\n')
        for problem_id in solved:
            check_problem(problem_id)
            print()
    else:
        raise ValueError(f'Invalid mode {MODE} (Only [user, problem] are accepted')
