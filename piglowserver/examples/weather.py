"""
   Get weather from Yahoo, and update PiGlow using the pg_rest_server API.
"""
import urllib2
import urllib
import json
import requests
import datetime

CITY_STR = 'Boston, MA'
API_SERVER = 'http://192.168.2.124:5000'

# These are not used at the moment
WEATHER_CODES = [
    {0, 'tornado', 1},
    {1, 'tropical storm', 1},
    {2, 'hurricane', 1},
    {3, 'severe thunderstorms', 1},
    {4, 'thunderstorms', 1},
    {5, 'mixed rain and snow', 1},
    {6, 'mixed rain and sleet', 1},
    {7, 'mixed snow and sleet', 1},
    {8, 'freezing drizzle', 1},
    {9, 'drizzle', 1},
    {10, 'freezing rain', 1},
    {11, 'showers', 1},
    {12, 'showers', 1},
    {13, 'snow flurries', 1},
    {14, 'light snow showers', 1},
    {15, 'blowing snow', 1},
    {16, 'snow', 1},
    {17, 'hail', 1},
    {18, 'sleet', 1},
    {19, 'dust', 1},
    {20, 'foggy', 1},
    {21, 'haze', 1},
    {22, 'smoky', 1},
    {23, 'blustery', 1},
    {24, 'windy', 1},
    {25, 'cold', 1},
    {26, 'cloudy', 1},
    {27, 'mostly cloudy (night)', 1},
    {28, 'mostly cloudy (day)', 1},
    {29, 'partly cloudy (night)', 1},
    {30, 'partly cloudy (day)', 1},
    {31, 'clear (night)', 1},
    {32, 'sunny', 1},
    {33, 'fair (night)', 1},
    {34, 'fair (day)', 1},
    {35, 'mixed rain and hail', 1},
    {36, 'hot', 1},
    {37, 'isolated thunderstorms', 1},
    {38, 'scattered thunderstorms', 1},
    {39, 'scattered thunderstorms', 1},
    {40, 'scattered showers', 1},
    {41, 'heavy snow', 1},
    {42, 'scattered snow showers', 1},
    {43, 'heavy snow', 1},
    {44, 'partly cloudy', 1},
    {45, 'thundershowers', 1},
    {46, 'snow showers', 1},
    {47, 'isolated thundershowers', 1},
    {3200, 'not available', 1}
]


def get_temp(loc_text):
    """
        Get temperature and other info from yahoo weather.
        :param loc_text:
    """
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="%s")' % loc_text

    yql_url = baseurl + urllib.urlencode({'q': yql_query}) + "&format=json"
    result = urllib2.urlopen(yql_url).read()
    data = json.loads(result)
    # print json.dumps(data['query']['results'], indent=4)
    r = data['query']['results']['channel']['item']['condition']
    print json.dumps(r, indent=4)
    temp = r['temp']
    return int(temp)


def map_temp_to_led(f):
    """
    Map temperature in F to 1-6 where 1=hot, 6=freezing
    Range split to 10F each level with last range below 32F
    """
    for i in range(1, 6):
        if f > (5 - i) * 10 + 31:
            return i
    return 6


def set_led(led):
    requests.put('%s/patterns/clear' % API_SERVER)
    data = {'brightness': 40}
    while led <= 6:
        requests.put('%s/leds/%d' % (API_SERVER, led), data=data)
        led += 1


def animate():
    requests.put('%s/patterns/clear' % API_SERVER)
    data = {'brightness': 20, 'speed': 200}
    requests.put('%s/patterns/starburst' % API_SERVER, data=data)


def go():
    t = get_temp(CITY_STR)
    led = map_temp_to_led(t)
    print datetime.datetime.now()
    print 'Temp %s F -> LED %d' % (t, led)
    animate()
    set_led(led)

if __name__ == '__main__':
    go()
