import time
import board, digitalio
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789

W = H = 240
FPS = 20
FONT = ImageFont.truetype("assets/fonts/Galmuri11.ttf", 12)

cs  = digitalio.DigitalInOut(board.CE0)
dc  = digitalio.DigitalInOut(board.D25)
rst = digitalio.DigitalInOut(board.D24)

bl = digitalio.DigitalInOut(board.D26)
bl.switch_to_output()
bl.value = True

spi = board.SPI()
disp = st7789.ST7789(spi, width=W, height=H, rotation=0, y_offset=80,
                     cs=cs, dc=dc, rst=rst, baudrate=24000000)

def btn(pin):
    d = digitalio.DigitalInOut(pin)
    d.direction = digitalio.Direction.INPUT
    d.pull = digitalio.Pull.UP
    return d

UP, DOWN = btn(board.D17), btn(board.D22)
LEFT, RIGHT = btn(board.D27), btn(board.D23)
CENTER = btn(board.D4)

img = Image.new("RGB", (W, H))
draw = ImageDraw.Draw(img)

while True:
    now = time.monotonic()

    draw.rectangle((0, 0, W, H), fill=(10, 10, 25))
    draw.text((8, 8), "중산층 가정에서 태어났다", font=FONT, fill=(255, 255, 255))
    disp.image(img)

    time.sleep(max(0, 1 / FPS - (time.monotonic() - now)))
