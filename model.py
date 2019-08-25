import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt   #Data visualisation libraries
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
# %matplotlib inline

session = pd.read_csv('Data/session 2.csv')
session.head()
session.info()
session.describe()
session.columns

sns.distplot(session['first_exam'])

session.corr()

X = session[['activity', 'mouse_wheel', 'mouse_wheel_click', 'mouse_click_left',
             'mouse_click_right', 'mouse_movement', 'keystroke', 'intermediate_grade']]
y = session['first_exam']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=101)


lm = LinearRegression()
lm.fit(X_train, y_train)

predictions = lm.predict(X_test)
plt.scatter(y_test, predictions)
