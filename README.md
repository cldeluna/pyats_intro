
# Getting Started with pyATS (including Genie)

### What is Python Automated Test System (pyATS)?

None of the answers I found to this question really made much sense to me initially.

A Python3 based **Test Automation and Validation Framework** developed by Cisco (but open and extensible to any vendor) is probably the best short answer but still too vague to be of much use.

For a while I dismissed it because I though it was a python testing framework like PyTest or Unittest and didn't have time to delve any further but common sense told me there had to be more to it than that.

When I had time to look deeper it was clear that this was a **python framework to help you test your network**!  Like, really test!

- Are all my routes there after my change?
- What changed from yesterday?
- Log my changes for my Change Request ticket in three commands!
- Do I have these bgp neighbors after my change?

Wow!

But still, I didn't pursue it because everything I saw focused on the CLI options available and while clearly powerful and returning structured data I'm far more interested in working with the data in a script.  I don't want structured data output the the screen. I want to process that structured data.

Now that I've had some time to spend working with it, it is clear this is something worth investing some time to learn because it is incredibly powerful and can be run from the CLI **or** as part of your python script and there are good use cases for both.

I'm not going to focus too much on the CLI version of this.  If you are more comfortable not having to deal with Python and scripts then there is alot of content out there for you to look at.  In my opinion this just delays the inevitable but some of the scripts will note their CLI equivalents if you just can't help yourself.

For those of you already comfortable with basic Python scripts, then you are my target audience!

In addition, if you spend alot of time parsing Cisco output then **you need to take a look at this module**!

For those of you that know a bit about Ansible or Nornir, then think of pyATS as something comparable (it is a framework) but just for network devices and which returns structured data (*note that Ansible and Nornir can also return structured data*).

| Function                                     | pyATS                                                 | Comparable Technology Equivalent                             |
| -------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------ |
| List of devices and how to access            | Testbed file                                          | Ansible Host file<br />Nornir Hosts file<br />Netmiko connection object |
| Topology                                     | Part of the Testbed file                              | None                                                         |
| Establish a connection to a device           | Object connect method<br />device.connect()           | Ansible Playbook and Network Modules<br />Nornir instance <br />Netmiko instance |
| Execute show commands                        | Object parse method<br />device.parse('show version') | Ansible Playbook and Network Modules<br />Nornir instance run method<br />Netmiko connect method |
| "Parse" show commands to get structured data | Object parse method<br />device.parse('show version') | TextFSM, Netmiko with TextFSM option<br />Napalm, like Genie will return structure data |
| Diff two different outputs                   | genie diff                                            | Python code <br />Ansible Playbook                           |
| Testing                                      | Stay Tuned!!!                                         | Manual                                                       |

Official Documentation:

- [pyATS Documentation](https://pubhub.devnetcloud.com/media/pyats/docs/index.html)
- [pyATS Genie Documentation](https://pubhub.devnetcloud.com/media/genie-docs/docs/overview/introduction.html)

### Why do I care?

I can't answer this question for you but I can tell you why its of interest to me. 

- Arguably an easier way to parse data from legacy network devices
- Easy way to compare "state" and configurations
- A testing framework that you can use to validate your network

This repository will focus on the parsing aspect.

#### Parsing

When dealing with network devices, particularly legacy network devices without APIs, I generally have a few basic workflows in my Python scripts:

- Connect to devices to get show commands and process (parse) and/or save output to a file
- Process (parse) text files of show commands to get structured data and then apply some logic depending on what I'm trying to do.
- Parse and Compare output
  - Compare the PRE Mac address table to the POST Mac address table
  - Compare the PRE routing table to the POST routing table
  - Compare PRE/POST interface configuration
  - Compare current configuration with standard

Accomplishing these workflows generally takes a number of modules and Python logic and they all have one thing in common. 

Parsing Text to get structured data

For example, if I'm getting show commands I'll use Ansible, Nornir, or Netmiko and then parse with TextFMS.

With PyATS, I can do that in one step!   In fact, I can do all three of those activities in a single command!!

So thats efficient but I've already done all the heavy lifting to do those workflows.  

#### Testing

Why is this still interesting?  Well, we've just scratched the surface of pyATS.    We have the structured data part down but the real goal is to use that structured data as part of our day to day processes and to test and verify our network.

PyATS is very good at parsing because it **needs structured data to automate the testing of your network**.

So this is taking our automation to the next level.  We've been so hung up on logging to the legacy device, running commands, getting output, parsing that output that sometimes the effort to get that point is such that we see that as the final accomplishment.  While it is an accomplishment, its only the beginning!



### Creating Your Environment

Always start with a virtual environment.  See the [Real Python vENV primer](https://realpython.com/python-virtual-environments-a-primer/) for more details on that.

Once you are in your virtual environment, you need to install the pyATS module and Genie (now basically one product).

There is alot of good material out there on how to install. See the [DevNet installation documentation](https://pubhub.devnetcloud.com/media/genie-docs/docs/installation/installation.html).

Most will tell you to install pyATS with the Genie library and that is a good minimum installation for testing and parsing.   

```bash
pip install pyats[library]
```

If you want to use the interactive testbed command to create your testbed environment and you are running pyATS 20.2.1 or later you will also need:

```
pip install pyats.contrib
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



As an alternative, there is a [pyATS Docker image](https://developer.cisco.com/codeexchange/github/repo/CiscoTestAutomation/pyats-docker).  The command below will instantiate the container (download the image if you don't have it) and give you an interactive shell.

```bash
$ docker run -it ciscotestautomation/pyats:latest /bin/bash
```



### Creating Your Testbed File

For those who are somewhat familiar with Ansible, you can think of this as your inventory or hosts file.  The testbed file actually has some additional capabilities that allow you to define your topology (this is new!!) but to get started we just want to define our devices and how to contact them.

The genie CLI has a handy interactive script that will walk you through creating your first testbed file without having to dig into the syntax of the file. (Note: You will need to pip install some Python Excel modules to run this but luckily it will tell you what you need if you don't already have them installed).

The **genie create testbed interactive**  command will walk you through some questions and then generate a properly formatted testbed file.  The command below will generate that file as *my_testbed.yml* in the local directory. You can provide a different path or subdirectory if you want to.  In production, I generally put testbed files in a subdirectory.

```
# Prior to pyATS version 20.4.1
genie create testbed --output my_testbed.yml

# pyATS version 20.4.1 or later to create a testbed file interactively
genie create testbed interactive --output my_testbed.yml
```

You can run it with the *--encode-password* option to encode your passwords but there are better ways to do that once you move into production.

Tip: make sure your <name> matches your device hostname exactly!

As of pyATS version 20.4.1, you can also generate testbed files from a file, an ansible hosts file, or netbox!

I found the [Testbed Topology Schema](https://pubhub.devnetcloud.com/media/pyats/docs/topology/schema.html) very helpful when trying to generate testbed files.

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

The *devenet_sbx_testbed.yml* Testbed file contains two example devices from the DevNet Always On Sandbox devices.

#### First Script

The *first\_genie.py* pyATS Genie script instantiates the *devnet_sbx_testbed.yml* testbed file which has two DevNet Always On Sandbox devices.   It then establishes a connection to each device and executes a show command ("show version").  In this script, all of this is hardcoded and there is lots of code repetition but this first script is intended to show the basics without alot of "extras" or flexibility.

This script also includes the Genie CLI equivalent so you can compare.

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

[Genie Feature Browser](https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/)

[List of Genie Parsers](https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/parsers)

[pyATS Release history from Libraries.io](https://libraries.io/pypi/pyats)



### GitHub Repositories from Cisco and other Network Engineers

https://github.com/CiscoTestAutomation/examples

https://github.com/kecorbin/pyats-network-checks/blob/master/devnet_sandbox.yaml

https://github.com/vsantiago113/pyATS-Boilerplate



### Tutorials

[pyATS on YouTube](https://www.youtube.com/results?search_query=pyats)

[pyATS | Genie - Getting Started! - Data Knox YouTube](https://www.youtube.com/watch?v=GhkkOxLheRY&t=327s)



###  Glossary

UUT = Unit Under Test

DUT = Device Under Test

EUT = Equipment Under Test