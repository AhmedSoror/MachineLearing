import os


# ---------------------------------------------- Import from Common File ----------------------------------------------
from commonMethods import sessions_in_parent
from commonMethods import features_string
from commonMethods import sessions_csv_parent


# ---------------------------------------------- Methods ----------------------------------------------


def insert_top(original_file, new_file, line):
    with open(original_file, 'r') as f:
        with open(new_file, 'w') as f2:
            f2.write(line+"\n")
            f2.write(f.read())


def add_features():
    for session in os.listdir(sessions_in_parent):
        for student in os.listdir(f'{sessions_in_parent}/{session}'):
            in_path = f'{sessions_in_parent}/{session}/{student}'
            out_path = f'{sessions_csv_parent}/{session}/{student}.csv'
            if not os.path.exists(f'{sessions_csv_parent}/{session}'):
                os.makedirs(f'{sessions_csv_parent}/{session}')
            insert_top(in_path, out_path, features_string)
    print("Process Completed")


# ---------------------------------------------- Main ----------------------------------------------
def run():
    add_features()


# run()
