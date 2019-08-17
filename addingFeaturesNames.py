import os


# ---------------------------------------------- Constants ----------------------------------------------

source_sessions_in_parent = "Data/Processes"
features_string = "session_id,student_id,exercise,activity,start_time,end_time,idle_time,mouse_wheel," \
                  "mouse_wheel_click,mouse_click_left,mouse_click_right,mouse_movement,keystroke "
sessions_csv_parent = "Data_Processed/Processes"

# ---------------------------------------------- Methods ----------------------------------------------


def insert_top(original_file, new_file, line):
    with open(original_file, 'r') as f:
        with open(new_file, 'w') as f2:
            f2.write(line+"\n")
            f2.write(f.read())


def add_features():
    for session in os.listdir(source_sessions_in_parent):
        for student in os.listdir(f'{source_sessions_in_parent}/{session}'):
            in_path = f'{source_sessions_in_parent}/{session}/{student}'
            out_path = f'{sessions_csv_parent}/{session}/{student}.csv'
            if not os.path.exists(f'{sessions_csv_parent}/{session}'):
                os.makedirs(f'{sessions_csv_parent}/{session}')
            insert_top(in_path, out_path, features_string)
    # print("Process Completed")


# ---------------------------------------------- Main ----------------------------------------------
def run():
    add_features()


run()
