import time
import board, digitalio
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789

W = H = 240
FPS = 20
FONT = ImageFont.truetype("assets/fonts/Galmuri11.ttf", 12)
FONT_BIG = ImageFont.truetype("assets/fonts/Galmuri11.ttf", 24)

cs  = digitalio.DigitalInOut(board.CE0)
dc  = digitalio.DigitalInOut(board.D25)
rst = digitalio.DigitalInOut(board.D24)

bl = digitalio.DigitalInOut(board.D26)
bl.switch_to_output()
bl.value = True

spi = board.SPI()
disp = st7789.ST7789(spi, width=W, height=H, rotation=180, y_offset=80,
                     cs=cs, dc=dc, rst=rst, baudrate=24000000)

def btn(pin):
    d = digitalio.DigitalInOut(pin)
    d.direction = digitalio.Direction.INPUT
    d.pull = digitalio.Pull.UP
    return d

UP, DOWN = btn(board.D17), btn(board.D22)
LEFT, RIGHT = btn(board.D27), btn(board.D23)
CENTER = btn(board.D4)
BTN_A, BTN_B = btn(board.D5), btn(board.D6)

img = Image.new("RGB", (W, H))
draw = ImageDraw.Draw(img)

scene = "title"
prev_a = False

def draw_title():
    draw.rectangle((0, 0, W, H), fill=(10, 10, 25))
    draw.text((W // 2, 90), "자수성가", font=FONT_BIG, fill=(255, 215, 0), anchor="mm")
    draw.text((W // 2, 170), "A 버튼을 눌러 시작", font=FONT, fill=(200, 200, 200), anchor="mm")

def draw_baby():
    draw.rectangle((0, 0, W, H), fill=(10, 10, 25))
    draw.text((8, 8), "0살", font=FONT, fill=(255, 255, 255))
    draw.text((8, 28), "중산층 가정에서 태어났다", font=FONT, fill=(255, 255, 255))

while True:
    now = time.monotonic()

    a = not BTN_A.value          # 누르면 LOW라서 반전
    a_pressed = a and not prev_a  # 이번 프레임에 처음 눌림
    prev_a = a

    if scene == "title" and a_pressed:
        scene = "baby"

    if scene == "title":
        draw_title()
    elif scene == "baby":
        draw_baby()
    disp.image(img)

    time.sleep(max(0, 1 / FPS - (time.monotonic() - now)))
