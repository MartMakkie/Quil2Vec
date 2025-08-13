import os
# import logging

loggingDir = 'logs'

import logging
import os
from app.core.status import StatusBarHandler

_loggers = {}

def get_logger(name: str, status_handler: StatusBarHandler = None, log_dir="logs"):
    if name in _loggers:
        logger = _loggers[name]
    else:
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        handleLogFiles(log_dir, f"{name}.log", 500000, 2)
        # File handler (only once)
        os.makedirs(log_dir, exist_ok=True)
        file_handler = logging.FileHandler(os.path.join(log_dir, f"{name}.log"))
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)

        logger.propagate = False
        _loggers[name] = logger

    # ✅ Always add status bar handler if passed and not already added
    if status_handler and not any(isinstance(h, StatusBarHandler) for h in logger.handlers):
        status_handler.setFormatter(logging.Formatter('%(name)s: %(message)s'))
        logger.addHandler(status_handler)

    return logger

# def get_logger(name: str, status_handler: StatusBarHandler = None, log_dir="logs"):
#     """
#     Creates or retrieves a logger configured for a module.

#     Args:
#         name (str): Typically use `__name__` or a custom name per module.
#         status_handler (StatusBarHandler): Optional shared handler for UI messages.
#         log_dir (str): Directory to store log files in.

#     Returns:
#         logging.Logger
#     """
#     if name in _loggers:
#         return _loggers[name]

#     os.makedirs(log_dir, exist_ok=True)
#     logger = logging.getLogger(name)
#     logger.setLevel(logging.INFO)

#     # File handler
#     file_path = os.path.join(log_dir, f"{name}.log")
#     file_handler = logging.FileHandler(file_path)
#     file_handler.setFormatter(logging.Formatter(
#         '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#     ))
#     logger.addHandler(file_handler)

#     # Optional status bar handler
#     if status_handler:
#         status_handler.setFormatter(logging.Formatter('%(name)s: %(message)s'))
#         logger.addHandler(status_handler)

#     logger.propagate = False  # Don't pass to root
#     _loggers[name] = logger
#     return logger


def createFileIfNotExist(fname: str):
    if not os.path.isfile(fname):
        with open(fname, "w") as outfile:
            outfile.write("")

def createDirCheckNotExist(dir:str, logger):
    if not os.path.isdir(dir):
        os.mkdir(dir)
        logger.info(f'Directory {dir} did not exist and was created succesfully')

def handleLogFiles(dirname: str, fname: str, maxSize=5000000, maxCache=10):
    """function to handle logs, if size of logfile is larger than maxSize (in mb) will create new logfile
    also creates new logfile if it does not exist"""
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    fullfname = dirname + "/" + fname
    createFileIfNotExist(fullfname)
    if os.path.getsize(fullfname) > maxSize:
        # if os.path.isfile(fullfname[:-4] + str(maxCache) + ".log"):
        filename = fullfname
        filenameCount = 0
        if os.path.isfile(filename):
            if not os.path.isfile(fullfname[:-4] + str(filenameCount) + ".log"):
                os.rename(fullfname, fullfname[:-4] + str(filenameCount) + ".log")
                createFileIfNotExist(fullfname)
            else:
                while os.path.isfile(filename):
                    # print(filenameCount)
                    # print('counting')
                    filename = fullfname[:-4] + str(filenameCount) + ".log"
                    filenameCount += 1
                filenameCount-=1
                # print(filenameCount)
                for i in reversed(range(0, filenameCount)):
                    if i != maxCache:
                        os.rename(
                            fullfname[:-4] + str(i) + ".log",
                            fullfname[:-4] + str(i + 1) + ".log",
                        )
                    else:
                        os.remove(fullfname[:-4] + str(i) + ".log")
                createFileIfNotExist(fullfname)




def createFileIfNotExist(fname: str):
    if not os.path.isfile(fname):
        with open(fname, "w") as outfile:
            outfile.write("")

def handleLogFiles(dirname: str, fname: str, maxSize=5000000, maxCache=10):
    """function to handle logs, if size of logfile is larger than maxSize (in mb) will create new logfile
    also creates new logfile if it does not exist"""
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    fullfname = dirname + "/" + fname
    createFileIfNotExist(fullfname)
    if os.path.getsize(fullfname) > maxSize:
        # if os.path.isfile(fullfname[:-4] + str(maxCache) + ".log"):
        filename = fullfname
        filenameCount = 0
        if os.path.isfile(filename):
            if not os.path.isfile(fullfname[:-4] + str(filenameCount) + ".log"):
                os.rename(fullfname, fullfname[:-4] + str(filenameCount) + ".log")
                createFileIfNotExist(fullfname)
            else:
                while os.path.isfile(filename):
                    # print(filenameCount)
                    # print('counting')
                    filename = fullfname[:-4] + str(filenameCount) + ".log"
                    filenameCount += 1
                filenameCount-=1
                # print(filenameCount)
                for i in reversed(range(0, filenameCount)):
                    if i != maxCache:
                        os.rename(
                            fullfname[:-4] + str(i) + ".log",
                            fullfname[:-4] + str(i + 1) + ".log",
                        )
                    else:
                        os.remove(fullfname[:-4] + str(i) + ".log")
                createFileIfNotExist(fullfname)
