import pandas as pd
import statistics
import os


# ---------------------------------------------- Import from Common File ----------------------------------------------
from commonMethods import write_csv_file
from commonMethods import add_sorted_rows
from commonMethods import handle_mode_not_unique
from commonMethods import get_student_log
from commonMethods import get_student_ids
from commonMethods import collapse_sessions

from commonMethods import sessions_collapsed
from commonMethods import data_processed_students
from commonMethods import sessions_average_csv
# ---------------------------------------------- init ----------------------------------------------


def init():
    if not os.path.exists(sessions_collapsed):
        os.makedirs(sessions_collapsed)
    header = "student_id,session_id,activity,start_time,end_time,total_idle_time,mouse_wheel,mouse_wheel_click," \
             "mouse_click_left,mouse_click_right,mouse_movement,keystroke,intermediate_grade "

    for i in range(1, 7):
        with open(f'{sessions_collapsed}/session {i}.csv', 'w+') as fd:
            fd.write(header+"\n")


def get_average_session_data(session_id):
    session_sheet = pd.read_csv(f'{sessions_collapsed}/session {session_id}.csv')
    # activity = handle_mode_not_unique(list(session_sheet.activity))
    try:
        activity = statistics.mode(session_sheet['activity'])
    except statistics.StatisticsError:
        activity = handle_mode_not_unique(list(session_sheet.activity))
        # print(f'Handled no unique mode in session{session_id}')
    # ------- Getting all variables -------
    st_time = min(session_sheet['start_time'])                                                      # not needed
    end_time = max(session_sheet['end_time'])                                                       # not needed
    # t1 = pd.to_datetime(st_time)                                                                    # not needed
    # t2 = pd.to_datetime(end_time)                                                                   # not needed
    # total_time = pd.Timedelta(t2 - t1).seconds / 60.0  # in minutes                                 # not needed
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
        # print(f'Started processing {session}')
        session_number = int(session.split(" ")[1].split(".")[0])
        session_average = get_average_session_data(session_number)
        filtered_features.append(session_average)

        # print("")

    file = sessions_average_csv
    write_csv_file(file, filtered_features)
    return filtered_features


def add_session_averages_to_students():
    student_ids_list = get_student_ids()
    filtered_features = get_all_sessions_averages()
    for student in student_ids_list:
        file = f'{data_processed_students}/{student}.csv'
        # csv_input = pd.read_csv(file)
        student_session_log = get_student_log(student)
        for session in range(1, 7):
            if student_session_log[session] == '0':
                # print(filtered_features[session])
                add_sorted_rows(file, [filtered_features[session]], "session_id")

        # csv_input.to_csv(f'{data_processed_students}/{student}.csv', index=False)


# --------------------------------------------- Main ---------------------------------------------


def run():
    init()
    collapse_sessions()
    add_session_averages_to_students()


run()
