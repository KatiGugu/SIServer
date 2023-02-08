'''
The module provides system information collection functions
'''
import json
import psutil
from platform import uname
import types
import time
from loggers import logger_si


def correct_size(bts, ending='iB'):
    '''
    Returns a value in human readable format.
    '''
    size = 1024
    for item in ["", "K", "M", "G", "T", "P"]:
        if bts < size:
            return f"{bts:.2f}{item}{ending}"
        bts /= size


def collect_info():
    '''
    Returns a dictionary with system information
    '''
    collect_info_dict = dict()
    if 'info' not in collect_info_dict:
        collect_info_dict['info'] = dict()
    collect_info_dict['info']['net_io'] = dict()
    net_io = psutil.net_io_counters(pernic=True)
    for interface in net_io:
        collect_info_dict['info']['net_io'][interface] = dict()
        for attr in dir(type(net_io[interface])):
            if not attr.startswith('_') and not \
                isinstance(getattr(net_io[interface], attr),
                           types.BuiltinMethodType):
                (collect_info_dict['info']['net_io'][interface]
                 [attr]) = getattr(net_io[interface], attr)

    collect_info_dict['info']['memory'] = dict()
    ram = psutil.virtual_memory()
    collect_info_dict['info']['memory']['ram'] = dict()
    for attr in dir(type(ram)):
        if not attr.startswith('_') and not \
                isinstance(getattr(ram, attr), types.BuiltinMethodType):
            collect_info_dict['info']['memory']['ram'][attr] = \
                getattr(ram, attr)

    swap = psutil.swap_memory()
    collect_info_dict['info']['memory']['swap'] = dict()
    for attr in dir(type(swap)):
        if not attr.startswith('_') and not \
                isinstance(getattr(swap, attr), types.BuiltinMethodType):
            collect_info_dict['info']['memory']['swap'][attr] = \
                getattr(swap, attr)

    for partition in psutil.disk_partitions():
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        if 'disk_info' not in collect_info_dict['info']:
            collect_info_dict['info']['disk_info'] = dict()
        if f"'device': {partition.device}" not in \
           collect_info_dict['info']['disk_info']:
            collect_info_dict['info']['disk_info'][partition.device] = dict()
            for attr in dir(type(partition_usage)):
                if not attr.startswith('_') and not \
                        isinstance(getattr(partition_usage, attr),
                                   types.BuiltinMethodType):
                    (collect_info_dict
                     ['info']['disk_info']
                     [partition.device][attr]) = getattr(partition_usage, attr)
    return collect_info_dict


def save_sysinfo(interval, Storage_time, dBase):
    '''
    Collects and saves system information in a database.
    Runs in a parallel process with an HTTP server.
    '''
    logger = logger_si(folder="Log", name='CollectingSysInfo')
    interval_sec = interval*24*3600
    try:
        while True and dBase is not None:
            jsonStr = json.dumps(collect_info())
            dBase.save_to_db(time.time(), jsonStr)
            dBase.conection.commit()
            time.sleep(interval)
            time_of_f_r = dBase.time_of_first_rec()
            if time_of_f_r is not None:
                if (time.time() - time_of_f_r[0]) > Storage_time:
                    dBase.del_records(time.time() - interval_sec)
    except KeyboardInterrupt:
        logger.info('Collectong system information was interupted by user.')
        pass
