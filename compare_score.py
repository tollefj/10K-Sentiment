import csv
from score import Score
from collections import defaultdict

years = defaultdict(list)


def init():
    with open('csv/AIV.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            years[row['Year']].append(Score(row.values()))


def show():
    for y in years:
        print(y)
        for s in years.get(y):
            print(s)


by_year = defaultdict(dict)


def populate_items():
    for year in years.keys():
        by_items = dict()
        for item in years.get(year):
            by_items[item.item] = item
        by_year[year].update(by_items)


def get_item(year, itemno):
    year = str(year) if isinstance(year, int) else year
    # pass in item as "1" or "9b"
    itemname = 'item_' + itemno
    item = by_year.get(year).get(itemname)
    print('Fetched item ' + item.get())
    return item


init()
years_found = list(years.keys())
print('Found years: ' + str(years_found))
populate_items()

print(get_item(2015, '1').get())
a = get_item(2015, '1a')
b = get_item(2016, '1a')

a.compare(b)
