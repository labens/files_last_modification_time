
# gets the date and time in UTC
import datetime
current_time = datetime.datetime.utcnow().replace(microsecond=0)
# .isoformat()

import os

# # connects to the SQlite DB

# # generates the path for the current month - 2020/03
# month_folder = "{:04}/{:02}".format(current_time.year, current_time.month)
# # generates the current day string - 2020-03-15
# current_date_str = "{:04}-{:02}-{:02}".format(current_time.year, current_time.month, current_time.day)

# # walks thought the current month files
# for dirname, dirnames, filenames in os.walk(month_folder):
#     for filename in filenames:
#         # selects only files from the current day
#         if current_date_str in filename:
#             # checks if the filename and folder are consistent
            
            
#             print(os.path.join(dirname, filename))


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

def generate_path(file_info):
    # filename = dispositivo_subclasse_local_tab-tech_identificacao_AAAA-MM-DD.csv

    # reconstructs full name path
    if file_info['dispositivo'] == 'dat':
        dispositivo = 'dataloggers'
    elif file_info['dispositivo'] == 'inv':
        dispositivo = 'inversores'
    else:
        dispositivo = file_info['dispositivo']
    
    path = (file_info['ano']           + '/' +
            file_info['mes']           + '/' +
            dispositivo                + '/' +
            file_info['tab-ou-tech']   + '/' +
            file_info['dispositivo']   + '_' +
            file_info['subclasse']     + '_' +
            file_info['tab_ou_tech']   + '_' +
            file_info['identificacao'] + '_' +
            file_info['ano']           + '-' +
            file_info['mes']           + '-' +
            file_info['dia']           + '-' +
            '.csv')
    
    return path

def get_file_info(file_path):   
    # filepath = AAAA / MM / dispositivo / tab-ou-tech / filename
    path_info = get_path_info(file_path)
    
    # filename = dispositivo_subclasse_local_tab-tech_identificacao_AAAA-MM-DD.csv
    tmp = path_info['filename'].replace('.csv','').split('_')
    dates = tmp[5].split('-')
    
    # check for discrepancies
    if dates[0] != path_info['ano']:
        raise NameError('Ano nas pastas e no nome do arquivo estão diferentes')
    if dates[1] != path_info['mes']:
        raise NameError('Mês nas pastas e no nome do arquivo estão diferentes')
    if tmp[0][0:3] != path_info['dispositivo'][0:3]:
        raise NameError('Dispositivo nas pastas e no nome do arquivo estão diferentes')
    if tmp[3] != path_info['tab_ou_tech']:
        if tmp[3] != 'teste':
            raise NameError('Tab-ou-tech nas pastas e no nome do arquivo estão diferentes')
    
    file_info = {   
        'dispositivo'  : tmp[0],
        'subclasse'    : tmp[1],
        'local'        : tmp[2],
        'tab_ou_tech'  : tmp[3],
        'identificacao': tmp[4],
        'ano'          : dates[0],
        'mes'          : dates[1],
        'dia'          : dates[2]}
    
    return file_info
