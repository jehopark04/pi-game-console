import time
import board, digitalio
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
from data import STAGES, STARTUP_40
from sprites import SCALE, BODY, BABY, PALETTES, AGE_SPRITE

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
PW, PH = 8 * SCALE, 12 * SCALE   # 캐릭터 크기 (24x36)
SPEED = 4            # 한 프레임에 움직이는 픽셀 수
px, py = 8, 130      # 캐릭터 왼쪽 위 좌표
age = 0
UP_DOOR   = (150, 50, 232, 120)    # (왼, 위, 오른, 아래)
DOWN_DOOR = (150, 160, 232, 230)
choices = {}         # 나이: 고른 선택지 이름

def move_player():
    global px, py
    if not LEFT.value:
        px -= SPEED
    if not RIGHT.value:
        px += SPEED
    if not UP.value:
        py -= SPEED
    if not DOWN.value:
        py += SPEED
    px = max(0, min(W - PW, px))
    py = max(40, min(H - PH, py))   # 위쪽 40칸은 글자 자리

def draw_player():
    name = AGE_SPRITE.get(age, "worker")
    grid = BABY if name == "baby" else BODY
    colors = PALETTES[name]
    for row, line in enumerate(grid):
        for col, ch in enumerate(line):
            if ch in colors:
                x, y = px + col * SCALE, py + row * SCALE
                draw.rectangle((x, y, x + SCALE - 1, y + SCALE - 1), fill=colors[ch])

def draw_background():
    draw.rectangle((0, 0, W, H), fill=(25, 30, 60))        # 하늘
    draw.rectangle((0, 40, W, 42), fill=(80, 80, 120))     # 글자 영역 구분선
    draw.rectangle((0, 226, W, H), fill=(60, 45, 30))      # 땅

def draw_door(door, label):
    x1, y1, x2, y2 = door
    draw.rectangle(door, fill=(110, 70, 35), outline=(60, 35, 15), width=3)
    draw.ellipse((x2 - 14, (y1 + y2) // 2 - 3, x2 - 8, (y1 + y2) // 2 + 3), fill=(255, 215, 0))
    draw.text(((x1 + x2) // 2, (y1 + y2) // 2), label, font=FONT, fill=(255, 255, 255), anchor="mm")

def hit(door):
    x1, y1, x2, y2 = door
    return px < x2 and px + PW > x1 and py < y2 and py + PH > y1

def stage_data():
    if age == 40 and choices.get(27) == "창업":
        return STARTUP_40
    return STAGES.get(age)

def choose(choice):
    global age, scene, px, py
    choices[age] = choice["label"]
    px, py = 8, 130
    if choice["next"] is None:
        scene = "ending"
    else:
        age = choice["next"]

def draw_title():
    draw.rectangle((0, 0, W, H), fill=(10, 10, 25))
    draw.text((W // 2, 90), "자수성가", font=FONT_BIG, fill=(255, 215, 0), anchor="mm")
    draw.text((W // 2, 170), "A 버튼을 눌러 시작", font=FONT, fill=(200, 200, 200), anchor="mm")

def draw_baby():
    draw_background()
    draw.text((8, 8), "0살", font=FONT, fill=(255, 255, 255))
    draw.text((8, 28), "중산층 가정에서 태어났다", font=FONT, fill=(255, 255, 255))
    draw_player()

def draw_stage():
    draw_background()
    draw.text((8, 8), f"{age}살", font=FONT, fill=(255, 255, 255))
    st = stage_data()
    if st:
        draw.text((8, 24), st["text"], font=FONT, fill=(255, 255, 255))
        for door, choice in ((UP_DOOR, st["up"]), (DOWN_DOOR, st["down"])):
            draw_door(door, choice["label"])
    else:
        draw.text((8, 24), "군대: 오른쪽 끝까지 가자 (임시)", font=FONT, fill=(150, 150, 150))
    draw_player()

def draw_ending():
    draw.rectangle((0, 0, W, H), fill=(10, 10, 25))
    draw.text((8, 8), "엔딩 (2주차에 구현)", font=FONT, fill=(255, 215, 0))
    for i, (a, c) in enumerate(choices.items()):
        draw.text((8, 32 + i * 16), f"{a}살: {c}", font=FONT, fill=(255, 255, 255))
    draw.text((8, 216), "A: 처음으로", font=FONT, fill=(200, 200, 200))

while True:
    now = time.monotonic()

    a = not BTN_A.value          # 누르면 LOW라서 반전
    a_pressed = a and not prev_a  # 이번 프레임에 처음 눌림
    prev_a = a

    if scene == "title" and a_pressed:
        scene = "baby"
    elif scene == "baby":
        move_player()
        if px >= W - PW:          # 오른쪽 끝에 닿으면
            scene = "stage"
            age = 15
            px, py = 8, 130
    elif scene == "stage":
        move_player()
        st = stage_data()
        if st:
            if hit(UP_DOOR):
                choose(st["up"])
            elif hit(DOWN_DOOR):
                choose(st["down"])
        elif age == 22 and px >= W - PW:     # 군대 임시: 오른쪽 끝까지 가면 통과
            age = 30 if choices.get(20) == "바로 취업" else 27
            px, py = 8, 130
    elif scene == "ending" and a_pressed:
        scene = "title"
        age = 0
        choices.clear()

    if scene == "title":
        draw_title()
    elif scene == "baby":
        draw_baby()
    elif scene == "stage":
        draw_stage()
    elif scene == "ending":
        draw_ending()
    disp.image(img)

    time.sleep(max(0, 1 / FPS - (time.monotonic() - now)))
