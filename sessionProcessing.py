import pandas as pd
import statistics
import csv
import os
from operator import itemgetter
import openpyxl as xl


sessions_max_grades = [5, 6, 4, 5, 4, 4]

# ---------------------------------------------- I/O ----------------------------------------------


def log_to_csv(filename):
    with open(filename, 'r') as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split("\t") for line in stripped if line)
        with open(f'Data/logs.csv', 'w') as out_file:
            writer = csv.writer(out_file)
            writer.writerows(lines)


def file_write(filename, my_data):
    my_file = open(filename, 'w')
    with my_file:
        writer = csv.writer(my_file)
        writer.writerows(my_data)
    print("Writing file complete")


# ---------------------------------------------- Getters ----------------------------------------------

def get_all_students(log_file):
    log_data = pd.read_csv(log_file)
    return list(log_data.Student_Id)


def get_student_log(log_file, student_id):
    with open(log_file, 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)
    x = your_list[student_id]
    return x


def get_session_data(session_sheet, student_id):
    session_id = session_sheet['session'][0]
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
    mouse_wheel_rate = total_mouse_wheel  #/ (total_time - total_idle_time)
    mouse_wheel_click_rate = total_mouse_wheel_click  #/ (total_time - total_idle_time)
    mouse_click_left_rate = total_mouse_click_left  #/ (total_time - total_idle_time)
    mouse_click_right_rate = total_mouse_click_right  #/ (total_time - total_idle_time)
    mouse_movement_rate = total_mouse_movement # / (total_time - total_idle_time)
    keystroke_rate = total_keystroke  #/ (total_time - total_idle_time)
    intermediate_grades_file = xl.load_workbook('Data/intermediate_grades.xlsx')
    session_grade = get_intermediate_grade(intermediate_grades_file, student_id, session_id)
    # -----------------
    data = [session_id, activity, st_time, end_time, total_idle_time, mouse_wheel_rate,
            mouse_wheel_click_rate, mouse_click_left_rate, mouse_click_right_rate, mouse_movement_rate,
            keystroke_rate, session_grade]
    return data


def get_intermediate_grade(intermediate_grades, student_id, session_id):
    if session_id == 1:
        return 1.00
    sheet = intermediate_grades['Intermediate grades']
    cell = sheet.cell(student_id + 1, session_id)
    return 1.0 * cell.value / sessions_max_grades[session_id-1]


# --------------------------------------------- Handlers  ---------------------------------------------

def handle_session_absence(session_number):
    print(f"student was absent in session {session_number}")


def handle_mode_not_unique(data_list):
    lst_count = [[x, data_list.count(x)] for x in set(data_list)]
    lst_count = sorted(lst_count, reverse=True, key=itemgetter(1))
    maximum = lst_count[0][1]
    lst_count = [x for x in set(data_list) if data_list.count(x) >= maximum]
    return lst_count[0]


# ------------------------------------------- Logic Methods ---------------------------------------------


def process_student_sessions(student_id, data_source):
    filtered_features = [["session_id", "activity", "st_time", "end_time", "total_idle_time", "mouse_wheel_rate",
                          "mouse_wheel_click_rate", "mouse_click_left_rate", "mouse_click_right_rate",
                          "mouse_movement_rate", "keystroke_rate", "intermediate_grade"]
                         ]

    # get the student log in all sessions to handle session absence
    student_session_log = get_student_log('Data/logs.csv', student_id)

    for session in os.listdir(data_source):
        print(f'Started processing {session}')
        session_number = int(session.split(" ")[1])

        if student_session_log[session_number] == '0':
            handle_session_absence(session_number)
        else:
            try:
                my_file = f'{data_source}/{session}/{student_id}.csv'
                session_data = pd.read_csv(my_file)
                session_row = get_session_data(session_data, student_id)
                filtered_features.append(session_row)
            except FileNotFoundError as e:
                print(f'wrong data in log file: {student_session_log} in session {session_number}')
                handle_session_absence(session_number)
        print("")

    file = f"Data/Processed/{student_id}.csv"
    if not os.path.exists("Data/Processed"):
        os.makedirs("Data/Processed")
    file_write(file, filtered_features)


# ------------------------------------------- Main ---------------------------------------------


log_to_csv("Data/logs.txt")
data_path = 'Data/Processes/'

for student in get_all_students("Data/logs.csv"):
    print(f'-------------- student: {student} --------------')
    process_student_sessions(student, data_path)

print("Process Completed")
