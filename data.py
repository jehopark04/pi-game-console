# 나이별 상황 문구와 위·아래 문 선택지
# next: 그 문을 고르면 넘어갈 나이
# result: 고른 뒤 결과 화면에 나올 문구

STAGES = {
    15: {
        "text": "어느 고등학교에 갈까?",
        "up":   {"label": "인문계",     "next": 20, "result": "공부해서 대학을 준비했다"},
        "down": {"label": "마이스터고", "next": 20, "result": "일찍 기술을 배웠다"},
    },
    20: {
        "text": "대학에 갈까, 바로 일할까?",
        "up":   {"label": "대학",       "next": 22, "result": "대학에 입학했다"},
        "down": {"label": "바로 취업",  "next": 22, "result": "일찍 사회에 나왔다"},
    },
    27: {
        "text": "어디서 일을 시작할까?",
        "up":   {"label": "대기업",     "next": 30, "result": "대기업에 입사했다"},
        "down": {"label": "창업",       "next": 30, "result": "내 회사를 차렸다"},
    },
    30: {
        "text": "모은 돈을 어떻게 할까?",
        "up":   {"label": "저축",       "next": 40, "result": "꾸준히 돈을 모았다"},
        "down": {"label": "투자",       "next": 40, "result": "모은 돈을 투자했다"},
    },
    40: {   # 대기업, 바로 취업 경로
        "text": "다음 10년을 정할 때다",
        "up":   {"label": "현상 유지",  "next": 60, "result": "안정된 생활을 이어 갔다"},
        "down": {"label": "사업 시작",  "next": 60, "result": "회사를 나와 사업을 시작했다"},
    },
    60: {
        "text": "은퇴할 나이가 됐다",
        "up":   {"label": "은퇴",       "next": None, "result": "일을 내려놓고 쉬기로 했다"},
        "down": {"label": "계속 일하기", "next": None, "result": "계속 일하기로 했다"},
    },
}

# 27살에 창업한 경로의 40살
STARTUP_40 = {
    "text": "사업이 자리를 잡았다",
    "up":   {"label": "현상 유지",  "next": 60, "result": "사업을 지금 규모로 지켰다"},
    "down": {"label": "사업 확장",  "next": 60, "result": "사업을 크게 늘렸다"},
}
