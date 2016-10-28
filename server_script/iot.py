import time
import os
import re
import PIL.Image
import csv
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Nominatim

import emailer
import pathnames

upload_dir_path = pathnames.upload_dir_path
upload_dir_path_no_space = pathnames.upload_dir_path_no_space
move_here_if_success = pathnames.move_here_if_success
move_here_if_fail = pathnames.move_here_if_fail

LP_POS = 0
CONFIDENCE_POS = 1
LAT_POS = 2
LON_POS = 3
ADDRESS_POS = 4
TIME_POS = 5
NAME_POS = 6

k = ","
n = "\n"
t = "\t"

emailer.server.ehlo()
def tx_email(message_data):
    emailer.server.starttls()
    emailer.server.login(emailer.username, emailer.password)
    emailer.server.sendmail(emailer.fromaddr, emailer.toaddrs, message_data)
    emailer.server.quit()


# https://gist.github.com/erans/983821
def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data

# https://gist.github.com/erans/983821
def _get_if_exist(data, key):
    if key in data:
        return data[key]

    return None


# https://gist.github.com/erans/983821
def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)


# https://gist.github.com/erans/983821
def get_lat_lon(exif_data):
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    lat = None
    lon = None

    if "GPSInfo" in exif_data:
        gps_info = exif_data["GPSInfo"]

        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":
                lat = 0 - lat

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

    return lat, lon
 

def get_time_pic_taken(exif_data):
    if "DateTimeOriginal" in exif_data:
        date = exif_data["DateTimeOriginal"]
        return date

# stack overflow
def run_script(script, stdin=None):
    """Returns (stdout, stderr), raises error on non-zero return code"""
    import subprocess
    # Note: by using a list here (['bash', ...]) you avoid quoting issues, as the
    # arguments are passed in exactly this order (spaces, quotes, and newlines won't
    # cause problems):
    proc = subprocess.Popen(['bash', '-c', script],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        stdin=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode:
        raise ScriptException(proc.returncode, stdout, stderr, script)
    return stdout, stderr


class ScriptException(Exception):
    def __init__(self, returncode, stdout, stderr, script):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        Exception.__init__('Error in script')


def remove_spaces():
    pic_list = os.listdir(upload_dir_path)
    for picture_name in pic_list:
        os.rename(os.path.join(upload_dir_path, picture_name), os.path.join(upload_dir_path, picture_name.replace(' ', '-')))


def get_lp_and_confidence(data, n_lp, m_nf):
    lines = data.split("\n")
    for i in range(1,10):
        if "pattern_match: 1" in lines[i + 9*n_lp]:
            m_nf = 0
            lp = re.search("- (.*)\t conf", lines[i + 9*n_lp])
            conf = re.search('confidence: (.*)\t patt', lines[i + 9*n_lp])
            lp_string = lp.group(1)
            conf_float = float(conf.group(1))
            return lp_string, conf_float, m_nf


def get_address(lat, lon):
    if (lat != None and lon != None):
        location_string = (str(lat) + ', ' + str(lon))
        # print(location_string)
        geolocator = Nominatim()
        try:
            location = geolocator.reverse(location_string)
        except:
            print("could not resolve location")
            return("no location known")
        return location.address
    else:
        return "not available"


def get_exif(pic_name):
    img = PIL.Image.open(upload_dir_path + pic_name)
    exif_d = get_exif_data(img)
    return exif_d


def get_address_by_gps(lat, lon):
    found_address = get_address(lat, lon)
    return found_address


# function takes a string(comma seperated!)
# and puts it in the csv file
def csv_write(list):
    with open('lp_db.csv', 'a') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        csv_writer.writerow(list)


# function that searchers the csv db for a
# given license plate and returns
# the results in a dict
def csv_check_match_lp(licsene_plate):
    i = 1
    dict = {}
    with open('lp_db.csv', 'rt') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            if row[0] == licsene_plate:
                dict[i] = row
                i+=1
    return dict

ENABLE_MOVING_FILES = 0
ENABLE_EMAILING = 1
ENABLE_DB_WRITE = 1
ENABLE_MATCH_SEARCH = 1

def search_csv_for_match(license_plate):
    string = ""
    matches = csv_check_match_lp("GZVX47")
    if matches != {}:
        string = ("We have a logged history of this licenseplate:" + n)
        for row in matches:
            string += ("location:"+t+matches[row][ADDRESS_POS]+n)
            string += ("date     "+t+matches[row][TIME_POS]+n)
    return string

print("IOT-license plate recognition example")
while(1):
    if ENABLE_DB_WRITE:
        file_oploaded = 0
        # bash and python handle spaces differently,
        # remove all spaces from picture names
        remove_spaces()
        new_pictures = os.listdir(upload_dir_path)
        all_data_string = "\n"
        append_to_mail = ""
        for pic_name in new_pictures:
            file_oploaded = 1
            print(pic_name)
            full_command = "alpr -n 8 -c eu -p nl " + upload_dir_path_no_space + pic_name
            output, err = run_script(full_command)
            output_string = output.decode(encoding='utf-8')
            print(output_string)
            append_to_mail = "";#empty varaible for every picture
            if "results" in output_string:
                #number_lp: number of lp in the picture
                match_nf = 1 #Initialise "match_nf"
                if "plate2" in output_string:
                    number_lp = 3
                elif "plate1" in output_string:
                    number_lp = 2
                elif "plate0" in output_string:
                    number_lp = 1
                else:
                    number_lp = 0
                #
                while(number_lp > 0):
                    number_lp -= 1
                    lp, conf, match_nf = get_lp_and_confidence(output_string, number_lp, match_nf)
                    exif_data = get_exif(pic_name)
                    lat, lon = get_lat_lon(exif_data)
                    address = get_address_by_gps(lat, lon)
                    timestamp = get_time_pic_taken(exif_data)

                    if ENABLE_MOVING_FILES:
                        os.rename(upload_dir_path + pic_name, move_here_if_success+pic_name)

                    # gather info to e-mail
                    append_to_mail += pic_name + ": " + "found a lp!" + n
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
                #end while  

                if match_nf:
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


        msg = """From: <iotproject.tudelft@gmail.com >
        To: <dviterig@gmail.com>
        Subject: IOT - license plates scan results:

        """ + all_data_string
        if(ENABLE_EMAILING and file_oploaded == 1):
            tx_email(msg)


    print("round done")
    #time.sleep(20)
    break