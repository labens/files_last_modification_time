import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
 
    return conn
 

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_file(conn, file):
    """
    Create a new file into the files table
    :param conn: Connection object
    :param file: file turple with (dispositivo, subclasse, local, tab_ou_tech, identificacao)
    :return: file id
    """
    sql = ''' INSERT INTO files(dispositivo, subclasse, local, tab_ou_tech, identificacao)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, file)
    return cur.lastrowid
 

def create_update(conn, update):
    """
    Create a new update into the updates table
    :param conn: Connection object
    :param update: update turple with (file_id, measure_time, last_update_in_s)
    :return: update id
    """
    sql = ''' INSERT INTO updates(file_id, measure_time, last_update_in_s)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, update)
    return cur.lastrowid


def select_all_files(conn):
    """
    Query all rows in the files table
    :param conn: the Connection object
    :return: all files
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM files")
 
    rows = cur.fetchall()
 
    return rows
        
def select_all_updates(conn):
    """
    Query all rows in the updates table
    :param conn: the Connection object
    :return: all updates
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM updates")
 
    rows = cur.fetchall()
 
    return rows
 
 
def select_updates_by_file_id(conn, file_id):
    """
    Query rows with the selected file_id in the updates table
    :param conn: the Connection object
    :return: rows with the selected file_id
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM updates WHERE file_id=?", (file_id, ))

    rows = cur.fetchall()

    return rows

def select_specific_file(conn, dispositivo, subclasse, local, tab_ou_tech, identificacao):
    """
    Query files by all fields
    :param conn: the Connection object
    :return: all found files
    """    
    select_query = """SELECT * FROM files WHERE 
                                    dispositivo=? AND
                                    subclasse=?   AND
                                    local=?       AND
                                    tab_ou_tech=? AND
                                    identificacao=?
                                    ;"""

    cur = conn.cursor()
    cur.execute(select_query, (dispositivo, subclasse, local, tab_ou_tech, identificacao))
 
    rows = cur.fetchall()
 
    return rows

def specific_file_exists(conn, dispositivo, subclasse, local, tab_ou_tech, identificacao):
    """
    Query files by all fields and returns if it exists or not
    :param conn: the Connection object
    :return: True or False and gives raise an excpetion if two or more files are found
    """    
    # query the specific file with all fields
    files = select_specific_file(conn, dispositivo, subclasse, local, tab_ou_tech, identificacao)
    
    if len(files) > 1:
        print(files)
        raise NameError('Duplicated files')
    elif len(files) == 1:
        return True
    else:
        return False
 

def execute(conn, query):
    """ run the selected query
    :param conn: Connection object
    :param query: the query to be run on the DB
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(query)
    except Error as e:
        print(e)


def create_tables(conn, database):
    """ create the files and updates table if not already created
    :param conn: Connection object
    :param database: path where to create and save the DB
    :return:
    """
 
    # int for primary key
    sql_create_files_table = """CREATE TABLE IF NOT EXISTS files (
                                        id integer PRIMARY KEY,
                                        dispositivo text NOT NULL,  
                                        subclasse text NOT NULL, 
                                        local text NOT NULL, 
                                        tab_ou_tech text NOT NULL, 
                                        identificacao int NOT NULL
                                    );"""


    sql_create_updates_table = """CREATE TABLE IF NOT EXISTS updates (
                                        id integer PRIMARY KEY,
                                        file_id string NOT NULL,
                                        measure_time text NOT NULL,
                                        last_update_in_s int NOT NULL,
                                        FOREIGN KEY (file_id) REFERENCES files (id)
                                    );"""
 
    # creates tables table if not available
    create_table(conn, sql_create_files_table)
    
    # creates updates table if not available
    create_table(conn, sql_create_updates_table)

