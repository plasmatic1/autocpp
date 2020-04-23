from settings import *
from threading import Thread, current_thread
import mosspy
import re
from bs4 import BeautifulSoup


# def f():
#     print('Ready to send moss query on', current_thread())
#     m = mosspy.Moss(MOSS_ID, 'cc')
#     m.addFile('subs/ccc14s5/155236_src.cpp')
#     m.addFile('subs/ccc14s5/169346_src.cpp')
#     print('Sending query...')
#     url = m.send()
#     print('Url:', url)
#
#
# for i in range(2):
#     t = Thread(target=f)
#     t.start()

def parse_report():
    def match_sub_id_and_prec(tag):
        match = re.search(r'(\d+) \((\d+)%\)', tag.text)
        return match.group(1), int(match.group(2)) / 100

    with open('subs/ccc14s5/report.html') as f:
        bs = BeautifulSoup(f.read(), features='html')
        for row in bs.find_all('tr'):
            if row.find('th'): # Header row
                continue

            oth_sub = row.find_all('a', text=re.compile(r'\d+ '))
            target_sub = row.find_all('a', text=re.compile(r'target_submission'))

            if target_sub:
                target_match = int(re.search(r'(\d+)%', target_sub[0].text).group(1)) / 100
                other_id, _ = match_sub_id_and_prec(oth_sub[0])
                if target_match >= th:
                    print(target_match)
                    print(other_id)
            else:
                other_id_1, other_match_1 = match_sub_id_and_prec(oth_sub[0])
                other_id_2, _ = match_sub_id_and_prec(oth_sub[1])
                if other_match_1 >= th:
                    print(other_id_1, other_match_1)
                    print(other_id_2)


parse_report()
