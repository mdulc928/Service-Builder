from mysql.connector import connect
import dbconfig
from datetime import date

def getDetails(svc_id: str, cursor):
    # We don't close the following explicitly because they are automatically closed
    # when the variables go out of scope when hello() returns
    
    cursor.execute("""
    select *
    from service_view
    where Service_ID = %s
    """, (svc_id,))
    
    result = cursor.fetchall()

    cursor.execute("""
    SELECT event_type.Description, service_item.Title, CONCAT(person.First_Name, ' ', person.Last_Name) AS Person, Confirmed, ensemble.Name, song.Title AS Song, Notes
    FROM service_item LEFT JOIN person ON service_item.Person_ID = person.Person_ID
    LEFT JOIN ensemble ON ensemble.Ensemble_ID = service_item.Service_Item_ID
    LEFT JOIN song ON song.Song_ID = service_item.Song_ID
    LEFT JOIN event_type ON event_type.Event_Type_ID = service_item.Event_Type_ID
    WHERE Service_ID = %s
    """, (svc_id,))
    
    service_items = cursor.fetchall()

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
    </tr>
    """

    tableRow = "<tr>"
    for item in result[0][1:4]:
        tableRow += f"""<td style="border: 2px solid black">{item}"""
    tableRow += "</tr>"
    table += tableRow
    table += "</table>"

    table += """
    &nbsp;
    <table style="border: 3px solid black; border-collapse: collapse">
    <tr>
        <th>Description
        <th>Title
        <th>Person
        <th>Confirmed
        <th>Name
        <th>Song
        <th>Notes
    </tr>
    """

    for row in service_items:
        tableRow = "<tr>"
        itemCount = 0
        for item in row:
            if itemCount == 5: #song title index
                tableRow += """<td style="border: 2px solid black"><select>"""
                if row[5] == None:
                    tableRow += "<option value="" selected></option>"
                else:
                    tableRow += "<option value=""></option>"
                for song in songs:
                    if song[2] != None and row[5] != None and song[2] in row[5]:
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
        <h2>Service Details</h2>
        {0}</body></html>
        &nbsp; 
        <h2>Create New Service</h2>
        <form method='get' action='create'>
          Date and time: *<input type='datetime-local' name='Svc_DateTime' value='' required>
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
        