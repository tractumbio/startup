#!/usr/bin/env python3
"""Regenerate assets/og.jpg (1200x630 social share card). Run after changing the landing headline.
Usage: python3 tools/make_og.py   (needs Pillow and DejaVu fonts)"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
HEADLINE = "I help biotechs decide whether a drug belongs in the eye, and help CROs build the services to test it."
SUBS = ["Opportunity assessment for biotechs", "Capability builds for CROs"]
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans{}.ttf"
NAVY, MUTED, BLUE, GROUND = (24, 53, 83), (94, 108, 118), (36, 99, 167), (249, 251, 248)

W, H = 1200, 630
im = Image.new("RGB", (W, H), GROUND)
d = ImageDraw.Draw(im)
d.rectangle([0, 0, 14, H], fill=BLUE)
bold, reg = (lambda s: ImageFont.truetype(FONT.format("-Bold"), s)), (lambda s: ImageFont.truetype(FONT.format(""), s))

x = 72
d.text((x, 66), "tractum", font=bold(38), fill=NAVY)
d.text((x + d.textlength("tractum", font=bold(38)), 66), "bio", font=reg(38), fill=MUTED)

# wrap the headline to the left column so it never runs under the photo
f, maxw, lines, cur = bold(42), 610, [], ""
for word in HEADLINE.split():
    trial = (cur + " " + word).strip()
    if d.textlength(trial, font=f) <= maxw: cur = trial
    else: lines.append(cur); cur = word
lines.append(cur)
y = 160
for ln in lines:
    d.text((x, y), ln, font=f, fill=NAVY); y += 56
y += 26
for s in SUBS:
    d.text((x, y), s, font=reg(24), fill=MUTED); y += 34
d.text((x, 560), "tractumbio.com", font=reg(22), fill=BLUE)

photo = Image.open(ROOT / "assets/adrian-og.jpg").convert("RGB").resize((320, 320), Image.LANCZOS)
mask = Image.new("L", (320 * 4, 320 * 4), 0)
ImageDraw.Draw(mask).ellipse([0, 0, 320 * 4 - 1, 320 * 4 - 1], fill=255)
im.paste(photo, (830, 155), mask.resize((320, 320), Image.LANCZOS))
assert max(d.textlength(l, font=f) for l in lines) <= maxw and y < 550, "headline too long for the card"
im.save(ROOT / "assets/og.jpg", quality=88)
print("wrote assets/og.jpg,", len(lines), "headline lines")
