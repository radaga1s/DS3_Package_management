#!../ex02/bs_pt_venv/bin/python3

import sys
import time
import requests
from bs4 import BeautifulSoup as bs


def main(ticker, field):
    result = [field,]
    res = None
    url_template = f'https://finance.yahoo.com/quote/{ticker}/financials/?p={ticker.lower()}'
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://finance.yahoo.com/",
    "DNT": "1"}
    response = requests.get(url_template, headers=headers)
    time.sleep(5)
    if response.status_code == 200:
        sp = bs(response.text, 'html.parser')
        lines = sp.find(attrs={'class': 'tableBody'})
        for line in lines:
            txt = line.text.strip()
            if txt.startswith(field):
                res = txt.split(field)[1]
                res = res if len(res.split()) == 5 else None 
                if res:
                    result.extend(res.split())
                    print(tuple(result))
                break
        if res is None:
            raise Exception(f'The requested field {field} does not exist')
    else:
        raise Exception(f'{response.status_code}    The URL does not exist or site is not responding')


if __name__ == '__main__':
    try:
        ticker, field = sys.argv[1:]
        main(ticker, field)
    except ValueError:
        print('Not enough values passed in command line arguments')
    except TypeError:
        print('The URL does not exist and the request has been forwarded')
    except Exception as e:
        print(e)
