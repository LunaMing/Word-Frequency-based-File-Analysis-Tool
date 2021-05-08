import requests


def spider():
    proxies = {"http": None, "https": None}
    r = requests.get('https://www.usenix.org/conference/nsdi20/presentation/gadre',
                     proxies=proxies)
    print(r.status_code)
    exit()


if __name__ == '__main__':
    spider()
