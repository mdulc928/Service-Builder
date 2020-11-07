# Requires the Bottle and MySQL libraries
# To use this app:
#   pip install mysql-connector-python


from flask import Flask
from datetime import datetime
import time
from mysql.connector import connect
import dbconfig

app = Flask(__name__)

@app.route('/')
def hello():
    qty = 0
    selectedCourseno = None
    if 'courseNo' in bottle.request.params:
        selectedCourseno = bottle.request.params['courseNo']

    # We don't close the following explicitly because they are automatically closed
    # when the variables go out of scope when hello() returns
    con = connect(user=dbconfig.DB_USER, password=dbconfig.DB_PASS, database='univdb', host=dbconfig.DB_HOST) 
    cursor = con.cursor() 

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
    
# Launch the BottlePy dev server
if __name__ == "__main__":
    app.run(host='', port=5000, debug=True)