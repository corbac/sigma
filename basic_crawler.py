# -*- coding: utf-8 -*-

import requests
import time
from bs4 import BeautifulSoup

# URL_BASE_TAG = "https://steamdb.info/tags/?tagid=492"


def _emulate_agent():
    USER_AGENT = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"}
    return USER_AGENT

# Requesting The Page
def _steamdb_request(URL_BASE_TAG = "https://steamdb.info/tags/?tagid=492", file_save = False):
    r = requests.get(URL_BASE_TAG, headers=_emulate_agent())
    print(r.status_code)
    print(r.encoding)

    if file_save :
        html_sample = open("sample.html", "w", encoding=r.encoding)
        html_sample.write(r.text)

    return r.text
    # print(r.content)

def _steamdb_all_app_indie(file_save =  False):
    if file_save:
        html_sample = open("sample.html", "r", encoding="UTF-8")
        sample = ''.join(html_sample.readlines())
    else:
        sample = _steamdb_request(file_save=True)

    soup = BeautifulSoup(sample, "lxml")
    all_td = soup.find_all("td", class_="text-left")
    apps = {}
    for td in all_td:
        # print(td.a)
        if td.a and td.a.get('href'):
            # print(td.a.get('href'))
            apps[td.a.get('href').split('/')[-2]] = td.a.get_text()

    # if file_save:
    #     file = open("out.txt", "w", encoding="UTF-8")
    #     file.write(str(apps))
    
    return apps

def _stats_str_parsing(stats_str=''):
    print('*' * 99)
    print(stats_str.encode('UTF-8'))
    print('*' * 99)
    stats_raw_list = stats_str.split('\t')
    print(len(stats_raw_list))
    result = []
    for s in stats_raw_list:
        print(s.encode('UTF-8'))
        if stats_raw_list.index(s) in [0,1]:
            continue
        
        # print(type(s))
        # print(type(s.encode('UTF-8')))
        s = str(s.encode('UTF-8')).replace('\\n', '', 1)
        if 'followers' in s:
            print('\t>Processing...')
            stat_nb = s.split(' ')[0]
            stat_desc = s.replace(stat_nb+' ', '')
            result.append(stat_nb)
        elif 'all-time player peak' in s:
            print('\t>Processing...')
            stat_nb = s.split(' ')[0]
            stat_desc = s.replace(stat_nb+' ', '')
            print([stat_desc.replace('all-time player peak ', '')])
            stat_date = stat_desc.replace('all-time player peak ', '').replace("\\xc3\\xa2\\xc2\\x80\\xc2\\x93 ", '').replace(" UTC'", "")

            result.append(stat_nb)
            result.append(stat_date)
        elif 'minutes median playtime' in s or 'minutes average playtime' in s:
            print('\t>Processing...')
            stat_nb_2_wk = s.split(' ')[0]
            stat_desc_tmp = s.replace(stat_nb_2_wk+' ', '')
            stat_desc_2_wk = stat_desc_tmp.split(' ')[0]

            print(stat_desc_tmp.split('\\n'))
            stat_nb_ltd = stat_desc_tmp.split('\\n')[1].split(' ')[0]
            stat_desc_tmp = stat_desc_tmp.split('\\n')[1].replace(stat_nb_ltd+' ', '')
            stat_desc_ltd = stat_desc_tmp.split(' ')[0]

            result.append(stat_nb_2_wk)
            result.append(stat_desc_2_wk)
            result.append(stat_nb_ltd)
            result.append(stat_desc_ltd)
        elif 'owners' in s:
            print('\t>Processing...')
            stat_nb = s.split(' owners ')[0].split(' .. ')
            stat_nb_min = stat_nb[0].replace(',', '')
            stat_nb_max = stat_nb[1].replace(',', '')
            result.append(stat_nb_min)
            result.append(stat_nb_max)

    return result

################################

apps = _steamdb_all_app_indie(file_save=True)

result_file = open("app_stats.csv", "w", encoding="UTF-8")
for k in apps.keys():
    print("https://steamdb.info/app/{}/graphs/".format(k))
    r = requests.get("https://steamdb.info/app/{}/graphs/".format(k), headers=_emulate_agent())
    r = r.text.encode("UTF-8")
    # print(r.text.encode("UTF-8"))
    soup = BeautifulSoup(r, "lxml")
    if len(soup.find(class_="span8").find_all("tr")) > 6:
        release_date = soup.find(class_="span8").find_all("tr")[-1].find_all("td")[-1].get_text()
        print(release_date.encode("UTF-8"))
        all_ul = soup.find_all("ul", class_="app-chart-numbers")
        stats_raw_str = []
        for ul in all_ul:
            stats = ul.find_all("li")
            for s in stats:
                # print(s.get_text().encode("UTF-8"))
                stats_raw_str.append(s.get_text())
        try:
            # print('\t'.join(stats_raw_str).encode('UTF-8'))
            out_put = '"'+ '","'.join(_stats_str_parsing(stats_str='\t'.join(stats_raw_str)))+'"'
            result_file.write('"'+k+'","'+apps[k]+'","'+'"'+release_date+'","'+out_put+'\n')
            result_file.flush()
        except Exception as e:
            # print('\t'.join(stats_raw_str).encode('UTF-8'))
            print('ERROR '* 12)
            print(e.__traceback__)
            print(e)
    else :
        print("Mauvaise App")
    time.sleep(5)

result_file.close()


# date_str = "May 31, 2017 ()"
# stats_str = """1 players right now\t6 24-hour player peak\t108 all-time player peak November 22, 2011 \xe2\x80\x93 20:43:21 UTC\t848 followers\t\n0 minutes median playtime in last 2 weeks\n3.1 hours median total playtime\n\t\n0 minutes average playtime in last 2 weeks\n2.5 hours average total playtime\n\t\n500,000 .. 1,000,000 owners (?)\n
# """


# print(_stats_str_parsing(stats_str))