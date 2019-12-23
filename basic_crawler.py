# coding: utf8

import requests
import time
from bs4 import BeautifulSoup
import re
import traceback

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
            stat_nb = str(s.split(' ')[0])
            stat_desc = s.replace(stat_nb+' ', '')
            result.append(stat_nb)
        elif 'all-time player peak' in s:
            print('\t>Processing...')
            stat_nb = str(s.split(' ')[0])
            stat_desc = s.replace(stat_nb+' ', '')
            print([stat_desc.replace('all-time player peak ', '')])
            stat_date = str(stat_desc.replace('all-time player peak ', '').replace("\\xc3\\xa2\\xc2\\x80\\xc2\\x93 ", '').replace('\\xe2\\x80\\x93', '').replace(" UTC'", ""))

            result.append(stat_nb)
            result.append(stat_date)
        elif 'minutes median playtime' in s or 'minutes average playtime' in s:
            print('\t>Processing...')
            stat_nb_2_wk = str(s.split(' ')[0])
            stat_desc_tmp = s.replace(stat_nb_2_wk+' ', '')
            stat_desc_2_wk = str(stat_desc_tmp.split(' ')[0])

            print(stat_desc_tmp.split('\\n'))
            stat_nb_ltd = str(stat_desc_tmp.split('\\n')[1].split(' ')[0])
            stat_desc_tmp = stat_desc_tmp.split('\\n')[1].replace(stat_nb_ltd+' ', '')
            stat_desc_ltd = str(stat_desc_tmp.split(' ')[0])

            result.append(stat_nb_2_wk)
            result.append(stat_desc_2_wk)
            result.append(stat_nb_ltd)
            result.append(stat_desc_ltd)
        elif 'owners' in s:
            print('\t>Processing...')
            stat_nb = s.split(' owners ')[0].split(' .. ')
            stat_nb_min = str(stat_nb[0].replace(',', ''))
            stat_nb_max = str(stat_nb[1].replace(',', ''))
            result.append(stat_nb_min)
            result.append(stat_nb_max)

    return result

def _get_tag_list(max_=10, appid=None):
    if not appid:
        return
    STEAM_BASE_URL = "https://store.steampowered.com/app/"
    r = requests.get("{}{}".format(STEAM_BASE_URL,appid), headers=_emulate_agent())
    r = r.text.encode("UTF-8")
    soup = BeautifulSoup(r, "lxml")
    tags = soup.find("div", class_="glance_ctn_responsive_right").find_all("a", class_='app_tag')
    tags = [t.get_text().replace('\n', '').replace('\t', '').replace('\r', '') for t in tags]
    max_ = min(max_, len(tags))
    return [tags[i] for i in range(max_)]


def _get_price_list(appid=None):
    if not appid:
        return
    STEAM_BASE_URL = "https://store.steampowered.com/app/"
    r = requests.get("{}{}".format(STEAM_BASE_URL,appid), headers=_emulate_agent())
    r = r.text.encode("UTF-8")
    soup = BeautifulSoup(r, "lxml")
    price = soup.find("div", class_="game_purchase_price") if soup.find("div", class_="game_purchase_price") else soup.find("div", class_="discount_original_price")
    if not price:
        return None

    return str(re.findall("[0-9]+.?[0-9]*", price.get_text())[-1].replace(',', '.'))


def get_steam_apps_stats(app_id=None):
    apps = _steamdb_all_app_indie(file_save=True)
    keys = [app_id] if app_id else apps.keys()

    result_file = open("app_stats.csv", "w+", encoding="UTF-8")

    for k in keys:
        print("https://steamdb.info/app/{}/graphs/".format(k))
        r = requests.get("https://steamdb.info/app/{}/graphs/".format(k), headers=_emulate_agent())
        r = r.text.encode("UTF-8")
        soup = BeautifulSoup(r, "lxml")

        
        if len(soup.find(class_="span8").find_all("tr")) > 6:
            try:
                # Retrieve: Release Date
                release_date = soup.find(class_="span8").find_all("tr")[-1].find_all("td")[-1].get_text().replace(' UTC', '').replace(' ()', '').replace('"', '')
                print(release_date.encode("UTF-8"))

                # Retrieve: Stats
                all_ul = soup.find_all("ul", class_="app-chart-numbers")
                stats_raw_str = []
                for ul in all_ul:
                    stats = ul.find_all("li")
                    for s in stats:
                        # print(s.get_text().encode("UTF-8"))
                        stats_raw_str.append(s.get_text())
                
                # Retrieve: Tags list
                tag_list = _get_tag_list(appid=k)

                # Retrieve: Price
                price = _get_price_list(appid=k)

                # Retrieve: Reviews numbers
                good_reviews_nb = soup.find("span", class_="header-thing-good").get_text().replace(',', '')
                bad_reviews_nb = soup.find("span", class_="header-thing-poor").get_text().replace(',', '')
                all_reviews_nb = good_reviews_nb + bad_reviews_nb

                
                out_put = '"'+'","'.join(tag_list)+'"'
                out_put = '"'+ '","'.join(_stats_str_parsing(stats_str='\t'.join(stats_raw_str)))+'",'+out_put
                out_put = '"'+all_reviews_nb+'","'+good_reviews_nb+'","'+bad_reviews_nb+'",'+out_put
                out_put = '"'+str(k)+'","'+apps[str(k)]+'","'+'"'+release_date+'","'+price+'",'+out_put
                result_file.write(out_put+'\n')
                result_file.flush()
            except Exception as e:
                # print('\t'.join(stats_raw_str).encode('UTF-8'))
                fail_log = open("failed_app.log", "a", encoding="UTF-8")
                fail_log.write("https://steamdb.info/app/{app_id}/graphs/ ...Failed with: \t > {e}\n".format(e=e, app_id=k))
                fail_log.close()
                print('ERROR '* 12)
                print(e.__traceback__)
                print(e)
                traceback.print_exc()
        else :
            print("Mauvaise App")
        time.sleep(5)

    result_file.close()
################################


get_steam_apps_stats(2520)