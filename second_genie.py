#!/usr/bin/python -tt
# Project: pyats
# Filename: second_genie
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


def device_info(dev, testbed_obj, showcmd='show version', save_to_json=False):
    """
    This function connects to the device provided when called (dev) in the instantiated testbed (testbed_obj)
    and executes the provided show command (if none was provided, 'show version' is executed by defulat.

    If the Save option = True (-s in the command line) was provided then the output will be saved to a JSON file in
    the current working directory with the name <device name>.json.  The default behavior is NOT to save the output.

    :param dev: the testbed device to query
    :param testbed_obj:  the testbed object
    :param showcmd: what show command to execute
    :return: Return the device object and the show command response
    """

    device = testbed_obj.devices[dev]
    device.connect()
    response = device.parse(showcmd)
    print(f"Response from {dev} is of type {type(response)} and length {len(response)}")
    print(response)
    print()
    print(json.dumps(response, indent=4))
    print(response.keys())

    if save_to_json:
        json_filename = f"{dev}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(response, f, ensure_ascii=False, indent=4)
        print(f"\nFILE SAVED: Saved Response to JSON file {json_filename}")

    return device, response


def main():

    # Instantiate the Testbed
    testbed = load(arguments.testbed_file)
    print(f"\n======= TESTBED INFO =======\n")
    print(f"\tTestbed Value (object): {testbed}")
    # Use the dir method to check what options are available for this object
    # Uncomment to see output
    print(dir(testbed))
    print(f"\tTestbed Name: \n\t\t{testbed.name}")
    print(f"\tTestbed Devices: \n\t\t{testbed.devices}")
    print(f"\tNumber of Testbed Links: \n\t\t{testbed.links}")
    print(f"\tNumber of Testbed Devices: \n\t\t{len(testbed.devices)}")
    print(f"\n======= END TESTBED INFO =======\n")

    # Using the default parameters and therefore the default Testbed
    if testbed.name == 'DevNet_Always_On_Sandbox_Devices':
        # Sandbox NXOS Device
        nx_dev, nx_resp = device_info('sbx-n9kv-ao', testbed, arguments.command, arguments.save)

        # csr1000v-1
        csr_dev, csr_resp = device_info('csr1000v-1', testbed, arguments.command, arguments.save)

    else:
        # A non default testbed file has been provided
        # Example showing how to iterate over the devices in the testbed file
        for dev in testbed.devices:
            print(f"\n>>>>>>> DEVICE {dev}")
            dev, resp = device_info(dev, testbed, arguments.command, arguments.save)


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python second_genie' ")
    parser.add_argument('-c', '--command', help='Show command to execute on each device', action='store',
                        default='show version')
    parser.add_argument('-s', '--save', help='Save the results payload to a JSON file', action='store_true',
                        default=False)
    parser.add_argument('-t', '--testbed_file', help='Testbed file to use', action='store',
                        default='devnet_sbx_testbed.yml')
    arguments = parser.parse_args()
    main()
