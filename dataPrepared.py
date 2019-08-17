import os

from commonMethods import collapse_sessions
sessions_output_path = "output"


def init():
    if not os.path.exists(sessions_output_path):
        os.makedirs(sessions_output_path)
    header = "student_id,session_id,activity,start_time,end_time,total_idle_time,mouse_wheel,mouse_wheel_click," \
             "mouse_click_left,mouse_click_right,mouse_movement,keystroke,intermediate_grade,first_exam,second_exam"

    for i in range(1, 7):
        with open(f'{sessions_output_path}/session {i}.csv', 'w+') as fd:
            fd.write(header+"\n")


def run():
    init()
    collapse_sessions(sessions_output_path)


run()
