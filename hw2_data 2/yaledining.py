# Part A

import csv
import graphviz
from sklearn import tree

#data preprocessing section

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

meanTrafficBR = totalSwipesBR / 28 # 28 days total
meanTrafficSM = totalSwipesSM / 28

# constants for mean traffic comparisons
LOWTRAFFICBR = 0.95 * meanTrafficBR
HIGHTRAFFICBR = 1.05 * meanTrafficBR
LOWTRAFFICSM = 0.95 * meanTrafficSM
HIGHTRAFFICSM = 1.05 * meanTrafficSM

# 

# train decision tree

# prediction for Branford with given data
# 78 swipes by 11:45am, 131 swipes by 12:00pm, 232 swipes by 12:15pm on a Monday

BRSamples = 
BRLabels = 

clf = tree.DecisionTreeClassifier()

clf_train = clf.fit()


# prediction for Silliman with given data
# 90 swipes by 11:45am, 171 swipes by 12:00pm, 230 swipes by 12:15pm on a Sunday