import os
from pysentiment.lm import LM
_lm = LM()
analysis = dict()
os.chdir(os.getcwd())
for ticker in os.listdir('filings'):
    if '.' not in ticker:
        print(ticker)
        for part in os.listdir(os.path.join('filings', ticker)):
            if '.DS' not in part and '1A' in part:
                # part_name = part.rsplit('_', 1)[1].replace('.txt', '')
                # print(part_name)
                with open(os.path.join('filings', ticker, part)) as f:
                    txt = f.read()
                    tokens = _lm.tokenize(txt)
                    print('Sentiment analysis for ' + part)
                    print(_lm.get_score(tokens))

                    # analysis[part_name] = _lm.get_score(tokens)
# for key in analysis.keys():
    # print('*** ' + key + ' ***')
    # print(analysis[key])
    # print()
