import pandas as pd
import numpy as np
import pyodbc
import pymysql
from datetime import date,datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression



df = pd.read_csv('stockprices.csv')
df.drop(columns=['Open Price','High Price','Low Price','Last Price','Average Price','Turnover','No of Trades','Total Traded Quantity'],inplace=True)
df.drop(columns=['Deliverable Qty','Dly Qt to Traded Qty'],inplace=True)
df['Date']= pd.to_datetime(df['Date'])
df['year']=pd.DatetimeIndex(df['Date']).year
df['month']=pd.DatetimeIndex(df['Date']).month
df['day']=pd.DatetimeIndex(df['Date']).day
df.drop(columns=['Date'],inplace=True)
x = df.drop('status', axis = 1)
y = df['status']

X_train, X_test, y_train, y_test = train_test_split(x,y,test_size=.3,random_state = 2)
modelRF = RandomForestClassifier(max_depth=2)
modelRF.fit(X_train,y_train)
y_predictRFTrain = modelRF.predict(X_train)
y_predictRFTese = modelRF.predict(X_test)

linreg = LinearRegression()
x = df.drop(columns=['status','Close Price','TodayDiff','PercentageChange'])
y = df['Close Price']

X_train, X_test, y_train, y_test = train_test_split(x,y,test_size=.3,random_state = 2)
linreg.fit(X_train,y_train)
y_predict = linreg.predict(X_test)
linreg.score(X_test,y_predict)
lst = []
for stock in x['Stock'].unique():
    prevPred = df[df['Stock']==stock]['Close Price'].mean()
    for i in range(0,60):
        lstd = []
        days_after = (date.today()+timedelta(days=i))
        day = days_after.weekday()
        if (day < 6):
            lstd.append(stock)
            lstd.append(prevPred)
            lstd.append(days_after.year)
            lstd.append(days_after.month)
            lstd.append(days_after.day)
            closePrice = linreg.predict([np.array(lstd)])[0]
            lstd.append(closePrice)
            lstd.append(closePrice-prevPred)
            lstd.append((closePrice-prevPred)/prevPred)
            prevPred = closePrice
            lst.append(lstd)

dfNew = pd.DataFrame(lst,columns=['Stock','Prev Close','year','month','day','Close Price','TodayDiff','PercentageChange',])

cols = list(dfNew.columns)
a, b, c, d, e, f, g, h = cols.index('Stock'), cols.index('Prev Close'), cols.index('year'), cols.index('month'),cols.index('day'),cols.index('Close Price'),cols.index('TodayDiff'),cols.index('PercentageChange')
cols[a], cols[b], cols[c], cols[d],  cols[e],  cols[f],  cols[g],  cols[h] = cols[a], cols[b], cols[f], cols[g],  cols[h],  cols[c],  cols[d],  cols[e]

dfNew = dfNew[cols]

dfNew['Pred'] = modelRF.predict(dfNew)

cols = "stockId,date,pred"
ques = "?,?,?,?"
query = "INSERT INTO prediction("+cols+") VALUES ("+ ques +")"
conn= ''
conn_str = (
        "DRIVER={MySQL ODBC 8.0 ANSI Driver};"
        "DATABASE=dbs;"
        "UID=root;"
        "PWD=mysql;"
        "SERVER=3.83.223.55;"
        "PORT=3306;"
    )


conn = pymysql.connect("3.83.223.55","mysql","mysql","dbs")



print(conn)

cursor = conn.cursor()
for index, row in dfNew.iterrows():
    cursor.execute(query, tuple(row['Stock'],row['year']+"-"+row['month']+"-"+row['day']))
    conn.commit()



