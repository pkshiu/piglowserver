#!/usr/bin/env python
"""
    This is a REST server that accept requests to control the PiGlow board.

    A few interesting things about this server:
    * It is designed with a RESTful Api
    * It uses a global lock to queue up operations to the PiGlow

    Run this server like this:

    python pg_rest_server.py

    Example in using the API:

    # set arm 3 to brightness 50
    curl -X PUT -d brightness=50 http://localhost:5000/arms/3

    # switch on and off LED 7
    curl -X PUT -d brightness=100 http://localhost:5000/leds/7
    curl -X PUT -d brightness=0 http://localhost:5000/leds/7

    # switch on led 3 and 5 with brightness 10 and 200
    curl -X PUT -H 'Content-Type: application/json' \
        -d '[{"led_id":3, "brightness": 10}, {"led_id":5, "brightness":200 }]' \
        http://localhost:5000/leds
"""
import threading
from time import sleep

from flask import Flask
from flask import request
from flask.ext.restful import (Resource, Api, reqparse, abort)

# Support a dummy PyGlow class so that we can test this code
# on something other than a real RPi
try:
    from PyGlow import (PyGlow, ARM_LED_LIST, COLOR_LED_LIST)
except ImportError:
    print 'Cannot import PyGlow library, use dummy interface for testing'
    from dummy_pyglow import (PyGlow, ARM_LED_LIST, COLOR_LED_LIST)


app = Flask(__name__)
api = Api(app)


@app.after_request
def add_cors_headers(response):
    """ To allow CORS """
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'PUT, POST, GET')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response


# internal cache of LED status
led_list = [{'led_id': i, 'brightness': 0} for i in range(1, 19)]

# global lock
lock = threading.Lock()

pyglow = PyGlow()


# interface to the h/w layer
def set_led(num, brightness):
    """
    Set one LED

    :param num: is the LED number, from 1 to 18
    :param brightness: is the light level, from 0-255
    """
    global lock

    # do this one at a time
    with lock:
        led_list[num - 1]['brightness'] = brightness
        pyglow.led(num, brightness=brightness)


def set_arm(num, brightness):
    """
    Set one arm of the PiGlow

    :param num: is the arm number, from 1 to 3
    :param brightness: is the light level, from 0-255
    """
    global lock

    # do this one at a time
    with lock:
        for i in ARM_LED_LIST[num - 1]:
            led_list[i - 1]['brightness'] = brightness
        pyglow.arm(num, brightness=brightness)


def set_color(num, brightness):
    """
    Set one color ring of the PiGlow

    :param num: is the color/ring number, from 1 to 6
    :param brightness: is the light level, from 0-255
    """
    global lock

    # do this one at a time
    with lock:
        for i in COLOR_LED_LIST[num - 1]:
            led_list[i - 1]['brightness'] = brightness
        pyglow.color(num, brightness=brightness)


def set_clear():
    """
        Turn off all LEDs.
    """
    global lock

    # do this one at a time
    with lock:
        for i in range(1, 19):
            led_list[i - 1]['brightness'] = 0
        pyglow.all(brightness=0)


def set_starburst(brightness, speed_ms):
    """
    Execute starburst pattern
    :param brightness: is the light level, from 0-255
    """
    global lock

    # do this one at a time
    with lock:
        # clear first
        pyglow.all(brightness=0)
        for i in range(1, 7):
            pyglow.color(i, brightness=brightness)
            sleep(speed_ms / 1000.0)
            pyglow.color(i, brightness=0)


# interface to the h/w layer
def set_leds(set_list):
    """
    Set list of LED

    :param set_list: is a list of (id, brightness)
    """
    global lock

    # do this one at a time
    with lock:
        for num, b in set_list:
            led_list[num - 1]['brightness'] = b
            pyglow.led(num, brightness=b)


class PiGlowResourceMixin(object):
    """
     Mixin provide some helper functions.
    """
    def validate_led_id(self, led_id):
        if led_id is None or not led_id in range(1, 19):
            abort(404, message='LED id must be in the range of 1 to 18')

    def validate_brightness(self, b):
        if b is None or not b in range(0, 256):
            abort(400, message='brightness must be in the range of 0 to 255')

    def validate_arm_id(self, arm_id):
        if arm_id is None or not arm_id in range(1, 4):
            abort(404, message='arm id must be in the range of 1 to 3')

    def validate_color_id(self, color_id):
        if color_id is None or not color_id in range(1, 7):
            abort(404, message='color id must be in the range of 1 to 6')

    def validate_speed(self, msec):
        """ speed is in millseconds """
        if msec is None or not msec in range(0, 5000):
            abort(404, message='speed must be milliseconds in the range of 0 to 5000')

    def queue_command(self, func, *args):
        """
        Queue function with optional args in a separate thread.
        """
        h = threading.Thread(target=func, args=args)
        h.setDaemon(True)
        h.start()
        return h


class LedListAPI(PiGlowResourceMixin, Resource):
    """
        REST interface to the list of LED as a whole.

        Set the brightness of one or more LEDs

        PUT /leds

        URL Parameters:
        None

        Data Parameters (required), list of one or more dictionaries:
        [
            {
                "led_id": [integer 1-18],
                "brightness": [integer 0-255]
            },

            {
                "led_id": [integer 1-18],
                "brightness": [integer 0-255]
            }
        ]

        curl example

        curl -X PUT -H 'Content-Type: application/json'
            -d '[{"led_id":1,\"brightness":100}, {"led_id":2, "brightness":100} ]' localhost:5000/leds

    """
    def get(self):
        return led_list

    def put(self):
        """
        Accept JSON [ {led_id:n, brightness:b}, ...]
        """
        set_list = []
        for d in request.json:
            n = d['led_id']
            b = d['brightness']
            self.validate_brightness(b)
            self.validate_led_id(n)
            set_list.append((n, b))

        self.queue_command(set_leds, set_list)
        return led_list


class LedAPI(PiGlowResourceMixin, Resource):
    """
        REST interface to control individual LED.

    """
    def get(self, led_id):
        """
        Get the brightness of a LED.

        (These are cached values, not necessary correct!)
        """
        return led_list[led_id]

    def put(self, led_id):
        """
        Set the brightness of a LED

        PUT /leds/:id

        URL Parameters:
        id=[integer] in the range of 1-18

        Optional:
        brightness=[integer 0-255]

        Data Parameters (optional):
        {
            "brightness": [integer 0-255]
        }
        """
        self.validate_led_id(led_id)

        parser = reqparse.RequestParser()
        parser.add_argument('brightness', type=int, default=0,
                            help='Brightness for this arm of LED')
        args = parser.parse_args()

        b = args.get('brightness')
        self.validate_brightness(b)

        self.queue_command(set_led, led_id, b)
        return led_list[led_id - 1]


class ArmAPI(PiGlowResourceMixin, Resource):
    """
        Control a single arm on the PiGlow.
        /arms/:arm_id/

        The brightness value can be specified as json or form data in the request,
        or directly on the URL.

        :param arm_id: on the URL is 1 to 3
        :param brightness: brightness=0..255
    """
    def get(self, arm_id):
        return led_list

    def put(self, arm_id):

        parser = reqparse.RequestParser()
        parser.add_argument('brightness', type=int, default=0,
                            help='Brightness for this arm of LED')
        args = parser.parse_args()

        self.validate_arm_id(arm_id)

        b = args.get('brightness')
        self.validate_brightness(b)

        self.queue_command(set_arm, arm_id, b)
        return led_list


class ColorAPI(PiGlowResourceMixin, Resource):
    """
        Control a single color ring on the PiGlow.
        /colors/:color_id/

        The brightness value can be specified as json or form data in the request,
        or directly on the URL.

        :param color_id: on the URL is 1 to 6
        :param brightness: brightness=0..255
    """
    def get(self, color_id):
        return led_list

    def put(self, color_id):

        parser = reqparse.RequestParser()
        parser.add_argument('brightness', type=int, default=0,
                            help='Brightness for this arm of LED')
        args = parser.parse_args()

        self.validate_color_id(color_id)

        b = args.get('brightness')
        self.validate_brightness(b)

        self.queue_command(set_color, color_id, b)
        return led_list


class PatternAPI(PiGlowResourceMixin, Resource):
    """
        This API allows display of patterns as a whole.
        /pattern/:pattern_name/

        :param brightness: brightness=0..255
    """
    def get(self, color_id):
        return led_list

    def put(self, pattern_name):

        parser = reqparse.RequestParser()
        parser.add_argument('brightness', type=int, default=0,
                            help='Brightness for the pattern')
        parser.add_argument('speed', type=int, default=0,
                            help='Speed for the pattern')

        args = parser.parse_args()
        b = args.get('brightness')
        self.validate_brightness(b)
        s = args.get('speed')
        self.validate_speed(s)

        if pattern_name == 'clear':
            self.queue_command(set_clear)
        if pattern_name == 'starburst':
            self.queue_command(set_starburst, b, s)
        return led_list

api.add_resource(LedListAPI, '/leds')
api.add_resource(LedAPI, '/leds/<int:led_id>')
api.add_resource(ArmAPI, '/arms/<int:arm_id>')
api.add_resource(ColorAPI, '/colors/<int:color_id>')
api.add_resource(PatternAPI, '/patterns/<pattern_name>')


@app.route('/', methods=['GET', ])
def index():
    return 'PiGlow RESTful API Server.<br />See http://github.com/pkshiu/piglowserver for info'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
