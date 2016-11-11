
from geopy.geocoders import Nominatim

def get_address_by_gps(lat, lon):
    found_address = get_address(lat, lon)
    return found_address

def get_address(lat, lon):
    if (lat != None and lon != None):
        location_string = (str(lat) + ', ' + str(lon))
        # print(location_string)
        geolocator = Nominatim()
        try:
            return geolocator.reverse(location_string)
        except:
            return "no address known"

    else:
        return "no address known"
