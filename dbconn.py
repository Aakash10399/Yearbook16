import MySQLdb
def connection():
    conn = MySQLdb.connect(host="HOSTNAME",
                           user="USER",
                           passwd="PASSWORD",
                           db="DATABASENAME")
    c=conn.cursor()

    return c,conn
