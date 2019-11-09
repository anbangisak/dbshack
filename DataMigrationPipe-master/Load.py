#from SQLList import loadQueries

def startLoadProcess(conn, dataDFListTransform):
    for df in dataDFListTransform:
        table = df[0]
        data = df[1]
        if (table == 'iris'):
            cols = ",".join([str(i) for i in data.columns.tolist()])
            ques = ",".join(['?' for i in range(0,len(data.columns.tolist()))])
            query = loadQueries[0]+cols+") VALUES ("+ ques +")"
            cursor = conn.cursor()
            for index, row in data.iterrows():
                cursor.execute(query, tuple(row))
            conn.commit()

