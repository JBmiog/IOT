import fcntl
import os
import signal
import pathnames
from picture_handler import PictureHandler

ENABLE_MOVING_FILES = 0
ENABLE_EMAILING = 0
ENABLE_DB_WRITE = 0
ENABLE_MATCH_SEARCH = 0

filename = pathnames.upload_dir_path


def remove_spaces(pathname):
    pic_list = os.listdir(pathname)
    for picture_name in pic_list:
        os.rename(os.path.join(pathnames.upload_dir_path, picture_name), os.path.join(pathnames.upload_dir_path, picture_name.replace(' ', '-')))


# so this is bad practice, but I can't seem to disable the interrupt
# so now it points to this fake handler, so I can change the white space
# in an address path, which would signal the handler again...
# this function servers as a "disable_signal", by pointing to a void
# handler...
def fake_handler(signum, frame):
    None


def new_pic_handler(signum, frame):
    print("modification in:", filename)
    signal.signal(signal.SIGIO, fake_handler)
    remove_spaces(pathnames.upload_dir_path)
    set_file_change_interrupt()
    process_images(pathnames.upload_dir_path)


def process_images(pic_path_name, db_path_name):
    # get list of pictures
    new_pictures_names = os.listdir(pic_path_name)
    path_name_space_corrected = pic_path_name.replace(" ", "\ ")
    # per picture, extract info
    for pic_name in new_pictures_names:
        ph = PictureHandler(str(path_name_space_corrected + pic_name), db_path_name)
        if ph.info_extract_procedure():
            if ENABLE_DB_WRITE:
                ph.db_write()
            if ENABLE_MATCH_SEARCH:
                ph.db_match_check()
        print(ph.format_info_to_string())


def set_file_change_interrupt():
    signal.signal(signal.SIGIO, new_pic_handler)
    fd = os.open(filename,  os.O_RDONLY)
    fcntl.fcntl(fd, fcntl.F_SETSIG, 0)
    fcntl.fcntl(fd, fcntl.F_NOTIFY,
                fcntl.DN_MODIFY | fcntl.DN_CREATE | fcntl.DN_MULTISHOT)

