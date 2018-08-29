from unittest.mock import patch
from unittest import TestCase

from src.block_bad_auth import read_process_file, log_ip_addresses, \
    PAST_IP_LOG, \
    run_process, WHITE_IPS


class TestClass(TestCase):
    TEST_MAIL_LOG = 'fixtures/mail.log'
    TEST_PAST_IP_LOG = 'fixtures/past_blocked_ips.log'

    class MyPopen:
        @staticmethod
        def communicate():
            return ['response', 'error']

    @patch("src.block_bad_auth.MAIL_LOG", TEST_MAIL_LOG)
    @patch("src.block_bad_auth.PAST_IP_LOG", TEST_PAST_IP_LOG)
    @patch("subprocess.Popen", return_value=MyPopen)
    def setUp(self,
              Popen):
        with open(self.TEST_PAST_IP_LOG, 'w') as f:
            f.write("94.102.56.215\n"
                    "121.237.137.75\n"
                    "should be gone")
        self.ip_set = read_process_file(self.TEST_MAIL_LOG)
        run_process()
        self.Popen = Popen
        import pdb;pdb.set_trace()


    def teardown_method(self,end):
        print("end")


    def test_one(self):
        print("This is SSSSSS")

