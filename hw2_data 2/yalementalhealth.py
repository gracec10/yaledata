# Grace Cheung
# gvc8
# CPSC 310
# HW 2
# Part B
# 2/21/2020

import csv

THREE_AM= 180 # 3am in minutes
FIVE_AM = 300 # 5am in minutes

def get_students():
    # parse student_list.txt
    students = []
    with open('student_list.txt', 'r') as txtfile1: #https://kite.com/python/answers/how-to-iterate-through-the-lines-of-a-file-in-python
        for line in txtfile1:
            stripped_line = line.strip()
            students.append(stripped_line)
    return (students)


# def skip_meals():
#     # Find all students who skip more than 7 brunch/lunch or dinner meals in a week at least twice.


# def skip_class():
#     # Find all students who skip all classes and academic activities for a week.

# def late_night():
#     # Find all students who swipe back into a residential college between 3:00am and 5:00am on at least 3 non-weekend nights (not Friday or Saturday night).

# def hermit():
#     # Find all students who, on at least 3 days, do not leave a residential college or swipe into a dining hall.

def main():
    students = get_students()
    print(students)

if __name__ == "__main__":
    main()