import os
from config import _url, _count, _form, _years


def get_ticker_url(ticker):
    return _url + '/cgi-bin/browse-edgar?' + \
        'action=getcompany&CIK=' + ticker + '&type=' + _form + \
        '&dateb=&owner=exclude&count=' + _count


def format_cell(cell):
    return cell.text.strip()


def valid_year(filed_date):
    # e.g. 2015-03-30 -> 2015, then check if it's in valid years
    return filed_date.split('-')[0] in _years


def create_folder(folder_name):
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)


def get_url(endpoint):
    return _url + str(endpoint)


def get_href(endpoint):
    return _url + endpoint['href']
