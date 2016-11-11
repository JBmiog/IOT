import os
import alpr_handler
import geolocator_handler
import db_handler
import exif_reader


class PictureHandler:
    lp_found = 0
    picture_path = None
    time_stamp = None
    gps_longitude = None
    gps_latitude = None
    address = None
    license_plate = None
    confidence = None
    license_plate_record = None

    def __init__(self, picture_path):
        self.picture_path = picture_path

    def get_lp(self):
        self.license_plate, self.confidence = alpr_handler(self.picture_path)
        if self.lp is not None and self.conf is not None:
            self.lp_found = 1
            return 1
        else:
            self.lp_found = 0
            return 0

    def get_exif(self):
        exif_data = exif_reader.get_exif(self.picture_path)
        self.time_stamp = exif_reader.get_time_pic_taken(exif_data)
        self.gps_latitude, self.gps_longitude = exif_reader.get_lat_lon(exif_data)

    def get_address(self):
        return geolocator_handler.get_address(self.gps_latitude, self.gps_longitude)

    def db_match_check(self):
        self.license_plate_record = db_handler.get_matches(self.license_plate)

    def db_write(self, csv_format_data):
        self.db_write(csv_format_data)

    def info_extract_procedure(self):
        if alpr_handler.get_lp():
            self.get_exif()
            self.get_address()
            self.db_match_check()
            self.db_write(
                str(self.license_plate) + "," + str(self.confidence) + "," + str(self.gps_latitude) + "," +
                str(self.gps_longitude) + "," + str(self.address) + "," + str(self.time_stamp)
            )
            return 1
        else:
            # no lp found
            return 0

    def format_info_to_string(self):
        if self.lp_found:
            string = "plate numb:\t " + str(self.license_plate) + "\n"
            string += "confidence:\t" + str(self.confidence) + "\n"
            string += "time spotted:\t" + str(self.time_stamp) + "\n"
            string += "address:\t" + str(self.address) + "\n"
            string += "gps latitude:\t" + str(self.gps_latitude) + "\n"
            string += "gps longitude:\t" + str(self.gps_longitude) + "\n"
        else:
            string = "could not find lp in picture at location:, ", self.picture_path
        return string
