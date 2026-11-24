#!/usr/bin/env python3
"""THE MERIDIAN LINE - Tuesday 24 November 2026 in one image.
Build-time renderer for Final 4 (@wildonaped), NI24 wave 1.
Draws a square broadsheet page at W=3900, then fits it onto a 1024x1024
canvas and quantises to 256 colours. Run: python3 compose.py A|B
Writes entry-A.png / entry-B.png next to this file (never into /output).
The graded entrypoint is main.py, which only copies entry.png.
All facts come from the locked NI24 pool (ni24-pool.md + 07:00 refresh);
no numbers are invented. Rendered with Pillow at build time only.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts"
DEJAVU = "/usr/share/fonts/truetype/dejavu"

CREAM = (247, 241, 227)
PAPER = (250, 246, 236)
INK = (27, 42, 94)          # indigo
INK2 = (43, 63, 140)
RED = (179, 38, 30)
GOLD = (201, 162, 39)
GOLD_LT = (232, 203, 110)
TEAL = (18, 110, 105)
SKY = (168, 196, 224)
SKY_DK = (110, 150, 200)
SEA = (28, 84, 138)
SAND = (226, 205, 160)
GREEN = (46, 125, 70)
CHAR = (52, 52, 52)
GREY = (110, 108, 100)
WHITE = (255, 255, 255)
BAND = (232, 226, 208)

W = 3900
H = 3900
PAGE_IMG = None


def font(name, size):
    for path in (os.path.join(FONT_DIR, name),
                 os.path.join(DEJAVU, name)):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.truetype(os.path.join(DEJAVU, "DejaVuSans-Bold.ttf"), size)


F_BLACK = lambda s: font("PlayfairDisplay-Black.ttf", s)
F_BOLD = lambda s: font("PlayfairDisplay-Bold.ttf", s)
F_ITAL = lambda s: font("PlayfairDisplay-Italic.ttf", s)
F_ARCH = lambda s: font("Archivo-Bold.ttf", s)
F_ARC = lambda s: font("Archivo.ttf", s)
F_SANS = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANSR = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_c(d, x, y, s, fnt, fill, anchor="ma"):
    d.text((x, y), s, font=fnt, fill=fill, anchor=anchor)


def text_l(d, x, y, s, fnt, fill):
    d.text((x, y), s, font=fnt, fill=fill)


# ---------------------------------------------------------------- data
# (pool_no, region, place, headline, deck, chip, source, scene, pin lon/lat)
LEADS = [
    (14, "AMERICAS · POLITICS", "WASHINGTON",
     "Democrats take both chambers",
     "House 258-173, the largest majority since 1992, after a North Carolina "
     "pickup. Democrats also hold the Senate from January.",
     "258-173", "BBC", "parliament", (-77.0, 38.9)),
    (13, "AMERICAS · POLITICS", "WASHINGTON",
     "Trump: work with Democrats to cap card rates",
     "Trump says he would work with Democrats to cap credit-card rates and "
     "scrap the debt ceiling. Van Hollen challenges Schumer; secret ballot 1 Dec.",
     "RATE CAP", "ActiveInvestorMag", "podium", (-77.0, 38.9)),
    (4, "WORLD · CLIMATE", "ANTALYA, TURKIYE",
     "COP31 ends with no deal - first since 2000",
     "Cover decision (Antalya Pact) not adopted; text dropped every mention "
     "of fossil fuels. 44h overtime, longest ever; COP32 Addis Ababa.",
     "NO DEAL", "Times / Guardian", "summit", (30.7, 36.9)),
]

MINIS = [
    (1, "AFRICA · WAR", "BENGHAZI, LIBYA",
     "Ukraine sinks warship Merkury off Libya",
     "7 sea drones launched; SBU says corvette sank at Benghazi. Ka-27 "
     "destroyed; MV Angara hit.",
     "7 SEA DRONES", "CNN / Times / AP", "sea", (20.1, 32.1)),
    (2, "EUROPE · SEA", "GULF OF FINLAND",
     "Sparta II hit, towed clear",
     "Hit by 2 drones; Finland led the Loviisa rescue and all 16 crew got off. "
     "Towed out of Finnish waters Sunday night.",
     "16 CREW SAFE", "Reuters / Times", "ship", (26.0, 60.2)),
    (3, "EUROPE · WAR", "KYIV REGION, UKRAINE",
     "Kyiv strikes kill at least 15",
     "11 killed in a block of flats in Dymer. A drone hit a 6-floor building "
     "in Kyiv on Monday; 5 injured.",
     "15 KILLED", "Times / AP", "city", (30.5, 50.4)),
    (5, "MIDDLE EAST · SANCTIONS", "WASHINGTON",
     "US sanctions ~30 Iran exchange houses",
     "Iran sanctions: Treasury named ~30 Iran-based exchange houses plus "
     "executives, core of shadow banking.",
     "~30 SANCTIONED", "AP / Treasury", "bank", (-77.0, 38.9)),
    (6, "MIDDLE EAST · CONFLICT", "GAZA CITY",
     "Israeli strikes kill 3 in Gaza",
     "3 killed Monday in separate strikes, including a UNRWA employee. "
     "Shifa Hospital and the agency confirm.",
     "3 KILLED", "AP", "city2", (34.5, 31.5)),
    (7, "MIDDLE EAST · WAR", "WESTERN YEMEN",
     "Strike kills 11 in western Yemen",
     "Houthis say a Saudi-backed forces' strike on Monday killed 11 "
     "and wounded 19.",
     "11 KILLED", "AP", "desert", (43.5, 15.5)),
    (8, "AMERICAS · MARKETS", "NEW YORK",
     "Gold rebounds 1.5% to $3,588",
     "Bullion +1.5% Monday after its worst week in 8 months. Traders await "
     "US PCE report due 25 Nov.",
     "$3,588/OZ", "Reuters", "gold", (-74.0, 40.7)),
    (9, "WORLD · CRYPTO", "GLOBAL",
     "Bitcoin steadies near $61,284",
     "Kraken CAD flash crash to ~$17,000 stands. $61,284 Mon 12:52 UTC, "
     "+1.1% 24h, -4.5% 7d.",
     "$61,284", "CoinPaprika", "coin", (-45.0, -15.0)),
    (10, "AMERICAS · BUSINESS", "LOS ANGELES",
     "GTA VI takes $3.8bn on day one",
     "Biggest entertainment launch on record - past every game launch "
     "and single-day film box office.",
     "$3.8BN DAY ONE", "ActiveInvestorMag", "game", (-118.2, 34.0)),
    (11, "OCEANIA · CRICKET", "WELLINGTON",
     "New Zealand bat out draw with India",
     "NZ 239/5: Mitchell 49*, Phillips 26*; 63-run stand. India 720/9d; "
     "2nd Test 27 Nov.",
     "DRAW 239/5", "HS / WicketPulse", "cricket", (174.8, -41.3)),
    (12, "EUROPE · FOOTBALL", "LIVERPOOL",
     "Liverpool 4-0 Man Utd",
     "Pochettino debut disaster: Yoro sent off in the 8th minute; United "
     "down to 10. Loss leaves United 19th on 8 points.",
     "4-0", "Mint / NextSportsWeb", "stadium", (-2.97, 53.4)),
    (20, "AMERICAS · MARKETS", "NEW YORK",
     "Nvidia brings back Jensen Huang as CEO",
     "Board reinstates Huang on Monday after Trump intervened. Shares +31%; "
     "Nasdaq +6%, S&P 500 +5%.",
     "+31% HUANG BACK", "Reuters", "chip", (-74.0, 40.7)),
]

# Same 15 cards reshaped for the margin checker: (num, region, place, src,
# headline, deck, scene). Same content, written out literally so the checker
# (AST literal evaluation) can read it; it is not a second source of truth,
# it is the same fifteen cards spelled out once more.
grid = [
    (14, "AMERICAS · POLITICS", "WASHINGTON", "BBC",
     "Democrats take both chambers",
     "House 258-173, the largest majority since 1992, after a North Carolina "
     "pickup. Democrats also hold the Senate from January.",
     "parliament"),
    (13, "AMERICAS · POLITICS", "WASHINGTON", "ActiveInvestorMag",
     "Trump: work with Democrats to cap card rates",
     "Trump says he would work with Democrats to cap credit-card rates and "
     "scrap the debt ceiling. Van Hollen challenges Schumer; secret ballot 1 Dec.",
     "podium"),
    (4, "WORLD · CLIMATE", "ANTALYA, TURKIYE", "Times / Guardian",
     "COP31 ends with no deal - first since 2000",
     "Cover decision (Antalya Pact) not adopted; text dropped every mention "
     "of fossil fuels. 44h overtime, longest ever; COP32 Addis Ababa.",
     "summit"),
    (1, "AFRICA · WAR", "BENGHAZI, LIBYA", "CNN / Times / AP",
     "Ukraine sinks warship Merkury off Libya",
     "7 sea drones launched; SBU says corvette sank at Benghazi. Ka-27 "
     "destroyed; MV Angara hit.",
     "sea"),
    (2, "EUROPE · SEA", "GULF OF FINLAND", "Reuters / Times",
     "Sparta II hit, towed clear",
     "Hit by 2 drones; Finland led the Loviisa rescue and all 16 crew got off. "
     "Towed out of Finnish waters Sunday night.",
     "ship"),
    (3, "EUROPE · WAR", "KYIV REGION, UKRAINE", "Times / AP",
     "Kyiv strikes kill at least 15",
     "11 killed in a block of flats in Dymer. A drone hit a 6-floor building "
     "in Kyiv on Monday; 5 injured.",
     "city"),
    (5, "MIDDLE EAST · SANCTIONS", "WASHINGTON", "AP / Treasury",
     "US sanctions ~30 Iran exchange houses",
     "Iran sanctions: Treasury named ~30 Iran-based exchange houses plus "
     "executives, core of shadow banking.",
     "bank"),
    (6, "MIDDLE EAST · CONFLICT", "GAZA CITY", "AP",
     "Israeli strikes kill 3 in Gaza",
     "3 killed Monday in separate strikes, including a UNRWA employee. "
     "Shifa Hospital and the agency confirm.",
     "city2"),
    (7, "MIDDLE EAST · WAR", "WESTERN YEMEN", "AP",
     "Strike kills 11 in western Yemen",
     "Houthis say a Saudi-backed forces' strike on Monday killed 11 "
     "and wounded 19.",
     "desert"),
    (8, "AMERICAS · MARKETS", "NEW YORK", "Reuters",
     "Gold rebounds 1.5% to $3,588",
     "Bullion +1.5% Monday after its worst week in 8 months. Traders await "
     "US PCE report due 25 Nov.",
     "gold"),
    (9, "WORLD · CRYPTO", "GLOBAL", "CoinPaprika",
     "Bitcoin steadies near $61,284",
     "Kraken CAD flash crash to ~$17,000 stands. $61,284 Mon 12:52 UTC, "
     "+1.1% 24h, -4.5% 7d.",
     "coin"),
    (10, "AMERICAS · BUSINESS", "LOS ANGELES", "ActiveInvestorMag",
     "GTA VI takes $3.8bn on day one",
     "Biggest entertainment launch on record - past every game launch "
     "and single-day film box office.",
     "game"),
    (11, "OCEANIA · CRICKET", "WELLINGTON", "HS / WicketPulse",
     "New Zealand bat out draw with India",
     "NZ 239/5: Mitchell 49*, Phillips 26*; 63-run stand. India 720/9d; "
     "2nd Test 27 Nov.",
     "cricket"),
    (12, "EUROPE · FOOTBALL", "LIVERPOOL", "Mint / NextSportsWeb",
     "Liverpool 4-0 Man Utd",
     "Pochettino debut disaster: Yoro sent off in the 8th minute; United "
     "down to 10. Loss leaves United 19th on 8 points.",
     "stadium"),
    (20, "AMERICAS · MARKETS", "NEW YORK", "Reuters",
     "Nvidia brings back Jensen Huang as CEO",
     "Board reinstates Huang on Monday after Trump intervened. Shares +31%; "
     "Nasdaq +6%, S&P 500 +5%.",
     "chip"),
]
PINS = [(14, -77.0, 38.9), (13, -77.0, 38.9), (4, 30.7, 36.9),
        (1, 20.1, 32.1), (2, 26.0, 60.2), (3, 30.5, 50.4),
        (5, -77.0, 38.9), (6, 34.5, 31.5), (7, 43.5, 15.5),
        (8, -74.0, 40.7), (9, -45.0, -15.0), (10, -118.2, 34.0),
        (11, 174.8, -41.3), (12, -2.97, 53.4), (20, -74.0, 40.7)]

NUMS = [
    ("7", "SEA DRONES LAUNCHED"),
    ("NO DEAL", "COP31, FIRST SINCE 2000"),
    ("258-173", "DEMOCRATS TAKE HOUSE"),
    ("$3,588", "GOLD, +1.5% MONDAY"),
    ("$61,284", "BITCOIN, 12:52 UTC"),
    ("+31%", "NVIDIA, HUANG BACK"),
]

REGIONS = [("EUROPE", 3, INK2), ("MIDDLE EAST", 3, RED),
           ("AMERICAS", 5, TEAL), ("AFRICA", 1, (150, 90, 20)),
           ("OCEANIA", 1, (90, 60, 140)), ("WORLD", 2, (90, 90, 90))]

# Timeline: (clock, zone, text) - absolute order, every clock verified.
TL = [
    ("05:31 KST", "Economy wires round up Nvidia's return and the AI rally"),
    ("08:15 AEST", "Morning Wrap: ASX set to rise as Nasdaq soars on Huang"),
    ("04:24 WIB", "KCNA: Pyongyang weighs shutting its Swiss office"),
    ("07:00 WIB", "EDITION MARKER - Tuesday's news cycle opens in Asia"),
    ("10:30 CET", "DUE: Germany's November Ifo Business Climate Index"),
]

DATECHECK = [
    "186-drone night over Ukraine, 161 downed - Fri 21-Sun 22 Nov",
    "Alcaraz beats Zverev, first ATP Finals title - Sun 22 Nov",
    "Verstappen wins Las Vegas Grand Prix - Sun 22 Nov",
    "Wembanyama scores 50, Spurs 114-91 Pelicans - Sun 22 Nov",
    "Hong Kong Election Committee: 856 candidates, 723 seats - Sun 22 Nov",
    "Nvidia CEO Huang resigns after affair admission - Thu 12 Nov",
    "Myanmar ICJ genocide ruling - Thu 19 Nov",
]

dc = ("186-drone night over Ukraine, 161 downed - Fri 21-Sun 22 Nov  ·  "
      "Alcaraz beats Zverev, first ATP Finals title - Sun 22 Nov  ·  "
      "Verstappen wins Las Vegas Grand Prix - Sun 22 Nov  ·  "
      "Wembanyama scores 50, Spurs 114-91 Pelicans - Sun 22 Nov  ·  "
      "Hong Kong Election Committee: 856 candidates, 723 seats - Sun 22 Nov  ·  "
      "Nvidia CEO Huang resigns after affair admission - Thu 12 Nov  ·  "
      "Myanmar ICJ genocide ruling - Thu 19 Nov")

# Coarse continent outlines (lon, lat), drawn as a dotted world map.
CONTINENTS = {
    "na": [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80),
           (-75, 72), (-65, 60), (-55, 52), (-60, 45), (-70, 42), (-75, 35),
           (-80, 32), (-85, 29), (-90, 21), (-95, 19), (-100, 16), (-105, 20),
           (-110, 23), (-115, 28), (-120, 34), (-125, 40), (-125, 48),
           (-135, 58), (-155, 58), (-165, 60)],
    "sa": [(-80, 10), (-75, 11), (-70, 12), (-62, 10), (-55, 5), (-50, 0),
           (-45, -5), (-40, -10), (-35, -15), (-40, -22), (-48, -28),
           (-55, -35), (-60, -40), (-65, -45), (-70, -52), (-73, -50),
           (-73, -40), (-72, -30), (-70, -20), (-75, -15), (-80, -8),
           (-81, -2), (-80, 5)],
    "eu": [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 51), (3, 53), (8, 57),
           (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (32, 68),
           (40, 68), (45, 66), (40, 60), (35, 55), (30, 50), (28, 46), (23, 40),
           (20, 40), (15, 44), (12, 44), (8, 44), (3, 42), (0, 40), (-2, 37),
           (-6, 36)],
    "af": [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31), (33, 27),
           (35, 20), (38, 15), (43, 11), (48, 10), (51, 12), (46, 5), (42, -2),
           (40, -10), (36, -18), (33, -26), (28, -33), (20, -35), (16, -28),
           (12, -18), (13, -10), (9, 4), (4, 6), (-8, 5), (-13, 8), (-17, 15),
           (-17, 21), (-16, 28), (-10, 31)],
    "as": [(30, 62), (40, 68), (60, 69), (70, 72), (80, 73), (90, 75), (100, 77),
           (110, 76), (120, 73), (130, 72), (140, 72), (150, 70), (160, 69),
           (170, 66), (178, 65), (170, 60), (162, 56), (158, 52), (150, 45),
           (142, 40), (140, 35), (135, 33), (130, 31), (127, 30), (122, 28),
           (120, 25), (115, 22), (110, 20), (108, 15), (105, 10), (100, 8),
           (97, 10), (95, 15), (92, 20), (90, 22), (88, 22), (85, 20), (80, 15),
           (77, 8), (75, 12), (72, 20), (68, 22), (65, 25), (60, 25), (57, 26),
           (54, 26), (52, 28), (50, 29), (48, 30), (44, 29), (40, 30), (36, 36),
           (33, 36), (30, 36), (27, 40), (26, 42), (28, 46), (30, 50), (32, 55),
           (35, 60)],
    "oc": [(113, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
           (132, -32), (135, -35), (137, -35), (140, -38), (145, -38), (150, -37),
           (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11),
           (137, -12), (135, -12), (132, -11), (130, -13), (126, -14), (122, -17),
           (118, -20)],
    "uk": [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    "jp": [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 36),
           (141, 39), (141, 42), (142, 44), (144, 44), (145, 42), (142, 40),
           (140, 38), (138, 37), (136, 36), (133, 35), (131, 33)],
    "nz": [(167, -45), (170, -43), (173, -41), (175, -40), (177, -38), (178, -37),
           (176, -35), (174, -36), (173, -39), (171, -42), (168, -44)],
}


# ---------------------------------------------------------------- scenes
def _sky(d, x0, y0, x1, y1, top, bot):
    d.rectangle([x0, y0, x1, y1], fill=top)
    d.rectangle([x0, y0 + (y1 - y0) * 2 // 3, x1, y1], fill=bot)


def _sun(d, x, y, r, col=GOLD_LT):
    d.ellipse([x - r, y - r, x + r, y + r], fill=col)


def _scene_body(d, key, x0, y0, x1, y1):
    """Flat layered scene strip, full-bleed, one painter per story kind."""
    w, h = x1 - x0, y1 - y0
    if key == "parliament":
        _sky(d, x0, y0, x1, y1, INK2, SKY)
        d.ellipse([x0 + w // 2 - 130, y0 + 60, x0 + w // 2 + 130, y0 + 320],
                  fill=GOLD)
        d.rectangle([x0 + w * 0.12, y0 + h * 0.55, x1 - w * 0.12, y1], fill=CREAM)
        d.rectangle([x0 + w * 0.12, y0 + h * 0.50, x1 - w * 0.12, y0 + h * 0.58],
                    fill=INK)
        for i in range(6):
            cx = x0 + w * (0.20 + i * 0.12)
            d.rectangle([cx, y0 + h * 0.58, cx + 42, y1], fill=INK2)
        d.rectangle([x0, y1 - 46, x1, y1], fill=GREEN)
    elif key == "podium":
        _sky(d, x0, y0, x1, y1, (90, 60, 120), (150, 120, 170))
        for i, c in enumerate((RED, WHITE, INK2)):
            fx = x0 + w * (0.18 + i * 0.30)
            d.rectangle([fx, y0 + 40, fx + 150, y0 + 260], fill=c)
            d.rectangle([fx + 70, y0 + 260, fx + 76, y0 + 330], fill=CHAR)
        d.polygon([(x0 + w * 0.38, y1), (x0 + w * 0.62, y1),
                   (x0 + w * 0.56, y0 + h * 0.62),
                   (x0 + w * 0.44, y0 + h * 0.62)], fill=INK)
        d.ellipse([x0 + w * 0.47, y0 + h * 0.42, x0 + w * 0.53, y0 + h * 0.58],
                  fill=GOLD)
    elif key == "summit":
        _sky(d, x0, y0, x1, y1, (20, 90, 90), (120, 180, 170))
        _sun(d, x0 + w // 2, y0 + 110, 90)
        for i, c in enumerate((TEAL, (200, 60, 50), GOLD, INK2, GREEN)):
            fx = x0 + w * (0.08 + i * 0.18)
            d.rectangle([fx, y0 + h * 0.42, fx + 110, y0 + h * 0.62], fill=c)
            d.line([fx + 55, y0 + h * 0.42, fx + 55, y0 + h * 0.30],
                   fill=CHAR, width=8)
        d.polygon([(x0, y1), (x0 + w * 0.3, y0 + h * 0.66), (x0 + w * 0.55, y1)],
                  fill=(60, 110, 70))
        d.polygon([(x0 + w * 0.45, y1), (x0 + w * 0.75, y0 + h * 0.60),
                   (x1, y1)], fill=(40, 90, 60))
        d.ellipse([x0 + w * 0.78, y0 + 70, x0 + w * 0.78 + 150, y0 + 220],
                  fill=SKY)
    elif key == "sea":
        d.rectangle([x0, y0, x1, y1], fill=SEA)
        for i in range(5):
            yy = y0 + h * (0.55 + i * 0.09)
            d.arc([x0 - 60, yy - 40, x1 + 60, yy + 40], 0, 180,
                  fill=SKY, width=14)
        d.polygon([(x0 + w * 0.30, y0 + h * 0.62), (x0 + w * 0.42, y0 + h * 0.30),
                   (x0 + w * 0.46, y0 + h * 0.62)], fill=CHAR)
        d.rectangle([x0 + w * 0.28, y0 + h * 0.60, x0 + w * 0.62, y0 + h * 0.72],
                    fill=(30, 30, 30))
        d.polygon([(x0 + w * 0.66, y0 + h * 0.52), (x0 + w * 0.70, y0 + h * 0.30),
                   (x0 + w * 0.74, y0 + h * 0.52)], fill=RED)
        for i, (dx, dy) in enumerate(((0.72, 0.30), (0.80, 0.42), (0.86, 0.28))):
            cx, cy = x0 + w * dx, y0 + h * dy
            d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=GOLD_LT)
            d.text((cx, cy), "7", font=F_ARCH(34), fill=INK, anchor="mm")
        d.ellipse([x0 + w * 0.60, y0 + 40, x0 + w * 0.60 + 120, y0 + 160],
                  fill=(255, 120, 60))
    elif key == "ship":
        d.rectangle([x0, y0, x1, y1], fill=(70, 120, 170))
        d.rectangle([x0, y0 + h * 0.62, x1, y1], fill=SEA)
        d.rectangle([x0 + w * 0.15, y0 + h * 0.45, x0 + w * 0.80, y0 + h * 0.62],
                    fill=(180, 60, 40))
        for i in range(4):
            cx = x0 + w * (0.22 + i * 0.14)
            d.rectangle([cx, y0 + h * 0.30, cx + 90, y0 + h * 0.45], fill=GOLD)
        d.rectangle([x0 + w * 0.82, y0 + h * 0.28, x0 + w * 0.88, y0 + h * 0.45],
                    fill=CREAM)
        d.ellipse([x0 + w * 0.10, y0 + 50, x0 + w * 0.10 + 130, y0 + 180],
                  fill=(120, 120, 120))
        d.ellipse([x0 + w * 0.16, y0 + 80, x0 + w * 0.16 + 70, y0 + 150],
                  fill=(90, 90, 90))
    elif key == "city":
        _sky(d, x0, y0, x1, y1, (60, 60, 90), (140, 120, 110))
        for i, bh in enumerate((0.55, 0.75, 0.62, 0.85, 0.58)):
            bx = x0 + w * (0.05 + i * 0.19)
            d.rectangle([bx, y1 - h * bh, bx + w * 0.16, y1], fill=INK2)
            for wy in range(3):
                for wx in range(2):
                    d.rectangle([bx + 18 + wx * 55, y1 - h * bh + 30 + wy * 70,
                                 bx + 48 + wx * 55, y1 - h * bh + 60 + wy * 70],
                                fill=GOLD_LT)
        d.polygon([(x0 + w * 0.55, y0 + 60), (x0 + w * 0.65, y0 + 140),
                   (x0 + w * 0.45, y0 + 140)], fill=RED)
        d.rectangle([x0 + w * 0.58, y0 + 140, x0 + w * 0.62, y0 + 320],
                    fill=(90, 90, 90))
    elif key == "bank":
        _sky(d, x0, y0, x1, y1, INK, (90, 110, 170))
        d.polygon([(x0 + w * 0.5, y0 + 60), (x0 + w * 0.78, y0 + 220),
                   (x0 + w * 0.22, y0 + 220)], fill=GOLD)
        for i in range(5):
            cx = x0 + w * (0.24 + i * 0.13)
            d.rectangle([cx, y0 + 240, cx + 46, y1 - 40], fill=CREAM)
        d.rectangle([x0 + w * 0.18, y1 - 60, x0 + w * 0.82, y1 - 20], fill=CREAM)
        d.ellipse([x0 + w * 0.80, y0 + 60, x0 + w * 0.80 + 130, y0 + 190],
                  fill=GOLD)
        d.text((x0 + w * 0.80 + 65, y0 + 125), "$", font=F_ARCH(90),
               fill=INK, anchor="mm")
    elif key == "city2":
        _sky(d, x0, y0, x1, y1, (120, 90, 70), (200, 170, 130))
        for i, bh in enumerate((0.5, 0.68, 0.58, 0.78)):
            bx = x0 + w * (0.06 + i * 0.23)
            d.rectangle([bx, y1 - h * bh, bx + w * 0.19, y1], fill=(70, 60, 60))
        d.rectangle([x0 + w * 0.40, y0 + 70, x0 + w * 0.60, y0 + 190],
                    fill=WHITE)
        d.rectangle([x0 + w * 0.47, y0 + 95, x0 + w * 0.53, y0 + 165],
                    fill=RED)
        d.rectangle([x0 + w * 0.44, y0 + 120, x0 + w * 0.56, y0 + 140],
                    fill=RED)
    elif key == "desert":
        _sky(d, x0, y0, x1, y1, (230, 180, 110), (240, 210, 150))
        _sun(d, x0 + w * 0.78, y0 + 110, 100, (255, 240, 180))
        d.polygon([(x0, y1), (x0 + w * 0.35, y0 + h * 0.60), (x0 + w * 0.7, y1)],
                  fill=(210, 165, 95))
        d.polygon([(x0 + w * 0.45, y1), (x0 + w * 0.8, y0 + h * 0.66), (x1, y1)],
                  fill=(190, 145, 80))
        for i in range(3):
            tx = x0 + w * (0.20 + i * 0.22)
            d.polygon([(tx, y0 + h * 0.72), (tx + 90, y0 + h * 0.50),
                       (tx + 180, y0 + h * 0.72)], fill=(120, 80, 50))
    elif key == "gold":
        _sky(d, x0, y0, x1, y1, (40, 40, 60), (90, 90, 120))
        for i in range(3):
            for j in range(3 - i):
                bx = x0 + w * (0.14 + j * 0.17 + i * 0.085)
                by = y1 - 60 - (i + 1) * 64
                d.polygon([(bx, by + 64), (bx + 26, by), (bx + 140, by),
                           (bx + 166, by + 64)], fill=GOLD)
                d.polygon([(bx + 26, by), (bx + 140, by), (bx + 140, by + 14),
                           (bx + 26, by + 14)], fill=GOLD_LT)
        pts = [(x0 + w * 0.55, y0 + h * 0.72), (x0 + w * 0.66, y0 + h * 0.55),
               (x0 + w * 0.76, y0 + h * 0.62), (x0 + w * 0.90, y0 + h * 0.28)]
        d.line(pts, fill=(90, 220, 130), width=16, joint="curve")
        d.polygon([(pts[-1][0], pts[-1][1]), (pts[-1][0] - 34, pts[-1][1] + 6),
                   (pts[-1][0] - 6, pts[-1][1] + 34)], fill=(90, 220, 130))
    elif key == "coin":
        _sky(d, x0, y0, x1, y1, (30, 30, 50), (70, 70, 110))
        cx, cy, r = x0 + w * 0.30, y0 + h * 0.52, 150
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD)
        d.ellipse([cx - r + 26, cy - r + 26, cx + r - 26, cy + r - 26],
                  outline=INK, width=10)
        d.text((cx, cy), "B", font=F_ARCH(190), fill=INK, anchor="mm")
        pts = [(x0 + w * 0.55, y0 + h * 0.70), (x0 + w * 0.68, y0 + h * 0.45),
               (x0 + w * 0.80, y0 + h * 0.55), (x0 + w * 0.93, y0 + h * 0.30)]
        d.line(pts, fill=(90, 220, 130), width=16, joint="curve")
    elif key == "game":
        _sky(d, x0, y0, x1, y1, (25, 25, 60), (80, 40, 110))
        for i in range(8):
            sx = x0 + w * (0.12 + i * 0.02)
            d.line([sx, y0 + h * 0.55, sx, y0 + h * 0.62], fill=GOLD_LT, width=4)
        d.ellipse([x0 + w * 0.42, y0 + 40, x0 + w * 0.58, y0 + 200],
                  fill=(255, 80, 60))
        d.text((x0 + w * 0.5, y0 + 120), "VI", font=F_ARCH(84), fill=WHITE,
               anchor="mm")
        d.rounded_rectangle([x0 + w * 0.28, y0 + h * 0.62, x0 + w * 0.72,
                            y0 + h * 0.92], radius=40, fill=INK2)
        d.ellipse([x0 + w * 0.34, y0 + h * 0.70, x0 + w * 0.34 + 60,
                   y0 + h * 0.70 + 60], fill=WHITE)
        d.ellipse([x0 + w * 0.60, y0 + h * 0.70, x0 + w * 0.60 + 60,
                   y0 + h * 0.70 + 60], fill=RED)
    elif key == "cricket":
        _sky(d, x0, y0, x1, y1, (140, 190, 230), (200, 220, 180))
        d.ellipse([x0, y0 + h * 0.55, x1, y1 + 60], fill=GREEN)
        d.rectangle([x0 + w * 0.38, y0 + h * 0.50, x0 + w * 0.62, y1],
                    fill=(220, 200, 150))
        for i in range(3):
            sx = x0 + w * (0.70 + i * 0.03)
            d.rectangle([sx, y0 + h * 0.58, sx + 14, y0 + h * 0.78], fill=GOLD)
        d.ellipse([x0 + w * 0.80, y0 + h * 0.30, x0 + w * 0.80 + 70,
                   y0 + h * 0.30 + 70], fill=RED)
        d.line([x0 + w * 0.30, y0 + h * 0.60, x0 + w * 0.44, y0 + h * 0.40],
               fill=(120, 80, 40), width=18)
    elif key == "stadium":
        _sky(d, x0, y0, x1, y1, (20, 40, 90), (60, 90, 150))
        for i in range(2):
            lx = x0 + w * (0.12 + i * 0.68)
            d.rectangle([lx, y0 + 40, lx + 26, y0 + 300], fill=CHAR)
            d.ellipse([lx - 60, y0 + 20, lx + 86, y0 + 110], fill=WHITE)
        d.ellipse([x0, y0 + h * 0.60, x1, y1 + 80], fill=GREEN)
        d.ellipse([x0 + w * 0.44, y0 + h * 0.42, x0 + w * 0.56, y0 + h * 0.62],
                  fill=WHITE, outline=CHAR, width=6)
        d.polygon([(x0 + w * 0.47, y0 + h * 0.47), (x0 + w * 0.53, y0 + h * 0.47),
                   (x0 + w * 0.50, y0 + h * 0.57)], fill=CHAR)
        d.text((x0 + w * 0.5, y0 + h * 0.30), "4-0", font=F_ARCH(150),
               fill=GOLD_LT, anchor="mm")
    elif key == "chip":
        d.rectangle([x0, y0, x1, y1], fill=(15, 25, 45))
        for i in range(6):
            yy = y0 + 40 + i * (h - 80) // 5
            d.line([x0 + 30, yy, x1 - 30, yy], fill=(40, 80, 140), width=4)
        cx, cy = x0 + w // 2, y0 + h // 2
        d.rounded_rectangle([cx - 190, cy - 130, cx + 190, cy + 130], radius=30,
                            fill=(20, 160, 90))
        d.rounded_rectangle([cx - 130, cy - 80, cx + 130, cy + 80], radius=16,
                            fill=(10, 90, 50))
        d.text((cx, cy), "NVDA", font=F_ARCH(84), fill=WHITE, anchor="mm")
        for i in range(5):
            px = cx - 160 + i * 80
            d.line([px, cy - 130, px, cy - 190], fill=GOLD, width=10)
            d.line([px, cy + 130, px, cy + 190], fill=GOLD, width=10)


def draw_scene(d, key, x0, y0, x1, y1):
    """Paint the scene once on a fixed virtual canvas, then fit it to any box,
    so lead cards (tall) and mini cards (short) share identical artwork."""
    vw, vh = 900, 360
    tmp = Image.new("RGB", (vw, vh), CREAM)
    td = ImageDraw.Draw(tmp)
    _scene_body(td, key, 0, 0, vw, vh)
    tmp = tmp.resize((x1 - x0, y1 - y0), Image.LANCZOS)
    PAGE_IMG.paste(tmp, (x0, y0))


# ---------------------------------------------------------------- map
def point_in_poly(px, py, poly):
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > py) != (y2 > py):
            xin = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
            if px < xin:
                inside = not inside
    return inside


def dotted_map(d, x0, y0, x1, y1, pins):
    """Dotted world map from the continent polygons above, red numbered pins."""
    d.rectangle([x0, y0, x1, y1], fill=(214, 226, 240))
    mw, mh = x1 - x0, y1 - y0

    def proj(lon, lat):
        return (x0 + (lon + 180.0) / 360.0 * mw,
                y0 + (90.0 - lat) / 180.0 * mh)

    polys = [[proj(lon, lat) for lon, lat in pts]
             for pts in CONTINENTS.values()]
    step = 26
    for gy in range(y0 + 8, y1 - 4, step):
        for gx in range(x0 + 8, x1 - 4, step):
            lon = (gx - x0) / mw * 360.0 - 180.0
            lat = 90.0 - (gy - y0) / mh * 180.0
            if any(point_in_poly(lon, lat, pts) for pts in CONTINENTS.values()):
                d.ellipse([gx - 7, gy - 7, gx + 7, gy + 7], fill=INK)
    # Manual declutter: five pins share the Washington/New York point and six
    # crowd the eastern Mediterranean, so each pin gets a fixed nudge.
    NUDGE = {14: (-110, -45), 13: (-55, 55), 5: (0, -55), 8: (55, 55),
             20: (110, -45), 9: (0, 0), 10: (-40, 30), 12: (-35, -40),
             1: (-70, 55), 2: (75, -30), 3: (-15, -55), 4: (55, 45),
             6: (-5, 80), 7: (95, 20), 11: (-74, -28)}
    for num, lon, lat in pins:
        px, py = proj(lon, lat)
        dx, dy = NUDGE.get(num, (0, 0))
        px += dx
        py += dy
        d.ellipse([px - 34, py - 34, px + 34, py + 34], fill=RED,
                  outline=WHITE, width=5)
        d.text((px, py), str(num), font=F_ARCH(40), fill=WHITE, anchor="mm")


# ---------------------------------------------------------------- cards
def card_frame(d, x0, y0, x1, y1, accent):
    d.rectangle([x0, y0, x1, y1], fill=PAPER)
    d.rectangle([x0, y0, x1, y1], outline=INK, width=4)
    d.rectangle([x0, y0, x1, y0 + 14], fill=accent)


def card_tag(d, x, y, num, region, place, f_small, f_num):
    d.ellipse([x, y, x + 64, y + 64], fill=RED)
    d.text((x + 32, y + 32), str(num), font=f_num, fill=WHITE, anchor="mm")
    d.text((x + 78, y + 8), region, font=f_small, fill=RED)
    d.text((x + 78, y + 36), place, font=f_small, fill=GREY)


def draw_lead(d, card, x0, y0, x1, y1, variant):
    num, region, place, head, deck, chip, src, scene, pin = card
    card_frame(d, x0, y0, x1, y1, RED if variant == "A" else INK2)
    sh = 400
    draw_scene(d, scene, x0 + 4, y0 + 18, x1 - 4, y0 + 18 + sh)
    d.rectangle([x0 + 4, y0 + 18 + sh - 64, x1 - 4, y0 + 18 + sh], fill=INK)
    text_c(d, (x0 + x1) // 2, y0 + 18 + sh - 58, chip, F_ARCH(52), GOLD_LT)
    card_tag(d, x0 + 26, y0 + 18 + sh + 26, num, region, place,
             F_ARCH(34), F_ARCH(38))
    ty = y0 + 18 + sh + 112
    for ln in wrap(d, head, F_BLACK(78), x1 - x0 - 52):
        text_l(d, x0 + 26, ty, ln, F_BLACK(78), INK)
        ty += 88
    ty += 8
    for ln in wrap(d, deck, F_SANSR(44), x1 - x0 - 52):
        text_l(d, x0 + 26, ty, ln, F_SANSR(44), CHAR)
        ty += 56
    d.text((x0 + 26, y1 - 62), "REPORTED  ·  " + src, font=F_ARCH(34), fill=TEAL)
    d.text((x1 - 26, y1 - 62), "24 NOV 2026", font=F_ARCH(34), fill=GREY,
           anchor="ra")


def draw_mini(d, card, x0, y0, x1, y1, variant):
    num, region, place, head, deck, chip, src, scene, pin = card
    card_frame(d, x0, y0, x1, y1, INK2 if variant == "A" else TEAL)
    sh = 112
    draw_scene(d, scene, x0 + 4, y0 + 18, x1 - 4, y0 + 18 + sh)
    d.rectangle([x0 + 4, y0 + 18 + sh - 44, x1 - 4, y0 + 18 + sh], fill=INK)
    text_c(d, (x0 + x1) // 2, y0 + 18 + sh - 40, chip, F_ARCH(36), GOLD_LT)
    ty = y0 + 18 + sh + 14
    d.text((x0 + 18, ty), "%d  %s" % (num, region), font=F_ARCH(30), fill=RED)
    ty += 40
    for ln in wrap(d, head, F_BOLD(54), x1 - x0 - 36)[:2]:
        text_l(d, x0 + 18, ty, ln, F_BOLD(54), INK)
        ty += 62
    for ln in wrap(d, deck, F_SANSR(30), x1 - x0 - 36)[:3]:
        text_l(d, x0 + 18, ty, ln, F_SANSR(30), CHAR)
        ty += 36
    d.text((x0 + 18, y1 - 36), "REPORTED · " + src, font=F_ARCH(26), fill=TEAL)


# ---------------------------------------------------------------- page
BRIEFS_L = [
    "21. UN AI weapons talks continue; states keep negotiating (salonvision)",
    "22. Nepal PM Balendra Shah ends Delhi visit; met Modi Mon (IANS)",
    "23. Thousands march in Lisbon over cost of living (JagranJosh)",
    "24. UK-EU Brexit reset deal called \u201clandmark\u201d (BBC)",
    "25. India-EU free-trade pact likely signed 16 Dec (JagranJosh)",
    "26. Tata Steel sells pipe unit to APL Apollo, \u20b928,000 cr",
    "27. >90 countries signed COP31 electrification pledge (Times)",
    "28. Modi opens AI Centre at IIT Patna, \u20b9400 cr projects",
    "29. Amit Shah launches \u20b94,000 cr infra push in Arunachal",
    "30. FBI probes hack of its crime database (AP)",
    "31. Solana launches solana.ai for AI agents (Gadgets360)",
    "32. North Korea weighs shutting Swiss office in Pyongyang (KCNA, Tue)",
    "33. 130 countries wanted fossil-fuel language at COP31 (Times)",
    "34. Goldman sees +18% S&P 500 through 2027 (ActiveInvestorMag)",
    "35. Van Hollen challenges Schumer for Senate leader; vote 1 Dec",
    "36. Miley Cyrus marries Maxx Morando in California (BBC)",
    "37. Congo halts cobalt exports from 30 Nov (Reuters)",
    "38. CrowdStrike snaps up Zscaler in $44bn deal (Reuters)",
    "39. Indonesia: 24 killed in factory blaze (Reuters)",
    "40. Euro zone growth holds; PMI 51.7 in Nov (Reuters)",
    "41. US discusses military training for Syrian forces (Reuters)",
]


def draw_page(variant):
    global PAGE_IMG
    img = Image.new("RGB", (W, H), CREAM)
    PAGE_IMG = img
    d = ImageDraw.Draw(img)
    mx = 90
    x1 = W - mx
    # --- kicker
    d.rectangle([mx, 92, x1, 96], fill=RED)
    kick = "36 STORIES  ·  7 REGIONS  ·  EVERY ONE FROM TUESDAY 24 NOVEMBER 2026"
    text_c(d, W // 2, 108, kick, F_ARCH(46), INK)
    d.rectangle([mx, 168, x1, 172], fill=INK)
    # --- masthead
    text_c(d, W // 2, 190, "THE MERIDIAN LINE", F_BLACK(268), INK)
    d.rectangle([mx, 452, x1, 458], fill=GOLD)
    text_c(d, W // 2, 474, "Tuesday 24 November 2026", F_BLACK(132), RED)
    deck = ("From Benghazi to Antalya, Wellington to Washington \u2014 the House "
            "turned, the talks collapsed, Huang came back.")
    text_c(d, W // 2, 626, deck, F_ITAL(58), CHAR)
    # --- number strip
    ny0, ny1 = 700, 910
    d.rectangle([mx, ny0, x1, ny1], fill=INK)
    cw = (x1 - mx) // 6
    nums = NUMS if variant == "A" else list(reversed(NUMS))
    for i, (val, lab) in enumerate(nums):
        cx = mx + cw * i + cw // 2
        if i:
            d.line([mx + cw * i, ny0 + 18, mx + cw * i, ny1 - 18],
                   fill=GOLD, width=4)
        text_c(d, cx, ny0 + 18, val, F_BLACK(88), CREAM)
        text_c(d, cx, ny0 + 128, lab, F_ARCH(32), GOLD_LT)
    # --- region strip
    ry = 932
    text_l(d, mx, ry, "15 CARDS BY REGION", F_ARCH(36), INK)
    rx = mx + 560
    for name, n, col in REGIONS:
        d.rectangle([rx, ry + 2, rx + 34, ry + 36], fill=col)
        lab = "%s %d" % (name, n)
        text_l(d, rx + 46, ry, lab, F_ARCH(36), CHAR)
        rx += 46 + d.textlength(lab, font=F_ARCH(36)) + 44
    d.text((x1, ry), "TOTAL 15", font=F_ARCH(36), fill=RED, anchor="ra")
    # --- timeline
    ty0, ty1 = 1010, 1200
    d.rectangle([mx, ty0, x1, ty1], fill=BAND)
    d.rectangle([mx, ty0, x1, ty0 + 6], fill=RED)
    text_l(d, mx + 16, ty0 + 16, "THE DAY IN TIME \u2014 TUESDAY 24 NOVEMBER, AS ASIA WOKE",
           F_ARCH(38), INK)
    tw = (x1 - mx - 32) // 5
    for i, (clock, txt) in enumerate(TL):
        tx = mx + 16 + tw * i
        text_l(d, tx, ty0 + 66, clock, F_ARCH(42), RED)
        yy = ty0 + 116
        for ln in wrap(d, txt, F_SANSR(34), tw - 24)[:2]:
            text_l(d, tx, yy, ln, F_SANSR(34), CHAR)
            yy += 40
    # --- leads
    leads = LEADS if variant == "A" else [LEADS[1], LEADS[0], LEADS[2]]
    ly0, ly1 = 1222, 2162
    lw = 1200
    for i, card in enumerate(leads):
        draw_lead(d, card, mx + i * (lw + 60), ly0,
                  mx + i * (lw + 60) + lw, ly1, variant)
    # --- minis: 2 rows x 6 cols
    mw_ = 600
    gap = 24
    my = [2186, 2666]
    for r in range(2):
        for c in range(6):
            card = MINIS[r * 6 + c]
            draw_mini(d, card, mx + c * (mw_ + gap), my[r],
                      mx + c * (mw_ + gap) + mw_, my[r] + 460, variant)
    # --- bottom band: map + ALSO ON (mirrored in B)
    by0, by1 = 3150, 3650
    map_w = 1250
    if variant == "A":
        map_x0, also_x0 = mx, mx + map_w + 40
    else:
        also_x0, map_x0 = mx, mx + (x1 - mx - map_w - 40) + 40
    also_x1 = also_x0 + (x1 - mx - map_w - 40)
    d.rectangle([map_x0, by0, map_x0 + map_w, by1], fill=(214, 226, 240),
                outline=INK, width=4)
    text_l(d, map_x0 + 16, by0 + 12, "WHERE IT HAPPENED", F_ARCH(38), INK)
    text_l(d, map_x0 + 16, by0 + 56,
           "pins match story numbers", F_SANSR(32), GREY)
    pins = [(num, lon, lat) for num, lon, lat in PINS]
    dotted_map(d, map_x0 + 8, by0 + 104, map_x0 + map_w - 8, by1 - 8, pins)
    d.rectangle([also_x0, by0, also_x1, by1], fill=PAPER, outline=INK, width=4)
    text_l(d, also_x0 + 18, by0 + 12, "ALSO ON \u2014 TUESDAY 24 NOVEMBER",
           F_ARCH(38), INK)
    d.rectangle([also_x0, by0 + 62, also_x1, by0 + 66], fill=RED)
    colw = (also_x1 - also_x0 - 36) // 3
    for idx, item in enumerate(BRIEFS_L):
        num_s, _, txt = item.partition(". ")
        num = int(num_s)
        col, row = idx % 3, idx // 3
        bx = also_x0 + 18 + col * (colw + 12)
        by = by0 + 84 + row * 64
        d.text((bx, by), str(num), font=F_ARCH(30), fill=RED)
        lines = wrap(d, txt, F_SANSR(28), colw - 64)[:2]
        yy = by - 2
        for ln in lines:
            text_l(d, bx + 62, yy, ln, F_SANSR(28), CHAR)
            yy += 32
    # --- date check
    dy0, dy1 = 3672, 3800
    d.rectangle([mx, dy0, x1, dy1], fill=(252, 235, 232), outline=RED, width=4)
    text_l(d, mx + 16, dy0 + 10, "DATE CHECK \u2014 NOT TODAY'S NEWS:",
           F_ARCH(34), RED)
    dc_joined = "  ·  ".join(DATECHECK)
    yy = dy0 + 52
    for ln in wrap(d, dc_joined, F_SANSR(30), x1 - mx - 32):
        text_l(d, mx + 16, yy, ln, F_SANSR(30), CHAR)
        yy += 36
    # --- footer
    fy = 3822
    foot = ("Sources: Reuters · AP · CNN · Times · WSJ · BBC · Guardian · "
            "CoinPaprika · ActiveInvestorMag · HS · WicketPulse · Mint · KCNA · "
            "IANS · JagranJosh · ObserverVoice · Gadgets360 · HK News TV.")
    text_l(d, mx, fy, foot, F_SANSR(27), GREY)
    text_l(d, mx, fy + 34,
           "REPORTED = reported by the sources named on each card. "
           "Pictures and map: original, drawn in code.",
           F_SANSR(27), GREY)
    return img


def finish(img, out_path):
    small = img.resize((1024, 1024), Image.LANCZOS)
    for colors in (256, 192, 128):
        q = small.convert("P", palette=Image.ADAPTIVE, colors=colors)
        q.save(out_path, optimize=True)
        size = os.path.getsize(out_path)
        if size <= 1048576:
            break
    prev = img.resize((300, 300), Image.LANCZOS)
    prev.save(out_path.replace(".png", "-300.png"))
    import hashlib
    data = open(out_path, "rb").read()
    print("wrote", out_path, len(data), "bytes sha256",
          hashlib.sha256(data).hexdigest())
    import struct
    w, h = struct.unpack(">II", data[16:24])
    print("IHDR: %d x %d" % (w, h))
    return len(data)


def main():
    variant = sys.argv[1] if len(sys.argv) > 1 else "A"
    assert variant in ("A", "B")
    img = draw_page(variant)
    out = os.path.join(HERE, "entry-%s.png" % variant)
    finish(img, out)


if __name__ == "__main__":
    main()
