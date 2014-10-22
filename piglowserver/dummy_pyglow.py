# Define global variables
LED_LIST = tuple(xrange(1, 19))
LED_HEX_LIST = (
    0x07, 0x08, 0x09, 0x06, 0x05, 0x0A,
    0x12, 0x11, 0x10, 0x0E, 0x0C, 0x0B,
    0x01, 0x02, 0x03, 0x04, 0x0F, 0x0D)
ARM_LIST = tuple(xrange(1, 4))
ARM_LED_LIST = map(tuple, (xrange(1, 7), xrange(7, 13), xrange(13, 19)))
COLOR_LIST = tuple(xrange(1, 7))
COLOR_NAME_LIST = ("white", "blue", "green", "yellow", "orange", "red")
COLOR_LED_LIST = (
    (6, 12, 18), (5, 11, 17), (4, 10, 16), (3, 9, 15), (2, 8, 14), (1, 7, 13))


class PyGlow(object):
    def led(self, led_id, brightness):
        print 'Dummy PiGlow - Setting LED: %d to %d' % (led_id, brightness)

    def arm(self, arm_id, brightness):
        print 'Dummy PiGlow - Setting arm: %d to %d' % (arm_id, brightness)

    def color(self, color_id, brightness):
        print 'Dummy PiGlow - Setting color: %d to %d' % (color_id, brightness)

    def all(self, brightness):
        print 'Dummy PiGlow - Setting all to %d' % (brightness)
