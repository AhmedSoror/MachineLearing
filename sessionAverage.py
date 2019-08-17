import pandas as pd
import statistics
import csv
import os
from operator import itemgetter
import openpyxl as xl


# ---------------------------------------------- Import from Common File ----------------------------------------------
from commonMethods import file_write
from commonMethods import handle_mode_not_unique

from commonMethods import sessions_in_parent
from commonMethods import sessions_collapsed
from commonMethods import data_processed_students
from commonMethods import sessions_average_csv
from commonMethods import log_csv_path
from commonMethods import sessions_max_grades
# ---------------------------------------------- init ----------------------------------------------


def init():
    if not os.path.exists(sessions_collapsed):
        os.makedirs(sessions_collapsed)
    header = "student_id,session_id,activity,start_time,end_time,total_idle_time,mouse_wheel,mouse_wheel_click,mouse_click_left,mouse_click_right,mouse_movement,keystroke,intermediate_grade"

    for i in range(1, 7):
        with open(f'{sessions_collapsed}/session {i}.csv', 'w+') as fd:
            fd.write(header+"\n")


def get_student_log(student_id):
    with open(log_csv_path, 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)
    x = your_list[student_id]
    return x


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


def get_average_session_data(session_id):
    session_sheet = pd.read_csv(f'{sessions_collapsed}/session {session_id}.csv')
    activity = handle_mode_not_unique(list(session_sheet.activity))
    try:
        activity = statistics.mode(session_sheet['activity'])
    except statistics.StatisticsError as e:
        activity = handle_mode_not_unique(list(session_sheet.activity))
        # print(f'Handled no unique mode in session{session_id}')
    # ------- Getting all variables -------
    st_time = min(session_sheet['start_time'])                                                      # not needed
    end_time = max(session_sheet['end_time'])                                                       # not needed
    t1 = pd.to_datetime(st_time)                                                                    # not needed
    t2 = pd.to_datetime(end_time)                                                                   # not needed
    total_time = pd.Timedelta(t2 - t1).seconds / 60.0  # in minutes                                 # not needed
    total_idle_time = sum(session_sheet['total_idle_time']) / 60000.0  # in minutes                       # not needed
    total_mouse_wheel = sum(session_sheet['mouse_wheel'])
    total_mouse_wheel_click = sum(session_sheet['mouse_wheel_click'])
    total_mouse_click_left = sum(session_sheet['mouse_click_left'])
    total_mouse_click_right = sum(session_sheet['mouse_click_right'])
    total_mouse_movement = sum(session_sheet['mouse_movement'])
    total_keystroke = sum(session_sheet['keystroke'])

    # mouse_wheel_rate = total_mouse_wheel/(total_time - total_idle_time)
    # mouse_wheel_click_rate = total_mouse_wheel_click / (total_time - total_idle_time)
    # mouse_click_left_rate = total_mouse_click_left  / (total_time - total_idle_time)
    # mouse_click_right_rate = total_mouse_click_right  / (total_time - total_idle_time)
    # mouse_movement_rate = total_mouse_movement / (total_time - total_idle_time)
    # keystroke_rate = total_keystroke  / (total_time - total_idle_time)

    session_grade = session_sheet['intermediate_grade'].mean()
    # -----------------
    data = [session_id, activity, st_time, end_time, total_idle_time, total_mouse_wheel,
            total_mouse_wheel_click, total_mouse_click_left, total_mouse_click_right, total_mouse_movement,
            total_keystroke, session_grade]
    return data


def get_all_sessions_averages():
    filtered_features = [["session_id", "activity", "start_time", "end_time", "total_idle_time", "mouse_wheel",
                          "mouse_wheel_click", "mouse_click_left", "mouse_click_right",
                          "mouse_movement", "keystroke", "intermediate_grade"]
                         ]

    for session in os.listdir(sessions_collapsed):
        print(f'Started processing {session}')
        session_number = int(session.split(" ")[1].split(".")[0])
        session_average = get_average_session_data(session_number)
        filtered_features.append(session_average)

        print("")

    # student_session_log = get_student_log(student_id)
    # if student_session_log[session_number] == '0':
    #     handle_session_absence(session_number)


    file = sessions_average_csv
    file_write(file, filtered_features)


# --------------------------------------------- Main ---------------------------------------------
def run():
    init()
    collapse_sessions()
    get_all_sessions_averages()


run()
