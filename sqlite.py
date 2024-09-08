import sqlite3

# Connect to the SQLite database (it will create the database if it doesn't exist)
with sqlite3.connect("student.db") as connection:
    cursor = connection.cursor()

    # Create the STUDENT table if it doesn't already exist
    table_info = """
    CREATE TABLE IF NOT EXISTS STUDENT (
        NAME VARCHAR(25), 
        CLASS VARCHAR(25), 
        SECTION VARCHAR(25),
        MARKS INT
    );
    """
    cursor.execute(table_info)

    # Insert records into the table
    cursor.execute("INSERT INTO STUDENT VALUES ('Disha', 'Data Science', 'A', 90)")
    cursor.execute("INSERT INTO STUDENT VALUES ('Diya', 'Data Science', 'B',100)")
    cursor.execute("INSERT INTO STUDENT VALUES ('Komal', 'Data Science', 'A',86)")
    cursor.execute("INSERT INTO STUDENT VALUES ('Yashasvi', 'DEVOPS', 'A',50)")
    cursor.execute("INSERT INTO STUDENT VALUES ('Himanshu', 'DEVOPS', 'A',35)")

    # Commit changes to the database
    connection.commit()

    # Display all the records in the table
    print("The inserted records are:")
    data = cursor.execute("SELECT * FROM STUDENT")
    for row in data:
        print(row)
##commit the connection commit your changes into database
connection.commit()
connection.close()
