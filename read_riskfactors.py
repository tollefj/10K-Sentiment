import os
import csv
import sys
from pysentiment.lm import LM

if len(sys.argv) < 2:
    print('Missing sector selection as argument. Valid arguments:\n',
          '\n1\t-> business',
          '\n1a\t-> risk factors',
          '\n1b\t-> unresolved staff comments',
          '\n2\t-> properties',
          '\n3\t-> legal proceedings',
          '\n4\t-> mine safety disclosures',
          '\n5\t-> market for registrants ...',
          '\n6\t-> selected financial data',
          '\n7\t-> managements discussion and ...',
          '\n7a\t-> quantitative and qualitative ...',
          '\n8\t-> financial statements and suppl ... ',
          '\n9\t-> changes in and disagreements ...',
          '\n9a\t-> controls and procedures',
          '\n9b\t-> other information',
          '\n10\t-> directors executive officers ...',
          '\n11\t-> executive compensation',
          '\n12\t-> security ownership of certain ...',
          '\n13\t-> certain relationships and ...',
          '\n14\t-> principal accounting fees ...',
          '\n15\t-> exhibits financial statement ...')
    sys.exit(0)
print(sys.argv[1])
sys.exit(0)

os.chdir(os.getcwd())
_lm = LM()
risk_dir = 'risk_factors'
if not os.path.isdir(risk_dir):
    os.mkdir(risk_dir)


csvfile = open(os.path.join(risk_dir, 'risks.csv'), 'w')
fieldnames = ['Company',
              '2014_Polarity', '2014_Ratio',
              '2015_Polarity', '2015_Ratio',
              '2016_Polarity', '2016_Ratio']
writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
writer.writerow(fieldnames)


class Ticker:
    def __init__(self, ticker):
        self.ticker = ticker

    def get_score(self, item):
        with open(item) as tmp:
            tokens = _lm.tokenize(tmp.read())
            return _lm.get_score(tokens)

    def sentiment(self, item_path):
        row = self.get_score(item_path)
        pos = row['Positive']
        neg = row['Negative']
        ratio = float(neg)/float(pos)
        polarity = row['Polarity']
        #  polarity = polar + ' (Pos: ' + pos + ', Neg: ' + neg + ')'
        print(polarity)
        return [polarity, ratio]


os.chdir(os.getcwd())
rows = []
for ticker in os.listdir('filings'):
    if 'DS' not in ticker:
        print(ticker)
        _ticker = Ticker(ticker)
        ticker_path = os.path.join('filings', ticker)
        ticker_data = [ticker]
        for year in os.listdir(ticker_path):
            year_path = os.path.join(ticker_path, year)
            if 'DS' not in year and os.path.isdir(year_path):
                print(year)
                for item in os.listdir(year_path):
                    if 'risk factors' in item:
                        print(item)
                        item_path = os.path.join(year_path, item)
                        score = _ticker.sentiment(item_path)
                        ticker_data.extend(score)
        print('writing: ' + str(ticker_data))
        rows.append(ticker_data)
for row in rows:
    writer.writerow(row)
csvfile.close()
