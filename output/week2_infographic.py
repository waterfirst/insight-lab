#!/usr/bin/env python3
"""Insight Lab Week 2 - SNS Infographic (1080x1920)"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1920
img = Image.new('RGB', (W, H), '#0d1117')
draw = ImageDraw.Draw(img)

# Fonts
try:
    font_bold = ImageFont.truetype("/usr/share/fonts/truetype/nanum/NanumSquareB.ttf", 48)
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/nanum/NanumSquareEB.ttf", 56)
    font_body = ImageFont.truetype("/usr/share/fonts/truetype/nanum/NanumSquareR.ttf", 32)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/nanum/NanumSquareR.ttf", 26)
    font_huge = ImageFont.truetype("/usr/share/fonts/truetype/nanum/NanumSquareEB.ttf", 72)
    font_num = ImageFont.truetype("/usr/share/fonts/truetype/nanum/NanumSquareEB.ttf", 44)
except:
    font_bold = font_title = font_body = font_small = font_huge = font_num = ImageFont.load_default()

# Colors
RED = '#e63946'
TEAL = '#2a9d8f'
ORANGE = '#f4a261'
WHITE = '#f1faee'
GRAY = '#8b949e'
DARK = '#161b22'
ACCENT = '#264653'

# --- Header gradient ---
for y in range(300):
    r = int(13 + (38-13) * y/300)
    g = int(17 + (70-17) * y/300)
    b = int(23 + (83-23) * y/300)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Tag
draw.rounded_rectangle([40, 40, 340, 90], radius=20, fill=RED)
draw.text((60, 47), "INSIGHT LAB W2", fill=WHITE, font=font_small)

# Title
draw.text((W//2, 140), "엔트로피와 제국", fill=WHITE, font=font_huge, anchor="mm")
draw.text((W//2, 210), "열역학으로 읽는 문명의 흥망", fill=ORANGE, font=font_bold, anchor="mm")

# Divider
draw.line([(100, 280), (W-100, 280)], fill=TEAL, width=2)

# --- Section 1: Core Thesis ---
y = 320
draw.rounded_rectangle([40, y, W-40, y+220], radius=15, fill=DARK)
draw.text((70, y+20), "01", fill=RED, font=font_num)
draw.text((140, y+22), "핵심 테제", fill=WHITE, font=font_bold)
lines1 = [
    "열역학 제2법칙: 고립계의 엔트로피는",
    "항상 증가한다 → 질서는 스스로 유지되지 않는다",
    "",
    "제국도 같다. 팽창할수록 무질서가 누적되고,",
    "유지 비용이 창출 능력을 초과하면 붕괴한다."
]
for i, line in enumerate(lines1):
    draw.text((70, y+85+i*28), line, fill=GRAY if not line else WHITE, font=font_small)

# --- Section 2: Three Scholars ---
y = 580
draw.rounded_rectangle([40, y, W-40, y+340], radius=15, fill=DARK)
draw.text((70, y+20), "02", fill=TEAL, font=font_num)
draw.text((140, y+22), "세 학자의 수렴", fill=WHITE, font=font_bold)

scholars = [
    ("이븐 할둔", "아사비야(연대의식) 쇠퇴", "→ 4세대 만에 왕조 붕괴", RED),
    ("폴 케네디", "군사적 과잉팽창", "→ 자원 초과 시 하강 나선", ORANGE),
    ("프리고진", "산일구조와 분기점", "→ 위기에서 새 질서 창발", TEAL),
]
for i, (name, desc, result, color) in enumerate(scholars):
    sy = y + 90 + i * 85
    draw.rounded_rectangle([70, sy, 120, sy+60], radius=8, fill=color)
    draw.text((95, sy+10), str(i+1), fill=WHITE, font=font_bold, anchor="mm")
    draw.text((140, sy+5), name, fill=color, font=font_bold)
    draw.text((140, sy+40), f"{desc} {result}", fill=GRAY, font=font_small)

# --- Section 3: 2026 Now ---
y = 960
draw.rounded_rectangle([40, y, W-40, y+320], radius=15, fill=DARK)
draw.text((70, y+20), "03", fill=ORANGE, font=font_num)
draw.text((140, y+22), "2026년 이란 전쟁 — 지금 여기", fill=WHITE, font=font_bold)

stats = [
    ("$126", "유가 정점\n(배럴)", RED),
    ("4억", "전략비축유\n방출(배럴)", ORANGE),
    ("20%", "글로벌 석유\n공급 차단", RED),
]
box_w = (W - 120) // 3
for i, (num, label, color) in enumerate(stats):
    bx = 60 + i * (box_w + 10)
    by = y + 90
    draw.rounded_rectangle([bx, by, bx+box_w, by+140], radius=12, fill=color, outline=color)
    draw.text((bx + box_w//2, by+35), num, fill=WHITE, font=font_num, anchor="mm")
    for j, ln in enumerate(label.split('\n')):
        draw.text((bx + box_w//2, by+80+j*25), ln, fill=WHITE, font=font_small, anchor="mm")

draw.text((70, y+255), "동맹 이탈 · 달러 패권 위기 · 국내 양극화 심화", fill=GRAY, font=font_small)
draw.text((70, y+285), "→ 케네디의 '과잉팽창' 테제가 실시간 전개 중", fill=ORANGE, font=font_small)

# --- Section 4: Bifurcation ---
y = 1320
draw.rounded_rectangle([40, y, W-40, y+280], radius=15, fill=DARK)
draw.text((70, y+20), "04", fill=TEAL, font=font_num)
draw.text((140, y+22), "분기점 — 두 개의 미래", fill=WHITE, font=font_bold)

# Path A
draw.rounded_rectangle([60, y+85, W//2-20, y+240], radius=10, outline=RED, width=2)
draw.text((80, y+95), "경로 A: 붕괴", fill=RED, font=font_bold)
pA = ["엔트로피 임계 초과", "로마 제국 패턴 반복", "패권 해체·다극 혼돈"]
for i, t in enumerate(pA):
    draw.text((80, y+140+i*30), f"· {t}", fill=GRAY, font=font_small)

# Path B
draw.rounded_rectangle([W//2+20, y+85, W-60, y+240], radius=10, outline=TEAL, width=2)
draw.text((W//2+40, y+95), "경로 B: 새 질서", fill=TEAL, font=font_bold)
pB = ["산일구조의 창발", "다극 협력 체제", "탈페트로달러 시스템"]
for i, t in enumerate(pB):
    draw.text((W//2+40, y+140+i*30), f"· {t}", fill=GRAY, font=font_small)

# --- Footer ---
y = 1640
draw.line([(100, y), (W-100, y)], fill=ACCENT, width=1)

quote = '"엔트로피는 운명이 아니라 경고다."'
draw.text((W//2, y+50), quote, fill=ORANGE, font=font_bold, anchor="mm")

draw.text((W//2, y+110), "질서를 유지하려면 끊임없는", fill=WHITE, font=font_body, anchor="mm")
draw.text((W//2, y+150), "에너지 투입과 개방성이 필요하다.", fill=WHITE, font=font_body, anchor="mm")

# Bottom bar
draw.rectangle([0, H-80, W, H], fill=ACCENT)
draw.text((W//2, H-45), "INSIGHT LAB  ·  Week 2  ·  2026.04.06", fill=GRAY, font=font_small, anchor="mm")

out = "/home/ubuntu/.cokacdir/workspace/cp7jpheo/insight_lab/output/week2_infographic.png"
img.save(out, quality=95)
print(f"Saved: {out}")
