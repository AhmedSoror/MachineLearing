import os
import pandas as pd
import csv
import openpyxl as xl
import xlrd
from statistics import mean

# -------------------------------- Constants & Global Variables ----------------------------------------

final_grades_xlsx = "Data/final_grades.xlsx"
data_processed_students = "Data_Processed/Students"
sheet1 = "Exam (First time)"
sheet2 = "Exam (Second time)"

final_grades_max = [5, 5, 10, 25, 15, 40]

wb = xlrd.open_workbook(final_grades_xlsx)
sheet1_pandas = pd.read_excel(final_grades_xlsx, index_col=0, sheet_name=sheet1)
sheet2_pandas = pd.read_excel(final_grades_xlsx, index_col=0, sheet_name=sheet2)

sessions_boundaries = []
average_grades = []
sheet1_pointer = 1                                         # starts from 1
sheet2_pointer = 1

# ------------------------------------ init & helpers --------------------------------------------


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


def get_student_ids():
    student_ids_list = []
    for student in os.listdir(data_processed_students):
        student_id = int(student.split(".")[0])
        student_ids_list.append(student_id)
    student_ids_list.sort()
    return student_ids_list
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
            grade_percent = sum_temp / final_grades_max[session-1]
            grades.append(round(grade_percent, 4))
            sum_temp = x[i]
            session += 1
    return grades


# ------------------------------------- Final Grade -------------------------------------


def get_grade_by_row(sheet, row_number):
    columns = sheet.ncols
    grades = []
    session = 1
    sum_temp = 0
    for i in range(1, columns - 1):
        x = sheet.cell_value(row_number, i)
        if i < sessions_boundaries[session - 1]:
            sum_temp += float(x)
        else:
            grade_percent = sum_temp / final_grades_max[session-1]
            grades.append(round(grade_percent, 4))
            sum_temp = float(x)
            session += 1
    grade_percent = sum_temp / final_grades_max[session-1]
    grades.append(round(grade_percent, 4))
    return grades


def find_student_final_grade(student_id):
    global sheet1_pointer
    global sheet2_pointer

    result = [[], []]
    first_time_sheet = wb.sheet_by_index(0)
    second_time_sheet = wb.sheet_by_index(1)
    if first_time_sheet.cell_value(sheet1_pointer, 0) == student_id:
        result[0] = get_grade_by_row(first_time_sheet, sheet1_pointer)
        sheet1_pointer += 1
    else:
        result[0] = average_grades[0]

    if second_time_sheet.cell_value(sheet2_pointer, 0) == student_id:
        result[1] = get_grade_by_row(second_time_sheet, sheet2_pointer)
        sheet2_pointer += 1
    else:
        result[1] = average_grades[1]

    return result


def get_all_students_grades():
    student_ids_list = get_student_ids()
    for student in student_ids_list:
        student_grade = find_student_final_grade(student)
        csv_input = pd.read_csv(f'{data_processed_students}/{student}.csv')
        print(student_grade[0])
        csv_input['first_exam'] = student_grade[0]
        csv_input['second_exam'] = student_grade[1]
        csv_input.to_csv(f'{data_processed_students}/{student}.csv', index=False)


# ------------------------------------- Main -------------------------------------


def run():
    init()
    get_all_students_grades()


run()

