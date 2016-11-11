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


def remove_spaces(pathname):
    pic_list = os.listdir(pathname)
    for picture_name in pic_list:
        os.rename(os.path.join(pathnames.upload_dir_path, picture_name), os.path.join(pathnames.upload_dir_path, picture_name.replace(' ', '-')))


def handler(signum, frame):
    print("modification in:", filename)
    remove_spaces(pathnames.upload_dir_path)
    # get list of pictures
    new_pictures_names = os.listdir(pathnames.upload_dir_path)
    # per picture, extract info
    for pic_name in new_pictures_names:
        ph = PictureHandler(pathnames.upload_dir_path_no_space + pic_name)
        if ph.info_extract_procedure():
            if ENABLE_MOVING_FILES:
                print("did not move, lol")
        print(ph.format_info_to_string())


signal.signal(signal.SIGIO, handler)
fd = os.open(filename,  os.O_RDONLY)
fcntl.fcntl(fd, fcntl.F_SETSIG, 0)
fcntl.fcntl(fd, fcntl.F_NOTIFY,
            fcntl.DN_MODIFY | fcntl.DN_CREATE | fcntl.DN_MULTISHOT)

while True:
    time.sleep(10000)