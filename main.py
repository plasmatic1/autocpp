import moss as pymoss
import requests
import time
import os
from lang_map import get_ext, get_moss_lang
from settings import MOSS_ID, DMOJ_HANDLE, DMOJ_URL, MODE, TARGET_HANDLE, PROBLEM_ID, PROBLEM_CHECK_COUNT, \
    DMOJ_REQUEST_DELAY
from problem import get_solved, get_sub_src


def solved_list(user_id):
    return requests.get(f'{DMOJ_URL}api/user/info/{user_id}').json()['solved_problems']


def check_problem(problem_id):
    print(f'Checking problem {problem_id}...')
    subs = get_solved(problem_id)
    target_sub_id = None
    target_lang = None

    # Make subs directory
    if not os.path.exists('subs'):
        os.mkdir('subs')

    # Get target submission
    for sub_id, user_id, lang in subs:
        if user_id == TARGET_HANDLE:
            target_sub_id = sub_id
            target_lang = lang
            with open(f'subs/target_src.{get_ext(lang)}', 'w') as f:
                f.write(get_sub_src(sub_id))
            time.sleep(DMOJ_REQUEST_DELAY)

            print(f'Got submission source of target: {sub_id} in {lang}')
            break

    if not target_lang:
        raise ValueError(f'Could not find Accepted submission for {problem_id}')

    # Get submission ids of other users
    other_ids = []
    for sub_id, user_id, lang in subs:
        if user_id != TARGET_HANDLE and lang == target_lang:
            with open(f'subs/{sub_id}_src.{get_ext(target_lang)}', 'w') as f:
                f.write(get_sub_src(sub_id))
            time.sleep(DMOJ_REQUEST_DELAY)
            other_ids.append(sub_id)

            print(f'Got accepted submission source: {sub_id} by {user_id}')

    # MOSS
    print()
    moss = pymoss.MOSS(MOSS_ID, get_moss_lang(target_lang), matching_file_limit=2500)
    moss.add_file_from_disk(f'subs/target_src.{get_ext(target_lang)}', display_name='target_submission')
    for sub_id in other_ids:
        moss.add_file_from_disk(f'subs/{sub_id}_src.{get_ext(target_lang)}', display_name=sub_id)

    print('Sending MOSS query...')
    url = moss.process()
    print(f'Report URL: {url}')
    report_path = f'subs/{problem_id}_report.html'
    print(f'Saved report to {report_path}')


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
