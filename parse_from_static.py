#!/usr/bin/python -tt
# Project: pyATS_Community_Solutions
# Filename: parse_from_static
# claudia
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "5/5/20"
__copyright__ = "Copyright (c) 2018 Indigo Wire Networks"
__license__ = "Python"

import argparse
from genie.conf.base import Device
import json

def load_data():
    data = """
Cisco IOS XE Software, Version 16.09.03
Cisco IOS Software [Fuji], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.9.3, RELEASE SOFTWARE (fc2)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2019 by Cisco Systems, Inc.
Compiled Wed 20-Mar-19 07:56 by mcpre


Cisco IOS-XE software, Copyright (c) 2005-2019 by cisco Systems, Inc.
All rights reserved.  Certain components of Cisco IOS-XE software are
licensed under the GNU General Public License ("GPL") Version 2.0.  The
software code licensed under GPL Version 2.0 is free software that comes
with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such
GPL code under the terms of GPL Version 2.0.  For more details, see the
documentation or "License Notice" file accompanying the IOS-XE software,
or the applicable URL provided on the flyer accompanying the IOS-XE
software.


ROM: IOS-XE ROMMON

csr1000v uptime is 5 hours, 25 minutes
Uptime for this control processor is 5 hours, 26 minutes
System returned to ROM by reload
System image file is "bootflash:packages.conf"
Last reload reason: reload



This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.

A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

If you require further assistance please contact us by sending email to
export@cisco.com.

License Level: ax
License Type: Default. No valid license found.
Next reload license Level: ax


Smart Licensing Status: Smart Licensing is DISABLED

cisco CSR1000V (VXE) processor (revision VXE) with 2392579K/3075K bytes of memory.
Processor board ID 95C9AN22Z68
3 Gigabit Ethernet interfaces
32768K bytes of non-volatile configuration memory.
8113280K bytes of physical memory.
7774207K bytes of virtual hard disk at bootflash:.
0K bytes of WebUI ODM Files at webui:.

Configuration register is 0x2102

    
    """
    return data

def main():
    """"
    Simple script which loads the text output of a show command from a variable and
    uses the Genie parsing engine to parse the output.

    This shows how to use the Genie parsers wit content obtained elsewhere,
    - a variable
    - a text file
    - output from some other means
    """

    # Because we are using the parsing engine without a testbed file and with static content
    # This creates a device model for parsing
    device = Device(name='csr1kv', os='iosxe')
    device.custom.abstraction = {'order': ['os']}

    print("Loading show command output...")
    response = load_data()
    print(f"show command output is: \b{response}")


    print(f"\n=================== DEVICE PARSING {device.name} ===================")
    parsed_output = device.parse('show version', output=response)
    print(f"\nParsed Output in a {type(parsed_output)}: \n{json.dumps(parsed_output, indent=4)}")
    print(f"\n=================== END DEVICE PARSING {device.name} ===================\n")


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python parse_from_static.py' ")
    arguments = parser.parse_args()
    main()
