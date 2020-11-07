# Requires the Bottle and MySQL libraries
# To use this app:
#   pip install mysql-connector-python


import bottle
from datetime import datetime
import time
from mysql.connector import connect
import dbconfig
from details import *

@bottle.route('/details')
def details():
    svc_id = bottle.request.params['svc_id']
    return getDetails(svc_id)



@bottle.route('/')
def hello():
    qty = 0
    selectedCourseno = None
    if 'courseNo' in bottle.request.params:
        selectedCourseno = bottle.request.params['courseNo']

    # We don't close the following explicitly because they are automatically closed
    # when the variables go out of scope when hello() returns
    con = connect(user=dbconfig.DB_USER, password=dbconfig.DB_PASS, database='wso_mysql', host=dbconfig.DB_HOST) 
    cursor = con.cursor() 

    cursor.execute("""
    select Service_ID, Svc_DateTime, Theme_Event
    from service
    """)

    # Retrieve results
    result = cursor.fetchall()

    #result.insert(2, )
    
    table = """
    <table>
    <tr>
        <td>Date
        <td>Time
        <td>Theme/Event
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
        <form>
          Show course number: <input type='text' name='courseNo' value=''>
          <input type='submit' value='Go!'>
        </form>
        {0}</body></html>"""

# Launch the BottlePy dev server
if __name__ == "__main__":
    bottle.run(host='', port=5000, debug=True)