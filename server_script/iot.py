import time
import os
import re
import PIL.Image
import csv
import shutil
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Nominatim

upload_dir_path = "/home/dviterig/Downloads/images/"
upload_dir_path_no_space = "/home/dviterig/Downloads/images/"
old_dir_path = "/home/dviterig/Downloads/images_old/"

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


def get_lp_and_confidence(data, second_lp):
    # data = "plate0: 10 results \n\t- H786P0J\tconfidence: 89.8356\n\t- H786POJ\t confidence: 87.6114\n"
    lp_correct = 0
    line = data.split("\n")
    for i in range(1,4):#check the first 3 lp's in the data in order to look for a dutch lp
        lp = re.search('- (.*)\t', line[i+second_lp])
        conf = re.search('confidence: (.*)', line[i+second_lp])
        lp_string = lp.group(1)
        conf_float = float(conf.group(1))
        if len(lp_string) == 6:#if not dutch lp length -> lp incorrect
            lp_correct = 1
            break

    return lp_string, conf_float, lp_correct


def get_address(lat, lon):
    if (lat != None and lon != None):
        location_string = (str(lat) + ', ' + str(lon))
        print(location_string)
        geolocator = Nominatim()
        location = geolocator.reverse(location_string)
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

new_pictures = os.listdir(upload_dir_path)
# bash and python handle spaces differently,
# remove all spaces from picture names
remove_spaces()
new_pictures = os.listdir(upload_dir_path)
print("IOT-license plate recognition example")
for pic_name in new_pictures:
    print(pic_name)
    full_command = "alpr -c eu " + upload_dir_path_no_space + pic_name
    output, err = run_script(full_command)
    output_string = output.decode(encoding='utf-8')
    if "results" in output_string:
        # strip location + time + date
        print (output_string)
        lp, conf, lp_ok = get_lp_and_confidence(output_string, 0)
        if lp_ok == 1:
            print("License plate detected: %s, confidence: %s  " % (lp, conf))
            exif_data = get_exif(pic_name)
            lat, lon = get_lat_lon(exif_data)
            address = get_address_by_gps(lat, lon)
            time = get_time_pic_taken(exif_data)
            data_list = [lp, conf, lat, lon, address, time]
            csv_write(data_list)
        else:
            print("No dutch license plate detected")

        if (len(output_string) > 400):  #in case of second lp in the picture
            print("2 license plates detected!!!")
            lp, conf, lp_ok = get_lp_and_confidence(output_string, 11)
            if lp_ok == 1:
                print("License plate detected: %s, confidence: %s  " % (lp, conf))
                exif_data = get_exif(pic_name)
                lat, lon = get_lat_lon(exif_data)
                address = get_address_by_gps(lat, lon)
                time = get_time_pic_taken(exif_data)
                data_list = [lp, conf, lat, lon, address, time]
                csv_write(data_list)
            else:
                print("No dutch license plate detected")

        # check if matches data from db
        # notify user
        # put data in .csv
    else:
        print(output_string)

for pic_name in new_pictures: #move pics to old_images directory
    shutil.move(upload_dir_path + pic_name, old_dir_path)
