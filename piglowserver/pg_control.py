"""
    Web server with a browser interface to control a PiGlow board
    by talking to the PiGlow RESTful API server.
"""
import requests
import json

from flask import (Flask, url_for, redirect)
from flask import (render_template, request)


app = Flask(__name__)
app.config.from_object('config')
# You can override config with local config file by setting PGS_SETTINGS
app.config.from_envvar('PGS_SETTINGS', silent=True)
print 'using API Server at: ', app.config['API_SERVER']

# zero entry is not used
led_list = [{'led_id': i, 'brightness': 0} for i in range(1, 19)]
ARM_LED_LIST = map(tuple, ([{'led_id': i, 'brightness': 0} for i in range(1, 7)],
                           [{'led_id': i, 'brightness': 0} for i in range(7, 13)],
                           [{'led_id': i, 'brightness': 0} for i in range(13, 19)]))


def make_url(path, *args):
    root = app.config.get('API_SERVER', 'http://localhost:5000')
    return root + path % args


@app.route('/', methods=['GET', ])
def show_control():
    return render_template('control.html', led_list=led_list,
                           arm_list=ARM_LED_LIST,
                           api_server=make_url('/'))


@app.route('/set_led', methods=['POST', ])
def set_led():
    """
    Set single LED
    """
    n = int(request.form.get('led_id'))
    v = request.form.get('brightness', 100)
    data = {'brightness': v}
    r = requests.put(make_url('/leds/%d', n), data=data)

    return redirect(url_for('show_control'))


@app.route('/set_leds', methods=['POST', ])
def set_leds():
    """
    Set multiple LEDs at the same time
    """
    data = []
    b = int(request.form.get('brightness', 0))
    for i in range(1, 19):
        checked = request.form.get('led_%d' % i)
        if checked == 'on':
            d = {'led_id': i, 'brightness': b}
        else:
            d = {'led_id': i, 'brightness': 0}
        data.append(d)

    r = requests.put(make_url('/leds'), data=json.dumps(data),
                     headers={'content-type': 'application/json'})
    return redirect(url_for('show_control'))


@app.route('/set_arms', methods=['POST', ])
def set_arms():

    b = request.form.get('brightness', 100)

    for i in range(1, 4):
        checked = request.form.get('arm_%d' % i)
        if checked == 'on':
            data = {'brightness': b}
        else:
            data = {'brightness': 0}

        r = requests.put(make_url('/arms/%d', i), data=data)

    return redirect(url_for('show_control'))


@app.route('/set_colors', methods=['POST', ])
def set_colors():

    b = request.form.get('brightness', 100)

    for i in range(1, 7):
        checked = request.form.get('color_%d' % i)
        if checked == 'on':
            data = {'brightness': b}
        else:
            data = {'brightness': 0}

        r = requests.put(make_url('/colors/%d', i), data=data)

    return redirect(url_for('show_control'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
