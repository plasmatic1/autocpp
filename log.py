from collections import namedtuple
from threading import current_thread

from settings import LOG_FILE, SUSPICIOUS_SUBS_FILE, SAVED_DATA_DIR, DMOJ_URL


def dmoj_sub_url(sub_id):
    return f'{DMOJ_URL}submission/{sub_id}/'


OffendingSubmissions = namedtuple('OffendingSubmissions',
                                  'offending_sub_id original_sub_id match_amount offending_user')


class Logger:
    def __init__(self):
        self.subs_file = open(f'{SAVED_DATA_DIR}/{SUSPICIOUS_SUBS_FILE}', 'w')
        self.log_file = open(f'{SAVED_DATA_DIR}/{LOG_FILE}', 'w')

    def close_streams(self):
        self.subs_file.close()
        self.log_file.close()

    def log(self, line):
        log_line = f'[t:{current_thread().name}] ' + line
        print(log_line)
        self.log_file.write(log_line + '\n')

    def add_sub(self, offending_sub_id, original_sub_id, match_amount, offending_user=None):
        """
        Adds a submission to list of offending submissions
        :param offending_sub_id: Id of the offending sub
        :param original_sub_id: Id of the original sub
        :param match_amount: The matching % (from moss).  This argument should be a float between 0 and 1
        :param offending_user: Leave this empty if the submission is from the target user.  This parameter should be specified only if the offending submission was from another user (discovered accidentally while MOSSing)
        :return: None
        """

        if offending_user:
            log_line = f'other ({offending_user}) {match_amount}: {dmoj_sub_url(offending_sub_id)}, from {dmoj_sub_url(original_sub_id)}'
        else:
            log_line = f'MATCH {match_amount}: {dmoj_sub_url(offending_sub_id)}, from {dmoj_sub_url(original_sub_id)}'

        self.subs_file.write(log_line + '\n')
        self.log(log_line)

    def add_problem(self, problem_id, subs):
        """
        Logs a list of offending submissions for a problem
        :param problem_id: Id of the problem
        :param subs: List of OffendingSubmissions objects
        :return: None
        """

        self.log(f'Found offending submissions of {problem_id}')
        self.subs_file.write(f'-- BEGIN PROBLEM: {problem_id}')
        for sub in sorted(subs, key=lambda sub: sub.offending_user or ''):
            self.add_sub(*sub)

