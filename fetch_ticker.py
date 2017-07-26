import os
import re
import bleach
import urllib
from collections import defaultdict
from bs4 import BeautifulSoup as BS

os.chdir(os.getcwd())  # setting current dir as working one
_form = '10-K'
_count = '10'  # Amount of links to fetch. Only recent years are interesting.
_url = 'https://www.sec.gov'
#  _years = ['2017', '2016', '2015']  # TODO: set years in sys.args or similar
_years = ['2016']
#  toc = ['Item 1', 'Item 1A', 'Item 1B', 'Item 2', 'Item 3',
#         'Item 4', 'Item 5', 'Item 6', 'Item 7', 'Item 7A',
#         'Item 8', 'Item 9', 'Item 9A', 'Item 9B', 'Item 10',
#         'Item 11', 'Item 12', 'Item 13', 'Item 14', 'Item 15']

toc = ['Item 1 Business',
       'Item 1A Risk Factors',
       'Item 1B Unresolved Staff Comments',
       'Item 2 Properties',
       'Item 3 Legal Proceedings',
       'Item 4 Mine Safety Disclosures',
       'Item 5 Market for Registrant’s Common Equity, Related Stockholder Matters and Issuer Purchases of Equity Securities',
       'Item 6 Selected Financial Data',
       'Item 7 Management’s Discussion and Analysis of Financial Condition and Results of Operations',
       'Item 7A Quantitative and Qualitative Disclosures about Market Risk',
       'Item 8 Financial Statements and Supplementary Data',
       'Item 9 Changes in and Disagreements with Accountants on Accounting and Financial Disclosure',
       'Item 9A Controls and Procedures',
       'Item 9B Other Information',
       'Item 10 Directors, Executive Officers and Corporate Governance',
       'Item 11 Executive Compensation',
       'Item 12 Security Ownership of Certain Beneficial Owners and Management and Related Stockholder Matters',
       'Item 13 Certain Relationships and Related Transactions, and Director Independence',
       'Item 14 Principal Accounting Fees and Services',
       'Item 15 Exhibits and Financial Statement Schedules'
       ]


def get_ticker_url(ticker):
    return _url + '/cgi-bin/browse-edgar?' + \
        'action=getcompany&CIK=' + ticker + '&type=' + _form + \
        '&dateb=&owner=exclude&count=' + _count


def format_cell(cell):
    return cell.text.strip()


def valid_year(filed_date):
    return filed_date.split('-')[0] in _years


def create_folder(folder_name):
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)


found_links = []
ticker_data = defaultdict(list)
ticker_10k_data = defaultdict(list)
# Create Filings folder to store downloads
create_folder('filings')


def process_page(page, cache):
    if not os.path.isfile(cache):
        print('bleaching...')
        page = bleach.clean(page, tags=[], attributes={},
                            styles=[], strip=True)
        # Remove all newlines and carriage returns from the page
        print('stripping...')
        page = page.strip().replace('\n', ' ').replace('\r', '')
        # Clear html-style spaces
        print('cleaning html...')
        page = page.replace('&nbsp;', ' ').replace('&#160;', ' ')
        print('removing tabs')
        page = page.replace('\t', ' ')
        while '  ' in page:
            page = page.replace('  ', ' ')
        print('substituing non-alpha chars')
        pattern = re.compile('([^\s\w]|_)+')
        page = pattern.sub('', page)

    # find the second match of "PAGE I" - this is where each report starts
    print('finding start')
    #  look for table of contents, first occurrence
    # store the page, as cache
    toc_rx = r"(\bPART I\b)"
    match = [(m.start(0)) for m in re.finditer(
        toc_rx, page, flags=re.IGNORECASE)]
    start_idx = match[0]
    #  for m in match:
    #      print(page[m:m+50])
    print(str(match))
    return page[start_idx:]


#  def get_regex(start, end):
#      # 1: bold before the item subtitle
#      r1 = 'bold;\">\s*' + start + '\.(.+?)bold;\">\s*' + end + '\.'
#      # 2: tag <b> before the item subtitle
#      r2 = 'b>\s*' + start + '\.(.+?)b>\s*' + end + '\.'
#      # 3: tag <\b> after the item subtitle
#      r3 = start + '\.\s*<\/b>(.+?)' + end + '\.\s*<\/b>'
#      # 4: tag <\b> after the item+description subtitle
#      r4 = start + '\.\s*Business\.\s*<\/b(.+?)'\
#          + end + '\.\s*Risk Factors\.\s*<\/b'
#
#      regex = [r1, r2, r3, r4]
#      return regex


#  def text_in(s, e):
#      return 'bold;\">\s*'+s+'\.(.+?)bold;\">\s*'+e+'\.'


def between_items(a, b):
    #  item_a = a.replace(' ', '.')
    #  item_b = b.replace(' ', '.')
    #  print(item_a, item_b)
    #  return '('+item_a+')(.*)('+item_b+')'
    return '(\\b' + a + '\\b)(.+?)(\\b' + b + '\\b)'


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
    #  htmlfile = open(path+'.html', 'wb')
    #  htmlfile.write(page.read())
    #  htmlfile.close()

    print('analyzing page for ' + filename)
    for i in range(len(toc) - 1):
        print(toc[i] + '->' + toc[i + 1])
        regex = between_items(toc[i], toc[i + 1])
        #  regexs = get_regex(toc[i], toc[i + 1])
        #  regex = text_in(toc[i], toc[i + 1])
        #  for regex in regexs:
        match = re.search(regex, page, flags=re.IGNORECASE)
        print(str(match))
        match = [(m.start(0), m.end(0)) for m in re.finditer(
            regex, page, flags=re.IGNORECASE)]
        print("ITERMATCH: " + str(match))
        if len(match) > 1:
            newtext = page[match[1][0]:match[1][1]]
            txt = open(os.path.join(path, toc[i]) + '.txt', 'w')
            txt.write(newtext)
            txt.close()
        #  if match:
        #      print('Regex match')
        #      txt = open(os.path.join(path, toc[i]) + '.txt', 'w')
        #      out = match.group(2)
        #      txt.write(out)
        #      txt.close()
        #      # important to use html.parser here over lxml,
        #      # as the file is read as a utf-8 file,
        #      # not a binary file with xml-like properties
        #      #  soup = BS(match.group(1), "html.parser")
        #      #  out = soup.text.strip()
        #      #  print(len(out))
        #


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
                form_link = _url + str(endpoint)
                ticker_cell.append(form_link)
                ticker_10k_data[ticker_cell[0]].append(ticker_cell)
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
    current_doc = 1
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
                link = _url + endpoint['href']
                #  ticker_data[ticker].append([ticker,
                #  current_doc, link, descr,
                #  filedate, pretty_filedate])
                #  cell_data = [ticker, current_doc, link, descr,
                #  filedate, pretty_filedate]
                #
                #  access the 10k form
                #  print('Accessing table to fetch 10k form,
                #  cell: ' + str(cell_data))
                #  get_10k_data(cell_data)
                get_10k_data(link, [ticker, pretty_filedate])

                current_doc += 1
    print()


get_link_table('MSFT')

# Iterate all files found
# for k, v in ticker_10k_data.items():
# print(k, v)
# for company in ticker_10k_data.keys():
# for reports in ticker_10k_data[company]:
# print(reports)
