from lib.base import Base


class Kitt(Base):
    pass

    def __init__(self):
        super()
        print("init kitt")

    def run(self):
        # Clear all the pixels to turn them off.
        pixels.clear()
        pixels.show()  # Make sure to call show() after changing any pixels!

        rainbow_cycle_successive(pixels, wait=0.1)
        rainbow_cycle(pixels, wait=0.01)

        brightness_decrease(pixels)

        appear_from_back(pixels)

        for i in range(3):
            blink_color(pixels, blink_times=1, color=(255, 0, 0))
            blink_color(pixels, blink_times=1, color=(0, 255, 0))
            blink_color(pixels, blink_times=1, color=(0, 0, 255))

        rainbow_colors(pixels)

        brightness_decrease(pixels)
