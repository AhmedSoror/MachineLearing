import os
import pandas as pd
import csv
import openpyxl as xl
import xlrd
from statistics import mean

# ------------------------------------ constants --------------------------------------------

final_grades_xlsx = "Data/final_grades.xlsx"
sheet1 = "Exam (First time)"
sheet2 = "Exam (Second time)"
sessions_boundaries = []
average_grades = []
wb = xlrd.open_workbook(final_grades_xlsx)
sheet1_pandas = pd.read_excel(final_grades_xlsx, index_col=0, sheet_name=sheet1)
sheet2_pandas = pd.read_excel(final_grades_xlsx, index_col=0, sheet_name=sheet2)
students_final_grades = []
# ------------------------------------ init --------------------------------------------


def init():
    global sessions_boundaries, average_grades
    sheet = wb.sheet_by_index(0)
    columns = sheet.ncols
    sessions_boundaries = get_session_boundaries(sheet, columns)
    average_grades = get_average_grades()


def get_session_boundaries(sheet, columns):
    sessions_limits = []
    session_end = 1
    s = sheet.cell_value(0, 1)
    session_id = s.split(" ")[1].split(".")[0]
    for i in range(1, columns - 1):
        s = sheet.cell_value(0, i)
        current_session_id = s.split(" ")[1].split(".")[0]
        if current_session_id == session_id:
            session_end = i
        else:
            session_id = current_session_id
            sessions_limits.append(session_end + 1)

    sessions_limits.append(session_end + 1)
    return sessions_limits
# ------------------------------------- average -------------------------------------


def get_average_grades():

    x = get_average_grades_helper(sheet1_pandas)
    y = get_average_grades_helper(sheet2_pandas)
    return [x, y]


def get_average_grades_helper(df):
    x = df.mean()
    grades = []
    session = 1
    sum_temp = 0
    for i in range(0, sessions_boundaries[-1]):
        if i < sessions_boundaries[session - 1]-1:
            sum_temp += x[i]
        else:
            grades.append(round(sum_temp, 2))
            sum_temp = x[i]
            session += 1
    return grades


# ------------------------------------- Final Grade -------------------------------------


def get_grades(sheet, row_number):
    columns = sheet.ncols
    grades = []
    session = 1
    sum_temp = 0
    for i in range(1, columns - 1):
        x = sheet.cell_value(row_number, i)
        if i < sessions_boundaries[session - 1]:
            sum_temp += float(x)
        else:
            grades.append(sum_temp)
            sum_temp = float(x)
            session += 1
    grades.append(sum_temp)
    return grades


def find_final_grades(student_id):
    result = [[], []]

    first_time_sheet = wb.sheet_by_index(0)
    second_time_sheet = wb.sheet_by_index(1)

    result[0] = get_grades(first_time_sheet, student_id)
    result[1] = get_grades(second_time_sheet, student_id)
    return result


# ------------------------------------- Main -------------------------------------


def run():
    init()

    row = 1
    x = find_final_grades(row)
    print(average_grades)
    print(x)

run()


'''
    *) search for students      get_student_row(student_id)    returns row
    then add these data to each student.csv 
'''