import fcntl
import os
import signal
import email_handler
import pathnames
from picture_handler import PictureHandler
import _thread

ENABLE_MOVING_FILES = 1
ENABLE_EMAILING = 1
ENABLE_DB_WRITE = 1
ENABLE_MATCH_SEARCH = 1
ENABLE_DEBUG_INFO = 1

filename = pathnames.upload_dir_path


def remove_spaces(pathname):
    pic_list = os.listdir(pathname)
    for picture_name in pic_list:
        try:
            os.rename(os.path.join(pathnames.upload_dir_path, picture_name), os.path.join(pathnames.upload_dir_path, picture_name.replace(' ', '_')))
        except FileNotFoundError as err:
            print("could not rename file; ", err)


# so this is bad practice, but I can't seem to disable the interrupt
# so now it points to this fake handler, so I can change the white space
# in an address path, which would signal the handler again...
# this function servers as a "disable_signal", by pointing to a void
# handler...
def fake_handler(signum, frame):
    None


def new_pic_handler(signum, frame):
    signal.signal(signal.SIGIO, fake_handler)
    print("modification in:", filename)
    remove_spaces(pathnames.upload_dir_path)
    set_file_change_interrupt()
    # process_images(pathnames.upload_dir_path, pathnames.db_location)
    _thread.start_new_thread(process_images, (pathnames.upload_dir_path, pathnames.db_location))

def process_images(pic_path_name, db_path_name, pic_fail_path=None, pic_success_path=None, e_mail_message=None):
    print("a new thread started")
    if pic_fail_path is None:
        pic_fail_path = pathnames.move_here_if_fail
    if pic_success_path is None:
        pic_success_path = pathnames.move_here_if_success
    if e_mail_message is None:
        # we will append the data behind the subject of the email.
        e_mail_message = "Subject: License plates scan results\n\n"
    # get list of pictures
    new_pictures_names = os.listdir(pic_path_name)
    path_name_space_corrected = pic_path_name.replace(" ", "\ ")
    # per picture, extract info
    for pic_name in new_pictures_names:
        ph = PictureHandler(str(path_name_space_corrected + pic_name), db_path_name)
        if ph.info_extract_procedure():
            if ENABLE_MATCH_SEARCH:
                ph.db_match_check()
            if ENABLE_DB_WRITE:
                ph.db_write()
            if ENABLE_MOVING_FILES:
                try:
                    os.rename(pic_path_name+pic_name, pic_success_path+pic_name)
                except FileNotFoundError as err:
                    print("could not move file;", err)
        else:
            if ENABLE_MOVING_FILES:
                try:
                    os.rename(pic_path_name + pic_name, pic_fail_path + pic_name)
                except FileNotFoundError as err:
                    print("could not move file;", err)
        e_mail_message += str(ph.format_info_to_string())
        if ENABLE_DEBUG_INFO:
            print(ph.format_info_to_string())
    if ENABLE_EMAILING:
        eh = email_handler.Emailer()
        eh.tx_email(e_mail_message)


def set_file_change_interrupt():
    signal.signal(signal.SIGIO, new_pic_handler)
    fd = os.open(filename,  os.O_RDONLY)
    fcntl.fcntl(fd, fcntl.F_SETSIG, 0)
    fcntl.fcntl(fd, fcntl.F_NOTIFY,
                fcntl.DN_MODIFY | fcntl.DN_CREATE | fcntl.DN_MULTISHOT)

