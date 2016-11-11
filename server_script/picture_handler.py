import os
import alpr_handler
import geolocator_handler
import db_handler
import exif_reader
import pathnames


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
    picture_path_no_space = None

    def __init__(self, picture_path):
        self.picture_path = picture_path
        self.picture_path_no_space = str(picture_path).replace("\\", "")

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
        self.license_plate_record = db_handler.get_matches(self.license_plate, pathnames.db_location)

    def db_write(self):
        csv_format_data = str(self.license_plate) + "," + str(self.confidence) + ","
        csv_format_data += str(self.gps_latitude) + "," + str(self.gps_longitude) + ","
        csv_format_data += str(self.address) + ","+ str(self.time_stamp)
        db_handler.db_write(csv_format_data, pathnames.db_test_location)

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
            string =  "Plate numb:\t\t" + str(self.license_plate) + "\n"
            string += "Confidence:\t\t" + str(self.confidence) + "\n"
            string += "Time spotted:\t" + str(self.time_stamp) + "\n"
            string += "Address:\t\t" + str(self.address) + "\n"
            string += "Gps latitude:\t" + str(self.gps_latitude) + "\n"
            string += "Gps longitude:\t" + str(self.gps_longitude) + "\n"
            string += "--------------------------------------------------\n"
            string += "previous records:" + str(self.license_plate_record)
        else:
            string = "could not find lp in picture at location:, ", self.picture_path
        return string
