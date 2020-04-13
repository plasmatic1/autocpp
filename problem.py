import re
import requests
import time
from bs4 import BeautifulSoup
from collections import namedtuple
from settings import DMOJ_URL, DMOJ_API_KEY, DMOJ_REQUEST_DELAY

Submission = namedtuple('Submission', 'sub_id user_id lang')

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
    print(f'Getting best submissions for {problem_id}')

    subs = []
    page_no = 1
    cur_subs = get_solved_page(problem_id, page_no)
    time.sleep(DMOJ_REQUEST_DELAY)
    while cur_subs:
        subs.extend(cur_subs)
        print(f'Parsed page {page_no}, got {len(cur_subs)} submission ids')

        page_no += 1
        cur_subs = get_solved_page(problem_id, page_no)
        time.sleep(DMOJ_REQUEST_DELAY)

    return subs


def get_user_subs(user_id):
    return requests.get(f'{DMOJ_URL}api/user/submissions/{user_id}').json()


def get_sub_src(sub_id):
    return requests.get(f'{DMOJ_URL}src/{sub_id}/raw', headers=dmoj_auth_header).text.replace('\r', '')
