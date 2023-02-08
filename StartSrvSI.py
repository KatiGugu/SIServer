'''
Main module. Starts an HTTP server and in a parallel process runs a code
that accumulates statistical information about the system in the database.
Understands two types of Get request. If the request is of the form
http://hostname/current then the current information will be returned.
If http:/hostname/stat/?time1=t1&time2=t2, then records from the database
in the "data" range between t1 and t2 will be returned if they were
previously stored there.
The current information is returned as a dictionary converted to JSON format.
Its contents may differ depending on the OS. Statistical information consists
of the same set of characteristics as information for the current moment, but
for each moment of time within the specified interval as the list.
'''

from ReadConf import get_param
from collect_info import save_sysinfo
from db import dbase
from loggers import logger_si
from HTTP_si import ServerInfoRequestHandler
from http.server import HTTPServer
from multiprocessing import Process


def CreatHTTPserv(dBase, hostName, serverPort):
    '''
    Return instans of ServerInfoRequestHandler
    '''
    InstServerInfoRequestHandler = ServerInfoRequestHandler
    InstServerInfoRequestHandler.dBase = dBase
    InsServerInfo = HTTPServer((hostName, serverPort),
                               InstServerInfoRequestHandler)
    return InsServerInfo


if __name__ == '__main__':

    dic_param = get_param()
    logger = logger_si(folder="Log", name='ServerSysInfo')
    if dic_param['DataBase']:
        dbInfo = dbase()
        process_save_si = Process(target=save_sysinfo,
                                  args=(dic_param['W_Interval'],
                                        dic_param['Storage_time'], dbInfo))
        process_save_si.start()

    else:
        dbInfo = None
        logger.error('Connection database error!')

    HTTPserv = CreatHTTPserv(dbInfo, hostName=dic_param['HostName'],
                             serverPort=dic_param['Port'])
    try:
        print("Server started http://%s:%s" % (dic_param['HostName'],
                                               dic_param['Port']))
        HTTPserv.serve_forever()
    except KeyboardInterrupt:
        logger.info('Server was stopped by user!')
        pass

    HTTPserv.server_close()
    print("Server stopped.")
