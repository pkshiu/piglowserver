# Piglow Server

This project has two parts:

1. A RESTful API server running on a RPi thas has a PiGlow board attached. This server will provide an interface for controlling the PiGlow remotely.

2. An example web server with a simple browser interface. You can run this on the same RPi, or on a completely different computer. It will control the PiGlow via the RESTful API server above.

By providing a web based API on the RPi to the PiGlow, we can move the application code to a different platform. For example your web store can use the API to send store product levels to the RPi via the web.

## Technical Details

This project also serves as an example for:

- running the [Flask web framework](http://flask.pocoo.org/) on the RPi
- designing a RESTful API using the [Flask RESTful](http://flask-restful.readthedocs.org/) package
- use [Python thread locks](https://docs.python.org/2/library/threading.html) to manipulate a shared resource (the PiGlow) on the RPi within a web server environment.
- using [Python unittest](https://docs.python.org/2/library/unittest.html) to test the API server


# API Usage

Here are some example in using the API with curl.

```shell
    # set arm 3 to brightness 50
    curl -X PUT -d brightness=50 http://localhost:5000/arms/3

    # switch on and off LED 7
    curl -X PUT -d brightness=100 http://localhost:5000/leds/7
    curl -X PUT -d brightness=0 http://localhost:5000/leds/7

    # switch on led 3 and 5 with brightness 10 and 200
    curl -X PUT -H 'Content-Type: application/json' \
        -d '[{"led_id":3, "brightness": 10}, {"led_id":5, "brightness":200 }]' \
        http://localhost:5000/leds

    # excute a starburst pattern
    curl -X PUT -d brightness=100 http://localhost:5000/patterns/starburst

    # turn everything off
    curl -X PUT http://localhost:5000/patterns/clear
```

You can also see the `test.py` test suite to see how it uses the [Python requests](http://docs.python-requests.org/) library to talk to the API. The pg_control web server also uses the requests library to talk to the API.

## Prerequisite

This project uses the __PyGlow__ library from https://github.com/benleb/PyGlow to talk to the PiGlow board. Note that there are several different python libraries that support the PyGlow board. This one is more pythonic.

Because the web server part of this project can run on a different server from a RPi, this project does *not* automatically install the PyGlow library. You have to follow their instruction to get the PiGlow board working and install the PyGlow library separately. This project ships with an emulator, so you can actually try out the entire project either on a RPi or on a different server (I do most of the development on my Mac.)

This project does *automatically install* other python packages, __flask__ and __flask-restful__ required for the servers to work. You can see the list of packages in the requirements file.

# Installation

You can install __piglowserver__ inside a virtualenv or sysetm wide. I always prefer to install python software inside a __virtualenv__ to keep libraries separate. If you have virtualenv available, the piglowserver is virtualenv friendly.

## Option 1: Installation inside a virtualenv

Because the hardware interface libraries require root access to compile, it is best to link them them globally. So create your virtualenv with the *--system-site-package* argument.

Once your virtualenv is created, simply use the local __pip__ command to install piglowserver locally

    pip install git+https://github.com/pkshiu/piglowserver.git

The files will go into you virtualenv's lib directory at:

    (your virtualenv project)lib/python2.7/site-packages/piglowserver

## Option 2: Intallation system wide

If you simply use pip to install piglowserver, you can install it into the system wide location using:

    pip install git+https://github.com/pkshiu/piglowserver.git

This will typically result in the files going to:

    /usr/local/lib/python2.7/site-packages/piglowserver

Because __piglowserver__ requires flask etc, those will also be installed globally.

## Getting Hardware Permission

Because accessing the PiGlow board requires access to the i2c bus and library, your normal "pi" user account cannot do that. Do *not* run as root or use *sudo*. Instead, simple add the user to the i2c user group:

    sudo adduser pi i2c

# Using PiGlowServer

After installation, depending on where you installed the package, e.g. `/usr/local/lib/python2.7/site-packages/piglowserver` or `{my_virtual_env}/lib/python2.7/site-packages/piglowserver`

```
# start up the API server:
python /usrlocal/lib/python2.7/site-packages/piglowserver/pg_rest_server.py

# run the tests and watch the LED comes on and off (this takes a long time)
# feel free to control-c out of it after awhile:
python /usrlocal/lib/python2.7/site-packages/piglowserver/tests.py

# start up the web server in a separate window:
python /usrlocal/lib/python2.7/site-packages/piglowserver/pg_control.py

# now point your browser to your RPi on port 8000 and try the web interface
http://YOUR_RPI_IP_ADDRESS:8000
```

# Additional Settings

The piglowserver runs as installed without any need for additional configuration. However you can change the servers behavior with some additional configuration:

## API Server Location

By default the #web server# looks for the #API Server# at `http://localhost:5000` .
This is useful if you are running both the web server and the API server on the
same RPi. If you are running the web server on a different computer, you can
setup the address by using a local configuration file:

1. Create a local_config.py file
2. set the optional environment variable #PGS_SETTINGS# to point to that file:

```
    export PGS_SETTINGS=local_config.py
```

# License
This project is licensed under the MIT license.

