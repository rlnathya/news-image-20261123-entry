#!/usr/bin/env python3
"""Draw the front page of THE WORLD for Monday 23 November 2026.

A single 1024x1024 newspaper front page: masthead with the date,
one lead story on the Iran war, five more stories in a grid, and a
wire ticker at the foot. Everything is drawn with Pillow from the
vendored DejaVu fonts, so the output is byte-identical on every run.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
EDGE = 38
PAPER = (248, 245, 238)
INK = (18, 18, 18)
RED = (168, 35, 26)
GREY = (98, 96, 90)
RULE = (18, 18, 18)
TICKER_BG = (18, 18, 18)
TICKER_FG = (244, 242, 236)

_HERE = os.path.dirname(os.path.abspath(__file__))
_ASSETS = os.path.join(_HERE, "assets")


def _font(name, size):
    path = os.path.join(_ASSETS, name)
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def _serif_bold(size):
    return _font("DejaVuSerif-Bold.ttf", size)


def _serif(size):
    return _font("DejaVuSerif.ttf", size)


def _serif_italic(size):
    path = os.path.join(_ASSETS, "DejaVuSerif-Italic.ttf")
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return _font("DejaVuSerif.ttf", size)


def _sans(size):
    return _font("DejaVuSans.ttf", size)


def _sans_bold(size):
    return _font("DejaVuSans-Bold.ttf", size)


def _wrap(draw, text, font, width):
    """Split text into lines that fit inside width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _rule(draw, x0, x1, y, width=2):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=width)


def _kicker(draw, x, y, text):
    font = _sans_bold(17)
    draw.text((x, y), text, font=font, fill=RED)
    return y + 22


def _headline(draw, x, y, width, text, size=28):
    font = _serif_bold(size)
    lines = _wrap(draw, text, font, width)
    for line in lines:
        draw.text((x, y), line, font=font, fill=INK)
        y += size + 5
    return y + 4


def _deck(draw, x, y, width, text, size=19, leading=23):
    font = _sans(size)
    for line in _wrap(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=INK)
        y += leading
    return y


def _story(draw, x, y, width, kicker, headline, deck, head_size=28):
    y = _kicker(draw, x, y, kicker)
    y = _headline(draw, x, y, width, headline, size=head_size)
    y = _deck(draw, x, y, width, deck)
    return y


def _masthead(draw):
    width = PAGE - 2 * EDGE
    y = 28
    _rule(draw, EDGE, PAGE - EDGE, y, width=3)
    y += 10
    font = _serif_bold(86)
    title = "THE WORLD"
    tw = draw.textlength(title, font=font)
    draw.text(((PAGE - tw) / 2, y), title, font=font, fill=INK)
    y += 96
    _rule(draw, EDGE, PAGE - EDGE, y, width=2)
    y += 8
    small = _sans_bold(18)
    draw.text((EDGE, y), "MONDAY, 23 NOVEMBER 2026", font=small, fill=INK)
    right = "SIX STORIES  •  ONE DAY"
    rw = draw.textlength(right, font=small)
    draw.text((PAGE - EDGE - rw, y), right, font=small, fill=GREY)
    y += 28
    _rule(draw, EDGE, PAGE - EDGE, y, width=3)
    return y + 12


def _lead(draw, y):
    width = PAGE - 2 * EDGE
    y = _kicker(draw, EDGE, y, "IRAN WAR WIDENS")
    y = _headline(
        draw, EDGE, y, width, "Tankers attacked in the Strait of Hormuz", size=40
    )
    y = _deck(
        draw,
        EDGE,
        y,
        width,
        "At least three oil tankers were hit as Iran widened its war, "
        "striking US positions and a civilian site in Bahrain, wounding "
        "two people.",
        size=21,
        leading=27,
    )
    y += 6
    quote = "\u201cWe want a real deal, not a fake deal.\u201d \u2014 President Trump on Iran"
    font = _serif_italic(20)
    draw.text((EDGE, y), quote, font=font, fill=RED)
    y += 26
    stats = "3 TANKERS ATTACKED   •   2 WOUNDED IN BAHRAIN   •   US BASES TARGETED"
    sfont = _sans_bold(17)
    draw.text((EDGE, y), stats, font=sfont, fill=INK)
    return y + 28


def _pair_row(draw, y, left, right):
    width = PAGE - 2 * EDGE
    gutter = 28
    col = (width - gutter) // 2
    left_end = _story(draw, EDGE, y, col, *left)
    right_end = _story(draw, EDGE + col + gutter, y, col, *right)
    return max(left_end, right_end) + 8


def _wide_story(draw, y, kicker, headline, deck):
    width = PAGE - 2 * EDGE
    y = _kicker(draw, EDGE, y, kicker)
    y = _headline(draw, EDGE, y, width, headline, size=28)
    y = _deck(draw, EDGE, y, width, deck, size=17, leading=23)
    return y


def _ticker(draw):
    bar_top = PAGE - 64
    draw.rectangle(
        [(EDGE, bar_top), (PAGE - EDGE, bar_top + 40)], fill=TICKER_BG
    )
    font = _sans_bold(15)
    text = (
        "THE WIRE — Belgium strike halts transport  •  "
        "Korea minister quits in AI scandal  •  "
        "Indonesia fire search"
    )
    draw.text((EDGE + 14, bar_top + 12), text, font=font, fill=TICKER_FG)


def build_frontpage(target):
    """Render the front page and write it to target as PNG."""
    page = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(page)

    y = _masthead(draw)
    y = _lead(draw, y)
    _rule(draw, EDGE, PAGE - EDGE, y, width=2)
    y += 10

    y = _pair_row(
        draw,
        y,
        (
            "UKRAINE WAR",
            "Ukraine sinks Russian warship off Libya",
            "Seven sea drones sank the corvette Mercury in Benghazi, "
            "Zelenskyy says, as Ukraine also hit a Russian cargo ship "
            "in the Baltic.",
        ),
        (
            "MARKETS",
            "Markets rebound after AI rout",
            "US stocks bounce as S&P futures climb 2.4% and the Nasdaq "
            "3%. Anthropic rises, CrowdStrike buys Zscaler for $43.9bn, "
            "Nvidia jumps 7% and bitcoin tops $60,000.",
        ),
    )
    _rule(draw, EDGE, PAGE - EDGE, y, width=1)
    y += 8

    y = _pair_row(
        draw,
        y,
        (
            "CLIMATE",
            "COP31 collapses without a deal",
            "The longest climate talks in history end in Antalya with no "
            "agreement \u2014 the first full collapse since Copenhagen in "
            "2009, split over fossil fuels.",
        ),
        (
            "WASHINGTON",
            "Democrats\u2019 biggest House win since 1992",
            "Democrats take at least 258 seats, their largest House "
            "majority in 34 years, as Trump moves to curb congressional "
            "oversight.",
        ),
    )
    _rule(draw, EDGE, PAGE - EDGE, y, width=1)
    y += 8

    y = _wide_story(
        draw,
        y,
        "EUROPE",
        "Russia \u2018plotted to kill rapper\u2019",
        "Denmark says Russian intelligence planned to kill a "
        "Ukrainian-American rapper at a Copenhagen concert.",
    )
    _ticker(draw)

    page.save(target, format="PNG")
    return target


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build_frontpage(out)
    print("wrote", out)
