import urllib3
from bs4 import BeautifulSoup
import sys
import json
from .parameters import createChatHash


def get_last_transaction():
    # url = 'https://cardanoscan.io/metadata'
    req = urllib3.PoolManager()
    messages = []
    for p in range(1, 10):
        url = 'https://cardanoscan.io/metadata?pageNo=' + str(p)
        res = req.request('GET', url)
        soup = BeautifulSoup(res.data, 'html.parser')
        divs = soup.findAll('div', {'class': 'metadata-item'})
        for div in divs:
            spans = div.findAll('span')
            for span in spans:
                obj = span.encode_contents().decode("utf-8")
                try:
                    int(obj)
                except ValueError:
                    data = json.loads(obj)
                    try:
                        chatHash = data["1"]
                        if chatHash == createChatHash():
                            messages.append(data)
                    except (TypeError, KeyError):
                        pass
    return messages



def get_meta_data(url):
    req = urllib3.PoolManager()
    res = req.request('GET', url)
    soup = BeautifulSoup(res.data, 'html.parser')
    events = soup.findAll('span', {'class': 'metadata-value'})
    for value in events:
        check = value.encode_contents().decode("utf-8")
        print(check)


if __name__ == "__main__":

    messages= get_last_transaction() 
    print(messages)
