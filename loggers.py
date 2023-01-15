import os
import logging
import  logging.handlers
#import logging.config


class logger_si(logging.Logger):
    def __init__(self, folder="log", name = 'ServerSI', *args, **kwargs):
        self.LOG_FILE = 'error.log'
        if folder == None:
            self.FOLDER_LOG = "log"
        else:
            self.FOLDER_LOG =  folder

        if not os.path.exists(self.FOLDER_LOG):
            os.mkdir(self.FOLDER_LOG)
        super().__init__(name, *args, **kwargs)

        self.setLevel(logging.INFO)
        fh = logging.handlers.WatchedFileHandler(
            os.environ.get("LOGFILE", self.FOLDER_LOG+"/"+ self.LOG_FILE))
        #ch = logging.StreamHandler()
        fh.setLevel(logging.INFO)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        fh.setFormatter(formatter)

        # add ch to logger
        self.addHandler(fh)
        


    def get_logger(self, name, template='default'):

        # create logger
        logger = self.getLogger(name)
        logger.setLevel(self.INFO)

        # create console handler and set level to debug
        fh = self.handlers.WatchedFileHandler(
            os.environ.get("LOGFILE", self.FOLDER_LOG+"/"+ self.LOG_FILE))
        #ch = logging.StreamHandler()
        fh.setLevel(self.INFO)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        fh.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(fh)
        return logger



