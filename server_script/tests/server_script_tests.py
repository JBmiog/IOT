import server_script
import unittest
import pathnames

class ServerScriptTest(unittest.TestCase):

    # tests if we  works correctly
    # def test_process_images_from_path_with_space(self):
    #     server_script.ENABLE_DB_WRITE = 0
    #     server_script.ENABLE_MATCH_SEARCH = 0
    #     server_script.ENABLE_MOVING_FILES = 0
    #     server_script.ENABLE_EMAILING = 0
    #     server_script.process_images(pathnames.pic_test_location_with_space, pathnames.db_test_location)
    #     self.assertEquals(True, True)

    # def test_process_images_write_to_test_db(self):
    #     server_script.ENABLE_DB_WRITE = 1
    #     server_script.ENABLE_MATCH_SEARCH = 0
    #     server_script.ENABLE_MOVING_FILES = 0
    #     server_script.ENABLE_EMAILING = 0
    #     server_script.process_images(pathnames.pic_test_location_with_space, pathnames.db_test_location)
    #     self.assertEquals(True, True)


    def test_process_images_match_search(self):
        server_script.ENABLE_DB_WRITE = 0
        server_script.ENABLE_MATCH_SEARCH = 1
        server_script.ENABLE_MOVING_FILES = 0
        server_script.ENABLE_EMAILING = 0
        server_script.process_images(pathnames.pic_test_location_with_space, pathnames.db_test_location)
        self.assertEquals(True, True)



