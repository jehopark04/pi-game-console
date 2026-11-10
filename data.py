# 나이별 상황 문구와 위·아래 문 선택지
# next: 그 문을 고르면 넘어갈 나이

STAGES = {
    15: {
        "text": "어느 고등학교에 갈까?",
        "up":   {"label": "인문계",     "next": 20},
        "down": {"label": "마이스터고", "next": 20},
    },
    20: {
        "text": "대학에 갈까, 바로 일할까?",
        "up":   {"label": "대학",       "next": 22},
        "down": {"label": "바로 취업",  "next": 22},
    },
    27: {
        "text": "어디서 일을 시작할까?",
        "up":   {"label": "대기업",     "next": 30},
        "down": {"label": "창업",       "next": 30},
    },
    30: {
        "text": "모은 돈을 어떻게 할까?",
        "up":   {"label": "저축",       "next": 40},
        "down": {"label": "투자",       "next": 40},
    },
    40: {   # 대기업, 바로 취업 경로
        "text": "다음 10년을 정할 때다",
        "up":   {"label": "현상 유지",  "next": 60},
        "down": {"label": "사업 시작",  "next": 60},
    },
    60: {
        "text": "은퇴할 나이가 됐다",
        "up":   {"label": "은퇴",       "next": None},
        "down": {"label": "계속 일하기", "next": None},
    },
}

# 27살에 창업한 경로의 40살
STARTUP_40 = {
    "text": "사업이 자리를 잡았다",
    "up":   {"label": "현상 유지",  "next": 60},
    "down": {"label": "사업 확장",  "next": 60},
}
