import time
import fcntl
import os
import signal
import pathnames
from picture_handler import PictureHandler

ENABLE_MOVING_FILES = 0
ENABLE_EMAILING = 0
ENABLE_DB_WRITE = 0
ENABLE_MATCH_SEARCH = 0

print("IOT-license plate recognition example")
filename = pathnames.upload_dir_path
ph = PictureHandler()


def remove_spaces(pathname):
    pic_list = os.listdir(pathname)
    for picture_name in pic_list:
        os.rename(os.path.join(pathnames.upload_dir_path, picture_name), os.path.join(pathnames.upload_dir_path, picture_name.replace(' ', '-')))


def handler(signum, frame):
    print("modification in:", filename)
    remove_spaces(pathnames.upload_dir_path)
    # get list of pictures
    new_pictures_paths = os.listdir(pathnames.upload_dir_path)
    # per picture, extract info
    for pic_path in new_pictures_paths:
        ph = PictureHandler(pic_path)
        data_found = ph.info_extract_procedure()
        if data_found:
            if ENABLE_EMAILING:
                print("print iets")
        else:
            # append not find to e-mail data
            print("iets anders")
        if ENABLE_MOVING_FILES:
            print("weer iets anders")
            # send e-mail with all info
            # move files


signal.signal(signal.SIGIO, handler)
fd = os.open(filename,  os.O_RDONLY)
fcntl.fcntl(fd, fcntl.F_SETSIG, 0)
fcntl.fcntl(fd, fcntl.F_NOTIFY,
            fcntl.DN_MODIFY | fcntl.DN_CREATE | fcntl.DN_MULTISHOT)

while True:
    time.sleep(10000)