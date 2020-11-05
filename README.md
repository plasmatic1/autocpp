# autocpp

DM::OJ automatic copy paste police service!

## Background

Ever since the introduction of points to DM::OJ. it has had an issue with code copiers who use publically available solution repositories.  This tool attempts to address that issue by using Stanford MOSS to help find copied code.

## Steps

1. Register with MOSS and get your user ID
2. Create a DM::OJ API key
3. Run `pip install -r requirements.txt` to install the necessary python packages
4. Create a `settings.py` in the same directory as `main.py`, check the section below for the content of the settings file
5. Run `main.py`
6. :)

## Configuration

Here is a sample `settings.py`.  Aside from the `DMOJ_API_KEY` and `MOSS_ID` keys (which must be changed), other options can be left intact (though `TARGET_HANDLE`, `MODE`, `PROBLEM_ID`, and `PROBLEM_CHECK_COUNT` should also be changed).

```python
# Authentication
DMOJ_URL = 'https://dmoj.ca/'  # Base URL for DM::OJ.  Change this if you're checking a DM::OJ derivative (i.e. MCPT)
DMOJ_HANDLE = 'Plasmatic'  # Your DM::OJ username.  This will help the tool determine which problems are accessible (can have sources downloaded).  Currently, the tool only checks problems both you and the target have already solved
DMOJ_API_KEY = 'put_your_token_here'  # Your DM::OJ API key, this can be found at the bottom of your profile
MOSS_ID = 987654321  # Your MOSS user id

# Who to target
TARGET_HANDLE = 'SpontaneousCombustion'  # The target user
MODE = 'problem'  # Set to 'problem' to only check one problem, set to 'user' to check all problems solved by a user from highest points to lowest points
PROBLEM_ID = 'dmpg15g3'  # If MODE == 'problem', this is the id of the problem that will be checked
PROBLEM_CHECK_COUNT = 20  # If MODE == 'user', this is the number of problems to check from the target user (i.e. setting this option to 20 means that the 20 highest point problems of the target user will be checked)
# If MODE == 'problem', then PROBLEM_CHECK_COUNT does not need to bet set, and if MODE == 'user', then PROBLEM_ID does not need to be set
# Note: if you want to check all problems, just set PROBLEM_CHECK_COUNT to int(2e9) or similar

# Misc
SAVED_DATA_DIR = 'subs'  # Where the retrieved data will be saved.  This includes MOSS reports and submission sources
DMOJ_REQUEST_DELAY = 2.  # DM::OJ has a cloudflare system that flags your ip if you send more than 100 requests/minute.  A delay of DMOJ_REQUEST_DELAY seconds will be put between requests to the DMOJ website to prevent your ip from being flagged
MOSS_THRESHOLD = 0.8  # (TO BE IMPLEMENTED) Threshold for submissions to be flagged as suspicious.  If two submissions are matching by >=MOSS_THRESHOLD, then the submissions ids will be flagged and outputted.
LOG_FILE = 'log.txt'
SUSPICIOUS_SUBS_FILE = 'suspicious.txt'
MAX_THREADS = 1
```

# TODO

* Update requirements.txt if needed
* Customize where the submissions are downloaded to
* Parse the MOSS report for "most" copied submissions
* Check if the user is an admin account, and if so, don't limit problems being checked to solved problems
* Documentation :p
* Update with DMOJ APIv2 when it's ready
