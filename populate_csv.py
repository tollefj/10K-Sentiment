import os

allitems = ['1', '1a', '1b', '2', '3', '4', '5', '6', '7', '7a', '8',
            '9', '9a', '9b', '10', '11', '12', '13', '14', '15']

for item in allitems:
    os.system('python3 create_csv_from_item.py '+item)
