import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder

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



def encode(file_path):
    df = pd.read_csv(file_path)
    x = df.iloc[:, :].values
    encoder = LabelEncoder()
    x[:, 2] = encoder.fit_transform((x[:, 2]))
    y = pd.DataFrame(x)
    # df.to_csv(r'test.csv', index=False)
    df["activity"] = y[2]
    df.to_csv(file_path, index=False)


def run():
    init()
    collapse_sessions(sessions_output_path)
    for i in range(1, 7):
        encode(f'{sessions_output_path}/session {i}.csv')

run()
