import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt   #Data visualisation libraries
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

def predict_session(path, exam):
    session = pd.read_csv(path)
    sns.distplot(session[exam])
    session.corr()
    x = session[['activity', 'mouse_wheel', 'mouse_wheel_click', 'mouse_click_left',
                 'mouse_click_right', 'mouse_movement', 'keystroke', 'intermediate_grade']]
    y = session[exam]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=101)
    lm = LinearRegression()
    model = lm.fit(x_train, y_train)
    print(f'score :  {model.score(x_test, y_test)}')
    predictions_list = lm.predict(x_test)
    return y_test, predictions_list


def run(target_exam):
    data_source = "output"
    predictions_list = []
    y_test = []
    for i in range(1, 7):
        session_test, session_prediction = predict_session(f'{data_source}/session {i}.csv', target_exam)
        y_test = np.append(y_test, session_test)
        predictions_list = np.append(predictions_list, session_prediction)
    return y_test, predictions_list


# ---------------------------------- First Exam -------------------------------------

exam = "first_exam"
exam = "second_exam"
print(exam)
true_values, predicted_values = run(exam)

mean_absolute_error = mean_absolute_error(true_values, predicted_values)
print(mean_absolute_error)

mean_squared_error = mean_squared_error(true_values, predicted_values)
print(mean_squared_error)

r2_score = r2_score(true_values, predicted_values)
print(r2_score)
# x = 15
# print(true_values[x])
# print(expected_values[x])
