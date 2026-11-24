#!/usr/bin/env python3
"""Draw the 24 November 2026 front page for news-image-20261124.

Builds a 1024x1024 JPEG newspaper front page, "THE WORLD TODAY", from
the real stories reported on Tuesday 24 November 2026, and writes it to
entry.png next to this file. Deterministic: same input, same bytes.
Run: python3 build_image.py
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (178, 34, 34)
GREY = (90, 86, 78)
RULE = (17, 17, 17)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_IT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap using real glyph widths."""
    words = text.split()
    lines, line = [], ""
    for word in words:
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def centred(draw, y, text, fnt, fill=INK):
    draw.text((W // 2, y), text, font=fnt, fill=fill, anchor="ma")


def rule(draw, y, width=3):
    draw.line([(48, y), (W - 48, y)], fill=RULE, width=width)


def story(draw, x, y, w, kicker, headline, deck, head_size=32, deck_size=20):
    kfont = font(SANS_B, 19)
    hfont = font(SERIF, head_size)
    dfont = font(SANS, deck_size)
    draw.line([(x, y), (x + w, y)], fill=RULE, width=2)
    draw.text((x, y + 10), kicker, font=kfont, fill=RED)
    cy = y + 38
    for line in wrap(draw, headline, hfont, w):
        draw.text((x, cy), line, font=hfont, fill=INK)
        cy += head_size + 4
    cy += 4
    for line in wrap(draw, deck, dfont, w):
        draw.text((x, cy), line, font=dfont, fill=INK)
        cy += deck_size + 5
    return cy


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Top dateline.
    centred(d, 26, "TUESDAY, 24 NOVEMBER 2026  |  WORLD NEWS IN ONE PAGE",
            font(SANS_B, 20))
    rule(d, 58, 2)

    # Masthead, sized to fit the page width.
    mast_size = 92
    while (d.textlength("THE WORLD TODAY", font=font(SERIF, mast_size))
           > W - 96 and mast_size > 40):
        mast_size -= 2
    centred(d, 72, "THE WORLD TODAY", font(SERIF, mast_size))
    centred(d, 178, "The day's world news, in one page.",
            font(SERIF_IT, 26), fill=GREY)
    rule(d, 222, 5)
    rule(d, 230, 2)

    # Lead story: Poland airspace.
    y = 248
    d.text((48, y), "POLAND  |  WAR IN UKRAINE", font=font(SANS_B, 20),
           fill=RED)
    y += 34
    for line in wrap(d, "Russian drone crosses into Poland; Warsaw scrambles jets",
                     font(SERIF, 48), W - 96):
        d.text((48, y), line, font=font(SERIF, 48), fill=INK)
        y += 54
    y += 6
    for line in wrap(d, "Polish air defence was activated overnight near Dorohusk, "
                     "in the Lublin region, during a Russian drone attack on "
                     "Ukraine, officials said on Tuesday.",
                     font(SANS, 22), W - 96):
        d.text((48, y), line, font=font(SANS, 22), fill=INK)
        y += 29

    rule(d, y + 14, 2)

    # Four stories, two columns. Row 2 starts below the taller row 1 cell.
    col_w = 440
    left_x, right_x = 48, 536
    top = y + 30
    end_left = story(d, left_x, top, col_w, "MARKETS  |  NVIDIA",
                     "Huang returns to Nvidia; shares jump a third",
                     "The board reinstated Jensen Huang on Monday, 11 days "
                     "after he resigned. The Nasdaq rallied 6%.",
                     head_size=30, deck_size=19)
    end_right = story(d, right_x, top, col_w, "BRUSSELS  |  SANCTIONS",
                      "EU proposes 22nd sanctions package on Russia",
                      "Brussels targets banks and crypto platforms, days "
                      "after COP31 ended with no deal.",
                      head_size=30, deck_size=19)
    row2 = max(end_left, end_right) + 12
    end_left = story(d, left_x, row2, col_w, "GAZA",
                     "Israeli strike kills UN aid worker in Gaza",
                     "At least three people were killed, the UN relief "
                     "agency said on Monday.",
                     head_size=30, deck_size=19)
    end_right = story(d, right_x, row2, col_w, "BANGLADESH",
                      "Ousted PM Hasina plans return on 16 December",
                      "Sheikh Hasina seeks to fly home from exile in India, "
                      "her spokesperson said on Tuesday.",
                      head_size=30, deck_size=19)

    also_y = max(end_left, end_right) + 12
    rule(d, also_y, 2)

    # Also today: three one-line items.
    d.text((48, also_y + 12), "ALSO TODAY", font=font(SANS_B, 19), fill=RED)
    items = [
        "Australia to fine tech firms up to 5% of global revenue under a new internet safety bill.",
        "Sport: CAS to rule on Tuesday on Senegal's appeal over its Africa Cup of Nations title.",
        "India: scores missing after a Himalayan flood kills four and sweeps down a mountain valley.",
    ]
    y = also_y + 40
    for item in items:
        d.text((48, y), "\u2022  " + item, font=font(SANS, 18), fill=INK)
        y += 22

    rule(d, 996, 1)
    centred(d, 1002, "Sources: Reuters and other wires, 24 November 2026.",
            font(SANS, 15), fill=GREY)

    img.save(OUT, "JPEG", quality=88, optimize=True, progressive=False)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()
