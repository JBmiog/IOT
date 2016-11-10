import unittest
import pathnames
import alpr_handler

class AlprHandlerTests(unittest.TestCase):

    # test if a previous succesfully tested
    # lp will still give a good result
    # as this is open source, only confidence
    # will be verified
    def test_correct_recognition(self):
        path = pathnames.success_picture
        lp, conf = alpr_handler.get_lp_and_confidence(path)
        self.assertEquals(conf, 90.8965)

    # test if a picture without a lp
    # will result in no result
    def test_incorrect_image(self):
        path = pathnames.fail_picture
        lp, conf = alpr_handler.get_lp_and_confidence(path)
        print(lp,conf)
        self.assertEquals(conf, 0)

    # test if two lp's can be recognized
    # todo: add two_lp_in_one_image
    def test_two_lp_in_image(self):
        self.assertEquals(True, True)