#!/usr/bin/python -tt
# Project: pyats
# Filename: first_genie
# claudia
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "4/25/20"
__copyright__ = "Copyright (c) 2018 Claudia"
__license__ = "Python"

from genie.testbed import load
import json
import unittest

class ParseTest(unittest.TestCase):
    def testSuccess(self):
        result = {'platform':
                      {'name': 'Nexus',
                       'os': 'NX-OS',
                       'software':
                           {'system_version': '9.3(3)',
                            'system_image_file': 'bootflash:///nxos.9.3.3.bin',
                            'system_compile_time': '12/22/2019 2:00:00 [12/22/2019 14:00:37]'},
                       'hardware':
                           {'model': 'Nexus9000 C9300v',
                            'chassis': 'Nexus9000 C9300v',
                            'slots': 'None',
                            'rp': 'None',
                            'cpu': 'Intel(R) Xeon(R) Platinum 8176 CPU @ 2.10GHz',
                            'memory': '16409068 kB',
                            'processor_board_id': '9N3KD63KWT0',
                            'device_name': 'sbx-n9kv-ao',
                            'bootflash': '4287040 kB'},
                       'kernel_uptime':
                           {'days': 0,
                            'hours': 4,
                            'minutes': 11,
                            'seconds': 12},
                       'reason': 'Unknown'
                       }
                  }
        # print(f"{result['platform']['software']['system_version']}")
        self.assertRegex(result['platform']['software']['system_version'], r'^\d.\d\(\d\)$',
                         msg="TEST FAILED: Value is NOT a valid version string")



def main():
    """
    This first pyATS Genie script instantiates the devnet_sbx_testbed.yml Testbed file which has two DevNet Always On
    Sandbox devices.   It then establishes a connection to each device and executes a show command ("show version").
    All of this is hardcoded and there is lots of code repetition but this first script is intended to show the basics
    without alot of "extras" or flexibility.
    :return:
    """

    # Instantiate the Testbed
    testbed = load('devnet_sbx_testbed.yml')
    print(f"\n======= TESTBED INFO =======\n")
    print(f"\tTestbed Value (object): {testbed}")
    print(f"\n======= END TESTBED INFO =======\n")


    # Sandbox NXOS Device
    # CLI: genie parse "show version" --testbed-file "devnet_sbx_testbed.yml" --devices "sbx-n9kv-ao"
    # This CLI command outputs the results into a directory called "out1" which does not have to exist
    # CLI & SAVE: genie parse "show version" --testbed-file "devnet_sbx_testbed.yml" --devices "sbx-n9kv-ao" --output PRE
    # DIFF CLI:  genie diff PRE POST
    device = testbed.devices['sbx-n9kv-ao']
    # print(dir(device))
    # device.connect()
    # response = device.parse('show version')
    # print(f"Response from sbx-n9kv-ao is of type {type(response)} and length {len(response)}")
    # print(response)
    # print()
    # print(json.dumps(response, indent=4))
    # print(response.keys())
    #
    # # csr1000v-1
    # # CLI: genie parse "show version" --testbed-file "devnet_sbx_testbed.yml" --devices "csr1000v-1"
    # device = testbed.devices['csr1000v-1']
    # device.connect()
    # response = device.parse('show version')
    # print(f"Response from csr1000v-1 is of type {type(response)} and length {len(response)}")
    # print(response)
    # print()
    # print(json.dumps(response, indent=4))
    # print(response.keys())

    print(f'\n\n====== Execute UnitTest')
    unittest.main()

# Standard call to the main() function.
if __name__ == '__main__':
    main()
