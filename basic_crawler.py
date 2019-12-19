import requests
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
    else:
        html_sample = _steamdb_request(file_save=True)
        
    sample = ''.join(html_sample.readlines())

    soup = BeautifulSoup(sample, "lxml")
    all_td = soup.find_all("td", class_="text-left")
    apps = {}
    for td in all_td:
        # print(td.a)
        if td.a and td.a.get('href'):
            # print(td.a.get('href'))
            apps[td.a.get('href').split('/')[-2]] = td.a.get_text()

    if file_save:
        file = open("out.txt", "w", encoding="UTF-8")
        file.write(str(apps))
    
    return apps

