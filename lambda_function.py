import json

# external libraries
import os
from ftplib import FTP
from dateutil import parser
from datetime import datetime, timedelta

# ftp login credentials
credentials = {
		'host': "ftp.controle.eng.br",
		'user': "controle01",	
		'passwd': "labens"
	}

def show_last_update_time():    
    # tries to connnect with the ftp
    try:
        ftp = FTP(**credentials)
    except:
        print('Not able to connect to FTP')
        return
    
    # gets folders and files on the ftp server
    all_folders = ftp.nlst()

    # select desired folders
    sonda = [folder for folder in all_folders if 'SONDA' in folder]
    epe   = [folder for folder in all_folders if 'EPE'   in folder]

    # combine both lists
    folder_list = sonda + epe

    # sets alphabetical order
    folder_list.sort()
    
    # gets current time
    current_time = datetime.utcnow()
    
    # creates dictionary to store timestamps
    last_update = {}
    last_update["current_time"] = current_time.isoformat()

    for folder in folder_list:
        # info about available files
        files = ftp.mlsd(folder)

        # 1st level dionary keys
        last_update[folder] = {}

        # runs for each file
        for file in files:
            # reads file name
            name = file[0]

            # excludes folder, parent folder and old files
            if name == '.' or name == '..' or '.DAT' in name:
                continue

            # gets last updated time
            timestamp = file[1]['modify']
            file_time = parser.parse(timestamp)
            
            # gets the timedifference in seconds
            if current_time > file_time:
                time_diff = current_time - file_time
                time_diff_in_s = time_diff.total_seconds()
            else:
                time_diff_in_s = 0
            
            # creates 2nd level dictionary and saves timestamp
            last_update[folder][name[4:10]] = time_diff_in_s

    # close ftp connections
    ftp.quit()
    
    # converts dict to JSON
    last_update_JSON = json.dumps(last_update)
    print(last_update_JSON)

def lambda_handler(event, context):
    # change later to secrets or so
    show_last_update_time()

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
