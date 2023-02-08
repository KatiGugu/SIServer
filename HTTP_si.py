'''
The Http server accepts two types of Get requests:
http://HostName:Port/current
The current system data will be returned.
and
http://HostName:Port/stat?time1={time interval start}&time2={time interval
finish} The data accumulated in the database for the specified time
interval will be returned.

'''

import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from collect_info import collect_info


class ServerInfoRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        '''
        Returns a result depending on the content of the request. If
        URL = /current, then current data will be returned, if /stat,
        then data will be returned for a period between time1 and
        time2 previously stored in the database.
        '''
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        urlres = urlparse(self.path)
        if urlres.path == '/current' or urlres.path == '/current/':
            SysInfo = json.dumps(collect_info(), )
        elif urlres.path == '/stat/' or urlres.path == '/stat':
            param = self.pars_q(urlres.query)
            if self.dBase is not None:
                records = self.dBase.retrive_from_db(param['time1'],
                                                     param['time2'])
                res = {}
                list_rec = []
                for row in records:
                    list_rec.append({'Date': row[0], 'SysData': row[1]})
                    res['Date'] = row[0]
                    res['SysData'] = row[1]
                SysInfo = json.dumps(list_rec)
            else:
                SysInfo = 'Statistics are missing!'

        else:
            SysInfo = "Invalid request!!!"
        self.wfile.write(bytes(SysInfo, "utf-8"))

    def pars_q(self, query):
        '''Pars HTML query and returns parameters'''
        list_par = query.split('&')
        if len(list_par) == 2:
            dic_par = {}
            par1 = list_par[0].split('=')
            par2 = list_par[1].split('=')
            if len(par1) == 2:
                if par1[0].strip() == 'time1' and par1[1].isdigit():
                    dic_par['time1'] = int(par1[1])
                else:
                    return None
                if par2[0].strip() == 'time2' and par2[1].isdigit():
                    dic_par['time2'] = int(par2[1])
                else:
                    return None
            else:
                return None
        else:
            return None
        return dic_par
