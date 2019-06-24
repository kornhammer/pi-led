import lib.base as config

import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
import time
import asyncio


class KnightRider():

    def knight_rider(self, led_stripe, trail_nb_leds=3, color=[255, 0, 0], times=5, sleep=0.08):
        if trail_nb_leds > self.led_count or trail_nb_leds <= 0:
            raise ValueError("Wrong trail_nb_leds value")
        black_color = Adafruit_WS2801.RGB_to_color(0, 0, 0)

        for i in range(times):
            # left to right
            for i in range(self.led_count + trail_nb_leds):
                led_stripe.set_pixels(black_color)
                for j in range(min(i + 1, trail_nb_leds)):
                    if i - j <= self.led_count - 1:
                        # division is to fake lower brightness
                        color_arr = [x / max((j * 8), 1) for x in color]
                        led_stripe.set_pixel(i - j, Adafruit_WS2801.RGB_to_color(
                            int(color_arr[0]), int(color_arr[1]), int(color_arr[2])))
                led_stripe.show()
                time.sleep(sleep)

            # right to left
            for i in reversed(range(-trail_nb_leds, self.led_count)):
                led_stripe.set_pixels(black_color)
                for j in range(min(self.led_count - i - 1, trail_nb_leds)):
                    if i + j >= 0:
                        # division is to fake lower brightness
                        color_arr = [x / max((j * 8), 1) for x in color]
                        led_stripe.set_pixel(i + j, Adafruit_WS2801.RGB_to_color(
                            int(color_arr[0]), int(color_arr[1]), int(color_arr[2])))
                led_stripe.show()
                time.sleep(sleep)

            time.sleep(0.7)

    def __init__(self, times=1, color=[255, 0, 0], sleep=0.002):
        self.led_stripe = config.led_stripe
        self.led_count = config.PIXEL_COUNT
        self.times = times
        self.color = color
        self.sleep = sleep

    async def run(self):
        self.led_stripe.clear()
        self.knight_rider(self.led_stripe, 45, self.color,
                          self.times, self.sleep)
        self.led_stripe.clear()
