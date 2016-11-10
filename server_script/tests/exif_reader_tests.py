import exif_reader
import unittest
import pathnames

class ExifReaderTest(unittest.TestCase):

    # test if any exif data is found
    def test_exif_read(self):
        path = pathnames.success_picture
        exif_data = exif_reader.get_exif(path)
        print(exif_data)
        self.assertNotEquals = (None, exif_data)

    # test if exif data has correct GPS location
    def test_gps_location_read(self):
        path = pathnames.success_picture
        exif_data = exif_reader.get_exif(path)
        lat, lon = exif_reader.get_lat_lon(exif_data)
        self.assertEquals(lat, 51.9986995)
        self.assertEquals(lon, 4.371992722222222)

    # test if exif data has correct time stamp
    def test_time_stamp_read(self):
        path = pathnames.success_picture
        exif_data = exif_reader.get_exif(path)
        time_stamp = exif_reader.get_time_pic_taken(exif_data)
        print(time_stamp)
        self.assertEquals(time_stamp, "2016:10:18 15:06:16")