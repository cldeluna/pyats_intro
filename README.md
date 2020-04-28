
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





### Handy Links

[pyATS Documentation](https://pubhub.devnetcloud.com/media/pyats/docs/index.html)

[pyATS Genie Documentation](https://pubhub.devnetcloud.com/media/genie-docs/docs/overview/introduction.html)

[List of Genie Parsers](https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/parsers)



### GitHub Repositories from Cisco and other Network Engineers

https://github.com/CiscoTestAutomation/examples

https://github.com/kecorbin/pyats-network-checks/blob/master/devnet_sandbox.yaml

https://github.com/vsantiago113/pyATS-Boilerplate

