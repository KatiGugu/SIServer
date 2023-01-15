'''
The module provides functions for obtaining the parameters of the system 
information server operation.
'''
from loggers import logger_si

CONF_FILE = 'srv_info.conf'

logger = logger_si(folder="Log", name = 'GetingParameters') 

def verif_conf_file(param_dict):
    '''
    Checks the operation parameters of the system information server. Replaces invalid 
    values ​​with default values.
    '''
    if 'DataBase' in param_dict:
        if type(param_dict['DataBase']) is not int or (param_dict['DataBase'] != 1 
                                                       and param_dict['DataBase'] != 0):
            param_dict['DataBase'] = 1
    else:    
        param_dict['DataBase'] = 1
    if 'W_Interval' in param_dict:
        if type(param_dict['W_Interval']) is not int or param_dict['W_Interval'] <= 0:
            param_dict['W_Interval'] = 30
    else:    
        param_dict['W_Interval'] = 30
    if 'Storage_time' in param_dict:
        if type(param_dict['Storage_time']) is not int or param_dict['Storage_time'] <= 0:
            param_dict['Storage_time'] = 7
    else:
        param_dict['Storage_time'] = 7
    if 'Port' in param_dict:
        if type(param_dict['Port']) is not int or (param_dict['Port'] <= 1024
                                                   or param_dict['Port'] > 65535):
            param_dict['Port'] = 8083
            logger.error(f"The value of the 'port' parameter is incorrect. Default value set: 8083.")
    else:    
        param_dict['Port'] = 8083
        logger.error(f"The value of the 'port' parameter is incorrect. Default value set: 8083.")
    if 'Folder_Log' in param_dict:
        if type(param_dict['Folder_Log']) is not str:
            param_dict['Folder_Log'] = 'Log'
    else:    
        param_dict['Folder_Log'] = 'Log'
 
    
    return param_dict


def get_param():
    '''
    Reads the configuration file srv_info.conf and returns a dictionary with the 
    parameters of the system information server.
    '''
    param = {}
    try:
        with open(CONF_FILE, mode='r') as conffile:
            onstring = conffile.read().split("\n")
            for _line in onstring:
                line = _line.replace(" ","")
                if len(line) == 0 or line[0] == '#':
                    continue
                key, value = line.split(':')
                if key.lower() == "url" or key.lower() == 'Folder_Log':
                    param[key] = value.replace(' ', '')
                else:
                    try:
                        param[key] = int(value)

                    except ValueError:
                        param[key] = ''
            param = verif_conf_file(param)
    except  FileNotFoundError:
        logger.error(f"The configuration file is missing or corrupted. \
                     The default configuration has been applied.")     
        param = verif_conf_file(param)
    return param