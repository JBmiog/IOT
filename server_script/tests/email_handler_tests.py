import unittest
import email_handler


class EmailHandlerTest(unittest.TestCase):

    def test_tx_email(self):
        message = "Subject: License plates scan results\n\n"
        ms = email_handler.Emailer()
        result = ms.tx_email(message)
        self.assertTrue(result)