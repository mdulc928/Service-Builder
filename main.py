# Requires the Bottle and MySQL libraries
# To use this app:
#   pip install mysql-connector-python


from flask import Flask, request
from datetime import datetime
import time
from mysql.connector import connect
import dbconfig

app = Flask(__name__)

con = connect(user=dbconfig.DB_USER, password=dbconfig.DB_PASS, database='univdb', host=dbconfig.DB_HOST) 
cursor = con.cursor()

error_msg = ["Another service is being held at the same time."]

@app.route('/')
def hello():
    global cursor
    qty = 0
    selectedCourseno = None
    if 'courseNo' in request.args:
        selectedCourseno = request.args["blah"]
    # We don't close the following explicitly because they are automatically closed
    # when the variables go out of scope when hello() returns
     

    if selectedCourseno != None and selectedCourseno != "":
        cursor.execute("""
        select *
        from course
        where courseno = %s
        """, (selectedCourseno,))
    else:
        cursor.execute("""
        select *
        from course
        """)

    # Retrieve results
    result = cursor.fetchall()

    table = """
    <table>
    <tr>
        <td>Course No
        <td>Course Desc
        <td>Course Units
    </tr>
    """

    for row in result:
        (courseno, coursedesc, courseunits) = row
        tableRow = """
        <tr>
            <td>{0}
            <td>{1}
            <td>{2}
        </tr>
        """.format(courseno, coursedesc, courseunits)
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


@app.route("/create")
def create():
    global cursor
    
    #do checks
    svc_id, svc_datetime, theme = (0, 0, 0)


    #create service
    cursor.callproc('create_service', (svc_id, svc_datetime, theme))
    #create update fills role
    
# Launch the BottlePy dev server
if __name__ == "__main__":
    app.run(host='', port=5000, debug=True)