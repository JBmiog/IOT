import os
import alpr_handler
import geolocator_handler
import db_handler
import exif_reader
import pathnames


class PictureHandler:
    lp_found = 0
    found_record = 0
    picture_path = None
    time_stamp = None
    gps_longitude = None
    gps_latitude = None
    address = None
    license_plate = None
    confidence = None
    license_plate_record = None
    picture_path_no_space = None
    db_path = None


    def __init__(self, picture_path, db_path=None):
        self.picture_path = picture_path
        self.picture_path_no_space = str(picture_path).replace("\\", "")
        if db_path is not None:
            self.db_path = db_path

    def get_lp(self):
        self.license_plate, self.confidence = alpr_handler(self.picture_path)
        if self.lp is not None and self.conf is not None:
            return 1
        else:
            return 0

    def get_exif(self):
        exif_data = exif_reader.get_exif(self.picture_path_no_space)
        self.time_stamp = exif_reader.get_time_pic_taken(exif_data)
        self.gps_latitude, self.gps_longitude = exif_reader.get_lat_lon(exif_data)

    def get_address(self):
        self.address = geolocator_handler.get_address(self.gps_latitude, self.gps_longitude)

    def db_match_check(self):
        self.found_record, self.license_plate_record = db_handler.get_matches(self.license_plate, self.db_path)

    def db_write(self):
        csv_format_data = [
            self.license_plate, self.confidence, self.gps_latitude,
            self.gps_longitude, self.address, self.time_stamp]
        print("write in db")
        db_handler.db_write(csv_format_data, self.db_path)

    def info_extract_procedure(self):
        # alpr needs with \\ as space
        self.license_plate, self.confidence = alpr_handler.get_lp_and_confidence(self.picture_path)
        if self.license_plate is not None:
            self.get_exif()
            self.get_address()
            self.lp_found = 1
            return 1
        else:
            # no lp found
            self.lp_found = 0
            return 0

    def format_info_to_string(self):
        if self.lp_found:
            string = "\n--------------------------------------------------\n"
            string += "Plate numb:\t" + str(self.license_plate) + "\n"
            string += "Confidence:\t" + str(self.confidence) + "\n"
            string += "Time spott:\t" + str(self.time_stamp) + "\n"
            string += "Address   :\t" + str(self.address) + "\n"
            string += "Gps latitu:\t" + str(self.gps_latitude) + "\n"
            string += "Gps longit:\t" + str(self.gps_longitude) + "\n"
            string += "File path :\t" + str(self.picture_path) + "\n"
            if self.found_record != 1:
                string += "previous records:" + "\n"
                string += "records   :\t" + str(self.found_record - 1) + "\n"
                for record in range(1, self.found_record):
                    string += "-------" + "\n"
                    string += "record  :\t" + str(record) + "\n"
                    string += "time    :\t" + str(self.license_plate_record[record][5] + "\n")
                    string += "location:\t" + str(self.license_plate_record[record][4] + "\n")
                    string += "-------" + "\n"
                string += "--------------------------------------------------\n"
            else:
                string += "no previous records known" + "\n"
                string += "--------------------------------------------------\n"
        else:
            string  = "\n--------------------------------------------------\n"
            string += "could not find lp in picture: " + str(self.picture_path)
            string += "\n--------------------------------------------------\n"
        return string
