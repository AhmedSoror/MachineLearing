import os


def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)


def add_features(data_source, line):
    for session in os.listdir(data_source):
        for student in os.listdir(f'{data_source}/{session}'):
            path = f'{data_source}/{session}/{student}'
            line_prepender(path, line)
            base = os.path.splitext(path)[0]
            os.rename(path, base + '.csv')
    print("Process Completed")


features_string = "session,student_Id,exercise,activity,start_time,end_time,idle_time,mouse_wheel,mouse_wheel_click,mouse_click_left,mouse_click_right,mouse_movement,keystroke"

add_features('Data/Processes', features_string)

