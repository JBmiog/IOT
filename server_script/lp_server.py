import os
import alpr_handler
import exif_reader
import pathnames

ENABLE_MOVING_FILES = 0
ENABLE_EMAILING = 1
ENABLE_DB_WRITE = 1
ENABLE_MATCH_SEARCH = 1

def remove_spaces():
    pic_list = os.listdir(upload_dir_path)
    for picture_name in pic_list:
        os.rename(os.path.join(upload_dir_path, picture_name), os.path.join(upload_dir_path, picture_name.replace(' ', '-')))


class LpServer():

    def get_lp(self, picture_path):
        self.lp, self.conf = alpr_handler(picture_path)
        if self.lp != "0" && self.conf != 0:
            return 1
        else:
            return 0

    def get_exif(self, picture_path):
        time, gps = exif_reader.get_exif()

    def get_address(self, lat, lon):
        return geolocator.get_address(lat, lon)

    def db_io(self):
        db_write(record)
        return db_get_match(record)

    def email(self):
        email_handler.write(results, receiver_address)

print("IOT-license plate recognition example")
