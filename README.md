
# Getting Started with pyATS (and Genie)

### What is Python Automated Test System (pyATS)?

None of the answers I found to this question really made much sense to me initially.

A Python3 based **Test Automation and Validation Framework** developed by Cisco (but open and extensible to any vendor) is probably the best short answer but still too vague. 

Add in Genie because at least originally you always heard bout Genie and pyATS together but it was never clear why.  Today Cisco is working hard to streamline this so that Genie (I like to think of it as the parsing and testing library) and pyATS (the overarching testing support framework) are bundled together. 

For a while I dismissed it because I thought it was a Python testing framework like PyTest or Unittest but common sense told me there had to be more to it than that. After all, why would Cisco develop a Python testing framework?   Well, because it **IS** a testing framework but for your network rather than for your code!

PyATS is a **python framework to help you test your network**!  Like, actual functional testing!!

- Are all my routes there after my change?
- What changed from yesterday?
- Log my changes for my Change Request ticket in a single command!
- Do I have these bgp neighbors after my change?

Wow!

But still, I didn't pursue it because everything I saw focused on the CLI options available and while clearly powerful and returning structured data I'm far more interested in working with the data in a script.  I don't want structured data output to the screen. I want to work with that structured data and apply logic!   Luckily, the CLI is just one way to use this powerful framework!  It can be run from the CLI **or** as part of your Python script and there are good use cases for both.

I'm not going to focus too much on the CLI version of this.  If you are more comfortable not having to deal with scripts then there is alot of content out there for you to look at showing the CLI.  In my opinion, this just delays the inevitable but some of the scripts will note their CLI equivalents if you just can't help yourself.

For those of you already comfortable with basic Python scripts, then you are my target audience!

In addition, if you spend alot of time parsing Cisco output then **you need to take a look at this module**!

For those of you that know a bit about Ansible or Nornir, then think of pyATS as something comparable (to a degree) and complementary  (it is a framework) but focused on testing network devices.

| Function                                     | pyATS                                                 | Comparable Technology Equivalent                             |
| -------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------ |
| List of devices and how to access            | Testbed file                                          | Ansible Host file<br />Nornir Hosts file<br />Netmiko connection object |
| Topology                                     | Part of the Testbed file                              | N/A                                                          |
| Establish a connection to a device           | Object connect method<br />device.connect()           | Ansible Playbook and Network Modules<br />Nornir instance <br />Netmiko instance |
| Execute show commands                        | Object parse method<br />device.parse('show version') | Ansible Playbook and Network Modules<br />Nornir instance run method<br />Netmiko connect method |
| "Parse" show commands to get structured data | Object parse method<br />device.parse('show version') | TextFSM, Netmiko with TextFSM option<br />Napalm, like Genie will return structure data for supported commands |
| Diff two different outputs                   | genie diff                                            | Python code <br />Ansible Playbook                           |
| Testing                                      | Stay Tuned!!!                                         | Python code <br />Ansible Playbook                           |

Official Documentation:

- [pyATS Documentation](https://pubhub.devnetcloud.com/media/pyats/docs/index.html)
- [pyATS Genie Documentation](https://pubhub.devnetcloud.com/media/genie-docs/docs/overview/introduction.html)

### Why do I care?

I can't answer this question for you but I can tell you why its of interest to me. 

- Arguably an easier way to parse data from legacy network devices particularly if you are just starting out
- Easy way to compare "state" and configurations
- A testing framework that you can use to validate your network devices and topology
  - Envision a workflow using Nornir to deploy configurations to your devices and pyATS to ensure that your network is in an operational state!

This repository will focus on the parsing aspect and hopefully get you interested enough to look beyond the parsing.

#### Parsing

When dealing with network devices, particularly legacy network devices without APIs, I generally have a few basic workflows in my Python scripts:

- Connect to devices to get show commands and process (parse) and/or save output to a file
- Process (parse) text files of show commands to get structured data and then apply some logic depending on what I'm trying to do
- Parse and Compare output for Validation
  - Compare the PRE Mac address table to the POST Mac address table
  - Compare the PRE routing table to the POST routing table
  - Compare PRE/POST interface configuration
  - Compare current configuration against a standard template
- Testing

Accomplishing these workflows generally takes a number of modules and Python logic but they all have one thing in common: 

***Parsing Text to get structured data***

For example, if I'm getting show commands I'll use Ansible, Nornir, or Netmiko and then parse with TextFMS.

With PyATS, I can do all of those activities in just a few commands!!

So that is efficient but I've already done all the heavy lifting to do those workflows and its even easier now that Netmiko and Ansible integrate TextFSM.   

So why should you take a look at pyATS?

If you have not done all of that heavy lifting, then starting with pyATS gets you "simplified parsing" to begin with but really it sets you up to use a testing framework for your network!



#### Testing

With parsing, we've just scratched the surface of pyATS.    We have the structured data part down but the real goal is to use that structured data as part of our day to day processes and to test and verify our network.  

PyATS is very good at parsing because it **needs structured data to automate the testing of your network**.

So this is taking our automation to the next level.  We've been so hung up on logging in to the device, running commands, getting output, and parsing that output that sometimes the effort to get that point can feel like the final accomplishment.  While it is an accomplishment, its only the beginning!



### Creating Your Environment

PyATS is supported on Linux with Python 3.4 or greater (but 3.5 or later is recommended) . There is no Windows support at the time of writing (2020-04) but Mac OS X is supported.  For those of you on Windows, fear not, as you can always spin up a Virtual Machine or a Docker image.  Keep reading to learn more about your Docker image options.    

Always start with a virtual environment.  See the [Real Python vENV primer](https://realpython.com/python-virtual-environments-a-primer/) for more details on that.

Once you are in your virtual environment, you need to install the pyATS module and the Genie Libraries (now basically one framework encompassed in pyATS).

There is alot of good material out there on how to install pyATS. Start with the [DevNet installation documentation](https://pubhub.devnetcloud.com/media/genie-docs/docs/installation/installation.html).

Most will tell you to install pyATS with the Genie library and that is a good minimum installation for testing and parsing.   

```bash
pip install pyats[library]
```

If you want to use the interactive testbed command to create your testbed environment and you are running pyATS 20.4.1 or later you will also need:

```
pip install pyats.contrib
```

Since I want to use some of the additional pyATS capabilities (like [robot](https://robotframework.org/)) I installed the full package and that is what I recommend.

```
root@38c3258b2fd7:/# pip install pyats[full]
root@38c3258b2fd7:/# pip list | grep robot
genie.libs.robot             20.4       
pyats.robot                  20.4       
robotframework               3.1.2      
```

*Note:  On my Mac running Catalina with Zsh I had to quote the install string:*

```
pip install "pyats[full]"
```



#### Upgrading Your Environment

```
pip install pyats[full] --upgrade
or
pip install pyats[library] --upgrade
pip install pyats.contrib --upgrade
```



#### Docker Image

As an alternative, there is a [pyATS Docker image](https://developer.cisco.com/codeexchange/github/repo/CiscoTestAutomation/pyats-docker). The command below will download the image if you don't have it, instantiate the container, and give you an interactive shell into the container that now has your environment.

```bash
$ docker run -it ciscotestautomation/pyats:latest /bin/bash
```

Note: The Image documentation indicates that one of the Cisco example repositories is part of that container.  If it is not, simply git clone into your container (see below).

At the time of this writing the image was a Debian image (buster) with pyATS 20.2 so remember to upgrade to use the latest and greatest pyATS features.

```
## Download if needed and spin up the CiscoTestAutomation Container
claudia@Claudias-iMac ~ % docker run -it ciscotestautomation/pyats:latest

## Note the promt change indicating you are now in the container
root@441cbac66b2e:/pyats# cat /etc/*-release
PRETTY_NAME="Debian GNU/Linux 10 (buster)"
NAME="Debian GNU/Linux"
VERSION_ID="10"
VERSION="10 (buster)"
VERSION_CODENAME=buster
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"
root@441cbac66b2e:/pyats# python --version
Python 3.6.10

## Check the version
root@d4c00fd6662c:/pyats# pyats version check
You are currently running pyATS version: 20.2
Python: 3.6.10 [64bit]

  Package                      Version
  ---------------------------- -------
  genie                        20.2
  genie.libs.conf              20.2
  genie.libs.filetransferutils 20.2
  genie.libs.ops               20.2
  genie.libs.parser            20.2
  genie.libs.sdk               20.2
  pyats                        20.2
  pyats.aereport               20.2
  pyats.aetest                 20.2
  pyats.async                  20.2
  pyats.connections            20.2
  pyats.datastructures         20.2
  pyats.easypy                 20.2
  pyats.kleenex                20.2
  pyats.log                    20.2
  pyats.reporter               20.2
  pyats.results                20.2
  pyats.tcl                    20.2
  pyats.topology               20.2
  pyats.utils                  20.2
  unicon                       20.2
  unicon.plugins               20.2


root@d4c00fd6662c:/pyats#

## Upgrade to the latest version of pyATS
root@441cbac66b2e:/pyats# pip install pyats[full] --upgrade

## Install Git
root@441cbac66b2e:/pyats# apt-get udpate
root@441cbac66b2e:/pyats# apt-get install git-core
Y

## Install the Intro to pyATS (this) Repository
root@441cbac66b2e:/pyats# git clone https://github.com/cldeluna/pyats_intro.git
root@441cbac66b2e:/pyats# cd pyats_intro
root@441cbac66b2e:/pyats/pyats_intro# python first_genie.py

## Install the Cisco pyATS Example Repositories
## pyATS | Library Usages, Examples & etc
root@441cbac66b2e:/pyats# git clone https://github.com/CiscoTestAutomation/examples
## pyATS example solutions for NetDevOps use cases
root@441cbac66b2e:/pyats# git clone https://github.com/CiscoTestAutomation/solutions_examples
```

You can also use one of my Docker images, **bionic-immigrant**, which comes with git and pyATS 19.12 already installed.  Again, just remember to upgrade.

[Using Docker as an Ansible and Python platform for Network Engineers](https://gratuitous-arp.net/ansible-server-in-docker-for-network-engineers/)

The link above also has more information on installing and running Docker including a cheat sheet.

```
## Download if needed and spin up the CiscoTestAutomation Container
claudia@Claudias-iMac ~ % docker run -it cldeluna/bionic-immigrant

## Note the prompt change from claudia@Claudias-iMac to root@441cbac66b2e.  You are now in your container as root (your prompts will obviously be different).
## Upgrade to the latest version of pyATS
root@441cbac66b2e:/pyats# pip install pyats[full] --upgrade

## Install the Intro to pyATS (this) Repository
root@441cbac66b2e:/pyats# git clone https://github.com/cldeluna/pyats_intro.git
## Move into the new pyats_intro directory
root@441cbac66b2e:/pyats# cd pyats_intro
## Run the first_genie.py script
root@441cbac66b2e:/pyats/pyats_intro# python first_genie.py
```



### Clone this Repository

Now that you have your working environment, make sure you have cloned the the [pats_intro repository](https://github.com/cldeluna/pyats_intro).  This has everything you need to get started including sample Testbed files and some basic scripts.   These scripts are named "genie" scripts because they use more of the Genie Library connect and parse functionality than the pyATS testing framework.

```
## Install the Intro to pyATS (this) Repository
root@441cbac66b2e:/pyats# git clone https://github.com/cldeluna/pyats_intro.git
root@441cbac66b2e:/pyats# cd pyats_intro
root@441cbac66b2e:/pyats/pyats_intro# python first_genie.py
```



### Creating Your Testbed File

For those who are somewhat familiar with Ansible, you can think of this as your inventory or hosts file.  In fact, you can build your testbed from your Ansible hosts file. The testbed file actually has some additional capabilities that allow you to define your topology (this is huge and will be necessary when you get to testing!!) but to get started we just want to define our devices and how to connect to them.

The pyATS/Genie CLI has a handy interactive script that will walk you through creating your first testbed file without having to dig into the syntax of the file.

Note: You will need to pip install some Python Excel modules to run this but luckily it will tell you what you need if you don't already have them installed (xlsxwriter, xlrd, xlwt).

The **genie create testbed interactive**  command will walk you through some questions and then generate a properly formatted testbed file.  The command below will generate that file as *my_testbed.yml* in the local directory. You can provide a different path or subdirectory if you want to.  In production, I generally put testbed files in a subdirectory.

```
## Prior to pyATS version 20.4.1
genie create testbed --output my_testbed.yml

## pyATS version 20.4.1 or later
## Create a testbed file interactively with genie
genie create testbed interactive --output my_testbed.yml

## Create a testbed file interactively with pyats using the pre 20.4.1 syntax
## This still works but you may want to start using the newer syntax below
pyats create testbed interactive --output my_testbed.yml

## Note the syntax change. As of 20.4.1 this syntax is used
pyats create testbed interactive --output=my_testbed.yml

```

You can create your testbed with the *--encode-password* option to encode your passwords but there are better ways to do that once you move into production.

Tip: make sure your <name> matches your device hostname exactly!

As of pyATS version 20.4.1, you can also generate testbed files from a file (CSV, Excel), an Ansible hosts file, or netbox!  I won't cover that here but stay tuned, this is just getting you started with pyATS.

```

# Creating a testbed YAML file from a CSV or Excel file (Sample template can be found in the repository)
pyats create testbed file —-path=<.csv or Excel file> —-output=my_testbed_from_file.yml
```

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

The *devenet_sbx_testbed.yml* Testbed file contains two devices from the DevNet Always On Sandbox so that you can get started immediately.

#### First Script

The *first\_genie.py* pyATS Genie script instantiates the *devnet_sbx_testbed.yml* testbed file with the two DevNet Always On Sandbox devices.   It then establishes a connection to each device and executes a show command ("show version").  In this script, all of this is hardcoded and there is lots of code repetition but this first script is intended to show the basics without alot of "extras" or flexibility (or any thought to good python code).

This script also includes the Genie CLI equivalent so you can compare.

#### Second Script

The *second\_genie.py* pyATS Genie script has more features.

- It removes the code repetition and moves the repetitive code into a function.
- The script takes arguments but uses the default  *devnet_sbx_testbed.yml* testbed file if no options are provided.
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
<...>
```

You can also use the **-s** option and save the output to a JSON file for processing later.

```
(pyats) claudia@Claudias-iMac pyats_intro % python second_genie.py -t uwaco_testbed.yml -c "show interfaces description" -s 

```

Tip: 

- Make sure that the command you are providing with the -c option is a valid Genie Parser command for your type of network OS (IOS etc). Check the [list of Genie Parsers](https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/parsers).  

  - If you see an error like this make sure you are using a valid parser and that you are not using shorthand

  ```
  Exception: Could not find parser for 'show interface status'
  or 
  Search for 'show ip int br' is ambiguous. Please be more specific in your keywords.
  ```

- When using command shorthand like "sh int status"  you must also make sure its a valid command for your type of network OS (IOS etc).

  ```
  genie.metaparser.util.exceptions.InvalidCommandError: Invalid command has been executed
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

[Introduction to Genie | Python Network Automation! - IPvZero YouTube](https://www.youtube.com/watch?v=THgHwS-zVt8)


### Community Support

There is an active community on Cisco Webex Teams open to everyone.

- You can join this WebEx Teams space using https://eurl.io/#r18UzrQVr or by finding it listed at https://eurl.io/



###  Glossary

UUT = Unit Under Test

DUT = Device Under Test

EUT = Equipment Under Test



### Troubleshooting

Action:  Creating a Testbed

Error: pyats.topology.loader is a required dependency for this command 

Solution: Remember to install pats.contrib  **pip install pyats.contrib**

```
(test) root@3a10684f8c82:# pyats create testbed interactive --output my_testbed.yml


pyats.topology.loader is a required dependency for this command. 'interactive' source cannot be found.


```

