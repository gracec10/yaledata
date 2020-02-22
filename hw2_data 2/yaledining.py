# Grace Cheung
# gvc8
# CPSC 310
# HW 2
# Part A
# 2/21/2020

import csv
import graphviz
from sklearn import tree

# constants
TOTAL_DAYS = 28
TIME1 = 705 # 11:45 in minutes
TIME2 = 720 # 12:00 in minutes
TIME3 = 735 # 12:15 in minutes
LUNCH_START_WEEKDAY = 690 # lunch starts at 11:30am on weekdays
LUNCH_START_WEEKEND = 660 # lunch starts at 11:00am on weekends
LUNCH_END = 810 # lunch ends at 1:30 every day

# order of data in files
# building_codes.csv = id, code, name, type
# door_data.csv = day, day_of_the_week, student_id, time_of_day, building, is_dining_hall

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
                # different lunch hours for weekend and weekday
                if row[1] in ("1", "2", "3", "4", "5"):
                    if LUNCH_START_WEEKDAY <= int(row[3]) <= LUNCH_END:
                        total_swipes += 1
                if row[1] in ("6", "0"):
                    if LUNCH_START_WEEKEND <= int(row[3]) <= LUNCH_END:
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

                #assigning sample data and incrementing total swipes for label use later
                samples[day][0] = day_of_the_week

                # different lunch hours for weekend and weekday
                if day_of_the_week in (1, 2, 3, 4, 5):
                    if LUNCH_START_WEEKDAY <= time_of_day <= LUNCH_END:
                        total_swipes[day] += 1
                        if time_of_day <= TIME1:
                            samples[day][1] += 1 # swipes by 11:45 (incl 11:45)
                        if time_of_day <= TIME2:
                            samples[day][2] += 1 # swipes by 12:00 (incl 12:00)
                        if time_of_day <= TIME3:
                            samples[day][3] += 1 # swipes by 12:15 (incl 12:15)
                if day_of_the_week in (6, 0):
                    if LUNCH_START_WEEKEND <= time_of_day <= LUNCH_END:
                        total_swipes[day] += 1
                        if time_of_day <= TIME1:
                            samples[day][1] += 1 # swipes by 11:45 (incl 11:45)
                        if time_of_day <= TIME2:
                            samples[day][2] += 1 # swipes by 12:00 (incl 12:00)
                        if time_of_day <= TIME3:
                            samples[day][3] += 1 # swipes by 12:15 (incl 12:15)

    # assigning labels for the sample data
    for z in range(TOTAL_DAYS):
        if total_swipes[z] < low_traffic_threshold:
            labels[z] = -1
        if total_swipes[z] > high_traffic_threshold:
            labels[z] = 1
        
    return (samples, labels)

def decision_tree(samples, labels, bldg_id, given):
    # decision tree classifier for "given" (in an array in the form of samples: [0, 0, 0, 0])
    
    clf = tree.DecisionTreeClassifier(random_state=65535)
    clf.fit(samples, labels)

    prediction = clf.predict(given)[0]

    #graphviz https://scikit-learn.org/stable/modules/generated/sklearn.tree.export_graphviz.html
    output_file = str(bldg_id) + ".dot"
    
    tree.export_graphviz(clf, out_file=output_file, feature_names=["Day of the Week", "Swipes by 11:45am", "Swipes by 12:00pm", "Swipes by 12:15pm"], class_names=["low-traffic day", "normal day", "high-traffic day"])

    return (prediction)
            
def main():

    bldg_id_BR = get_building_code("BR")
    bldg_id_SM = get_building_code("SM")
    low_traffic_threshold_BR, high_traffic_threshold_BR = get_mean_traffic(bldg_id_BR)
    low_traffic_threshold_SM, high_traffic_threshold_SM = get_mean_traffic(bldg_id_SM)

    samples_BR, labels_BR = assign_training_labels_samples(bldg_id_BR, low_traffic_threshold_BR, high_traffic_threshold_BR)
    samples_SM, labels_SM = assign_training_labels_samples(bldg_id_SM, low_traffic_threshold_SM, high_traffic_threshold_SM)

    # predict for Branford: 78 swipes by 11:45am, 131 swipes by 12:00pm, 232 swipes by 12:15pm on a Monday
    given_BR = [[1, 78, 131, 232]]

    # predict for Silliman: 90 swipes by 11:45am, 171 swipes by 12:00pm, 230 swipes by 12:15pm on a Sunday
    given_SM = [[0, 90, 171, 230]]

    prediction_BR = decision_tree(samples_BR, labels_BR, bldg_id_BR, given_BR)
    prediction_SM = decision_tree(samples_SM, labels_SM, bldg_id_SM, given_SM)

    if prediction_BR == -1:
        prediction_BR_text = "a low-traffic day."
    if prediction_BR == 0:
        prediction_BR_text = "a normal day."
    if prediction_BR == 1:
        prediction_BR_text = "a high-traffic day"

    if prediction_SM == -1:
        prediction_SM_text = "a low-traffic day."
    if prediction_SM == 0:
        prediction_SM_text = "a normal day."
    if prediction_SM == 1:
        prediction_SM_text = "a high-traffic day"

    print ("The prediction for Branford with 78 swipes by 11:45am, 131 swipes by 12:00pm, and 232 swipes by 12:15pm on a Monday is: ", prediction_BR_text)
    print ("The prediction for Silliman with 90 swipes by 11:45am, 171 swipes by 12:00pm, and 230 swipes by 12:15pm on a Sunday is: ", prediction_SM_text)

if __name__ == "__main__":
    main()