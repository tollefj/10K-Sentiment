import os
import csv
import time
from pysentiment.lm import LM


os.chdir(os.getcwd())
_lm = LM()
csv_dir = 'csv'
if not os.path.isdir(csv_dir):
    os.mkdir(csv_dir)


"""
Positive: +score for each positive word

Negative: +score for each negative word

Polarity: (pos-neg)/(pos+neg)
            the amount of positive words divided by total pos/neg words
            100% positive: 1.0
            100% negative: -1.0
            positive=negative: 0.0
            -> more positive words: higher polarity

Subjectivity: (pos+neg)/total_words
                -> the threshold between weighted vs neutral words
                if there is a significant amount of
                positive/negative words against the overall
                word count, then this value will be high
"""


def format_item(item):
    tmp = item.split(' ', 2)
    # return (item_x, the name)
    return (tmp[0]+'_'+tmp[1], tmp[2].replace('.txt', ''))


class Ticker:
    def __init__(self, ticker):
        self.ticker = ticker
        self.logs = list()

    def get_score(self, item):
        with open(item) as tmp:
            tokens = _lm.tokenize(tmp.read())
            return _lm.get_score(tokens)

    def add_item_to_year(self, year, item, name, descr):
        scores = dict()
        scores['Year'] = year
        scores['Item'] = name
        scores['Description'] = descr
        scores.update(self.get_score(item))
        self.logs.append(scores)

    def close(self):
        # write to csv
        csvname = self.ticker + '.csv'
        csvpath = os.path.join(csv_dir, csvname)
        with open(csvpath, 'w') as csvfile:
            fieldnames = ['Year', 'Item', 'Description',
                          'Positive', 'Negative',
                          'Polarity', 'Subjectivity']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for log in self.logs:
                writer.writerow(log)


os.chdir(os.getcwd())
for ticker in os.listdir('filings'):
    if '.' not in ticker:
        print(ticker)
        _ticker = Ticker(ticker)
        ticker_path = os.path.join('filings', ticker)
        for year in os.listdir(ticker_path):
            year_path = os.path.join(ticker_path, year)
            if os.path.isdir(year_path):
                for item in os.listdir(year_path):
                    if 'item' in item:
                        item_path = os.path.join(year_path, item)
                        item_name, item_descr = format_item(item)
                        _ticker.add_item_to_year(year, item_path,
                                                 item_name, item_descr)
        _ticker.close()

