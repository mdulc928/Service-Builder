from mysql.connector import connect
import dbconfig

def getDetails(svc_id: str):
        # We don't close the following explicitly because they are automatically closed
    # when the variables go out of scope when hello() returns
    con = connect(user=dbconfig.DB_USER, password=dbconfig.DB_PASS, database='wsoapp', host=dbconfig.DB_HOST) 
    cursor = con.cursor() 

    cursor.execute("""
    select *
    from serviceview
    """)
    
    result = cursor.fetchall()

    #result.insert(2, )
    
    table = """
    <table style="border: 3px solid black; border-collapse: collapse">
    <tr>
        <th>Date
        <th style="background-color: yellow">Theme
        <th>Song Leader
        <th>Organist
        <th>Pianist
        <th>Sequence No.
        <th>Description
        <th>Song Title
        <th>Name
        <th>Notes
    </tr>
    """

    for row in result:
        (Svc_DateTime, Theme_Event, songleader, organist, pianist, Seq_Num, Description, title, name, notes) = row[1:]
        tableRow = "<tr>"
        for item in row[1:]:
            tableRow += f"""<td style="border: 2px solid black">{item}"""
        tableRow += "</tr>"
        table += tableRow

    table += "</table>"
    return HTML_DETAILS.format(
            table)


HTML_DETAILS = """<html><body>
        <form>
          Show course number: <input type='text' name='courseNo' value=''>
          <input type='submit' value='Go!'>
        </form>
        {0}</body></html>"""