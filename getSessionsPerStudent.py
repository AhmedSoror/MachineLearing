import pandas as pd
import statistics
import csv
import os
from operator import itemgetter
import openpyxl as xl

# ---------------------------------------------- Import from Common File ----------------------------------------------
from commonMethods import handle_mode_not_unique
from commonMethods import get_student_log


from commonMethods import sessions_max_grades
from commonMethods import sessions_in_parent
from commonMethods import log_csv_parent
from commonMethods import log_csv_path
from commonMethods import log_txt_path
from commonMethods import intermediate_grades_xlsx
from commonMethods import data_processed_students
from commonMethods import write_csv_file

# ---------------------------------------------- init ----------------------------------------------


def init():
    if not os.path.exists(data_processed_students):
        os.makedirs(data_processed_students)

# ---------------------------------------------- I/O ----------------------------------------------


def log_to_csv(filename):
    with open(filename, 'r') as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split("\t") for line in stripped if line)
        with open(log_csv_path, 'w') as out_file:
            writer = csv.writer(out_file)
            writer.writerows(lines)

# ---------------------------------------------- Getters ----------------------------------------------


def get_all_students(log_file):
    log_data = pd.read_csv(log_file)
    return list(log_data["Student Id"])


def get_session_data(session_sheet, student_id):
    session_id = session_sheet['session_id'][0]
    activity = handle_mode_not_unique(list(session_sheet.activity))
    try:
        activity = statistics.mode(session_sheet['activity'])
    except statistics.StatisticsError as e:
        activity = handle_mode_not_unique(list(session_sheet.activity))
        # print(f'Handled no unique mode in session{session_id}')
    # ------- Getting all variables -------
    st_time = min(session_sheet['start_time'])
    end_time = max(session_sheet['end_time'])
    t1 = pd.to_datetime(st_time)
    t2 = pd.to_datetime(end_time)
    total_time = pd.Timedelta(t2 - t1).seconds / 60.0  # in minutes
    total_idle_time = sum(session_sheet['idle_time']) / 60000.0  # in minutes
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

    intermediate_grades_file = xl.load_workbook(intermediate_grades_xlsx)
    session_grade = get_intermediate_grade(intermediate_grades_file, student_id, session_id)
    # -----------------
    data = [session_id, activity, st_time, end_time, total_idle_time, total_mouse_wheel,
            total_mouse_wheel_click, total_mouse_click_left, total_mouse_click_right, total_mouse_movement,
            total_keystroke, session_grade]
    return data


def get_intermediate_grade(intermediate_grades, student_id, session_id):
    if session_id == 1:
        return 1.00
    sheet = intermediate_grades['Intermediate grades']
    cell = sheet.cell(student_id + 1, session_id)
    return 1.0 * cell.value / sessions_max_grades[session_id-1]


# --------------------------------------------- Handlers  ---------------------------------------------

def handle_session_absence(session_number):
    pass
    # print(f"student was absent in session {session_number}")

# ------------------------------------------- Logic Methods ---------------------------------------------


def process_student_sessions(student_id):
    filtered_features = [["session_id", "activity", "start_time", "end_time", "total_idle_time", "mouse_wheel",
                          "mouse_wheel_click", "mouse_click_left", "mouse_click_right",
                          "mouse_movement", "keystroke", "intermediate_grade"]
                         ]

    # get the student log in all sessions to handle session absence
    student_session_log = get_student_log(student_id)

    for session in os.listdir(sessions_in_parent):
        # print(f'Started processing {session}')
        session_number = int(session.split(" ")[1])

        if student_session_log[session_number] == '0':
            handle_session_absence(session_number)
        else:
            try:
                my_file = f'{sessions_in_parent}/{session}/{student_id}.csv'
                session_data = pd.read_csv(my_file)
                session_row = get_session_data(session_data, student_id)
                filtered_features.append(session_row)
            except FileNotFoundError as e:
                # print(f'wrong data in log file: {student_session_log} in session {session_number}')
                handle_session_absence(session_number)
        # print("")

    file = f"{data_processed_students}/{student_id}.csv"
    write_csv_file(file, filtered_features)


# ------------------------------------------- Run ---------------------------------------------
def run():
    init()
    log_to_csv(log_txt_path)

    for student in get_all_students(log_csv_path):
        # print(f'-------------- student: {student} --------------')
        process_student_sessions(student)

    # print("Process Completed")


run()
