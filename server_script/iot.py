import time
import os
import re
import PIL.Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Nominatim

upload_dir_path = "/home/jeffrey/Dropbox/Camera Uploads/"
upload_dir_path_no_space = "/home/jeffrey/Dropbox/Camera\ Uploads/"


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


def get_lp_and_confidence(data):
    # data = "plate0: 10 results \n\t- H786P0J\tconfidence: 89.8356\n\t- H786POJ\t confidence: 87.6114\n"
    line = data.split("\n")
    lp = re.search('- (.*)\t', line[1])
    conf = re.search('confidence: (.*)', line[1])
    lp_string = lp.group(1)
    conf_float = float(conf.group(1))
    print(lp_string)
    print(conf_float)
    return lp_string, conf_float


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
    exif_data = get_exif_data(img)
    return exif_data


def get_address_by_gps(exif_data):
    lat, lon = get_lat_lon(exif_data)
    address = get_address(lat, lon)
    return address


print("IOT-license plate recognition example")
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
    print (output_string)
    if "results" in output_string:
        # strip location + time + date
        lp, conf = get_lp_and_confidence(output_string)

        exif = get_exif(pic_name)
        address = get_address_by_gps(exif)
        time = get_time_pic_taken(exif)
        print("addres is:")
        print(address)
        print("time pic taken is:")
        print(time)

        # store lp + confidence
        # check if matches data from db
        # notify user
        # put data in .csv
    else:
        print(output_string)
