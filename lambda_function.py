import json

# external libraries
import os
from ftplib import FTP
from dateutil import parser
from datetime import datetime, timedelta

# ftp login credentials
credentials = {
		'host': os.environ['FTP_HOST'],
		'user': os.environ['FTP_USR'],	
		'passwd': os.environ['FTP_PASSWD']
	}

def show_last_update_time():    
    # tries to connnect with the ftp
    try:
        ftp = FTP(**credentials)
    except:
        print('Not able to connect to FTP')
        return
    
    current_time = datetime.utcnow()

    # gets folders and files on the ftp server
    all_folders = ftp.nlst()

    # select desired folders
    sonda = [folder for folder in all_folders if 'SONDA' in folder]
    epe   = [folder for folder in all_folders if 'EPE'   in folder]

    # combine both lists
    folder_list = sonda + epe

    # sets alphabetical order
    folder_list.sort()
    
    # creates dictionary to store timestamps
    last_update = {}

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
            time_difference = current_time - file_time
            
            # creates 2nd level dictionary and saves timestamp
            last_update[folder][name] = time_difference

    # close ftp connections
    ftp.quit()
    
    # prints results
    print("## Last updated times")
    print(last_update)
    


def lambda_handler(event, context):
    # change later to secrets or so
    show_last_update_time()

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
