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

    # print(r.content)

# _steamdb_request(file_save=True)
html_sample = open("sample.html", "r", encoding="UTF-8")
# print(html_sample.readlines())
sample = ''.join(html_sample.readlines())

# print(type(sample))

soup = BeautifulSoup(sample, "lxml")
file = open("out.txt", "w", encoding="UTF-8")
all_td = soup.find_all("td", class_="text-left")
apps = {}
for td in all_td:
    # print(td.a)
    if td.a and td.a.get('href'):
        # print(td.a.get('href'))
        apps[td.a.get('href').split('/')[-2]] = td.a.get_text()


file.write(str(apps))

