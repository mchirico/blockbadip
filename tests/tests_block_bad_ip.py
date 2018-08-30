from unittest.mock import patch
from unittest import TestCase

from block_bad_auth import read_process_file, log_ip_addresses, \
    PAST_IP_LOG, \
    run_process, WHITE_IPS


class BlockBadAuth(TestCase):
    TEST_MAIL_LOG = 'fixtures/mail.log'
    TEST_PAST_IP_LOG = 'fixtures/past_blocked_ips.log'

    @patch("block_bad_auth.MAIL_LOG", TEST_MAIL_LOG)
    @patch("block_bad_auth.PAST_IP_LOG", TEST_PAST_IP_LOG)
    def setUp(self):
        self.ip_set = read_process_file(self.TEST_MAIL_LOG)
        log_ip_addresses(self.ip_set)

    def tearDown(self):
        with open(self.TEST_PAST_IP_LOG, 'w') as f:
            f.write('')

    def test_ips_are_read_in_correctly(self):
        assert self.ip_set.intersection(WHITE_IPS) == set()
        assert self.ip_set == set(
            ['121.237.137.75', '138.68.245.91', '113.121.42.1',
             '84.38.130.207', '222.94.196.24', '185.165.31.12',
             '54.67.30.225', '192.241.212.160', '5.39.223.84',
             '95.181.178.182', '66.163.186.175',
             '107.170.236.113', '182.101.61.159', '208.38.136.12',
             '183.240.19.250', '5.188.9.40', '201.116.15.183',
             '185.100.87.191', '103.103.55.163', '208.100.26.232',
             '107.170.234.222', '162.213.136.106',
             '121.237.140.253', '5.101.0.34', '94.102.49.190', '52.8.136.37',
             '94.102.56.215', '66.240.192.138',
             '107.170.227.152', '171.12.10.140', '37.49.226.172',
             '107.170.224.153', '223.197.134.71', '66.163.190.61',
             '188.126.223.106', '107.170.231.79', '195.22.125.28',
             '210.72.142.7', '195.22.125.26', '37.49.227.152',
             '37.49.226.191', '94.102.50.96', '37.49.227.182',
             '201.187.101.222', '62.219.169.145', '173.11.84.226',
             '37.72.175.154', '121.237.142.237'])


class MainRun(TestCase):
    TEST_MAIL_LOG = 'fixtures/mail.log'
    TEST_PAST_IP_LOG = 'fixtures/past_blocked_ips.log'
    ip_set = {}

    class MyPopen:
        @staticmethod
        def communicate():
            return ['response', 'error']

    @patch("block_bad_auth.MAIL_LOG", TEST_MAIL_LOG)
    @patch("block_bad_auth.PAST_IP_LOG", TEST_PAST_IP_LOG)
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


    def tearDown(self):
        with open(self.TEST_PAST_IP_LOG, 'w') as f:
            f.write('')

    def test_write_past_blocked_ips(self):
        with open(self.TEST_PAST_IP_LOG, 'r') as f:
            m = f.readlines()
            m = [i.strip() for i in m]
        check_value = 'should be gone' in m
        assert check_value is False

    def test_bash_cmd(self):
        list_of_calls = self.Popen.mock_calls
        one_ufw_cmd = list_of_calls[0][1][0]
        assert 'bash' in one_ufw_cmd
        assert '-c' in one_ufw_cmd
        assert one_ufw_cmd[2].find('ufw insert 1 deny from ') == 0

    def test_main(self):
        ips_blocked = read_process_file(self.TEST_MAIL_LOG)
        assert self.ip_set.intersection(WHITE_IPS) == set()
        assert ips_blocked == set(
            ['52.8.136.37', '223.197.134.71', '94.102.50.96',
             '107.170.234.222', '162.213.136.106', '94.102.49.190',
             '138.68.245.91', '95.181.178.182', '173.11.84.226',
             '103.103.55.163', '5.39.223.84', '37.49.226.191',
             '185.165.31.12', '107.170.227.152', '210.72.142.7', '5.101.0.34',
             '183.240.19.250', '208.38.136.12',
             '84.38.130.207', '54.67.30.225', '66.163.186.175',
             '185.100.87.191', '171.12.10.140', '107.170.236.113',
             '195.22.125.28', '66.240.192.138', '121.237.137.75',
             '121.237.142.237', '37.49.227.152', '62.219.169.145',
             '107.170.224.153', '208.100.26.232', '37.72.175.154',
             '222.94.196.24', '195.22.125.26', '192.241.212.160',
             '94.102.56.215', '201.116.15.183', '37.49.227.182',
             '37.49.226.172', '107.170.231.79',
             '113.121.42.1', '182.101.61.159', '188.126.223.106', '5.188.9.40',
             '201.187.101.222', '66.163.190.61',
             '121.237.140.253'])











