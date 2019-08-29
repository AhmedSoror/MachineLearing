# MachineLearing

The data was to be processed where the target was to reduce all the session data to a single row to predict the final grade in 
the final exam. First data for every session was gathered from every student file into one csv file, then from this file the
average values of the features were calculated. 
For getting the data of each session in a single row, I got the average (mode with qualitative values) of the session per 
student and added to a separate file and for those students who did not attend the session, the calculated average values 
were  used. Session grade and final grade were added to every session row per student and the data were ready to be modeled.

Some columns were dropped due to inconsistent data and the data were split to training set (80%) and testing set (20%). Linea
r regression was used to model and predict the final grades. On calculating the error, small values were obtained which
indicated good model on the training data. On measuring accuracy it was low as the data was not enough and features are not
good indicators.

-----------------------------------------------------------------------------------------------------------------------------

log file has error :  student 62 didn't attend session 3 ( found 1 in the log) so flip it to 0 before start

# How to run:

1) run run.py

----------------------------------------- or -----------------------------------
                        ( uncomment last line from any file to run it )
1) addingFeaturesNames : to add headers and convert data to csv files ( if data is .csv skip )
2) getSessionsPerStudent : get a csv file for every student with session data
3) sessionAverage : get average per session to complete missing data
4) addFinalGrades : add final grade per session for each student.csv file in the processed data folder
5) dataPreparing : get csv file per session to model it
---------------------------------------------------------------------------------

# Now all data are ready to model (in "output" )

* run files from predictions ( to change between exams, choose it from the first couple of lines ix`n each file s)
* to get the error in all predictions per exam run predicting.py
