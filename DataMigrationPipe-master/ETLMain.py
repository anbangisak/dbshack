# from input import input_db_details, output_db_details
import Transform as tfm
import Load as load
# import pyodbc
import Extract as ext
# import TweetExtract as twt
import sqlite3
import pymysql
import pandas as pd


def getConnectionODBC(driver):

    conn_str = (
        driver + ";"
        "DATABASE=dbs;"
        "UID=root;"
        "PWD=mysql;"
        "SERVER=52.70.237.253;"
        "PORT=3306;"
    )
    error = ''
    try:
        conn = pymysql.connect("localhost","root","mysql","dbs" )
        # conn = pyodbc.connect(conn_str)
    # except pyodbc.Error as err:
    except Exception as err:
        error = 'ERROR'
        conn = err
    return error, conn

def initiateConnection(type):
    conn = '';
    error = '';

    #if (config_details['dbtype'] == 'dbs'):
    #     driver = 'DRIVER={MySQL ODBC 8.0 ANSI Driver}'
    #     error, conn = getConnectionODBC(driver)

    driver = 'DRIVER={MySQL ODBC 8.0 ANSI Driver}'
    error, conn = getConnectionODBC(driver)
    return error, conn;

def startExtract(conn):

    dataDFList = pd.read_csv("stockprices.csv")
    return dataDFList

def main():
    error, conn = initiateConnection('i')

    if (error == 'ERROR'):
        print('ALERT....'+ str(conn))
        return;
    print('connection established')

    print('---> Starting Extratcing Process')
    dataDFList = startExtract(conn)

    print('---> Starting Transform Process')
    dataDFListTransform = tfm.processTransform(dataDFList);
    print (dataDFListTransform)

    # print('---> Starting Load Process')
    # error, connL = initiateConnection(output_db_details, 'o')
    if (error == 'ERROR'):
        print('ALERT....' + str(conn))
        return;

    # if (output_db_details['dbtype'] == 'csv'):
    #     load.loadProcessCsv(output_db_details['csvloc'],dataDFListTransform)


if __name__ == "__main__":
    main()
