# Requires the Bottle and MySQL libraries
# To use this app:
#   pip install mysql-connector-python

from flask import Flask, request
from datetime import datetime
import time
from mysql.connector import connect
import dbconfig
from details import *

app = Flask(__name__)

con = connect(user=dbconfig.DB_USER, password=dbconfig.DB_PASS, database='wso_mysql', host=dbconfig.DB_HOST) 
cursor = con.cursor()

error_msg = ["Another service is being held at the same time."]

@app.route('/details')
def details():
    svc_id = request.args.get('svc_id')
    return getDetails(svc_id)


@app.route('/')
def hello():
    global cursor
    # We don't close the following explicitly because they are automatically closed
    # when the variables go out of scope when hello() returns
     

    cursor.execute("""
    select Service_ID, Svc_DateTime, Theme_Event
    from service
    """)

    # Retrieve results
    result = cursor.fetchall()

    #result.insert(2, )
    
    table = """
    <style> th { border: 3px solid black; background-color: gray }</style>
    <style> td { border: 2px solid black } </style>
    <table style="border: 3px solid black; border-collapse: collapse">
    <tr>
        <th>Details
        <th>Date
        <th>Time
        <th>Theme/Event
    </tr>
    """

    for row in result:
        date = row[1].strftime("%m/%d/%Y")
        time = row[1].strftime("%I:%M %p")
        theme = row[2]
        svc_id = row[0]
        tableRow = """
        <tr>
            <td>
                <form method='get' action='details'>
                    <button type='submit' name='svc_id' value='{0}'>Details</button>
                </form>
            <td>{1}
            <td>{2}
            <td>{3}
        </tr>
        """.format(svc_id, date, time, theme)
        table += tableRow

    table += "</table>"
    return HTML_DOC.format(
            table)

HTML_DOC = """<html><body>
        <h1>Services</h1>
        {0}</body></html>"""


@app.route("/create")
def create():
    global cursor
    
    cursor.execute("""
    select MAX(Service_ID)
    from service
    """)

    # Retrieve results
    result = cursor.fetchall()

    #do checks
    svc_id = int(result[0][0]) + 1
    svc_datetime = request.args.get('Svc_DateTime')
    theme = request.args.get('Theme_Event')

    songleader = int(request.args.get('songleader'))



    #notes to self: Will need to create drop for each row in item column that is modifiable
    #               for each field tmplate returns create input textbox with dropdown.

    #create service
    cursor.callproc('create_service', (svc_datetime, theme, songleader, svc_id, 0))
    #create update fills role
    return getDetails(svc_id)
    
# Launch the BottlePy dev server
if __name__ == "__main__":
    app.run(host='', port=5000, debug=True)