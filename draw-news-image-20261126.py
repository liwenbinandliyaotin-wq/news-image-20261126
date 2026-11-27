# Draws the 26 Nov 2026 news image: a 1024x1024 PNG newspaper front page.
# Six stories of Thursday 26 November 2026, each verified against Reuters,
# AP, Al Jazeera, Euronews or NDTV reporting dated 26 Nov 2026.
# Layout: masthead + dateline, then a 2x3 grid of story cards.
import os
from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
PAPER = (248, 246, 240)
INK = (18, 22, 30)
MASTHEAD_BG = (12, 28, 58)
ACCENT = (178, 34, 34)
MUTED = (96, 100, 110)
CARD = (255, 255, 255)
EDGE = (214, 216, 222)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def bold(size):
    return font("DejaVuSans-Bold.ttf", size)


def plain(size):
    return font("DejaVuSans.ttf", size)


def wrap(text, fnt, width):
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if fnt.getlength(trial) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


STORIES = [
    {
        "tag": "TRADE",
        "colour": (178, 34, 34),
        "title": "US proposes tariffs on 14 partners",
        "body": "Washington targets excess factory capacity in China, the EU, Japan and others.",
    },
    {
        "tag": "WAR",
        "colour": (178, 34, 34),
        "title": "Russian refinery ablaze after drone hit",
        "body": "Fire breaks out at the Slavyansk ECO plant in Krasnodar after a drone attack.",
    },
    {
        "tag": "MIDDLE EAST",
        "colour": (120, 40, 140),
        "title": "Israel kills Hamas official in Gaza",
        "body": "Strike kills a Hamas security official and his family, Gaza officials say.",
    },
    {
        "tag": "PACIFIC",
        "colour": (0, 110, 110),
        "title": "Solomons pick Australia as security partner",
        "body": "Treaty names Canberra the main partner and rules out foreign military bases.",
    },
    {
        "tag": "SPACE",
        "colour": (0, 110, 60),
        "title": "SpaceX cleared for a million satellites",
        "body": "Musk's firm gets the nod to launch satellites for orbital data centres.",
    },
    {
        "tag": "USA",
        "colour": (178, 34, 34),
        "title": "Thanksgiving parade postponed by storm",
        "body": "Macy's parade delayed by weather for the first time in 100 years.",
    },
]


def draw_card(d, x, y, w, h, story):
    d.rounded_rectangle([x, y, x + w, y + h], radius=16,
                        fill=CARD, outline=EDGE, width=2)
    d.ellipse([x + 22, y + 22, x + 36, y + 36], fill=story["colour"])
    d.text((x + 48, y + 16), story["tag"], font=bold(22), fill=story["colour"])
    inner = w - 44
    yy = y + 56
    for line in wrap(story["title"], bold(28), inner)[:2]:
        d.text((x + 22, yy), line, font=bold(28), fill=INK)
        yy += 37
    yy += 6
    for line in wrap(story["body"], plain(21), inner)[:3]:
        d.text((x + 22, yy), line, font=plain(21), fill=MUTED)
        yy += 29


canvas = Image.new("RGB", (SIZE, SIZE), PAPER)
d = ImageDraw.Draw(canvas)

# Masthead
d.rectangle([0, 0, SIZE, 186], fill=MASTHEAD_BG)
d.rectangle([0, 186, SIZE, 194], fill=ACCENT)
d.text((48, 30), "THE WORLD IN ONE DAY", font=bold(27), fill=(255, 255, 255))
d.text((48, 66), "Thursday, 26 November 2026", font=bold(48), fill=(255, 255, 255))
d.text((48, 134), "Six stories that defined the day — reported 26 Nov 2026",
       font=plain(24), fill=(198, 208, 226))

# Story grid: 2 columns x 3 rows
for i, story in enumerate(STORIES):
    x = 40 + (i % 2) * (462 + 20)
    y = 224 + (i // 2) * (228 + 20)
    draw_card(d, x, y, 462, 228, story)

d.text((48, 984), "Sources: Reuters · AP · Al Jazeera · Euronews · NDTV",
       font=plain(19), fill=MUTED)

out = os.path.expanduser(
    "~/workspace/make-fun/news-image-20261126-entry/entry.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
canvas.save(out, "PNG", optimize=True)
print(out, os.path.getsize(out), canvas.size)
