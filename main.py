import requests
import time
import mosspy
from .lang_map import get_ext
from .settings import MOSS_ID, DMOJ_HANDLE, DMOJ_URL, MODE, TARGET_HANDLE, PROBLEM_ID, PROBLEM_CHECK_COUNT, DMOJ_REQUEST_DELAY
from problem import get_solved, get_sub_src


def solved_list(user_id):
    return requests.get(f'{DMOJ_URL}api/user/info/{user_id}').json()['solved_problems']


def check_problem(problem_id):
    print(f'Checking problem {problem_id}...\n')
    moss = mosspy.Moss(MOSS_ID)
    subs = get_solved(problem_id)
    target_lang = None

    # Get target submission
    for sub_id, user_id, lang in subs:
        if user_id == TARGET_HANDLE:
            target_lang = lang
            with open(f'subs/target_src.{get_ext(lang)}', 'w') as f:
                time.sleep(DMOJ_REQUEST_DELAY)
                f.write(get_sub_src(sub_id))

            print(f'Found target submission: {sub_id} in {lang}')
            break

    if not target_lang:
        raise ValueError(f'Could not find Accepted submission for {problem_id}')

    # Get submission ids of other users



if __name__ == '__main__':
    if MODE == 'problem':
        check_problem(PROBLEM_ID)
    elif MODE == 'user':
        print(f'Checking {PROBLEM_CHECK_COUNT} highest point problems of user {TARGET_HANDLE}...')
        print('Note that only problems you already solved will be considered')

        problem_point_dict = dict(
            ((k, v['points']) for k, v in requests.get(f'{DMOJ_URL}api/problem/list').json().items()))
        time.sleep(DMOJ_REQUEST_DELAY)
        you_solved = set(solved_list(DMOJ_HANDLE))
        time.sleep(DMOJ_REQUEST_DELAY)
        solved = sorted(filter(lambda pid: pid in you_solved, solved_list(TARGET_HANDLE)),
                        key=lambda pid: -problem_point_dict[pid])[:PROBLEM_CHECK_COUNT]

        print(f'Problems being checked: {solved}\n')
        for problem_id in solved:
            check_problem(problem_id)
    else:
        raise ValueError(f'Invalid mode {MODE} (Only [user, problem] are accepted')
