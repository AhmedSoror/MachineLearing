import os

import pandas as pd
import csv


# with open('Data/Processed/1.csv') as csvfile:
#     readCSV = csv.reader(csvfile)
#     for row in readCSV:
#         print(row)
# for student in os.listdir("Data/Processed"):
#     student_number = int(student.split(".")[0])
#     print(student_number)

data_processed_students = "Data_Processed/Students"
if not os.path.exists(data_processed_students):
    os.makedirs(data_processed_students)
