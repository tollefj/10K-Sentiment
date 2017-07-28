import os
import re
import bleach
import urllib
from random import randint
from bs4 import BeautifulSoup as BS

from config import toc, toc_nospace, _form

from utils import get_ticker_url, format_cell, valid_year, create_folder
from utils import get_url, get_href

os.chdir(os.getcwd())  # setting current dir as working one


# Create Filings folder to store downloads
create_folder('filings')
# TODO: create a logger class


def process_page(page, cache):
    if not os.path.isfile(cache):
        # Remove non-breaking space
        page = page.replace('&nbsp;', ' ').replace('&#160;', ' ')
        # Replace all newlines and carriage returns
        page = page.strip().replace('\n', ' ').replace('\r', '')
        # Clear html-style spaces
        page = re.sub(' +', ' ', page)
        #  while '  ' in page:
        #      page = page.replace('  ', ' ')
        # Brutally remove all html tags
        page = bleach.clean(page, tags=[], attributes={},
                            styles=[], strip=True)
        page = page.lower()
        print('Extract only alphanumeric characters')
        pattern = re.compile('([^\s\w]|_)+')
        page = pattern.sub('', page)

    # find the second match of "PAGE I" - this is where each report starts
    print('Finding Table of Contents')
    start_idx = 0
    regex = r"(\bPART I\b)"
    match = [(m.start(0)) for m in re.finditer(
        regex, page, flags=re.IGNORECASE)]
    print('*******' + str(match))
    return page[start_idx:]


def between_items(a, b):
    #  return '(\\b' + a + '\\b)(.+?)(\\b' + b + '\\b)'
    return '(' + a + ')(.+?)(' + b + ')'


def download_10k(link, ticker, filename):
    # store the file in the correct ticker directory
    create_folder(os.path.join('filings', ticker))
    filing_year = filename.split('_')[0]
    path = os.path.join('filings', ticker, filing_year)
    create_folder(path)
    cache = path + 'report.txt'
    if not os.path.isfile(cache):
        print('Opening link... ' + link)
        pageopen = urllib.request.urlopen(link)
        print('Decoding...')
        readpage = pageopen.read().decode('utf-8')
    else:
        with open(cache) as tmp:
            readpage = tmp.read()
    page = process_page(readpage, cache)
    # store the read text, just in case
    with open(path + 'report.txt', 'w') as tmp:
        tmp.write(page)

    # Apply a regex match on items a->b in page
    def do_match(page, a, b):
        regex = between_items(a, b)
        match = re.search(regex, page, flags=re.IGNORECASE)
        return match.group(2) if match else None

    print('analyzing page for ' + filename)
    for i in range(len(toc) - 1):
        print(toc[i] + '->' + toc[i + 1])
        match = do_match(page, toc[i], toc[i + 1])
        if not match or match and len(match)<10:
            print('Attempting space->nospace')
            match = do_match(page, toc[i], toc_nospace[i + 1])
        if not match or match and len(match)<10:
            print('Attempting nospace->nospace')
            match = do_match(page, toc_nospace[i], toc_nospace[i + 1])
        if not match or match and len(match)<10:
            print('Attempting nospace->space')
            match = do_match(page, toc_nospace[i], toc[i + 1])
        if match:
            print('Regex match')
            txt = open(os.path.join(path, toc[i]) + '.txt', 'w')
            #  out = match.group(2)
            txt.write(match)
            txt.close()


def get_10k_data(link, ticker_cell):
    print('Getting 10k files...')
    ticker, filedate = ticker_cell
    page = urllib.request.urlopen(link)
    soup = BS(page.read(), "lxml")
    table = soup.find('table', {'summary': 'Document Format Files'})
    if table is None:
        print(str(ticker_cell) + ' is invalid!')
        return
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 5:
            # 10-K is positioned at the 4th column
            if cells[3].text.strip() == _form:
                # print(cells)
                endpoint = cells[2].find('a')['href']
                form_link = get_url(endpoint)
                download_10k(form_link, ticker, filedate)


def get_link_table(ticker):
    url = get_ticker_url(ticker)
    print(url)
    page = urllib.request.urlopen(url)
    soup = BS(page.read(), "lxml")
    # Attempt to find table
    table = soup.find('table', {'class': 'tableFile2'})
    if table is None:
        print('Invalid ticker: ' + ticker)
        return

    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 5:
            if cells[0].text.strip() == _form:
                # this is a form of type 10-K
                filedate = format_cell(cells[3])
                if not valid_year(filedate):
                    continue
                pretty_filedate = filedate.replace('-', '_')
                # descr = format_cell(cells[2])
                endpoint = cells[1].find('a', {'id': 'documentsbutton'})
                link = get_href(endpoint)
                get_10k_data(link, [ticker, pretty_filedate])


sp = []
with open(os.path.join('sp500', 'list.txt'), 'r') as sp500:
    sp = [s.strip() for s in sp500.readlines()]
random_tickers = [sp[randint(0, 500)] for i in range(10)]
print('Random tickers:')
print(random_tickers)
for stock in random_tickers:
    get_link_table(stock)
