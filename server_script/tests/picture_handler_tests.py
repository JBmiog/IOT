import unittest
import picture_handler
import pathnames

class PictureHandlerTest(unittest.TestCase):

    # make sure a pic with an recognisable license plate
    # does not crashes the system
    def test_complete_walktrough_valid(self):
        ph = picture_handler.PictureHandler(pathnames.success_picture)
        result = ph.info_extract_procedure()
        print(ph.format_info_to_string())
        self.assertTrue(True, result)

    def test_complete_walktrough_invalid(self):
        ph = picture_handler.PictureHandler(pathnames.fail_picture)
        result = ph.info_extract_procedure()
        print(ph.format_info_to_string())
        self.assertEquals(result, False)
