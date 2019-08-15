import pandas as pd
import statistics
import csv
import os
from operator import itemgetter
import openpyxl as xl


# ---------------------------------------------- Constants ----------------------------------------------
sessions_in_parent = "Data_Processed/Processes"
sessions_collapsed = "Data_Processed/Sessions_Collapsed/"
data_processed_students = "Data_Processed/Students"

# ---------------------------------------------- init ----------------------------------------------


def init():
    if not os.path.exists(sessions_collapsed):
        os.makedirs(sessions_collapsed)
    header = "student_id,session_id,activity,start_time,end_time,total_idle_time,mouse_wheel_rate,mouse_wheel_click_rate,mouse_click_left_rate,mouse_click_right_rate,mouse_movement_rate,keystroke_rate,intermediate_grade"

    for i in range(1, 7):
        with open(f'{sessions_collapsed}/session {i}.csv', 'w+') as fd:
            fd.write(header+"\n")


def get_session_from_student(source_path, output_path, student_id):
    header_loop = True
    for line in open(f'{source_path}/{student_id}.csv', "r"):
        if header_loop:
            header_loop = False
            continue
        session_id = line.split(",")[0]
        line = f'{student_id}, {line}'
        with open(f'{output_path}/session {session_id}.csv', 'a') as fd:
            fd.write(line)


def collapse_sessions():
    for current_student_id in range(1, 116):
        try:
            get_session_from_student(data_processed_students, sessions_collapsed, current_student_id)
        except FileNotFoundError as e:
            print(f'no processed file found for student {current_student_id}')


# --------------------------------------------- Handlers  ---------------------------------------------


# def handle_mode_not_unique(data_list):
#     lst_count = [[x, data_list.count(x)] for x in set(data_list)]
#     lst_count = sorted(lst_count, reverse=True, key=itemgetter(1))
#     maximum = lst_count[0][1]
#     lst_count = [x for x in set(data_list) if data_list.count(x) >= maximum]
#     return lst_count[0]

#
# def get_average_session_data(session_sheet, student_id):
#     session_id = session_sheet['session_id'][0]
#     activity = handle_mode_not_unique(list(session_sheet.activity))
#     try:
#         activity = statistics.mode(session_sheet['activity'])
#     except statistics.StatisticsError as e:
#         activity = handle_mode_not_unique(list(session_sheet.activity))
#         # print(f'Handled no unique mode in session{session_id}')
#     # ------- Getting all variables -------
#     st_time = min(session_sheet['start_time'])
#     end_time = max(session_sheet['end_time'])
#     t1 = pd.to_datetime(st_time)
#     t2 = pd.to_datetime(end_time)
#     total_time = pd.Timedelta(t2 - t1).seconds / 60.0  # in minutes
#     total_idle_time = sum(session_sheet['idle_time']) / 60000.0  # in minutes
#     total_mouse_wheel = sum(session_sheet['mouse_wheel'])
#     total_mouse_wheel_click = sum(session_sheet['mouse_wheel_click'])
#     total_mouse_click_left = sum(session_sheet['mouse_click_left'])
#     total_mouse_click_right = sum(session_sheet['mouse_click_right'])
#     total_mouse_movement = sum(session_sheet['mouse_movement'])
#     total_keystroke = sum(session_sheet['keystroke'])
#     mouse_wheel_rate = total_mouse_wheel  #/ (total_time - total_idle_time)
#     mouse_wheel_click_rate = total_mouse_wheel_click  #/ (total_time - total_idle_time)
#     mouse_click_left_rate = total_mouse_click_left  #/ (total_time - total_idle_time)
#     mouse_click_right_rate = total_mouse_click_right  #/ (total_time - total_idle_time)
#     mouse_movement_rate = total_mouse_movement # / (total_time - total_idle_time)
#     keystroke_rate = total_keystroke  #/ (total_time - total_idle_time)
#     intermediate_grades_file = xl.load_workbook('Data/intermediate_grades.xlsx')
#     session_grade = get_intermediate_grade(intermediate_grades_file, student_id, session_id)
#     # -----------------
#     data = [session_id, activity, st_time, end_time, total_idle_time, mouse_wheel_rate,
#             mouse_wheel_click_rate, mouse_click_left_rate, mouse_click_right_rate, mouse_movement_rate,
#             keystroke_rate, session_grade]
#     return data

# --------------------------------------------- Main ---------------------------------------------


init()
collapse_sessions()
