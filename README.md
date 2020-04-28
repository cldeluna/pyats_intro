
# Getting Started with PyATS (including Genie)

### Creating Your Environment

Always start with a virtual environment.  See the [Real Python vENV primer](https://realpython.com/python-virtual-environments-a-primer/) for more details on that.

Once you are in your virtual environment, you need to install the pyATS module and Genie (now basically one product).

There is alot of good material out there on how to install. See the [DevNet installation documentation](https://pubhub.devnetcloud.com/media/genie-docs/docs/installation/installation.html).

Most will tell you to install pyATS with the Genie library and that is a good minimum installation for testing and parsing.   

```bash
pip install pyats[library]
```

Since I want to use some of the additional pyATS capabilities (like robot) I installed the full package.

```
root@38c3258b2fd7:/# pip install pyats[full]
root@38c3258b2fd7:/# pip list | grep ro
arrow                        0.15.4
distro                       1.4.0
distro-info                  0.21ubuntu2
genie.libs.robot             19.10
pyats.robot                  19.10
robotframework               3.1.2
setproctitle                 1.1.10
```



*Note:  On my Mac running Catalina with Zsh I had to quote the install string:*

```
pip install "pyats[full]"
```



As an alternative, there is a [pyATS Docker image](https://developer.cisco.com/codeexchange/github/repo/CiscoTestAutomation/pyats-docker).

```bash
$ docker run -it ciscotestautomation/pyats:latest /bin/bash
```



### Creating Your Testbed File

For those who are somewhat familiar with Ansible, you can think of this as your inventory or hosts file.  The testbed file actually has some additional capabilities that allow you to define your topology for to get started we just want to define our devices and how to contact them.

The genie CLI has a handy interactive script that will walk you through creating your first testbed file without having to dig into the syntax of the file.

```
genie create testbed --output yaml/my_testbed.yaml
```

You can run it with the *--encode-password* option to encode your passwords but there are better ways to do that one you move into production.

I found the [Testbed Topology Schema](https://pubhub.devnetcloud.com/media/pyats/docs/topology/schema.html) very helpful:

Every section is broken down with explanatory comments, for example here is a section of the devices section:

```

# devices block
# -------------
#   all testbed devices are described here
devices:

    <name>: # device name (hostname) goes here. Each device requires its
            # own description section within devices block

        alias:  # device name alias.
                # (default: same as device name)
                # (optional)

        class:  # device object class.
                # use this field to provide an alternative subclass of
                # Device to instantiate this device block to. can be used
                # to extend the base Device class functionalities
                #   Eg: module.submodule.MyDeviceClass
                # (default: ats.topology.Device)
                # (optional)

        type:   # device type generic string
                # use this to describe the type of device
                #   Eg: ASR9k
                # (required)

        region: # device region string
                # (optional)

        role:   # device role string
                # (optional)

        os:     # device os string
                #  Eg: iosxe
                # (optional)

        series: # device series string
                #  Eg: cat3k
                # (optional)

        platform:   # device platform string
                    # Eg: cat9300
                    # (optional)

        model:  # device model string
                # (optional)

        power:  # device power string
                # (optional)

        hardware:   # device hardware block
                    # may contain anything describing the hardware info
                    # (optional)

        peripherals:  # device hardware block
                      # may contain anything describing peripherals
                      # connected to the device.
                      # (optional)

        credentials:
            # credential details common to the device
            # (optional)

            # All credentials in the testbed credentials block are
            # also available at this level if not specified here.

            <key>:        # Name of this credential.
                username: # (optional)
                password: # (optional)

                # Any other credential details
                <key>: <value>

```



### Executing PyATS

The devenet_sbx_testbed.yml Testbed file contains two example devices from the DevNet Always On Sandbox devices.

#### First Script

The *first\_genie.py* pyATS Genie script instantiates the *devnet_sbx_testbed.yml* testbed file which has two DevNet Always On Sandbox devices.   It then establishes a connection to each device and executes a show command ("show version").  In this script, all of this is hardcoded and there is lots of code repetition but this first script is intended to show the basics without alot of "extras" or flexibility.



#### Second Script

The *second\_genie.py* pyATS Genie script has more features.

- It removes the code repetition and moves the repetitive code into a function.
- The script takes arguments but uses the default  *devnet_sbx_testbed.yml* testbed file if not options are provided.
  1. **-t** option to use a non default testbed file. 
     Default Testbed file:  *devnet_sbx_testbed.yml*
  2. **-s** option to save the structured data response to a JSON file 
     Default: False (don't save)
  3. **-c** option to run a non default command 
     Default: "show version"
- Example showing how to iterate over all of the devices in the testbed file

Executed like below without any arguments, this script does what the *first_genie.py* script does. 

```
(pyats) claudia@Claudias-iMac pyats_intro % python second_genie.py
```

This second script is "better" code and provides the flexibility to run different commands on the same or different testbed topology and save the output.

Now, with this second script I can execute pyATS on my local lab topology:

```bash
(pyats) claudia@Claudias-iMac pyats_intro % python second_genie.py -t uwaco_testbed.yml
```



Sample output:

```

======= TESTBED INFO =======

        Testbed Value (object): <Testbed object 'Underwater_Corporation_Testbed' at 0x7fb0f8938710>
        Testbed Name: 
                Underwater_Corporation_Testbed
        Testbed Devices: 
                TopologyDict({'mgmt-sw05': <Device mgmt-sw05 at 0x7fb0b866dc50>})
        Number of Testbed Links: 
                set()
        Number of Testbed Devices: 
                1

======= END TESTBED INFO =======


>>>>>>> DEVICE mgmt-sw05

[2020-04-28 11:08:22,730] +++ mgmt-sw05 logfile /tmp/mgmt-sw05-cli-20200428T110822729.log +++
[2020-04-28 11:08:22,730] +++ Unicon plugin ios +++
Trying 10.1.10.102...

```



I can also run a different command and save the output to a JSON file for processing later.

```
(pyats) claudia@Claudias-iMac pyats_intro % python second_genie.py -t uwaco_testbed.yml -c "show interfaces description" -s 

```

Tip: 

- Make sure that the command you are providing with the -c option is a valid genie command. Check the [list of Genie Parsers](https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/parsers).  

  - If you see an error like this make sure you are using a valid parser and that you are not using shorthand

  ```
  Exception: Could not find parser for 'show interface status'
  ```

- Do not use command shorthand line "sh int status"

  ```
  Exception: Could not find parser for 'sh int status'
  ```

  

### Handy Links

[pyATS Documentation](https://pubhub.devnetcloud.com/media/pyats/docs/index.html)

[pyATS Genie Documentation](https://pubhub.devnetcloud.com/media/genie-docs/docs/overview/introduction.html)

[List of Genie Parsers](https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/parsers)



### GitHub Repositories from Cisco and other Network Engineers

https://github.com/CiscoTestAutomation/examples

https://github.com/kecorbin/pyats-network-checks/blob/master/devnet_sandbox.yaml

https://github.com/vsantiago113/pyATS-Boilerplate

