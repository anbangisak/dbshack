import pandas as pd
# from SQLList import extractQueries

def startExtractProcess(conn):
    dataDF = []
    for query in extractQueries:
        data = []
        data.append(query)
        rows = processExtract(conn, extractQueries[query])
        data.append(rows)
        dataDF.append(data)
    return dataDF

def processExtract(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    names = list(map(lambda x: x[0], cursor.description))
    rows = cursor.fetchall()
    df = convertToDataframe(rows,names)
    return df

def convertToDataframe(rows, names):
    lst = []
    for row in rows:
        lstd = []
        for i in row:
            lstd.append(i)
        lst.append(lstd)
    return pd.DataFrame(lst, columns=names)

def processExtractCSV(csvFile):
    df = pd.read_csv(csvFile)
    return df

