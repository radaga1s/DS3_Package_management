import requests
from bs4 import BeautifulSoup as bs
import pytest


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
    try:
        response = requests.get(url_template, headers=headers)
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
                        result = tuple(result)
                        print(result)
                        return result
                    break
            if res is None:
                raise Exception(f'The requested field {field} does not exist')
        else:
            raise Exception(f'{response.status_code}    The URL does not exist or site is not responding')
    except TypeError:
        raise Exception('The URL does not exist and the request has been forwarded')


def test_main_totrev():
    ticker, field = ('MSFT', 'Total Revenue')
    expected = ('Total Revenue', '261,802,000', '245,122,000', '211,915,000', '198,270,000', '168,088,000')
    try:
        result = main(ticker, field)
        if result:
            assert result == expected
    except Exception: ...

def test_main_istupl():
    ticker, field = ('MSFT', 'Total Revenue')
    try:
        result = main(ticker, field)
        if result:
            assert isinstance(result, tuple) == True
    except Exception: ...

def test_main_noticker():
    ticker, field = ('asde', 'Total Revenue')
    with pytest.raises(Exception) as exc:
        main(ticker, field)
    assert 'The URL does not exist and the request has been forwarded' in str(exc.value)

def test_main_nofield():
    ticker, field = ('MSFT', 'asde')
    with pytest.raises(Exception) as exc:
        main(ticker, field)
    assert f'The requested field {field} does not exist' in str(exc.value)


