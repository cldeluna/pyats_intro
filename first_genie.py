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

import argparse
from genie.testbed import load
import json



def device_info(dev, testbed_obj, showcmd='show version'):

    device = testbed_obj.devices[dev]
    device.connect()
    response = device.parse(showcmd)
    print(f"Response from {dev} is of type {type(response)} and length {len(response)}")
    print(response)
    print()
    print(json.dumps(response, indent=4))
    print(response.keys())

    return device, response

def main():

    # Instantiate the Testbed
    testbed = load('devnet_sbx_testbed.yml')
    print(testbed)

    # Sandbox NXOS Device
    nx_dev, nx_resp = device_info('sbx-n9kv-ao', testbed, 'show version')



    # csr1000v-1
    csr_dev, csr_resp = device_info('csr1000v-1', testbed, 'show ip interface brief')



# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python first_genie' ")

    #parser.add_argument('all', help='Execute all exercises in week 4 assignment')
    # parser.add_argument('-a', '--all', help='Execute all exercises in week 4 assignment', action='store_true',
    #                     default=False)
    arguments = parser.parse_args()
    main()
