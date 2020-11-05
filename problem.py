import os.path
import re
import time
from collections import namedtuple

import requests
from bs4 import BeautifulSoup

from lang_map import get_ext
from log import log
from moss_parser import problem_path, target_src_path, other_src_path
from settings import DMOJ_URL, DMOJ_API_KEY, DMOJ_REQUEST_DELAY, SAVED_DATA_DIR

Submission = namedtuple('Submission', 'sub_id user_id lang')
ProblemSubmissions = namedtuple('ProblemSubmissions', 'problem_id lang target_sub_id other_sub_ids sub_map')

dmoj_auth_header = {'Authorization': f'Bearer {DMOJ_API_KEY}'}


def get_solved_page(problem_id, page_no):
    """
    Parses a problem rank page and returns a list of accepted submissions along with the user that solved them
    :param problem_id: The problem id to parse
    :param page_no: The page to check
    :return:
    """

    def regex_find_href(tag, exp):
        return re.search(exp, tag.find('a', {'href': re.compile(exp)})['href'])

    res = requests.get(f'{DMOJ_URL}problem/{problem_id}/rank/{page_no}', headers=dmoj_auth_header)
    if res.status_code == 404:
        return []
    else:
        soup = BeautifulSoup(res.text, 'html.parser')
        subs = []
        for tag in soup.find_all('div', {'class': 'submission-row'}):
            if 'AC' in tag.find('div', {'class': 'sub-result'})['class']:  # Fake AC is not counted
                user_id = regex_find_href(tag, r'/user/(\w+)').group(1)
                sub_id = regex_find_href(tag, r'/submission/(\d+)').group(1)
                lang = tag.find('span', {'class': 'language'}).text
                subs.append(Submission(sub_id, user_id, lang))

        return subs  # Return nothing if subs is empty


def get_solved(problem_id):
    """
    Returns a list of submissions for a problem
    :param problem_id: The problem to check
    :return: A list of Submission objects
    """

    log.log(f'Getting best submissions for {problem_id}')

    subs = []
    page_no = 1
    cur_subs = get_solved_page(problem_id, page_no)
    time.sleep(DMOJ_REQUEST_DELAY)
    while cur_subs:
        subs.extend(cur_subs)
        log.log(f'Parsed page {page_no}, got {len(cur_subs)} submission ids')

        page_no += 1
        cur_subs = get_solved_page(problem_id, page_no)
        time.sleep(DMOJ_REQUEST_DELAY)

    return subs


def download_subs(target_handle, problem_id):
    """
    Downloads all accepted submissions for a problem that match the language used by a given target user.  Downloaded submissions will be in the folder ./SAVED_DATA_DIR/problem_id where SAVED_DATA_DIR is from configuration and `problem_id` is the parameter

    Additionally, this procedure assumes that user DMOJ_HANDLE has access to this problem's sources (either solved it already or is an Admin)
    :param target_handle: Only submissions with the same language as the target will be downloaded
    :param problem_id: The id of the problem to download submissions from
    :return: A ProblemSubmissions object, or None if an error occured
    """

    subs = get_solved(problem_id)
    target_sub_id = None
    target_lang = None

    # Make subs directory
    if not os.path.exists(SAVED_DATA_DIR):
        os.mkdir(SAVED_DATA_DIR)
    if not os.path.exists(problem_path(problem_id)):
        os.mkdir(problem_path(problem_id))

    # Submission map - maps submission id to handle
    sub_map = {}

    # Get target submission
    for sub_id, user_id, lang in subs:
        if user_id == target_handle:
            target_sub_id = sub_id
            target_lang = lang
            with open(target_src_path(problem_id, get_ext(lang)), 'w', encoding='utf8') as f:
                f.write(get_sub_src(sub_id))
            time.sleep(DMOJ_REQUEST_DELAY)

            log.log(f'Got submission source of target: {sub_id} in {lang}')
            sub_map[sub_id] = target_handle
            break

    if not target_lang:
        log.log(f'ERROR: Could not find Accepted submission for {problem_id}')

    # Get submission ids of other users
    other_ids = []
    target_lang_ext = get_ext(target_lang)
    if not target_lang_ext:
        log.log(f'ERROR: Language {target_lang} currently not supported')
        return None

    for sub_id, user_id, lang in subs:
        if user_id != target_handle and get_ext(lang) == target_lang_ext: # Use extension instead of DMOJ language so Java8/9/10/11 are grouped
            with open(other_src_path(problem_id, target_lang_ext, sub_id), 'w', encoding='utf8') as f:
                f.write(get_sub_src(sub_id))
            time.sleep(DMOJ_REQUEST_DELAY)
            other_ids.append(sub_id)

            log.log(f'Got accepted submission source: {sub_id} by {user_id}')
            sub_map[sub_id] = user_id

    return ProblemSubmissions(problem_id, target_lang, target_sub_id, other_ids, sub_map)


def get_user_subs(user_id):
    """
    Returns all submissions made by a user
    :param user_id: The DMOJ handle of the user
    :return: A list of submissions, in the DMOJ APIv2 format
    """

    return requests.get(f'{DMOJ_URL}api/v2/submissions?user={user_id}').json()


def get_sub_src(sub_id):
    """
    Returns the source code of a submission.  This assumes DMOJ_HANDLE has access to this submission already.
    :param sub_id: The id of the submission to download
    :return: Returns the source code of the submission
    """
    return requests.get(f'{DMOJ_URL}src/{sub_id}/raw', headers=dmoj_auth_header).text.replace('\r', '')
