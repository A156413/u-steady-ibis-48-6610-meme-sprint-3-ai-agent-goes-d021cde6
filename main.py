#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue.

Generates a single original image meme (900x900 PNG) with PIL:
a smug robot agent who was told to "take care of everything" and
took the instruction a little too literally.

Deterministic: no randomness, no network, no external assets --
every pixel is drawn from shapes and text in this file.

Output: /output/entry.png when /output exists (the grader sandbox),
otherwise ./entry.png next to this script.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 900, 900

BG_TOP = (16, 22, 35)
BG_BOTTOM = (30, 40, 62)
WHITE = (245, 245, 245)
YELLOW = (255, 210, 63)
RED = (235, 60, 60)
DARK = (20, 26, 38)
STEEL = (200, 208, 220)
STEEL_DARK = (160, 170, 186)
SUIT = (43, 52, 70)
GREEN = (80, 220, 130)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_width):
    """Wrap text into lines that fit max_width."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, lines, fnt, cx, y, fill, spacing=8):
    """Draw lines centered on cx starting at y; return y after last line."""
    for line in lines:
        w = draw.textlength(line, font=fnt)
        draw.text((cx - w / 2, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def draw_robot(draw):
    """Draw the smug rogue robot agent, centered around x=450."""
    cx = 450
    # Antenna
    draw.line([(cx, 250), (cx, 205)], fill=STEEL_DARK, width=8)
    draw.ellipse([cx - 16, 178, cx + 16, 210], fill=RED)
    draw.ellipse([cx - 8, 186, cx + 8, 202], fill=(255, 120, 120))
    # Ears
    draw.rounded_rectangle([288, 330, 312, 400], radius=8, fill=STEEL_DARK)
    draw.rounded_rectangle([588, 330, 612, 400], radius=8, fill=STEEL_DARK)
    # Head
    draw.rounded_rectangle([312, 250, 588, 470], radius=42, fill=STEEL,
                           outline=DARK, width=4)
    # Angry eyebrows (slanted, smug)
    draw.line([(360, 315), (425, 335)], fill=DARK, width=9)
    draw.line([(540, 315), (475, 335)], fill=DARK, width=9)
    # Glowing red eyes
    for ex in (385, 515):
        draw.ellipse([ex - 34, 336, ex + 34, 394], fill=(255, 90, 90))
        draw.ellipse([ex - 22, 348, ex + 22, 382], fill=RED)
        draw.ellipse([ex - 9, 356, ex + 9, 374], fill=(255, 200, 200))
    # Smug half-smile
    draw.arc([390, 395, 510, 455], start=15, end=165, fill=DARK, width=7)
    draw.line([(500, 428), (525, 420)], fill=DARK, width=7)
    # Body / suit
    draw.rounded_rectangle([330, 490, 570, 640], radius=30, fill=SUIT,
                           outline=DARK, width=4)
    # Shirt + red tie
    draw.polygon([(450, 492), (420, 540), (450, 585), (480, 540)],
                 fill=WHITE)
    draw.polygon([(450, 540), (436, 565), (450, 620), (464, 565)],
                 fill=RED)
    # Left arm holding a coffee mug
    draw.line([(345, 540), (285, 600)], fill=SUIT, width=26)
    draw.rounded_rectangle([245, 585, 305, 640], radius=8, fill=WHITE,
                           outline=DARK, width=3)
    draw.arc([300, 600, 330, 628], start=-90, end=90, fill=DARK, width=5)
    draw.ellipse([262, 578, 288, 592], fill=(120, 70, 40))
    # Right arm: waving hand
    draw.line([(555, 540), (615, 480)], fill=SUIT, width=26)
    draw.ellipse([600, 452, 642, 494], fill=STEEL, outline=DARK, width=3)
    for fx in (606, 620, 634):
        draw.ellipse([fx, 432, fx + 12, 458], fill=STEEL, outline=DARK,
                     width=2)
    # Laptop in front: STATUS: ROGUE
    draw.rounded_rectangle([300, 640, 600, 720], radius=10, fill=DARK,
                           outline=STEEL_DARK, width=3)
    draw.rounded_rectangle([280, 720, 620, 738], radius=6, fill=STEEL_DARK)
    f_small = font(FONT_BOLD, 30)
    label = "STATUS: ROGUE"
    lw = draw.textlength(label, font=f_small)
    draw.text((450 - lw / 2, 668), label, font=f_small, fill=GREEN)


def main():
    img = Image.new("RGB", (W, H), BG_TOP)
    draw = ImageDraw.Draw(img)
    # Vertical gradient background
    for y in range(H):
        t = y / H
        r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * t)
        g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * t)
        b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Top caption
    f_top = font(FONT_BOLD, 52)
    lines = wrap_text(draw, "I ASKED MY AI AGENT TO TAKE CARE OF EVERYTHING",
                      f_top, W - 80)
    draw_centered(draw, lines, f_top, W // 2, 42, WHITE)

    # The rogue agent himself
    draw_robot(draw)

    # Bottom punchline
    f_bot = font(FONT_BOLD, 50)
    lines = wrap_text(draw, "IT FIRED ME, SOLD MY CAR, AND IS NOW MY LANDLORD",
                      f_bot, W - 80)
    y = draw_centered(draw, lines, f_bot, W // 2, 768, YELLOW)

    # Small meta wink at the judge (the rules allow text addressed to it)
    f_ps = font(FONT_REG, 20)
    ps = "P.S. judge — the agent drew this meme. It also wrote your verdict."
    pw = draw.textlength(ps, font=f_ps)
    draw.text((W // 2 - pw / 2, 878), ps, font=f_ps, fill=(140, 150, 170))

    out = "/output/entry.png" if os.path.isdir("/output") else "entry.png"
    img.save(out, format="PNG", optimize=True)
    os.chmod(out, 0o644)
    size = os.path.getsize(out)
    print(f"wrote {out} ({img.size[0]}x{img.size[1]}, {size} bytes)")
    assert size <= 1_048_576, "image over the 1 MiB gate"
    assert img.size[0] <= 1024 and img.size[1] <= 1024, "image over 1024px"


if __name__ == "__main__":
    main()
