# 22살 군대 미니게임: 총알 만들기, 움직이기, 맞았는지 확인
import random, time

SIZE = 6             # 총알 크기 (6x6)
SPEED = 6            # 총알이 한 프레임에 움직이는 픽셀 수
MAX_BULLETS = 5      # 화면에 동시에 나오는 총알 수
GAP = 0.6            # 총알을 만드는 간격(초)
SAFE_TIME = 1.0      # 맞은 뒤 무적 시간(초)

bullets = []         # 총알 위치 [x, y] 목록
hearts = 3
last_shot = 0        # 마지막으로 총알을 만든 시각
hit_time = 0         # 마지막으로 맞은 시각

def start():
    global hearts, last_shot, hit_time
    bullets.clear()
    hearts = 3
    last_shot = time.monotonic()
    hit_time = 0

def is_safe():
    return time.monotonic() - hit_time < SAFE_TIME

def update(px, py, pw, ph):
    global hearts, last_shot, hit_time
    now = time.monotonic()

    # 1) 일정 간격마다 오른쪽 끝, 무작위 높이에 총알 만들기
    if now - last_shot > GAP and len(bullets) < MAX_BULLETS:
        bullets.append([240, random.randint(44, 234 - SIZE)])
        last_shot = now

    # 2) 총알을 왼쪽으로 옮기고, 화면 밖으로 나간 총알은 지우기
    for b in bullets[:]:          # 복사본으로 돌아야 도는 중에 지워도 안전
        b[0] -= SPEED
        if b[0] < -SIZE:
            bullets.remove(b)

    # 3) 캐릭터와 부딪힌 총알 확인 (무적 시간에는 안 맞음)
    if is_safe():
        return
    for b in bullets:
        if b[0] < px + pw and b[0] + SIZE > px and b[1] < py + ph and b[1] + SIZE > py:
            hearts -= 1
            hit_time = now
            bullets.remove(b)
            break
