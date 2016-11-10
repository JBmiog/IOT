import time
import os

import pathnames

upload_dir_path = pathnames.upload_dir_path
upload_dir_path_no_space = pathnames.upload_dir_path_no_space
move_here_if_success = pathnames.move_here_if_success
move_here_if_fail = pathnames.move_here_if_fail

k = ","
n = "\n"
t = "\t"

ENABLE_MOVING_FILES = 0
ENABLE_EMAILING = 1
ENABLE_DB_WRITE = 1
ENABLE_MATCH_SEARCH = 1

def remove_spaces():
    pic_list = os.listdir(upload_dir_path)
    for picture_name in pic_list:
        os.rename(os.path.join(upload_dir_path, picture_name), os.path.join(upload_dir_path, picture_name.replace(' ', '-')))


print("IOT-license plate recognition example")

while(1):
    if ENABLE_DB_WRITE:
        file_oploaded = 0
        remove_spaces()
        new_pictures = os.listdir(upload_dir_path)
        all_data_string = "\n"
        mail_info = ""
        for pic_name in new_pictures:
            file_oploaded = 1
            print(pic_name)
            full_command = "alpr -n 8 -c eu -p nl " + upload_dir_path_no_space + pic_name
            output, err = run_script(full_command)
            output_string = output.decode(encoding='utf-8')
            print(output_string)
            if "results" in output_string:
                if "pattern_match: 1" in output_string:

                    # strip location + time + date
                    lp, conf = get_lp_and_confidence(output_string)
                    exif_data = get_exif(pic_name)
                    lat, lon = get_lat_lon(exif_data)
                    address = get_address_by_gps(lat, lon)
                    timestamp = get_time_pic_taken(exif_data)

                    if ENABLE_MOVING_FILES:
                        os.rename(upload_dir_path + pic_name, move_here_if_success+pic_name)
                    # check if matches data from db
                    if ENABLE_MATCH_SEARCH:
                        matches = search_csv_for_match(lp)

                    # gather info to e-mail
                    append_to_mail = pic_name + ": " + "found a lp!" + n
                    append_to_mail += "lp is: " + t + str(lp) + n
                    append_to_mail += "conf:  " + t + str(conf) + n
                    append_to_mail += "adrs:  " + t + str(address) + n
                    append_to_mail += "time:  " + t + str(timestamp) + n

                    # check if matches data from db
                    if ENABLE_MATCH_SEARCH:
                        matches = search_csv_for_match(lp)
                        append_to_mail += "--history--" + n + matches
                        append_to_mail += "-----------" + n

                    # put data in .csv
                    data_list = [lp, conf, lat, lon, address, time]
                    csv_write(data_list)

                else:
                    append_to_mail = pic_name + ": " + "Could not find a dutch lp" + n
                    if ENABLE_MOVING_FILES:
                        os.rename(upload_dir_path + pic_name, move_here_if_fail + pic_name)

            else:
                print(output_string)
                append_to_mail = pic_name+": "+"Could not find a lp"+n
                if ENABLE_MOVING_FILES:
                    os.rename(upload_dir_path + pic_name, move_here_if_fail + pic_name)

            all_data_string += append_to_mail + "\n"

        print(all_data_string)

    print("round done")
    time.sleep(20)

import alpr_handler
import exif_reader

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


# check if new image has arrived
# get lp (if present)
# get exif (if lp is present)
# write to db, and get match from db
# create e-mail containing lp, gps location, previous record.