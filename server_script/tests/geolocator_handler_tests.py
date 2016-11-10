import geolocator_handler
import unittest

class GeolocatorTest(unittest.TestCase):

    def test_address_by_gps(self):
        lat = 51.9986995
        lon = 4.371992722222222
        address = geolocator_handler.get_address_by_gps(lat, lon)
        print (address)
        self.assertNotEqual(address, "no address known")