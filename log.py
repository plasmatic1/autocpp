from settings import LOG_FILE, SUSPICIOUS_SUBS_FILE, SAVED_DATA_DIR, DMOJ_URL


def dmoj_sub_url(sub_id):
    return f'{DMOJ_URL}submission/{sub_id}/'


class Logger:
    def __init__(self):
        self.subs_file = None
        self.log_file = None

    def log(self, line):
        print(line)
        self.log_file.write(line + '\n')

    def add_sub(self, offending_sub_id, original_sub_id, match_amount, offending_user=False):
        """
        Adds a submission to list of offending submissions
        :param offending_sub_id: Id of the offending sub
        :param original_sub_id: Id of the original sub
        :param match_amount: The matching % (from moss).  This argument should be a float between 0 and 1
        :param offending_user: Leave this empty if the submission is from the target user.  This parameter should be specified only if the offending submission was from another user (discovered accidentally while MOSSing)
        :return: None
        """

        if offending_user:
            self.subs_file.write(f'other ({offending_user}) {match_amount}: {dmoj_sub_url(offending_sub_id)}, from {dmoj_sub_url(original_sub_id)}\n')
        else:
            self.subs_file.write(f'MATCH {match_amount}: {dmoj_sub_url(offending_sub_id)}, from {dmoj_sub_url(original_sub_id)}\n')

    def __enter__(self):
        self.subs_file = open(f'{SAVED_DATA_DIR}/{SUSPICIOUS_SUBS_FILE}')
        self.log_file = open(f'{SAVED_DATA_DIR}/{LOG_FILE}')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.subs_file.close()
        self.log_file.close()
