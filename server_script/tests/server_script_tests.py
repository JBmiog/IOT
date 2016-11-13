import shutil
import server_script
import unittest
import pathnames
import time

class ServerScriptTest(unittest.TestCase):

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
    def smoke_run_steps(self):
        server_script.ENABLE_DB_WRITE = 1
        server_script.ENABLE_MATCH_SEARCH = 1
        server_script.ENABLE_MOVING_FILES = 1
        server_script.ENABLE_EMAILING = 1
        pic_fail_path = pathnames.move_here_if_fail_test
        pic_success_path = pathnames.move_here_if_success_test
        e_mail_message = "Subject: License plates smoke test\n\n"
        server_script.process_images(pathnames.pic_test_location_with_space, pathnames.db_test_location,
                                     pic_fail_path, pic_success_path)
        # now we copy a file into the test_location, if all good then we get a hook
        shutil.copy2(pathnames.test_pic_stash + "testimage1.jpg",
                     pathnames.pic_test_location_with_space + "testimage1.jpg")

    def test_run_smoke_test(self):
        # do a couple of runs
        self.smoke_run_steps()
        time.sleep(10)
        self.smoke_run_steps()
        time.sleep(10)
        self.smoke_run_steps()




