#-----------------------------------------------------
#File: details.py
#Created by: Colten Shipe and Melchisedek Dulcio
#-----------------------------------------------------


# Requires the Flask and MySQL libraries
# To use this app:
#   pip install mysql-connector-python

from flask import Flask, request
from datetime import *
import time
from mysql.connector import connect
import dbconfig
from details import *

app = Flask(__name__)

con = connect(user=dbconfig.DB_USER, password=dbconfig.DB_PASS, database='wsoapp2', host=dbconfig.DB_HOST) 
cursor = con.cursor()

error_msg = ["New service was successfully created!", "Another service is being held at the same time."]

@app.route('/details')  #Calls getDetails()
def details():
    global cursor
    svc_id = request.args.get('svc_id')
    return getDetails(svc_id, cursor)

#Home page of the website that lists services
@app.route('/')
def home():
    global cursor
    # We don't close the following explicitly because they are automatically closed
    # when the variables go out of scope when hello() returns
     
    #Get service information
    cursor.execute("""
    SELECT Service_ID, Svc_DateTime, Theme_Event
    FROM service
    """)

    # Retrieve results
    result = cursor.fetchall()

    #Start table
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
        #Pull date and time from datetime
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


#Called when creating a new service
@app.route("/create")
def create():
    global cursor

    svc_datetime, theme, songleader, tmpltsvc_id = (0, None, None, None) #initialize variables

    #Get values from the URL
    if 'Svc_DateTime' in request.args:
        svc_datetime = request.args.get('Svc_DateTime')
    else:
        return "<html>A service must be selected.</html>"

    if "Theme_Event" in request.args:
        theme = request.args.get('Theme_Event')

    if "songleader" in request.args:
        try: 
            songleader = int(request.args.get('songleader'))
        except:
            pass
    if "tmpltsvc_id" in request.args:
        try: 
            tmpltsvc_id = int(request.args.get('tmpltsvc_id'))
        except:
            pass

    #create service
    result = cursor.callproc('create_service', (datetime.strptime(svc_datetime, "%Y-%m-%dT%H:%M"), theme, songleader, tmpltsvc_id, 0, 0))
    svc_id = result[5]
    con.commit()
       
    return f"""<html><p style="color:{['green', 'red'][result[4]]};
    font-size:150%;">{error_msg[result[4]]}</p>{getDetails([svc_id, tmpltsvc_id][result[4]], cursor)}</html>"""
    
# Launch the BottlePy dev server
if __name__ == "__main__":
    app.run(host='', port=5000, debug=True)
    con.close()