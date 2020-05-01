import time
from queue import Queue
from threading import Thread

import requests

from log import log
from moss_parser import MossInteractor
from problem import download_subs
from settings import DMOJ_HANDLE, DMOJ_URL, MODE, TARGET_HANDLE, PROBLEM_ID, PROBLEM_CHECK_COUNT, \
    DMOJ_REQUEST_DELAY, MAX_THREADS


def solved_list(user_id):
    return requests.get(f'{DMOJ_URL}api/user/info/{user_id}').json()['solved_problems']


# Driver Code
moss_queue = Queue()
threads = []


def moss_query_runner():
    info = moss_queue.get()
    while info != -1:
        query_helper = MossInteractor(*info)
        log.log(f'Processing query for problem {info.problem_id}')
        query_helper.send_moss_query()
        if query_helper.report_exists():
            query_helper.parse_report()
        else:
            log.log(f'Report for problem {info.problem_id} not found')
        info = moss_queue.get()


def check_problem(problem_id):
    log.log(f'Checking problem {problem_id}...')
    info = download_subs(TARGET_HANDLE, problem_id)
    if info:
        moss_queue.put(info)


# Run Main

if __name__ == '__main__':
    # Init threads
    for i in range(MAX_THREADS):
        log.log(f'Initializing thread #{i}')
        th = Thread(target=moss_query_runner)
        th.start()
        threads.append(th)

    # Problem stuff
    if MODE == 'problem':
        check_problem(PROBLEM_ID)
    elif MODE == 'user':
        log.log(f'Checking {PROBLEM_CHECK_COUNT} highest point problems of user {TARGET_HANDLE}...')
        log.log('Note that only problems you already solved will be considered')

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
        log.log(f'Problems being checked: {solved}')
        log.log()
        for problem_id in solved:
            check_problem(problem_id)
            log.log()
    else:
        raise ValueError(f'Invalid mode {MODE} (Only [user, problem] are accepted')

    # Kill and wait for threads
    for i in range(MAX_THREADS):
        moss_queue.put(-1)  # Signals to threads that no more events are needed
    for thread in threads:
        log.log(f'Waiting for thread {thread.name} to terminate')
        thread.join()
        log.log(f'Thread {thread.name} terminated')

    # Close log files
    log.close_streams()
