#!/usr/bin/python3
import datetime # .isoformat()
import os

import database

def get_path_info(path):
    # filepath = AAAA / MM / dispositivo / tab-ou-tech / filename
    tmp = path.split('/')
    path_info = {
        'ano'        : tmp[-5],
        'mes'        : tmp[-4],
        'dispositivo': tmp[-3],
        'tab_ou_tech': tmp[-2],
        'filename'   : tmp[-1]}

    return path_info

def get_file_info(file_path):
    # filepath = AAAA / MM / dispositivo / tab-ou-tech / filename
    path_info = get_path_info(file_path)

    #filename = LOCAL-tab_ou_tech-AA-MM-DD.csv
    tmp = path_info['filename'].replace('.csv','').split('-')

    # check for discrepancies
    if ("20"+tmp[2]) != path_info['ano']:
        raise NameError('Ano nas pastas e no nome do arquivo estão diferentes')
    if tmp[3] != path_info['mes']:
        raise NameError('Mês nas pastas e no nome do arquivo estão diferentes')

    file_info = {
        'local'        : tmp[0],
        'tab_ou_tech'  : tmp[1],
        'ano'          : tmp[2],
        'mes'          : tmp[3],
        'dia'          : tmp[4]}

    return file_info

def create_tables(conn):
    """ create the files and updates table if not already created
    :param conn: Connection object
    :param database: path where to create and save the DB
    :return:
    """

    # int for primary key
    sql_create_files_table = """CREATE TABLE IF NOT EXISTS files (
                                        id integer PRIMARY KEY,
                                        local text NOT NULL,
                                        tab_ou_tech text NOT NULL,
                                        status int NOT NULL
                                    );"""


    sql_create_updates_table = """CREATE TABLE IF NOT EXISTS updates (
                                        id integer PRIMARY KEY,
                                        file_id string NOT NULL,
                                        measure_time text NOT NULL,
                                        last_update_in_s int NOT NULL,
                                        FOREIGN KEY (file_id) REFERENCES files (id)
                                    );"""

    # creates tables table if not available
    database.create_table(conn, sql_create_files_table)

    # creates updates table if not available
    database.create_table(conn, sql_create_updates_table)


def updateDB(conn):
    """ updates the last modification time to the DB
    :param conn: Connection object
    :return:
    """

    # get current time
    current_time = datetime.datetime.utcnow().replace(microsecond=0)

    # store number of files and updates added
    new_files = 0
    new_updates = 0

    # generates the path for the current month - eg. 2020/03
    month_folder = "{:04}/{:02}".format(current_time.year, current_time.month)
    # generates the current day string - eg. 2020-03-15
    current_date_str = current_time.strftime("%y")+"-"+current_time.strftime("%m")+"-"+current_time.strftime("%d")

    # walks thought the current month files
    for dirname, _, filenames in os.walk(month_folder):
        for filename in filenames:
            # selects only files from the current day
            if current_date_str in filename:
                # get file info
                full_file_path = os.path.join(dirname, filename)
                file_info = get_file_info(full_file_path)

                # checks if the filename and folder are consistent
                    # adds log if not

                # remove unused fields
                del file_info['ano']
                del file_info['mes']
                del file_info['dia']

                # connecting and modifying the DB
                with conn:

                    # checks if more than one file exists for this configuration
                    try:
                        file_exists = database.specific_file_exists(conn, **file_info)
                    except NameError:
                        print('Multiple files on th DB:')
                        continue

                    # gets the file_id by creating the file or selecting it
                    if file_exists:
                        file = database.select_specific_file(conn, **file_info)
                        file_id = file[0][0] # select the id
                    else:
                        file_id = database.create_file(conn, (file_info['local'],file_info['tab_ou_tech']))
                        new_files += 1

                    # gets the last modification time of the file
                    last_mod_file = datetime.datetime.utcfromtimestamp(os.path.getmtime(full_file_path))

                    # create update and store data
                    last_update_in_s = (current_time - last_mod_file).seconds
                    try:
                        database.create_update(conn, (file_id, current_time.isoformat(), last_update_in_s))
                        new_updates += 1
                    except:
                        print("Error adding the current update to the updates table")
                        print(file_info)

    print("{:5} additions to the files table".format(new_files))
    print("{:5} additions to the updates table".format(new_updates))
    print("Updating concluded")


if __name__ == "__main__":
    """
    Logs the last modification time to the DB
    """

    DB_path = r"database.db"

    # connects to the SQlite DB
    conn = database.create_connection(DB_path)

    # creates tables if not already available
    create_tables(conn)

    # logs the difference to the DB
    updateDB(conn)
