import db_handler
import unittest
import pathnames


class DbHandlerTest(unittest.TestCase):
    db_path = pathnames.db_test_location
    lp = "88-88-88"
    address = "Pietjesstraat 5"

    def test_write_succes(self):
        data = [self.lp, self.address]
        result = db_handler.db_write(data, self.db_path)
        self.assertTrue(result)

    def test_get_matches(self):
        data = [self.lp, self.address]
        db_handler.db_write(data, self.db_path)
        result = db_handler.get_matches(self.lp, self.db_path)
        self.assertIsNotNone(result)

