#!/usr/bin/env python3
"""
Code location:
https://github.com/mchirico/blockbadip


"""

import re
import subprocess
import shlex

MAIL_LOG = '/var/log/mail.log'
PAST_IP_LOG = '/var/log/past_blocked_ips.log'
WHITE_IPS = set(['108.52.226.221',
                 '104.236.87.120',
                 '45.55.125.83',
                 '104.198.21.57',
                 '100.34.255.15',
                 '0.0.0.0',
                 '127.0.0.1',
                 '127.0.0.2'])


def read_process_file(mail_log):
    with open(mail_log, 'r') as f:
        m = f.readlines()
        login_string = 'authentication failed: Invalid ' \
                       'authentication mechanism'
        ssl_string = 'SSL_accept error'
        reject_string = 'rejected:'
        reject_string2 = 'reject:'
        warning_hostname_string = 'warning: hostname'
        m = [i for i in m if i.find(login_string) >= 0
             or i.find(ssl_string) >= 0 or i.find(reject_string) >= 0 or
             i.find(warning_hostname_string) >= 0 or
             i.find(reject_string2)]
        ip_set = set()
        for i in m:
            aa = re.match(r".*\[(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\]: .*", i)
            if aa:
                ip_set.add(aa.group(1))
        ip_set = ip_set.difference(WHITE_IPS)
        return ip_set


def log_ip_addresses(ips):
    with open(PAST_IP_LOG, 'w') as f:
        for i in ips:
            f.write(i + '\n')


def get_ip_location(ips):
    for i in ips:
        cmd = 'curl "https://tools.keycdn.com/geo.json?host={}"'.format(i)
        r, e = bash_cmd(cmd)
        print(r)


def read_past_log_into_set():
    with open(PAST_IP_LOG, 'r') as f:
        m = f.readlines()
        m = set([i.strip() for i in m])
        return m


def run_ufw_commands(ips):
    for i in ips:
        if len(i) > 6:
            cmd = "ufw insert 1 deny from {}".format(i)
            bash_cmd(cmd)
    return


def bash_cmd(cmd):
    sscmd = shlex.split("bash -c '{}'".format(cmd))
    response, error = subprocess.Popen(sscmd,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE).communicate()
    return [response, error]


def run_process():
    mail_log = MAIL_LOG
    ip_set = read_process_file(mail_log)
    old_ip_set = read_past_log_into_set()
    ips_to_block = ip_set.difference(old_ip_set)

    run_ufw_commands(ips_to_block)
    log_ip_addresses(ip_set)


if __name__ == '__main__':
    run_process()
