import sqlite3
import json

def update_hauler(id, hauler_data):
    with sqlite3.connect("./shipping.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE Hauler
                SET
                    name = ?,
                    dock_id = ?
            WHERE id = ?
            """,
            (hauler_data['name'], hauler_data['dock_id'], id)
        )

        rows_affected = db_cursor.rowcount

    return True if rows_affected > 0 else False


def delete_hauler(pk):
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        DELETE FROM Hauler WHERE id = ?
        """, (pk,)
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False


def list_haulers(url):
    # Open a connection to the database
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
    
    if "_expand" in url["query_params"]:
        # Write the SQL Query to get the information you want
        db_cursor.execute("""
            SELECT
                h.id,
                h.name,
                h.dock_id,
                d.id dockId,
                d.location,
                d.capacity
            FROM Hauler h
            JOIN Dock d
            ON h.dock_id = d.id     
            """)
        query_results = db_cursor.fetchall()

        # Initializing an empty list and then add each dictionary to it
        haulers = []
        for row in query_results:
            dock = { 
                "id": row['dockId'],
                "location": row["location"],
                "capacity": row['capacity']
            }
            hauler = {
                "id": row['id'],
                "name": row['name'],
                "dock_id": row['dock_id'],
                "dock": dock
            }
            haulers.append(hauler)

        # Serialize Python list to JSON encoded string
        serialized_haulers = json.dumps(haulers)
    else:
        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            h.id,
            h.name,
            h.dock_id
        FROM Hauler h
        """)
        query_results = db_cursor.fetchall()

        # Initialize an empty list and then add each dictionary to it
        haulers=[]
        for row in query_results:
            haulers.append(dict(row))

        # Serialize Python list to JSON encoded string
        serialized_haulers = json.dumps(haulers)

    return serialized_haulers

def retrieve_hauler(url, pk):
    # Open a connection to the database
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

    if "_expand" in url["query_params"]:
        #Write the SQL query to get the information for the hauler and dock
        db_cursor.execute("""
            SELECT
                h.id,
                h.name,
                h.dock_id,
                d.id dockID,
                d.location,
                d.capacity
            FROM Hauler h
            JOIN Dock d
            ON h.dock_id = d.id
            WHERE h.id = ?
        """, (pk,))
        query_results = db_cursor.fetchone()

        #Serialize Python list to JSON encoded string
        hauler ={
            "id": query_results["id"],
            "name": query_results["name"],
            "dock_id": query_results["dock_id"],
            "dock": {
                "id": query_results['dockId'],
                "location": query_results["location"],
                "capacity": query_results["capacity"]
            }
        }
        serialized_hauler = json.dumps(hauler)
        
    else:    
        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            h.id,
            h.name,
            h.dock_id
        FROM Hauler h
        WHERE h.id = ?
        """, (pk,))
        query_results = db_cursor.fetchone()

        # Serialize Python list to JSON encoded string
        serialized_hauler = json.dumps(dict(query_results))

    return serialized_hauler

def create_hauler(request_body):
    with sqlite3.connect("./shipping.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        #Write the SQL query to insert the information you want
        db_cursor.execute('''
            INSERT INTO hauler
                (name, 
                dock_id)
            VALUES (?, ?)
            ''', (request_body['name'], request_body['dock_id']))
         #Return the row data that was created in the step above
        new_hauler_created_id = int(db_cursor.lastrowid)

        conn.commit()

        # Write the SQL query to SELECT the new ship created
        db_cursor.execute("""
        SELECT
            h.id,
            h.name,
            h.dock_id
        FROM Hauler h
        WHERE h.id = ?
        """, (new_hauler_created_id,))
        query_results = db_cursor.fetchone()

        dictionary_version_of_object = dict(query_results)
    return dictionary_version_of_object
