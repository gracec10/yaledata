# Grace Cheung
# gvc8
# CPSC 310
# HW 2
# Part B
# 2/21/2020

import csv

THREE_AM= 180 # 3am in minutes
FIVE_AM = 300 # 5am in minutes
LUNCH_START = 660 # earliest lunch starts for all days/colleges is 11:00am
DINNER_END = 1200 # latest dinner ends for all days/colleges is 8:00pm

# building_codes.csv = id, code, name, type
# door_data.csv = day, day_of_the_week, student_id, time_of_day, building, is_dining_hall

def get_students():
    # parse student_list.txt
    students = []
    with open('student_list.txt', 'r') as txtfile1: #https://kite.com/python/answers/how-to-iterate-through-the-lines-of-a-file-in-python
        for line in txtfile1:
            stripped_line = line.strip()
            students.append(stripped_line)
    return (students)

def skip_meals(students):
    # Find all students who skip more than 7 brunch/lunch or dinner meals in a week at least twice.
    meal_skippers = []
    student_meals = {}
    # dictionary with the key being each student ID, and the value being an array with each element representing lunch/brunch + dinner for that week (there are 4 weeks in 28 days)
    # the last element in the array is the counter
    for student in students:
        student_meals[student] = [0, 0, 0, 0, 0]
    with open('door_data.csv') as csvfile1:
        readCSV1 = csv.reader(csvfile1, delimiter=',')
        for row in readCSV1:
            if row[2] in students:
                curr_student = row[2]
                curr_day = int(row[0])
                if LUNCH_START <= int(row[3]) <= DINNER_END and row[5] == "1":
                    if 0 <= curr_day <= 6:
                        student_meals[curr_student][0] += 1
                    if 7 <= curr_day <= 13:
                        student_meals[curr_student][1] += 1
                    if 14 <= curr_day <= 20:
                        student_meals[curr_student][2] += 1
                    if 21 <= curr_day <= 27:
                        student_meals[curr_student][3] += 1
    
    # there are 14 brunch/lunch + dinner meals in a week. I am looking for students who have less than 7 meals for two weeks.
    for student in student_meals:
        for meals in student_meals[student]:
            if meals < 7:
                student_meals[student][4] += 1
    
    for student in student_meals:
        if student_meals[student][4] >= 2:
            meal_skippers.append(student)

    return (meal_skippers)


def skip_class(students):
    # Find all students who skip all classes and academic activities for a week.
    # building codes: 1 = academic, 2 = library
    school_bldgs = []
    student_presence = {}
    school_skippers = []

    for student in students:
        student_presence[student] = [0, 0, 0, 0]

    # parse building codes to find a list of academic buildings and libraries
    with open('building_codes.csv') as csvfile2:
        readCSV2 = csv.reader(csvfile2, delimiter=',')
        for row in readCSV2:
            if row[3] in ("1", "2"):
                school_bldgs.append(row[0])
    
    with open('door_data.csv') as csvfile3:
        readCSV3 = csv.reader(csvfile3, delimiter=',')
        for row in readCSV3:
            if row[2] in students:
                curr_student = row[2]
                curr_day = int(row[0])
                if row[4] in school_bldgs:
                    if 0 <= curr_day <= 6:
                        student_presence[curr_student][0] += 1
                    if 7 <= curr_day <= 13:
                        student_presence[curr_student][1] += 1
                    if 14 <= curr_day <= 20:
                        student_presence[curr_student][2] += 1
                    if 21 <= curr_day <= 27:
                        student_presence[curr_student][3] += 1
    
    for student in student_presence:
        for week in student_presence[student]:
            if week == 0 and student not in school_skippers:
                school_skippers.append(student)
    
    return (school_bldgs)

def late_night(students):
    # Find all students who swipe back into a residential college between 3:00am and 5:00am on at least 3 non-weekend nights (not Friday or Saturday night).
    late_nighters = []
    student_late = {}
    res_bldgs =[]

    # parse building codes to find a list of residential colleges (type 3)
    with open('building_codes.csv') as csvfile4:
        readCSV4 = csv.reader(csvfile4, delimiter=',')
        for row in readCSV4:
            if row[3] == "3":
                res_bldgs.append(row[0])

    for student in students:
        student_late[student] = 0

    with open('door_data.csv') as csvfile5:
        readCSV5 = csv.reader(csvfile5, delimiter=',')
        for row in readCSV5:
            if row[2] in students:
                if row[4] in res_bldgs and THREE_AM <= int(row[3]) <= FIVE_AM and row[1] in ("0", "1", "2", "3", "4"):
                    student_late[row[2]] += 1
    
    for student in student_late:
        if student_late[student] >= 3:
            late_nighters.append(student)
    
    return(late_nighters)

def hermit(students):
    # Find all students who, on at least 3 days, do not leave a residential college or swipe into a dining hall.
    hermits = []
    student_hermit = {}

    for student in students:
        student_hermit[student] = [0 for x in range(29)]

    with open('door_data.csv') as csvfile6:
        readCSV6 = csv.reader(csvfile6, delimiter=',')
        for row in readCSV6:
            if row[2] in students:
                curr_day = int(row[0])
                curr_student = row[2]
                student_hermit[curr_student][curr_day] += 1
    
    for student in student_hermit:
        for day in student_hermit[student]:
            if day == 0:
                student_hermit[student][28] += 1
    
    for student in student_hermit:
        if student_hermit[student][28] >= 3:
            hermits.append(student)
    
    return(hermits)

def send_email(meal_skippers, school_skippers, late_nighters, hermits):
    # combine list of students
    students_contact = {}
    students_total = []

    for x in meal_skippers:
        students_total.append(x)
    for x in school_skippers:
        if x not in students_total:
            students_total.append(x)
    for x in late_nighters:
        if x not in students_total:
            students_total.append(x)    
    for x in hermits:
        if x not in students_total:
            students_total.append(x)

    # send automated email
    with open('ug_database.csv') as csvfile7:
        readCSV7 = csv.reader(csvfile7, delimiter=',')
        for row in readCSV7:
            pronouns = row[4]
            ID = row[0]
            if ID in students_total:
                students_contact[ID] = pronouns

    return (students_contact)


def main():
    students = get_students()
    
    meal_skippers = skip_meals(students)
    school_skippers = skip_class(students)
    late_nighters = late_night(students)
    hermits = hermit(students)

    students_contact = send_email(meal_skippers, school_skippers, late_nighters, hermits)

    for student in students_contact:
        print("Dear ", student, "\n This is Yale University emailing because we are concerned about your mental health. There are many resources available for you!")
        print("Dear parent of ", student, " (", students_contact[student], ") ", "\n This is Yale University emailing because we are concerned about your child's mental health. There are many resources available for", students_contact[student], "!\n")

if __name__ == "__main__":
    main()