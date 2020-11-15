from mysql.connector import connect
import dbconfig
from datetime import date

def getDetails(svc_id: str, cursor):
    # We don't close the following explicitly because they are automatically closed
    # when the variables go out of scope when hello() returns
    #con = connect(user=dbconfig.DB_USER, password=dbconfig.DB_PASS, database='wsoapp2', host=dbconfig.DB_HOST) 
    #cursor = con.cursor() 
    
    cursor.execute("""
    select *
    from service_view
    where Service_ID = %s
    """, (svc_id,))
    
    result = cursor.fetchall()

    cursor.execute("""
    SELECT *
    FROM person
    """)

    people = cursor.fetchall()

    cursor.execute("""
    SELECT *
    FROM songusageview
    ORDER BY LastUsedDate DESC
    LIMIT 20
    """)

    songs = cursor.fetchall()
    
    table = """
    <style> th { border: 3px solid black; background-color: gray }</style>
    <table style="border: 3px solid black; border-collapse: collapse">
    <tr>
        <th>Date
        <th>Theme
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
        itemCount = 0
        for item in row[1:]:
            if itemCount == 7: #song title index
                tableRow += "<td><select>"
                if row[8] == None:
                    tableRow += "<option value="" selected></option>"
                else:
                    tableRow += "<option value=""></option>"
                for song in songs:
                    if song[2] != None and row[8] != None and song[2] in row[8]:
                        tableRow += f"""<option value="{song[0]}" selected>{song[2]}</option>"""
                    tableRow += f"""<option value="{song[0]}">{song[2]}</option>"""
                tableRow += "</select></td>"
                
            else:
                tableRow += f"""<td style="border: 2px solid black">{item}"""
            itemCount += 1
        tableRow += "</tr>"
        table += tableRow
    
    optionStr = ""
    for person in people:
        optionStr += f"""<option value="{person[0]}">{person[1] + " " + person[2]}</option>"""

    table += "</table>"
    return HTML_DETAILS.format(
            table, result[0][2], optionStr, svc_id)

HTML_DETAILS = """<html><body>
        <h2>Service Plan</h2>
        {0}</body></html>
        &nbsp; 
        <h2>Create New Service</h2>
        <form method='get' action='create'>
          Date and time: <input type='datetime-local' name='Svc_DateTime' value='' required>
          &nbsp;
          Theme or Event: <input type='text' name='Theme_Event' value="{1}">
          &nbsp;
          Song leader: 
          <select name='songleader' value=''>
            <option value=""></option>
            {2}
          </select>
          <br>
          <input type='submit' value='Go!'>
          <input type='hidden' name='tmpltsvc_id' value='{3}'></input>
        </form>"""
        