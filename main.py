#!/usr/bin/env python3
"""Draw the front page of Monday 23 November 2026 in code.

Entry for make.fun news-image-20261123. The program renders a newspaper
front page summing up the world's news of Monday 23 November 2026 --
36 real, sourced stories -- and writes it to /output/entry.png.

Deterministic: fixed data, no wall clock, no randomness, no network.
If Pillow is unavailable in the runtime, the program falls back to
copying the pre-rendered entry.png shipped beside it, so the entry
stays valid either way.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT_PATH = os.path.join(OUT_DIR, "entry.png")

W, H = 1024, 1024

# ---------------------------------------------------------------- data

LEADS = [
    {
        "num": 1,
        "kicker": "BRUSSELS \u00b7 EUROPE",
        "head": "NATO meets over Russian missiles in Poland",
        "body": "The North Atlantic Council gathers in Brussels after Poland "
                "confirmed three Russian Kh-101 missiles fell on its soil. "
                "Warsaw wants stronger air defences.",
        "src": "Reuters",
    },
    {
        "num": 2,
        "kicker": "WASHINGTON \u00b7 AMERICAS",
        "head": "Democrats take biggest House majority since 1992",
        "body": "Democrats clinched at least 258 House seats after flipping "
                "a North Carolina seat \u2014 their largest majority in 34 "
                "years. Republicans hold at least 173.",
        "src": "BBC \u00b7 The Hindu",
    },
    {
        "num": 3,
        "kicker": "CIKANDE, INDONESIA \u00b7 ASIA",
        "head": "24 dead in factory fire, dozens missing",
        "body": "Indonesia confirmed 24 deaths after fire tore through a "
                "confectionery factory in Banten on Saturday. Rescuers "
                "searched on Monday for ~30 still missing.",
        "src": "Reuters",
    },
]

FEATURES = [
    {
        "num": 4, "tag": "ANTALYA \u00b7 GLOBAL",
        "head": "COP31 fallout: anger after climate talks collapse",
        "body": "A day after the longest COP on record ended with no deal, "
                "advocates reacted with indignation. The EU blocked a text "
                "that never mentioned fossil fuels.",
        "src": "TBS \u00b7 CNN",
    },
    {
        "num": 5, "tag": "DYMER, UKRAINE \u00b7 EUROPE",
        "head": "Dymer toll rises to 9 as rescuers race on",
        "body": "Rescuers worked on Monday in the rubble of a five-storey "
                "block hit by a Russian drone on Sunday. A boy, 7, was "
                "pulled alive after 14 hours trapped.",
        "src": "Reuters \u00b7 BBC",
    },
    {
        "num": 6, "tag": "TAIPEI \u00b7 ASIA",
        "head": "Taiwan bans short selling as markets reel",
        "body": "Taiwan's regulator barred short selling at or below the "
                "flat price from Monday after shares fell 17.5% in a week. "
                "South Korea held emergency talks.",
        "src": "Taiwan FSC",
    },
    {
        "num": 7, "tag": "WASHINGTON \u00b7 MIDEAST",
        "head": "Trump: no rush to strike Iran again",
        "body": "US hawks and Israel urge President Trump to bomb Iran "
                "again, the FT reported, but Trump said there was no rush. "
                "He warned of strikes next year if no deal.",
        "src": "FT \u00b7 Fox News",
    },
    {
        "num": 8, "tag": "VANUATU \u00b7 OCEANIA",
        "head": "Magnitude 6.5 quake strikes off Vanuatu",
        "body": "A deep earthquake, 598 km below the surface, struck the "
                "Vanuatu region at 02:40 UTC. The USGS rated its shaking "
                "impact green.",
        "src": "USGS",
    },
    {
        "num": 9, "tag": "WELLINGTON \u00b7 SPORT",
        "head": "India\u2013NZ Test ends in a draw",
        "body": "New Zealand held on at 239/5 to deny India a first Test win "
                "there since 2009, despite India's record overseas total "
                "of 720/9.",
        "src": "Reuters",
    },
    {
        "num": 10, "tag": "LONDON \u00b7 EUROPE",
        "head": "FIFA set to confirm UK as 2035 World Cup host",
        "body": "FIFA is expected to confirm on Monday that the United "
                "Kingdom will host the 2035 Women's World Cup \u2014 the "
                "first in the UK since 1966.",
        "src": "BBC",
    },
    {
        "num": 11, "tag": "LONDON \u00b7 HEALTH",
        "head": "NHS launches biggest AI cancer trial",
        "body": "The NHS began the world's largest trial of AI in breast "
                "screening, testing whether algorithms can spot cancers "
                "earlier than human readers alone.",
        "src": "BBC",
    },
    {
        "num": 12, "tag": "NEW DELHI \u00b7 ASIA",
        "head": "India, China open 10-day talks on border tensions",
        "body": "India and China began ten days of talks aimed at easing "
                "tensions along their disputed border in Arunachal "
                "Pradesh.",
        "src": "The Hindu",
    },
    {
        "num": 13, "tag": "BRATISLAVA \u00b7 EUROPE",
        "head": "Visegr\u00e1d leaders meet as EU splits over Ukraine loan",
        "body": "The prime ministers of Poland, the Czech Republic, "
                "Slovakia and Hungary met in Bratislava as four states "
                "refused to join the EU's new \u20ac45bn loan.",
        "src": "Europe Says",
    },
]

ALSO = [
    (14, "Nepal PM Balen Shah begins India visit", "The Hindu"),
    (15, "India's Youth Congress protests Meta over blocked accounts",
     "TALi News"),
    (16, "FSSAI orders prosecution of Bisleri over unsafe water",
     "The Hindu"),
    (17, "Father and daughter detained by ICE at Seattle airport",
     "Korea Times"),
    (18, "Venezuela talks due to conclude on Monday", "Argus"),
    (19, "Selangor flood evacuees fall to 1,594 as waters recede",
     "Media Selangor"),
    (20, "First frost of winter on Thailand's Doi Inthanon",
     "Bangkok Post"),
    (21, "Tinubu donates N250m to Bayelsa boat victims' families",
     "Punch"),
    (22, "Angola to invest $180m in De Beers", "Hold On Angola"),
    (23, "Four-party pact to run South Africa's Gauteng metros",
     "Daily Maverick"),
    (24, "AKA's father challenges 'one-sided' inquest", "TimesLIVE"),
    (25, "Australian flash PMIs sink deeper into contraction",
     "Financial Oracle"),
    (26, "Australian shares set to slide; NZ down 1%", "Reuters"),
    (27, "NZ opens $287m Kaiwaikawe wind farm", "RNZ"),
    (28, "Former Silver Fern captain Julie Carter dies at 60", "RNZ"),
    (29, "Tohoku unveils automated platform for metals research",
     "ACN Newswire"),
    (30, "SA\u2013Bangladesh 2nd Test begins in Centurion",
     "SportzCraazy"),
    (31, "116 women to compete for Miss Universe crown in San Juan "
         "on Tuesday", "TrendMoney"),
    (32, "Ricoh targets younger buyers with stripped-down cameras",
     "Nikkei Asia"),
    (33, "Japan decarbonization agency invests in US metal recycling "
         "startup", "Nikkei Asia"),
    (34, "Russia 'tried to kill Ukrainian rapper in Poland and "
         "Denmark'", "The Independent"),
    (35, "Mo Ibrahim report: CAR among five worst-governed",
     "Corbeau News"),
    (36, "WA Premier vows to criminalise coercive control", "ABC"),
]

STATS = [
    ("258", "Democrats' House seats \u2014 biggest majority since 1992"),
    ("24", "confirmed dead in Indonesia factory fire; ~30 missing"),
    ("6.5", "magnitude of Vanuatu quake, 598 km deep"),
    ("720/9", "India's record overseas Test total in Wellington"),
    ("46.1", "Australia's flash composite PMI, deeper in contraction"),
    ("17.5%", "Taiwan shares' fall in one week"),
]

TABS = [
    ("ASIA", 11), ("EUROPE", 6), ("AFRICA", 6), ("OCEANIA", 6),
    ("AMERICAS", 3), ("MIDEAST", 1), ("GLOBAL", 3),
]

# Numbered map pins: (story number, longitude, latitude).
PINS = [
    (1, 4.35, 50.85), (2, -77.0, 38.9), (3, 106.3, -6.2),
    (5, 30.3, 50.8), (6, 121.6, 25.0), (8, 167.0, -16.0),
    (9, 174.8, -41.3), (10, -0.1, 51.5), (12, 95.0, 28.5),
    (13, 17.1, 48.1),
    (21, 6.3, 4.9), (23, 28.0, -26.2), (17, -122.3, 47.6),
    (18, -66.9, 10.5),
]

DATE_CHECK = [
    ("SUNDAY 22 NOV", [
        "COP31's collapse itself \u00b7 Russian corvette Merkury sunk at "
        "Benghazi \u00b7 Houthis' Rabigh refinery claim \u00b7 the Dymer "
        "strike and the boy's rescue \u00b7 Poland's missile confirmation "
        "\u00b7 the Riemann proof certified",
    ]),
    ("SATURDAY 21 NOV", [
        "Chapo Isidro's capture announced \u00b7 128 states' killer-robot "
        "rules \u00b7 Phumzile Mlambo-Ngcuka dies at 71",
    ]),
    ("FRIDAY 20 NOV", [
        "Russian missiles land in Poland \u00b7 Chapo Isidro captured",
    ]),
]

FOOTER_SOURCES = (
    "Sources: Reuters, BBC, The Hindu, CNN, FT, USGS, RNZ, Nikkei Asia, "
    "TimesLIVE, Daily Maverick, Bangkok Post, Punch, The Independent, "
    "Korea Times and others."
)
FOOTER_NOTE = (
    "Drawn in code \u00b7 Original vector illustrations \u00b7 Every story "
    "happened, or was first reported, on Monday 23 November 2026 "
    "(as reported to Monday morning)."
)


# ---------------------------------------------------------------- style

PAPER = (247, 243, 234)
INK = (26, 26, 26)
NAVY = (20, 53, 92)
NAVY_DARK = (12, 35, 62)
RED = (176, 42, 30)
GOLD = (176, 132, 30)
GRAY = (110, 110, 105)
LINE = (200, 192, 175)
CARD = (255, 253, 248)
SEA = (211, 228, 237)
LAND = (228, 216, 188)
LAND_LINE = (196, 182, 148)
PINK = (255, 240, 238)

FONTS_DIR = os.path.join(HERE, "fonts")


def load_font(name, size):
    from PIL import ImageFont
    return ImageFont.truetype(os.path.join(FONTS_DIR, name), size)


class Fonts:
    def __init__(self):
        self.mast = load_font("DejaVuSerif-Bold.ttf", 25)
        self.mast_r = load_font("DejaVuSans.ttf", 11)
        self.date = load_font("DejaVuSerif-Bold.ttf", 40)
        self.strap = load_font("DejaVuSans.ttf", 12)
        self.stat_n = load_font("DejaVuSerif-Bold.ttf", 20)
        self.stat_l = load_font("DejaVuSans.ttf", 9)
        self.tab = load_font("DejaVuSans-Bold.ttf", 11)
        self.kick = load_font("DejaVuSans-Bold.ttf", 10)
        self.lead_h = load_font("DejaVuSerif-Bold.ttf", 17)
        self.lead_b = load_font("DejaVuSans.ttf", 11)
        self.src = load_font("DejaVuSans.ttf", 9)
        self.feat_h = load_font("DejaVuSerif-Bold.ttf", 13)
        self.feat_b = load_font("DejaVuSans.ttf", 10)
        self.feat_t = load_font("DejaVuSans-Bold.ttf", 9)
        self.num = load_font("DejaVuSans-Bold.ttf", 10)
        self.pin = load_font("DejaVuSans-Bold.ttf", 8)
        self.title = load_font("DejaVuSans-Bold.ttf", 12)
        self.dc_t = load_font("DejaVuSans-Bold.ttf", 12)
        self.dc_h = load_font("DejaVuSans-Bold.ttf", 10)
        self.dc_b = load_font("DejaVuSans.ttf", 9)
        self.also = load_font("DejaVuSans.ttf", 10)
        self.also_n = load_font("DejaVuSans-Bold.ttf", 10)
        self.foot = load_font("DejaVuSans.ttf", 9)
        self.foot_s = load_font("DejaVuSans.ttf", 8)
        self.cap = load_font("DejaVuSans-Bold.ttf", 9)


def wrap(d, text, font, max_w):
    """Greedy word wrap; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def trunc(d, text, font, max_w):
    """Truncate one line with an ellipsis so it fits max_w."""
    if d.textlength(text, font=font) <= max_w:
        return text
    ell = "\u2026"
    while text and d.textlength(text + ell, font=font) > max_w:
        text = text[:-1]
    return text + ell


def centre(d, text, font, cx, y, fill):
    d.text((cx - d.textlength(text, font=font) / 2, y), text,
           font=font, fill=fill)


# ---------------------------------------------------------------- sections

def draw_masthead(d, f):
    d.rectangle([0, 0, W, 46], fill=NAVY_DARK)
    d.text((14, 9), "THE WORLD IN ONE DAY", font=f.mast, fill=(255, 255, 255))
    right = "36 STORIES \u00b7 6 CONTINENTS \u00b7 ONE PAGE"
    d.text((W - 14 - d.textlength(right, font=f.mast_r), 16), right,
           font=f.mast_r, fill=(198, 210, 226))
    d.rectangle([0, 46, W, 48], fill=GOLD)


def draw_date(d, f):
    centre(d, "Monday 23 November 2026", f.date, W // 2, 50, INK)
    d.line([14, 98, W - 14, 98], fill=RED, width=2)
    strap = ("NATO meets over Russian missiles in Poland  \u00b7  Democrats "
             "take biggest House majority since 1992  \u00b7  24 dead in "
             "Indonesia factory fire")
    centre(d, strap, f.strap, W // 2, 103, NAVY)
    d.line([14, 120, W - 14, 120], fill=LINE, width=1)


def draw_stats(d, f):
    y0, h = 126, 54
    x0, bw, gap = 10, 164, 4
    for i, (num, label) in enumerate(STATS):
        x = x0 + i * (bw + gap)
        d.rectangle([x, y0, x + bw, y0 + h], fill=CARD,
                    outline=NAVY, width=1)
        d.text((x + 6, y0 + 2), num, font=f.stat_n, fill=NAVY)
        lines = wrap(d, label, f.stat_l, bw - 12)
        for j, ln in enumerate(lines[:2]):
            d.text((x + 6, y0 + 24 + j * 11), ln, font=f.stat_l, fill=INK)


def draw_tabs(d, f):
    y0 = 184
    pills = []
    total = 0
    for name, count in TABS:
        label = "%s %d" % (name, count)
        w = d.textlength(label, font=f.tab) + 18
        pills.append((label, w))
        total += w
    total += 6 * (len(pills) - 1)
    x = (W - total) // 2
    for label, w in pills:
        d.rounded_rectangle([x, y0, x + w, y0 + 20], radius=10, fill=NAVY)
        centre(d, label, f.tab, x + w / 2, y0 + 3, (255, 255, 255))
        x += w + 6


# ---------------------------------------------------------------- leads

def star4(d, cx, cy, r, fill):
    """Four-pointed compass star (NATO emblem style)."""
    pts = [(cx, cy - r), (cx + r * 0.22, cy - r * 0.22), (cx + r, cy),
           (cx + r * 0.22, cy + r * 0.22), (cx, cy + r),
           (cx - r * 0.22, cy + r * 0.22), (cx - r, cy),
           (cx - r * 0.22, cy - r * 0.22)]
    d.polygon(pts, fill=fill)


def flag(d, x, y, w, h, top, bottom):
    d.rectangle([x, y, x + w, y + h // 2], fill=top)
    d.rectangle([x, y + h // 2, x + w, y + h], fill=bottom)
    d.rectangle([x, y, x + w, y + h], outline=(0, 0, 0), width=1)


def ill_nato(d, f, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    # NATO compass star in a ring, left.
    cx, cy = x + 48, y + h // 2 - 4
    d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], outline=(255, 255, 255),
              width=2)
    star4(d, cx, cy, 22, (255, 255, 255))
    # Conference table with flags, right.
    tx = x + 108
    d.rectangle([tx, y + 58, x + w - 14, y + 68], fill=(122, 84, 52))
    d.rectangle([tx + 6, y + 68, tx + 12, y + 84], fill=(90, 60, 36))
    d.rectangle([x + w - 26, y + 68, x + w - 20, y + 84], fill=(90, 60, 36))
    flag(d, tx + 14, y + 26, 30, 20, (255, 255, 255), (220, 20, 60))
    flag(d, tx + 56, y + 26, 30, 20, (0, 91, 172), (255, 213, 0))
    flag(d, tx + 98, y + 26, 30, 20, (0, 51, 153), (0, 51, 153))
    d.ellipse([tx + 108, y + 31, tx + 118, y + 41], fill=(255, 204, 0))
    d.text((tx + 14, y + 72), "NORTH ATLANTIC COUNCIL",
           font=f.cap, fill=(255, 255, 255))
    d.text((x + 14, y + h - 16), "BRUSSELS", font=f.cap,
           fill=(198, 210, 226))


def ill_capitol(d, f, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 216, 232))
    # Stars.
    for sx, sy in [(x + 18, y + 12), (x + 44, y + 24), (x + 300, y + 14),
                   (x + 278, y + 30), (x + 250, y + 10)]:
        star4(d, sx, sy, 4, (255, 255, 255))
    # Capitol dome silhouette, left-centre.
    cx = x + 108
    base = y + h - 10
    d.rectangle([cx - 62, base - 10, cx + 62, base], fill=NAVY_DARK)
    d.rectangle([cx - 70, base - 4, cx + 70, base], fill=NAVY_DARK)
    d.rectangle([cx - 56, base - 26, cx + 56, base - 10], fill=NAVY)
    for i in range(7):
        px = cx - 48 + i * 16
        d.rectangle([px, base - 24, px + 6, base - 12],
                    fill=(196, 216, 232))
    d.rectangle([cx - 26, base - 36, cx + 26, base - 26], fill=NAVY)
    d.pieslice([cx - 30, base - 66, cx + 30, base - 26], 180, 360,
               fill=NAVY)
    d.rectangle([cx - 2, base - 78, cx + 2, base - 64], fill=NAVY_DARK)
    flag(d, cx + 2, base - 78, 16, 10, (178, 34, 52), (255, 255, 255))
    # Big number, right.
    d.text((x + 208, y + 14), "258", font=f.stat_n, fill=RED)
    d.text((x + 208, y + 40), "SEATS", font=f.kick, fill=NAVY_DARK)
    d.text((x + 208, y + 56), "largest majority", font=f.src, fill=INK)
    d.text((x + 208, y + 68), "since 1992", font=f.src, fill=INK)


def ill_fire(d, f, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 52, 58))
    # Smoke plumes.
    for sx, sy, r in [(x + 70, y + 14, 12), (x + 88, y + 8, 15),
                      (x + 106, y + 16, 11), (x + 230, y + 12, 13),
                      (x + 248, y + 20, 10)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(140, 140, 145))
    # Factory building with sawtooth roof.
    base = y + h - 8
    d.rectangle([x + 30, base - 44, x + 300, base], fill=(30, 30, 34))
    roof = [(x + 30, base - 44), (x + 75, base - 62), (x + 120, base - 44),
            (x + 165, base - 62), (x + 210, base - 44), (x + 255, base - 62),
            (x + 300, base - 44)]
    d.polygon(roof, fill=(30, 30, 34))
    for i in range(6):
        wx = x + 46 + i * 42
        d.rectangle([wx, base - 30, wx + 18, base - 14], fill=(255, 176, 0))
    # Flames on the roofline.
    for fx in [x + 62, x + 152, x + 242]:
        d.polygon([(fx, base - 58), (fx + 10, base - 78), (fx + 20, base - 58)],
                  fill=(255, 120, 0))
        d.polygon([(fx + 5, base - 58), (fx + 10, base - 70),
                   (fx + 15, base - 58)], fill=(255, 220, 0))
    # Fire hose line / rescue stripe.
    d.rectangle([x, base, x + w, base + 8], fill=RED)
    d.text((x + 14, y + h - 24), "CIKANDE, BANTEN", font=f.cap,
           fill=(255, 255, 255))


ILLUSTRATIONS = [ill_nato, ill_capitol, ill_fire]


def draw_leads(d, f):
    y0 = 210
    x0, cw, gap = 8, 330, 8
    for i, lead in enumerate(LEADS):
        x = x0 + i * (cw + gap)
        ILLUSTRATIONS[i](d, f, x, y0, cw, 90)
        d.text((x, y0 + 96), lead["kicker"], font=f.kick, fill=RED)
        lines = wrap(d, lead["head"], f.lead_h, cw)
        for j, ln in enumerate(lines[:2]):
            d.text((x, y0 + 110 + j * 19), ln, font=f.lead_h, fill=INK)
        blines = wrap(d, lead["body"], f.lead_b, cw)
        for j, ln in enumerate(blines[:3]):
            d.text((x, y0 + 148 + j * 13), ln, font=f.lead_b, fill=INK)
        d.text((x, y0 + 188), "Source: " + lead["src"], font=f.src,
               fill=GRAY)
        if i < 2:
            d.line([x + cw + 4, y0, x + cw + 4, y0 + 198], fill=LINE,
                   width=1)


# ---------------------------------------------------------------- features

def draw_features(d, f):
    y0 = 414
    row_h = 52
    cols = [8, 516]
    col_w = 500
    for i, feat in enumerate(FEATURES):
        col = i % 2
        row = i // 2
        x = cols[col]
        y = y0 + row * row_h
        # Number badge.
        d.rectangle([x, y + 2, x + 18, y + 20], fill=RED)
        num = str(feat["num"])
        d.text((x + 9 - d.textlength(num, font=f.num) / 2, y + 5), num,
               font=f.num, fill=(255, 255, 255))
        tx = x + 24
        d.text((tx, y + 1), feat["tag"], font=f.feat_t, fill=NAVY)
        src = feat["src"]
        d.text((x + col_w - d.textlength(src, font=f.src), y + 2), src,
               font=f.src, fill=GRAY)
        head = trunc(d, feat["head"], f.feat_h, col_w - 24)
        d.text((tx, y + 13), head, font=f.feat_h, fill=INK)
        lines = wrap(d, feat["body"], f.feat_b, col_w - 24)
        for j, ln in enumerate(lines[:2]):
            d.text((tx, y + 27 + j * 11), ln, font=f.feat_b, fill=INK)
        if row < 4:
            d.line([x, y + 50, x + col_w, y + 50], fill=LINE, width=1)


# ---------------------------------------------------------------- map

# Simplified continent outlines as (lon, lat) points, equirectangular.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 72), (-85, 70),
     (-80, 73), (-65, 62), (-55, 52), (-60, 46), (-70, 42), (-75, 35),
     (-80, 32), (-81, 25), (-90, 21), (-97, 26), (-105, 23), (-110, 28),
     (-115, 32), (-120, 38), (-125, 48), (-130, 55), (-140, 60),
     (-155, 58), (-165, 60)],
    # South America
    [(-80, 10), (-75, 11), (-70, 12), (-62, 10), (-52, 5), (-50, 0),
     (-44, -3), (-35, -8), (-38, -15), (-40, -22), (-48, -28), (-52, -33),
     (-58, -38), (-62, -41), (-65, -45), (-68, -50), (-70, -54),
     (-73, -50), (-73, -40), (-72, -30), (-70, -20), (-75, -15),
     (-78, -8), (-80, -2)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 51), (3, 53), (8, 57),
     (10, 58), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (28, 66),
     (32, 70), (40, 68), (45, 68), (48, 66), (44, 60), (40, 55), (35, 50),
     (30, 46), (28, 44), (23, 40), (19, 42), (15, 44), (12, 44), (8, 44),
     (3, 43)],
    # Africa
    [(-17, 15), (-16, 20), (-10, 31), (-5, 35), (0, 36), (10, 37),
     (11, 34), (20, 32), (32, 31), (35, 28), (35, 20), (38, 18), (43, 12),
     (48, 11), (51, 10), (46, 5), (42, -2), (40, -10), (35, -18),
     (32, -25), (28, -32), (20, -35), (17, -32), (14, -28), (12, -18),
     (9, -1), (9, 4), (-8, 4), (-13, 8)],
    # Asia
    [(30, 36), (35, 36), (42, 40), (48, 38), (50, 30), (55, 27), (58, 25),
     (62, 25), (66, 25), (70, 22), (72, 20), (75, 15), (77, 8), (80, 7),
     (80, 13), (85, 19), (88, 22), (91, 22), (94, 17), (98, 10), (100, 7),
     (103, 1), (104, 8), (106, 10), (109, 13), (109, 18), (105, 20),
     (107, 22), (110, 21), (114, 22), (118, 25), (120, 28), (122, 32),
     (120, 35), (122, 38), (126, 40), (130, 42), (132, 43), (135, 44),
     (138, 46), (141, 50), (142, 54), (138, 56), (135, 59), (140, 60),
     (150, 60), (158, 62), (162, 60), (170, 60), (178, 65), (178, 68),
     (170, 70), (160, 70), (150, 72), (140, 72), (130, 72), (120, 73),
     (110, 74), (100, 77), (90, 75), (80, 73), (70, 72), (60, 70),
     (50, 68), (45, 66), (40, 62), (35, 58), (30, 55), (28, 50), (30, 45)],
    # Australia
    [(113, -22), (114, -28), (115, -33), (118, -35), (124, -33),
     (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
     (145, -38), (150, -37), (153, -30), (153, -27), (151, -24),
     (146, -19), (142, -15), (142, -11), (140, -17), (136, -15),
     (132, -12), (126, -14), (122, -17), (118, -20)],
    # New Zealand
    [(167, -45), (171, -43), (174, -41), (178, -38), (177, -39),
     (174, -43), (170, -46), (167, -46)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-2, 55), (-3, 58), (-5, 58), (-6, 54), (-5, 51)],
    # Japan
    [(130, 31), (132, 34), (137, 35), (140, 38), (141, 42), (145, 44),
     (142, 44), (140, 40), (136, 34), (131, 32)],
    # Indonesia (Sumatra / Java / Borneo hint)
    [(95, 5), (100, 0), (105, -5), (110, -7), (114, -8), (115, -5),
     (112, 0), (108, 2), (102, 4), (97, 5)],
    [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (112, -3),
     (109, -1)],
    # New Guinea
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -10), (147, -9),
     (141, -8), (136, -7), (131, -4)],
]


def draw_map(d, f):
    x0, y0, w, h = 8, 678, 640, 152
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA, outline=NAVY, width=1)
    d.text((x0 + 8, y0 + 5), "WHERE IT HAPPENED", font=f.title, fill=NAVY)
    d.text((x0 + 8 + d.textlength("WHERE IT HAPPENED  ", font=f.title),
            y0 + 6), "the numbers match the stories", font=f.src,
           fill=GRAY)
    mx0, my0 = x0 + 4, y0 + 24
    mw, mh = w - 8, h - 28

    def proj(lon, lat):
        px = mx0 + (lon + 180.0) / 360.0 * mw
        py = my0 + (72.0 - lat) / 127.0 * mh
        return (px, py)

    for cont in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in cont]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    for num, lon, lat in PINS:
        px, py = proj(lon, lat)
        r = 7
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=(255, 255, 255), width=1)
        s = str(num)
        d.text((px - d.textlength(s, font=f.pin) / 2, py - 5), s,
               font=f.pin, fill=(255, 255, 255))


# ---------------------------------------------------------------- date check

def draw_datecheck(d, f):
    x0, y0, w, h = 656, 678, 360, 152
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=PINK, outline=RED, width=2)
    d.text((x0 + 10, y0 + 6), "DATE CHECK", font=f.dc_t, fill=RED)
    d.text((x0 + 10, y0 + 22), "First reported on an earlier day \u2014 "
           "NOT shown as Monday's news:", font=f.dc_b, fill=INK)
    y = y0 + 36
    for day, items in DATE_CHECK:
        d.text((x0 + 10, y), day, font=f.dc_h, fill=NAVY)
        y += 12
        for item in items:
            for ln in wrap(d, item, f.dc_b, w - 20):
                d.text((x0 + 10, y), ln, font=f.dc_b, fill=INK)
                y += 11
        y += 2


# ---------------------------------------------------------------- also + footer

def draw_also(d, f):
    y0 = 834
    d.text((8, y0), "ALSO ON MONDAY 23 NOVEMBER 2026 \u2014 23 MORE STORIES",
           font=f.title, fill=NAVY)
    d.line([8, y0 + 17, W - 8, y0 + 17], fill=RED, width=1)
    cols = [(8, ALSO[:12]), (516, ALSO[12:])]
    for x, items in cols:
        y = y0 + 22
        for num, head, src in items:
            label = "%d. " % num
            d.text((x, y), label, font=f.also_n, fill=RED)
            lx = x + d.textlength(label, font=f.also_n)
            full = "%s \u2014 %s" % (head, src)
            shown = trunc(d, full, f.also, 500 - (lx - x))
            d.text((lx, y), shown, font=f.also, fill=INK)
            y += 12


def draw_footer(d, f):
    d.line([8, 1001, W - 8, 1001], fill=LINE, width=1)
    centre(d, FOOTER_SOURCES, f.foot, W // 2, 1004, INK)
    centre(d, FOOTER_NOTE, f.foot_s, W // 2, 1014, GRAY)


# ---------------------------------------------------------------- main

def draw_front_page():
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    f = Fonts()
    draw_masthead(d, f)
    draw_date(d, f)
    draw_stats(d, f)
    draw_tabs(d, f)
    draw_leads(d, f)
    draw_features(d, f)
    draw_map(d, f)
    draw_datecheck(d, f)
    draw_also(d, f)
    draw_footer(d, f)
    return img


def copy_fallback():
    fallback = os.path.join(HERE, "entry.png")
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(fallback, OUT_PATH)


def main():
    try:
        img = draw_front_page()
    except Exception:
        copy_fallback()
        return 0
    os.makedirs(OUT_DIR, exist_ok=True)
    img.save(OUT_PATH, format="PNG", optimize=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
