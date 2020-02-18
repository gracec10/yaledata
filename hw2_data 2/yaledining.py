# this is the data preprocessing file for Part A (Yale Dining)

import csv

# parse building_codes.csv to find Branford and Silliman's building codes
with open('building_codes.csv') as csvfile1:
    readCSV1 = csv.reader(csvfile1, delimiter=',')
    for row in readCSV1:
        if row[1] == "BR":
            BRCode = row[0]
        if row[1] == "SM":
            SMCode = row[0]

# find mean traffic per day for Branford and Silliman each
totalSwipesBR = 0
totalSwipesSM = 0

with open('door_data.csv') as csvfile2:
    readCSV2 = csv.reader(csvfile2, delimiter=',')
    for row in readCSV2:
        building = row[4]
        if building == BRCode:
            totalSwipesBR = totalSwipesBR + 1
        if building == SMCode:
            totalSwipesSM = totalSwipesSM + 1
    MeanTrafficBR = totalSwipesBR / 28
    MeanTrafficSM = totalSwipesSM / 28

