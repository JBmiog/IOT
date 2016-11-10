from geopy.geocoders import Nominatim

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