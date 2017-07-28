import matplotlib.pyplot as plt
import numpy as np
import os
import csv
os.chdir(os.getcwd())
risks = os.path.join('csv_files', 'risk factors.csv')
valid_rows = list()

years = '2013 2014 2015 2016 2017'.split()
print(years)

#  def save_plot(arr):
#      fig = plt.figure()
#

by_polarity = list()
by_ratio = list()
with open(risks, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) == 11:
            c, p13, r13, p14, r14, p15, r15, p16, r16, p17, r17 = row
            polar = [c, p13, p14, p15, p16, p17]
            ratio = [c, r13, r14, r15, r16, r17]
            #  print(polar)
            #  print(ratio)
            #  print()

x=[1,3,5,7,8]
y=[9,3,4,5,6]
z=[9,9,9,8,9]
plt.plot(years,x)
plt.savefig('fig.png')
