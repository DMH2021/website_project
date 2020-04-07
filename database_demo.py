import sqlite3
def main():
    conn = sqlite3.connect("site_data.db")
    # Adding new data with the insert statement
    cursor = conn.execute("INSERT INTO messages VALUES ('Sam', 'python is cool', 0)")
    cursor.close()
    conn.commit()
    # Querying the database with SELECT statement
    cursor = conn.execute("SELECT User, Content from messages")
    records = cursor.fetchall()
    for record in records:
        print('%s says "%s"' % (record[0], record[1]))
    cursor.close()
    conn.close()

    if __name__=="__main__":
        main()