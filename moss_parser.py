import mosspy

from lang_map import get_moss_lang, get_ext
from settings import SAVED_DATA_DIR, MOSS_ID, MOSS_THRESHOLD
from bs4 import BeautifulSoup
import os.path
import re


def problem_path(problem_id):
    return f'{SAVED_DATA_DIR}/{problem_id}'


def report_path(problem_id):
    return f'{problem_path(problem_id)}/report.html'


def target_src_path(problem_id, lang_ext):
    return f'{problem_path(problem_id)}/target_src.{lang_ext}'


def other_src_path(problem_id, lang_ext, sub_id):
    return f'{problem_path(problem_id)}/{sub_id}_src.{lang_ext}'


class MossInteractor:
    def __init__(self, problem_id, lang, target_sub_id, other_sub_ids, thread_id):
        self.thread_id = thread_id
        self.problem_id = problem_id
        self.lang_ext = get_ext(lang)
        self.moss_lang = get_moss_lang(lang)
        self.target_sub_id = target_sub_id
        self.other_sub_ids = other_sub_ids

    def send_moss_query(self):
        moss = mosspy.Moss(MOSS_ID, self.moss_lang)
        moss.addFile(target_src_path(self.problem_id, self.lang_ext), 'target_submission')
        for sub_id in self.other_sub_ids:
            moss.addFile(other_src_path(self.problem_id, self.lang_ext, sub_id), sub_id)

        print('Sending MOSS query...')
        url = moss.send()
        print(f'Report URL: {url}')
        moss.saveWebPage(url, report_path(self.problem_id))
        print(f'Saved report to {report_path(self.problem_id)}')

    def report_exists(self):
        return os.path.exists(report_path(self.problem_id))

    def parse_report(self):
        """
        Parses the written MOSS report and logs any suspicious submissions.  This function assumes moss_send_query has already completed successfully
        :return:
        """

        def match_sub_id_and_prec(tag):
            match = re.search(r'(\d+) \((\d+)%\)', tag.text)
            return match.group(1), int(match.group(2)) / 100

        with open(report_path(self.problem_id)) as f:
            bs = BeautifulSoup(f.read(), 'html.parser')
            for row in bs.find_all('tr'):
                if row.find('th'):  # Header row
                    continue

                oth_sub = row.find_all('a', text=re.compile(r'\d+ '))
                target_sub = row.find_all('a', text=re.compile(r'target_submission'))

                if target_sub:
                    target_match = int(re.search(r'(\d+)%', target_sub[0].text).group(1)) / 100
                    other_id, _ = match_sub_id_and_prec(oth_sub[0])
                    if target_match >= MOSS_THRESHOLD:
                        print(target_match)
                        print(other_id)
                else:
                    other_id_1, other_match_1 = match_sub_id_and_prec(oth_sub[0])
                    other_id_2, _ = match_sub_id_and_prec(oth_sub[1])
                    if other_match_1 >= MOSS_THRESHOLD:
                        print(other_id_1, other_match_1)
                        print(other_id_2)

