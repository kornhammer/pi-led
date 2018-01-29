# Simple demo of of the WS2801/SPI-like addressable RGB LED lights.
import time
import RPi.GPIO as GPIO

# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI

# Configure the count of pixels:
PIXEL_COUNT = 160

# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0

led_stripe = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

class Base:

    # led_stripe
    # led_count
    #
    PIXEL_COUNT = 160

    def __init__(self):
        print("init base")
        # self.led_count = PIXEL_COUNT
