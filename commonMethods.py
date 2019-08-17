import os
import pandas as pd
import csv
import openpyxl as xl
import xlrd
from statistics import mean
import statistics
from operator import itemgetter


# -------------------------------- Constants & Global Variables ----------------------------------------

final_grades_xlsx = "Data/final_grades.xlsx"
data_processed_students = "Data_Processed/Students"

sessions_in_parent = "Data_Processed/Processes"
sessions_collapsed = "Data_Processed/Sessions_Collapsed/"
sessions_average_csv = "Data_Processed/sessions_average.csv"
log_csv_path = "Data_Processed/logs.csv"
log_csv_parent = "Data_Processed"
log_txt_path = "Data/logs.txt"
intermediate_grades_xlsx = "Data/intermediate_grades.xlsx"
features_string = "session_id,student_id,exercise,activity,start_time,end_time,idle_time,mouse_wheel,mouse_wheel_click,mouse_click_left,mouse_click_right,mouse_movement,keystroke"
sessions_csv_parent = "Data_Processed/Processes"
sessions_max_grades = [5, 6, 4, 5, 4, 4]
final_grades_max = [5, 5, 10, 25, 15, 40]

# -------------------------------- Methods ----------------------------------------


def get_student_ids():
    student_ids_list = []
    for student in os.listdir(data_processed_students):
        student_id = int(student.split(".")[0])
        student_ids_list.append(student_id)
    student_ids_list.sort()
    return student_ids_list


def write_csv_file(filename, my_data):
    my_file = open(filename, 'w+')
    with my_file:
        writer = csv.writer(my_file)
        writer.writerows(my_data)
    # print("Writing file complete")


def add_sorted_rows(filename, my_data, col_name):
    add_rows_to_csv(filename, my_data)
    sort_csv(filename, col_name)


def add_rows_to_csv(filename, my_data):
    my_file = open(filename, 'a+')
    with my_file:
        writer = csv.writer(my_file)
        writer.writerows(my_data)
    # print("Writing file complete")


def sort_csv(file_path,col_name):
    df = pd.read_csv(file_path)
    df = df.sort_values(by=[f'{col_name}'])
    df.to_csv(file_path, index=False)


def handle_mode_not_unique(data_list):
    lst_count = [[x, data_list.count(x)] for x in set(data_list)]
    lst_count = sorted(lst_count, reverse=True, key=itemgetter(1))
    maximum = lst_count[0][1]
    lst_count = [x for x in set(data_list) if data_list.count(x) >= maximum]
    return lst_count[0]


def get_student_log(student_id):
    with open(log_csv_path, 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)

    return your_list[student_id]

