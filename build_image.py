#!/usr/bin/env python3
"""Draw the entry image for make.fun news-image-20261125.

A broadsheet front page summing up the world news of Wednesday
25 November 2026, drawn from scratch with Pillow. Deterministic:
same code, same bytes, every run. No network, no randomness.

Layout is computed from the real wrapped text heights, so nothing
overlaps: each block is placed after the one above it ends.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 230)
INK = (20, 20, 20)
RED = (176, 30, 36)
BLUE = (31, 78, 121)
GREY = (90, 86, 76)
NIGHT = (28, 38, 62)
GOLD = (214, 164, 65)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, fill, leading):
    """Draw wrapped text; return the y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def block_h(draw, text, fnt, max_w, leading):
    return len(wrap(draw, text, fnt, max_w)) * leading


def rule(draw, x0, x1, y, width=2):
    draw.line([(x0, y), (x1, y)], fill=INK, width=width)


def draw_tower_scene(draw, x0, y0, x1, y1):
    """Night skyline: the PIF Tower struck, smoke and a drone."""
    draw.rectangle([x0, y0, x1, y1], fill=NIGHT)
    for sx, sy in [(18, 20), (70, 12), (150, 30), (230, 14), (300, 26),
                   (40, 55), (200, 48), (330, 60), (120, 70)]:
        draw.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3],
                     fill=(220, 220, 200))
    for bx, bw, bh in [(0, 46, 90), (52, 34, 120), (250, 40, 100),
                       (296, 44, 130), (340, 28, 80)]:
        draw.rectangle([x0 + bx, y1 - bh, x0 + bx + bw, y1], fill=(48, 58, 86))
        for wy in range(y1 - bh + 10, y1 - 8, 16):
            for wx in range(x0 + bx + 6, x0 + bx + bw - 6, 12):
                draw.rectangle([wx, wy, wx + 4, wy + 6], fill=GOLD)
    # the PIF Tower: tall, centre-left, lit windows
    tx0, tx1 = x0 + 108, x0 + 196
    draw.rectangle([tx0, y0 + 34, tx1, y1], fill=(74, 88, 128))
    draw.rectangle([tx0 + 6, y0 + 34, tx1 - 6, y0 + 44], fill=(96, 112, 152))
    for wy in range(y0 + 52, y1 - 8, 18):
        for wx in range(tx0 + 10, tx1 - 10, 16):
            draw.rectangle([wx, wy, wx + 6, wy + 8], fill=GOLD)
    # small explosion glow at the tower top
    cx, cy = (tx0 + tx1) // 2, y0 + 30
    for r, col in [(26, (255, 120, 40)), (17, (255, 170, 60)),
                   (9, (255, 220, 130))]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    # smoke puffs drifting right
    for sx, sy, sr in [(230, 52, 16), (256, 40, 20), (288, 56, 14),
                       (316, 44, 11)]:
        draw.ellipse([x0 + sx - sr, y0 + sy - sr, x0 + sx + sr, y0 + sy + sr],
                     fill=(150, 150, 150))
    # drone quadcopter, upper right
    dx, dy = x0 + 300, y0 + 92
    draw.line([(dx - 16, dy - 8), (dx + 16, dy + 8)], fill=(230, 230, 230),
              width=3)
    draw.line([(dx - 16, dy + 8), (dx + 16, dy - 8)], fill=(230, 230, 230),
              width=3)
    draw.ellipse([dx - 6, dy - 6, dx + 6, dy + 6], fill=(200, 40, 40))
    for px, py in [(dx - 16, dy - 8), (dx + 16, dy + 8),
                   (dx - 16, dy + 8), (dx + 16, dy - 8)]:
        draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(180, 180, 180))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 36
    right = W - m
    y = 12

    # --- top strip ---
    d.text((m, y), "ONE DAY  ·  ONE PAGE  ·  THE WORLD'S NEWS",
           font=font(SANS_B, 20), fill=GREY)
    d.text((right, y), "25 NOV 2026", font=font(SANS_B, 20), fill=GREY,
           anchor="ra")
    y += 30

    # --- masthead, fitted to the page width ---
    size = 92
    while size > 60:
        fnt = font(SERIF_B, size)
        if d.textlength("THE WORLD TODAY", font=fnt) <= right - m:
            break
        size -= 2
    d.text((W // 2, y), "THE WORLD TODAY", font=font(SERIF_B, size),
           fill=INK, anchor="ma")
    y += size + 12
    rule(d, m, right, y, 3)
    y += 10
    d.text((W // 2, y), "WEDNESDAY, 25 NOVEMBER 2026",
           font=font(SANS_B, 30), fill=INK, anchor="ma")
    y += 36
    d.text((W // 2, y), "The day's world news, summed up in one picture",
           font=font(SERIF, 24), fill=GREY, anchor="ma")
    y += 30
    rule(d, m, right, y, 2)
    y += 10

    # --- lead story ---
    lead_text_w = 584
    head_f = font(SERIF_B, 40)
    body_f = font(SANS, 22)
    head = "Houthi drone hits Riyadh's tallest tower"
    body = ("Eleven people were wounded when a drone struck the PIF Tower "
            "in Riyadh's financial district on Tuesday, Saudi civil "
            "defence said.")
    head_h = block_h(d, head, head_f, lead_text_w, 48)
    body_h = block_h(d, body, body_f, lead_text_w, 28)
    text_h = 26 + 6 + head_h + 8 + body_h
    box_h = max(text_h, 190)
    # text, left column
    ty = y
    d.text((m, ty), "LEAD  ·  SAUDI ARABIA", font=font(SANS_B, 22), fill=RED)
    ty += 32
    ty = para(d, m, ty, head, head_f, lead_text_w, INK, 48)
    para(d, m, ty + 8, body, body_f, lead_text_w, INK, 28)
    # illustration, right column
    ix0, ix1 = 636, right
    d.rectangle([ix0 - 2, y - 2, ix1 + 2, y + box_h + 2], outline=INK, width=2)
    draw_tower_scene(d, ix0, y, ix1, y + box_h)
    d.text((ix0, y + box_h + 8), "The PIF Tower, Riyadh. (Illustration)",
           font=font(SERIF, 19), fill=GREY)
    y += max(text_h, box_h + 30)
    rule(d, m, right, y, 2)
    y += 8

    # --- six stories, 3 columns x 2 rows ---
    d.text((m, y), "THE DAY IN SIX STORIES", font=font(SANS_B, 22), fill=INK)
    y += 28
    stories = [
        ("UKRAINE", RED,
         "Zelenskyy confirms Baltic ship strike",
         "Kyiv says its drones hit the Russian cargo ship Sparta II in "
         "the Gulf of Finland."),
        ("RUSSIA", RED,
         "Putin vows retaliation for refinery strikes",
         "Moscow says Ukraine keeps hitting its oil refineries; its 2027 "
         "defence budget rises 27%."),
        ("THE GULF", BLUE,
         "Tankers hit mines in the Strait of Hormuz",
         "Iran's Revolutionary Guards say tankers under US air escort "
         "struck naval mines."),
        ("TECH", BLUE,
         "Huawei guilty in US trial",
         "A Brooklyn jury convicts Huawei of trade-secrets theft and "
         "bank-fraud conspiracy."),
        ("CHINA", BLUE,
         "Death sentence in spy case",
         "An official is sentenced to death for leaking state secrets; "
         "Shanghai's party chief is probed."),
        ("GAZA", RED,
         "Israeli strike kills Hamas security chief",
         "Naim Abu Nahl is killed in Gaza; health officials warn of a "
         "meningitis epidemic."),
    ]
    col_w, col_gap = 304, 16
    kick_f = font(SANS_B, 19)
    sh_f = font(SERIF_B, 24)
    sb_f = font(SANS, 18)
    for row in range(2):
        row_cards = stories[row * 3:(row + 1) * 3]
        row_h = 0
        for _, _, headline, text in row_cards:
            h = (10 + 22 + 6
                 + block_h(d, headline, sh_f, col_w, 27) + 4
                 + block_h(d, text, sb_f, col_w, 21))
            row_h = max(row_h, h)
        for i, (kick, col, headline, text) in enumerate(row_cards):
            cx = m + i * (col_w + col_gap)
            d.rectangle([cx, y, cx + col_w, y + 3], fill=col)
            d.text((cx, y + 10), kick, font=kick_f, fill=col)
            cy = para(d, cx, y + 38, headline, sh_f, col_w, INK, 27)
            para(d, cx, cy + 4, text, sb_f, col_w, INK, 21)
        y += row_h + 12
    rule(d, m, right, y, 2)
    y += 8

    # --- also today: four briefs ---
    d.text((m, y), "ALSO TODAY", font=font(SANS_B, 22), fill=INK)
    y += 28
    briefs = [
        ("Cartagena hostages",
         "Gunmen seize a supermarket after a failed cash-truck robbery."),
        ("Turkey pardon",
         "Freedom and Feathers are spared at the White House ceremony."),
        ("Seoul minister quits",
         "South Korea's education minister resigns over an exam scandal."),
        ("Drone over Poland",
         "A Russian drone enters Polish airspace overnight."),
    ]
    bw = 228
    bh_f = font(SANS_B, 19)
    bb_f = font(SANS, 17)
    brief_h = 0
    for head, text in briefs:
        h = (block_h(d, head, bh_f, bw, 23) + 2
             + block_h(d, text, bb_f, bw, 21))
        brief_h = max(brief_h, h)
    for i, (head, text) in enumerate(briefs):
        bx = m + i * (bw + 8)
        by = para(d, bx, y, head, bh_f, bw, INK, 23)
        para(d, bx, by + 2, text, bb_f, bw, INK, 21)
    y += brief_h + 8
    rule(d, m, right, y, 2)
    y += 6

    # --- footer ---
    d.text((W // 2, y),
           "Sources: Reuters · Al Jazeera · Kyiv Independent · The Guardian — "
           "all reported 25 November 2026.",
           font=font(SANS, 17), fill=GREY, anchor="ma")
    y += 24
    assert y <= H, f"layout overflow: y={y}"
    return img


if __name__ == "__main__":
    image = build()
    image.save("entry.png", format="PNG")
    print("entry.png:", image.size)
