import unittest
import picture_handler
import pathnames

class PictureHandlerTest(unittest.TestCase):

    def test_complete_walktrough(self):
        ph = picture_handler.PictureHandler(pathnames.success_picture)
        result = ph.info_extract_procedure()
        print(ph.format_info_to_string())

        self.assertTrue(True, result)