# Part A

import csv
import graphviz
from sklearn import tree

# constants
TOTAL_DAYS = 28
TIME1 = 705 # 11:45 in minutes
TIME2 = 720 # 12:00 in minutes
TIME3 = 735 # 12:15 in minutes

# order of data in files
# building_codes.csv = id, code, name, type
# door_data.csv = day, day_of_week, student_id, time_of_day, building, is_dining_hall

def get_building_code(bldg_code):
    # parse building_codes.csv to find building ID for a specified building, given building code (abbreviation) - for ex: BR, SM
    with open('building_codes.csv') as csvfile1:
        readCSV1 = csv.reader(csvfile1, delimiter=',')
        for row in readCSV1:
            if row[1] == bldg_code:
              bldg_id = row[0]
    return (bldg_id) # returns a str!!

def get_mean_traffic(bldg_id):
    # find mean traffic over the given 28 days for specified building
    total_swipes = 0

    with open('door_data.csv') as csvfile2:
        readCSV2 = csv.reader(csvfile2, delimiter=',')
        for row in readCSV2:
            if row[4] == bldg_id and row[5] == "1":
              total_swipes += 1

    mean_traffic = total_swipes / TOTAL_DAYS
    low_traffic_threshold = mean_traffic * 0.95
    high_traffic_threshold = mean_traffic * 1.05
    return (low_traffic_threshold, high_traffic_threshold)



def assign_training_labels_samples(bldg_id, low_traffic_threshold, high_traffic_threshold):
    samples = [[0, 0, 0, 0] for x in range(TOTAL_DAYS)] 
    # samples[x][0] = day of the week (0-6, Sunday to Saturday)
    # samples[x][1] = number of swipes by 11:45am
    # samples[x][2] = number of swipes by 12:00pm
    # samples[x][3] = number of swipes by 12:15pm

    labels = [0 for x in range(TOTAL_DAYS)]
    # labels to be used: -1 = low traffic, 0 = normal day, 1 = high traffic

    total_swipes = [0 for x in range(TOTAL_DAYS)]
    # counter variable for total swipes per day to calculate labels
    
    with open('door_data.csv') as csvfile3:
        readCSV3 = csv.reader(csvfile3, delimiter = ',')
        for row in readCSV3:
            bldg = row[4]
            if bldg == bldg_id and row[5] == "1":
                day = int(row[0])
                day_of_the_week = int(row[1])
                time_of_day = int(row[3])

                # increment total swipes for the day
                total_swipes[day] += 1

                # assigning sample data
                samples[day][0] = day_of_the_week

                if time_of_day <= TIME1:
                    samples[day][1] += 1 # swipes by 11:45 (incl 11:45)
                if (time_of_day > TIME1 & time_of_day <= TIME2):
                    samples[day][2] += 1 # swipes by 12:05 (incl 12:00)
                if (time_of_day > TIME2 & time_of_day <= TIME3):
                    samples[day][3] += 1 # swipes by 12:15 (incl 12:15)

        # assigning labels for the sample data
        for z in range(TOTAL_DAYS):
            if total_swipes[z] < low_traffic_threshold:
                labels[z] = -1
            if total_swipes[z] > high_traffic_threshold:
                labels[z] = 1
        
    return (samples, labels)
            
def main():

    bldg_id = get_building_code("SM")
    low_traffic_threshold, high_traffic_threshold = get_mean_traffic(bldg_id)

    samples, labels = assign_training_labels_samples(bldg_id, low_traffic_threshold, high_traffic_threshold)

    print(samples, labels)

# prediction for Branford with given data
# 78 swipes by 11:45am, 131 swipes by 12:00pm, 232 swipes by 12:15pm on a Monday

# BRSamples = 
# BRLabels = 

# clf = tree.DecisionTreeClassifier()

# clf_train = clf.fit()


# prediction for Silliman with given data
# 90 swipes by 11:45am, 171 swipes by 12:00pm, 230 swipes by 12:15pm on a Sunday

if __name__ == "__main__":
    main()