try:
    conn = teradatasql.connect(host="ncrdwprod.aib.pri", user="DW79940", password=password, logmech="LDAP")
    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE")
    print("Current Database", cursor.fetchone()[0])

    #List all databases

    cursor.execute("""SELECT TableName, TableKind from DBC.Tables WHERE DatabaseName = 'ddewd06s';""")
    print("Databases")
    for row in cursor.fetchall():
        print(row[0], row[1])
    # con.close()


except Exception as ex:
    print("error", ex)
    print(traceback.format_exc())
finally:
    conn.close()
