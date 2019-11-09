from flask import Flask, Response, render_template
import csv
import json
import matplotlib.pyplot as plt


app = Flask(__name__)

#for database connection and data fetch
import pymysql
import pandas as pd

conn = pymysql.connect("localhost","root","mysql","dbs" )

cursor = conn.cursor()
def to_csv():
    query = 'select name,date,data from prediction'
    cursor.execute(query)
    data = [x for x in cursor]
    df = pd.DataFrame(data,columns=['Name',"Date","Data"])
    file_name = 'pred_data.csv'
    df.to_csv(file_name, index=False)

# for database connection and data fetch close
@app.route('/')
def home():
    return "Hi Welcome to Future stock"

@app.route('/day')
def day():
    return " Prediction for next day"

@app.route('/pred', methods=['GET'])
def metrics():  # pragma: no cover
    to_csv()
    create_html_file()
    return render_template("pred_res.html", title='Projects')
    # content = get_file('jenkins_analytics.html')
    # return Response(content, mimetype="text/html")


@app.route('/month')
def month():
    return " Prediction for next month"

@app.route('/quarter')
def qtr():
    return " Prediction for next Quarter"

def create_html_file():
    import csv
    table = ''
    i = 0
    with open('pred_data.csv') as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        for row in reader:
            # i +=1

            if i == 0:
                pass
                # table += '<tr><td bgcolor = "#90EE90"><b>{}</b></td><td bgcolor = "#90EE90"><b>{}</b></td><td bgcolor = "#FF4500"><b>{}</b></tr>'.format(row[0],row[1],row[2])

            elif i == 0:
                table += '<tr><td bgcolor = "#FFFF00">SNo</td><td bgcolor = "#FFFF00">Date</td><td bgcolor = "#FFFF00">Prediction</td></tr>'

            else:
                if (row[2] == 'BUY'):
                    table += '<tr><td>{}</td> <td>{}</td><td bgcolor = "#42FF33">{}</td> </tr>'.format(row[0], row[1],
                                                                                                       row[2])
                elif (row[2] == 'SELL'):
                    table += '<tr><td>{}</td> <td>{}</td><td bgcolor = "#FF5733">{}</td> </tr>'.format(row[0], row[1],
                                                                                                       row[2])
                else:
                    table += '<tr><td>{}</td> <td>{}</td><td bgcolor = "#FFC300">{}</td> </tr>'.format(row[0], row[1],
                                                                                                       row[2])
            i += 1

    html = """
    <table border=3>
      {}
    </table>
    """.format(table)

    with open('./templates/pred_res.html', 'w') as f:
        f.write(html)
        f.close()


# Methods to get daily chart


# Main code starts from here
app.run(host = '0.0.0.0', port = 8080, debug= True)



print('debu')
