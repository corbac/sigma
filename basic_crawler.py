import requests

URL_BASE_TAG = "https://steamdb.info/tags/?tagid=492"
USER_AGENT = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"}


r = requests.get(URL_BASE_TAG, headers=USER_AGENT)
print(r.status_code)
print(r.content)