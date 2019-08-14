import pandas as pd
import os
import csv


def init(output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    header = "student_id,session_id,activity,st_time,end_time,total_idle_time,mouse_wheel_rate,mouse_wheel_click_rate,mouse_click_left_rate,mouse_click_right_rate,mouse_movement_rate,keystroke_rate,intermediate_grade"
    for i in range(1, 7):
        # if not os.path.exists(f'Data/Sessions_average/session {i}.csv'):
        #     os.mknod(f'Data/Sessions_average/session {i}.csv')
        with open(f'{output_path}/session {i}.csv', 'w+') as fd:
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


def collapse_sessions(source_path, output_path):
    for current_student_id in range(1, 116):
        try:
            get_session_from_student(source_path, output_path, current_student_id)
        except FileNotFoundError as e:
            print(f'no processed file found for student {current_student_id}')


data_in = "Data/Processed"
data_out = "Data/SessionsCollapsed/"
init(data_out)
collapse_sessions(data_in, data_out)
