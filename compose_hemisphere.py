#!/usr/bin/env python3
"""THE HEMISPHERE — NI24 Final 4 (wildonaped). Fresh compose, wave 2.
Deep purple + silver. Layout B: wide lead. All figures from ni24-pool.md."""
import os, sys
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FD = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)
PF_BLACK = "PlayfairDisplay-Black.ttf"
PF_IT = "PlayfairDisplay-Italic.ttf"
AR = "Archivo.ttf"
AR_B = "Archivo-Bold.ttf"

INK = (26, 18, 38)
PURPLE = (43, 24, 74)
PURPLE_D = (30, 16, 54)
SILVER = (198, 202, 214)
SILVER_L = (232, 234, 240)
PAPER = (244, 241, 233)
CARD = (252, 250, 244)
RED = (178, 32, 44)
TEAL = (16, 110, 110)
GOLD = (176, 128, 20)
BLUE = (30, 84, 160)
GREEN = (34, 120, 62)
GREY = (92, 92, 100)

REGION_COLORS = {
    "EUROPE": (30, 84, 160), "MIDDLE EAST": (178, 32, 44), "AFRICA": (176, 128, 20),
    "AMERICAS": (34, 120, 62), "ASIA": (140, 40, 130), "SOUTH ASIA": (200, 100, 20),
    "ASIA-PACIFIC": (16, 110, 110), "OCEANIA": (70, 90, 180), "WORLD": (92, 92, 100),
}

# num, region, place, headline lines, deck lines, source tag, chip, motif
CARDS = [
 (1, "EUROPE", "KYIV REGION, UKRAINE",
  ["Russian strikes kill at least 15", "near Kyiv; 11 die in Dymer flats"],
  ["Kyiv strikes: 11 killed in a block of flats in Dymer;", "drone hit a 6-floor Kyiv block, 5 injured. Zelenskyy:"],
  ['"for us, he\'s a killer" — on Putin, to CNN.'],
  "Times/AP · REPORTED", "15 KILLED / 11 DYMER", "city"),
 (2, "MIDDLE EAST", "WASHINGTON / TEHRAN",
  ["US sanctions ~30 Iran-linked", "exchange houses in one sweep"],
  ["Iran sanctions hit ~30 exchange houses + executives,", "the core of shadow banking dodging bank sanctions."],
  ["Treasury, Mon 23 Nov; Rubio meets Qatar PM."],
  "AP/Treasury · REPORTED", "~30 SANCTIONED", "bank"),
 (3, "MIDDLE EAST", "GAZA CITY",
  ["Israeli strikes kill 3 in Gaza,", "UNRWA employee among the dead"],
  ["3 killed Mon in separate Gaza strikes, incl. a UNRWA", "employee; Shifa Hospital + agency confirm the toll."],
  ["Ceasefire lines hold elsewhere; aid queues grow."],
  "AP · REPORTED", "3 KILLED", "dome"),
 (4, "EUROPE", "BENGHAZI, LIBYA",
  ["Ukraine sinks Russian warship", "Merkury off Benghazi — 7 sea drones"],
  ["7 sea drones launched; Steregushchiy-class Merkury", "sunk at Benghazi; Ka-27 helicopter destroyed aboard;"],
  ["MV Angara hit. SBU: 'Syrian Express' supply line."],
  "CNN/AP · REPORTED", "MERKURY SUNK", "ship"),
 (5, "WORLD", "ANTALYA, TURKIYE",
  ["COP31 ends with NO DEAL —", "first no-deal COP since 2000"],
  ["Antalya Pact NOT adopted; final text dropped fossil", "fuels entirely. 44 h overtime — longest COP ever."],
  [">90 states signed the electrification side pledge."],
  "Times/Guardian · REPORTED", "NO DEAL / SINCE 2000", "globe"),
 (6, "AMERICAS", "NEW YORK",
  ["Nvidia brings back Jensen Huang", "as CEO — shares leap +31%"],
  ["Board reinstates Huang Mon after Trump intervened;", "Huang had quit 12 Nov. Nasdaq +6%, chips +12%."],
  ["One of the wildest days in US market history."],
  "Reuters · REPORTED", "+31% / HUANG BACK", "chip"),
 (7, "AMERICAS", "GLOBAL MARKETS",
  ["Gold rebounds 1.5% to $3,588", "after worst week in 8 months"],
  ["Gold 3588 an ounce, off a 14-month low; traders await", "US PCE inflation report due 25 Nov. 10-yr ~4.96%."],
  ["Fed hike bets keep bullion buyers cautious."],
  "Reuters · REPORTED", "$3,588/OZ", "chart"),
 (8, "WORLD", "CRYPTO MARKETS",
  ["Bitcoin steadies at $61,284", "as liquidation storm eases"],
  ["Bitcoin 61284 Mon 12:52 UTC, +1.1% in 24 h, -4.5% in", "7 d; weekend low ~$55,100. Kraken CAD flash crash"],
  ["to ~$17,000 equivalent Sat — trades stand."],
  "CoinPaprika · REPORTED", "$61,284", "coin"),
 (9, "AMERICAS", "LOS ANGELES",
  ["GTA VI takes $3.8bn on day one —", "biggest launch in entertainment"],
  ["GTA VI's $3.8bn first day passes every game launch", "and every single-day film box office on record."],
  ["Rockstar's decade-long wait ends in a record."],
  "ActiveInvestorMag · REPORTED", "$3.8BN DAY ONE", "game"),
 (10, "EUROPE", "LIVERPOOL",
  ["Liverpool 4-0 Man Utd;", "Pochettino debut turns to disaster"],
  ["Yoro sent off in the 8th minute; United down to 10.", "Loss leaves United 19th in the league, 8 points."],
  ["Anfield sings as the rout completes a grim week."],
  "Mint/NextSports · REPORTED", "4-0", "pitch"),
 (11, "AMERICAS", "WASHINGTON",
  ["Democrats 258-173: biggest House", "majority since 1992"],
  ["Democrats 258 seats after the North Carolina pickup;", "Trump offers to work with Democrats 258 on card"],
  ["rate caps. Van Hollen challenges Schumer, 1 Dec."],
  "BBC · REPORTED", "258-173", "capitol"),
 (12, "OCEANIA", "WELLINGTON",
  ["Wellington Test DRAWN: NZ bat", "out the day at 239/5 vs India"],
  ["Mitchell 49* off 186 balls, Phillips 26* off 126;", "63-run stand, 258 balls. India 720/9d, lead 352."],
  ["2nd Test Christchurch 27 Nov-1 Dec."],
  "HS/WicketPulse · REPORTED", "DRAW / 239/5", "cricket"),
 (13, "EUROPE", "GULF OF FINLAND",
  ["Sparta II towed clear: 121 m ship,", "16 crew off after 2 drone hits"],
  ["Sparta II, 121 m, hit by 2 drones Sat; Finland led the", "Loviisa rescue, all 16 crew off, towed out Sun night."],
  ["PM Orpo: 'Ukraine has the right to fight back.'"],
  "Reuters/Times · REPORTED", "121 M / CREW SAFE", "ship2"),
]

BRIEFS = [
 (14, "AFRICA", "Congo halts cobalt exports from 30 Nov, top producer fights oversupply — Reuters"),
 (15, "ASIA", "KCNA: North Korea weighs shutting Swiss office in Pyongyang — Reuters, Tue 04:24 WIB"),
 (16, "ASIA-PACIFIC", "Indonesia: 24 killed in factory blaze, dozens still missing — Reuters"),
 (17, "ASIA-PACIFIC", "Hong Kong curbs drones + Wan Chai roads for Interpol summit 30 Nov-3 Dec — HK News TV"),
 (18, "SOUTH ASIA", "Nepal PM Balendra Shah ends Delhi state visit, met Modi Monday — IANS"),
 (19, "SOUTH ASIA", "India weighs rice export duties as domestic prices climb — Reuters"),
 (20, "MIDDLE EAST", "Strike kills 11 in western Yemen, 19 wounded; Houthis blame Riyadh-backed force — AP"),
 (21, "MIDDLE EAST", "US discussing military training for Syrian forces, first since 2024 — Reuters"),
 (22, "AMERICAS", "FBI probe: FBI probes hack of its crime database; WA pauses dealer checks — AP"),
 (23, "WORLD", "Solana launches solana.ai, platform for autonomous AI agents — Gadgets360"),
 (24, "WORLD", "UN AI weapons: UN states agree to keep negotiating lethal AI weapons — salonvision"),
 (25, "AMERICAS", "Miley Cyrus marries Maxx Morando in California — BBC/Reuters"),
 (26, "AMERICAS", "CrowdStrike snaps up Zscaler in $44bn deal as cyber threats mount — Reuters"),
 (27, "ASIA", "KOSPI falls ~3% Monday to a 10-month low; Taiwan steadies — Reuters"),
 (28, "EUROPE", "Euro zone growth holds steady, PMI 51.7 in November, fifth month up — Reuters"),
 (29, "EUROPE", "Thousands march in Lisbon over the cost of living — JagranJosh"),
 (30, "EUROPE", "UK-EU Brexit reset deal: Burnham calls it 'landmark' in parliament — BBC"),
 (31, "SOUTH ASIA", "India-EU free-trade pact likely signed 16 Dec in Brussels — JagranJosh"),
 (32, "SOUTH ASIA", "Tata Steel sells pipe business to APL Apollo, Rs 28,000 crore — ObserverVoice"),
 (33, "AMERICAS", "FORECAST: US PCE inflation report due 25 Nov, next clue on Fed rates — AP wire"),
 (34, "OCEANIA", "FORECAST: 2nd Test India vs New Zealand, Christchurch, 27 Nov-1 Dec — HS"),
 (35, "AMERICAS", "Senate: Van Hollen challenges Schumer for leader, secret ballot 1 Dec — AIM"),
 (36, "AMERICAS", "Mets + A.J. Ewing agree $95m, 8-year deal — AP wire"),
 (37, "AMERICAS", "US Army to detonate lead stockpile in Iowa: 68 barrels, ~10,000 lb — Reuters"),
]

REGIONS = [("EUROPE", 7), ("MIDDLE EAST", 4), ("AFRICA", 1), ("AMERICAS", 11),
           ("ASIA", 2), ("SOUTH ASIA", 4), ("ASIA-PACIFIC", 2), ("OCEANIA", 2), ("WORLD", 4)]

NUMBERS = [("15", "KILLED NEAR KYIV"), ("11", "DIED IN DYMER"), ("$3,588", "GOLD / OZ"),
           ("$61,284", "BITCOIN"), ("+31%", "NVIDIA / HUANG"), ("258-173", "US HOUSE"),
           ("4-0", "LIVERPOOL"), ("$3.8BN", "GTA VI DAY 1")]

TIMELINE = [
 ("04:24 WIB TUE", "KCNA: North Korea weighs closing Swiss office — Reuters"),
 ("MON PM NEW YORK = TUE AM WIB", "Huang reinstated at Nvidia; shares +31% — Reuters"),
 ("MON PM WASHINGTON = TUE AM WIB", "Treasury sanctions ~30 Iran exchange houses — AP"),
 ("MON PM GAZA = TUE AM WIB", "Strikes kill 3 in Gaza incl. UNRWA worker — AP"),
 ("MON PM LIVERPOOL = TUE AM WIB", "Liverpool 4-0 Man Utd; Yoro off 8' — Mint"),
 ("TUE AM WELLINGTON NZDT", "NZ 239/5: Wellington draw banked vs India — HS"),
]

DATECHECK = [
 "D1 - 186-drone night over Ukraine, 161 downed - Fri 21-Sun 22 Nov (was NI22's lead)",
 "D3 - Alcaraz beats Zverev 6-2, 7-6, first ATP Finals title - Sun 22 Nov",
 "D4 - Verstappen wins Las Vegas Grand Prix - Sun 22 Nov",
 "D5 - Wembanyama scores 50, Spurs 114-91 Pelicans - Sun 22 Nov",
 "D9 - Ukraine strike on Kerch Bridge - reported Sun 22 Nov",
 "D14 - Nvidia SEC probe, first reported - Fri 20 Nov",
 "D17 - Huang resigns as Nvidia CEO after affair admission - Thu 12 Nov",
]

MAP_ROWS = [
 "....##..........##########......##..####................",
 "..#######......##############..##########.....##..........",
 "...#####........##########......########....######........",
 "....###..........########........######......####.........",
 ".....#............######..........####........##..........",
 "...................####............##.....................",
 "......##...........###....................................",
 ".....####..........##.............##..........##..........",
 "....######..................................######........",
 ".....####............##....................########.......",
 "......##............####......................####........",
 "...................######.................................",
]
PINS = [(1, 27, 1), (4, 24, 4), (13, 28, 0), (10, 25, 1), (5, 30, 3),
        (2, 34, 4), (3, 33, 5), (6, 6, 2), (11, 7, 3), (12, 52, 9)]


def scene(d, box, motif, accent):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle(box, fill=(38, 30, 58))
    d.rectangle([x0, y1 - int(h * 0.28), x1, y1], fill=(58, 48, 84))
    cx, cy = x0 + w // 2, y0 + h // 2
    if motif in ("ship", "ship2"):
        d.rectangle([x0, y1 - int(h * 0.30), x1, y1], fill=(24, 70, 110))
        for i in range(4):
            d.arc([x0 + 6 + i * 22, y1 - 12, x0 + 24 + i * 22, y1 - 2], 0, 180, fill=SILVER, width=2)
        d.polygon([(x0 + 14, y0 + int(h * 0.62)), (x1 - 10, y0 + int(h * 0.62)),
                   (x1 - 20, y1 - int(h * 0.30)), (x0 + 24, y1 - int(h * 0.30))], fill=(150, 40, 48))
        d.rectangle([cx - 16, y0 + int(h * 0.34), cx + 20, y0 + int(h * 0.62)], fill=SILVER)
        d.rectangle([cx + 2, y0 + int(h * 0.16), cx + 8, y0 + int(h * 0.34)], fill=SILVER_L)
        d.ellipse([x1 - 30, y0 + 6, x1 - 16, y0 + 20], fill=(240, 200, 60))
    elif motif == "city":
        for i, bh in enumerate((0.55, 0.8, 0.65, 0.9, 0.5)):
            bx = x0 + 6 + i * (w // 5)
            d.rectangle([bx, y1 - int(h * bh), bx + w // 6, y1 - int(h * 0.28)], fill=(90, 84, 120))
            for r in range(3):
                d.rectangle([bx + 4, y1 - int(h * bh) + 5 + r * 9, bx + 10, y1 - int(h * bh) + 9 + r * 9], fill=(240, 200, 90))
        d.polygon([(x1 - 26, y0 + 8), (x1 - 14, y0 + 22), (x1 - 30, y0 + 24)], fill=(240, 120, 50))
    elif motif == "bank":
        for i in range(4):
            bx = x0 + 12 + i * (w // 4)
            d.rectangle([bx, y0 + int(h * 0.3), bx + 8, y1 - int(h * 0.3)], fill=SILVER)
        d.polygon([(x0 + 6, y0 + int(h * 0.3)), (cx, y0 + 6), (x1 - 6, y0 + int(h * 0.3))], fill=SILVER_L)
        d.rectangle([x0 + 6, y1 - int(h * 0.3), x1 - 6, y1 - int(h * 0.22)], fill=SILVER)
    elif motif == "dome":
        d.pieslice([cx - 26, y0 + int(h * 0.28), cx + 26, y0 + int(h * 0.95)], 180, 360, fill=(210, 180, 90))
        d.rectangle([cx - 30, y0 + int(h * 0.6), cx + 30, y1 - int(h * 0.26)], fill=(200, 190, 170))
        d.rectangle([cx - 2, y0 + int(h * 0.12), cx + 2, y0 + int(h * 0.3)], fill=(210, 180, 90))
    elif motif == "globe":
        d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=SILVER_L, width=3)
        d.ellipse([cx - 10, cy - 26, cx + 10, cy + 26], outline=SILVER, width=2)
        d.line([cx - 26, cy, cx + 26, cy], fill=SILVER, width=2)
        d.polygon([(x0 + 8, y1 - 14), (x0 + 22, y0 + 16), (x0 + 30, y1 - 14)], fill=(90, 160, 90))
    elif motif == "chip":
        d.rectangle([cx - 24, cy - 18, cx + 24, cy + 18], fill=(60, 130, 200), outline=SILVER_L, width=2)
        d.rectangle([cx - 10, cy - 8, cx + 10, cy + 8], fill=(240, 200, 60))
        for i in range(3):
            d.line([cx - 24, cy - 10 + i * 10, x0 + 8, cy - 10 + i * 10], fill=SILVER, width=2)
            d.line([cx + 24, cy - 10 + i * 10, x1 - 8, cy - 10 + i * 10], fill=SILVER, width=2)
    elif motif == "chart":
        pts = [(x0 + 8, y1 - 16), (x0 + 26, y1 - 24), (x0 + 44, y1 - 18), (x0 + 62, y0 + 14), (x1 - 8, y0 + 8)]
        d.line(pts, fill=(240, 200, 60), width=4)
        for px, py in pts:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(240, 200, 60))
    elif motif == "coin":
        d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=(240, 170, 40), outline=(200, 140, 20), width=3)
        d.text((cx, cy), "B", font=F(AR_B, 30), fill=(90, 60, 0), anchor="mm")
    elif motif == "game":
        d.rectangle([x0 + 12, y0 + 14, x1 - 12, y1 - 14], fill=(30, 30, 36), outline=SILVER_L, width=2)
        d.polygon([(cx - 14, cy - 8), (cx - 14, cy + 8), (cx + 2, cy)], fill=(240, 80, 90))
        d.rectangle([cx + 8, cy - 3, cx + 26, cy + 3], fill=SILVER)
    elif motif == "pitch":
        d.rectangle([x0 + 6, y0 + 8, x1 - 6, y1 - 8], fill=(30, 110, 55), outline=SILVER_L, width=2)
        d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], outline=SILVER_L, width=2)
        d.line([cx, y0 + 8, cx, y1 - 8], fill=SILVER_L, width=2)
    elif motif == "capitol":
        d.pieslice([cx - 22, y0 + int(h * 0.18), cx + 22, y0 + int(h * 0.62)], 180, 360, fill=SILVER_L)
        for i in range(4):
            bx = x0 + 14 + i * (w // 4)
            d.rectangle([bx, y0 + int(h * 0.52), bx + 7, y1 - int(h * 0.28)], fill=SILVER)
        d.rectangle([x0 + 8, y1 - int(h * 0.28), x1 - 8, y1 - int(h * 0.2)], fill=SILVER_L)
    elif motif == "cricket":
        d.polygon([(cx - 4, y0 + 10), (cx + 4, y0 + 10), (cx + 2, y1 - 12), (cx - 2, y1 - 12)], fill=(230, 200, 140))
        d.ellipse([x1 - 28, y0 + 10, x1 - 14, y0 + 24], fill=(200, 40, 50))
        d.rectangle([x0 + 10, y1 - 20, x0 + 34, y1 - 12], fill=(240, 200, 60))
    d.rectangle([x0, y1 - 13, x1, y1], fill=accent)
    return

def draw_card(d, card, x, y, w, h, scene_w=104, mode="grid"):
    num, region, place, head, deck, deck2, src, chip, motif = card
    accent = REGION_COLORS[region]
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=(180, 174, 160), width=1)
    scene(d, (x + 3, y + 3, x + scene_w, y + h - 3), motif, accent)
    tx = x + scene_w + 10
    d.ellipse([x + 6, y + 6, x + 28, y + 28], fill=accent)
    d.text((x + 17, y + 17), str(num), font=F(AR_B, 14), fill=(255, 255, 255), anchor="mm")
    if mode == "grid":
        d.text((tx, y + 3), f"{place} · {region}", font=F(AR_B, 9), fill=accent)
        cw = d.textlength(chip, font=F(AR_B, 9))
        d.rectangle([x + w - cw - 14, y + 3, x + w - 4, y + 15], fill=accent)
        d.text((x + w - cw - 9, y + 5), chip, font=F(AR_B, 9), fill=(255, 255, 255))
        yy = y + 15
        for ln in head:
            d.text((tx, yy), ln, font=F(AR_B, 14), fill=INK)
            yy += 15
        for ln in (deck + deck2)[:2]:
            d.text((tx, yy), ln[:64], font=F(AR, 9), fill=(50, 46, 58))
            yy += 11
        d.text((x + w - 6, y + h - 12), src, font=F(AR_B, 8), fill=GREY, anchor="ra")
    else:
        d.text((tx, y + 5), f"{place} · {region}", font=F(AR_B, 10), fill=accent)
        yy = y + 19
        hf = 16 if h >= 100 else 15
        for ln in head:
            d.text((tx, yy), ln, font=F(AR_B, hf), fill=INK)
            yy += 18 if h >= 100 else 16
        for ln in (deck + deck2)[:2]:
            d.text((tx, yy), ln, font=F(AR, 10), fill=(50, 46, 58))
            yy += 11.5
        if h >= 100:
            d.rectangle([tx, y + h - 16, tx + d.textlength(chip, font=F(AR_B, 10)) + 10, y + h - 3], fill=accent)
            d.text((tx + 5, y + h - 14), chip, font=F(AR_B, 10), fill=(255, 255, 255))
            sx = tx + d.textlength(chip, font=F(AR_B, 10)) + 18
            d.text((sx, y + h - 14), src, font=F(AR_B, 9), fill=GREY)
        else:
            cw = d.textlength(chip, font=F(AR_B, 9))
            d.rectangle([x + w - cw - 14, y + 4, x + w - 4, y + 16], fill=accent)
            d.text((x + w - cw - 9, y + 6), chip, font=F(AR_B, 9), fill=(255, 255, 255))
            d.text((x + w - 6, y + h - 12), src, font=F(AR_B, 8), fill=GREY, anchor="ra")

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = wd
    if cur:
        lines.append(cur)
    return lines

def build(variant, out):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # kicker
    d.rectangle([0, 0, W, 28], fill=PURPLE_D)
    d.text((512, 14), "37 STORIES · 9 REGIONS · EVERY ONE DATED TUESDAY 24 NOVEMBER 2026",
           font=F(AR_B, 14), fill=SILVER_L, anchor="mm")
    # masthead
    d.rectangle([0, 28, W, 98], fill=PURPLE)
    d.text((20, 30), "THE HEMISPHERE", font=F(PF_BLACK, 44), fill=SILVER_L)
    d.text((1004, 44), "ONE PAGE · THE WHOLE DAY", font=F(PF_IT, 15), fill=SILVER, anchor="ra")
    d.text((1004, 64), "Tuesday's world, drawn & dated", font=F(PF_IT, 13), fill=SILVER, anchor="ra")
    d.text((20, 82), "TUESDAY 24 NOVEMBER 2026", font=F(AR_B, 13), fill=(240, 200, 90))
    # number strip
    y = 98
    d.rectangle([0, y, W, y + 38], fill=(240, 236, 224))
    nw = W // len(NUMBERS)
    for i, (big, lab) in enumerate(NUMBERS):
        cx = i * nw + nw // 2
        d.text((cx, y + 3), big, font=F(AR_B, 20), fill=PURPLE_D, anchor="ma")
        d.text((cx, y + 26), lab, font=F(AR_B, 8), fill=GREY, anchor="ma")
        if i:
            d.line([i * nw, y + 5, i * nw, y + 33], fill=(200, 195, 180), width=1)
    # region strip (min segment 48 px, rescaled)
    y += 42
    total = sum(c for _, c in REGIONS)
    segs = [max(48, int(W * c / total)) for _, c in REGIONS]
    scale = W / sum(segs)
    segs = [int(s * scale) for s in segs]
    x = 0
    for (name, cnt), seg in zip(REGIONS, segs):
        d.rectangle([x, y, x + seg, y + 18], fill=REGION_COLORS[name])
        d.text((x + seg // 2, y + 9), f"{name} {cnt}", font=F(AR_B, 7.5), fill=(255, 255, 255), anchor="mm")
        x += seg
    # timeline — one line per slot, explicit zones
    y += 22
    d.rectangle([0, y, W, y + 30], fill=PURPLE_D)
    for i, (tm, ev) in enumerate(TIMELINE):
        col, row = i % 3, i // 3
        tx, ty = 10 + col * 340, y + 4 + row * 13
        d.text((tx, ty), f"{tm} — {ev}"[:80], font=F(AR, 8), fill=SILVER_L)
    # leads — Layout B: wide lead + two halves (variant B swaps wide lead)
    y += 34
    by = {c[0]: c for c in CARDS}
    if variant == "A":
        wide, halves = by[1], [by[2], by[3]]
    else:
        wide, halves = by[2], [by[1], by[3]]
    draw_card(d, wide, 8, y, W - 16, 100, scene_w=200, mode="lead")
    y += 104
    draw_card(d, halves[0], 8, y, (W - 24) // 2, 80, scene_w=110, mode="lead")
    draw_card(d, halves[1], 16 + (W - 24) // 2, y, (W - 24) // 2, 80, scene_w=110, mode="lead")
    y += 84
    # grid of 10
    grid = [by[i] for i in range(4, 14)]
    if variant == "B":
        grid = grid[::-1]
    gh, gw = 70, (W - 24) // 2
    for i, c in enumerate(grid):
        gx = 8 + (i % 2) * (gw + 8)
        gy = y + (i // 2) * (gh + 3)
        draw_card(d, c, gx, gy, gw, gh, scene_w=84, mode="grid")
    y += 5 * (gh + 3) + 2
    # map + date check
    mh = 84
    d.rectangle([8, y, 500, y + mh], fill=(18, 24, 54))
    d.text((16, y + 4), "WHERE IT HAPPENED — pins match story numbers", font=F(AR_B, 10), fill=SILVER_L)
    cw = (500 - 24) / 58.0
    for r, row in enumerate(MAP_ROWS):
        for ci, ch in enumerate(row):
            if ch == "#":
                px, py = 16 + ci * cw, y + 20 + r * 5
                d.ellipse([px, py, px + 3, py + 3], fill=(120, 150, 220))
    for num, ci, ri in PINS:
        px, py = 16 + ci * cw, y + 20 + ri * 5
        d.ellipse([px - 6, py - 6, px + 7, py + 7], fill=RED)
        d.text((px, py), str(num), font=F(AR_B, 8), fill=(255, 255, 255), anchor="mm")
    d.rectangle([508, y, W - 8, y + mh], fill=(250, 232, 230), outline=RED, width=2)
    d.text((516, y + 4), "DATE CHECK — NAMED & DATED, NOT TODAY'S NEWS", font=F(AR_B, 11), fill=RED)
    yy = y + 19
    for ln in DATECHECK:
        d.text((516, yy), ln, font=F(AR, 8.5), fill=(90, 30, 30))
        yy += 9.5
    d.text((516, yy + 1), "Tonight's real count: 7 sea drones, at the top of this page.",
           font=F(AR_B, 9), fill=RED)
    y += mh + 6
    # also on
    d.text((8, y), "ALSO ON TUESDAY — BRIEFS 14-37", font=F(AR_B, 12), fill=PURPLE_D)
    y += 16
    colw = (W - 24) // 2
    for i, (num, region, text) in enumerate(BRIEFS):
        col, row = i // 12, i % 12
        bx, byy = 8 + col * (colw + 8), y + row * 10
        d.text((bx, byy), f"{num}.", font=F(AR_B, 9), fill=REGION_COLORS[region])
        lines = wrap(d, text, F(AR, 9), colw - 26)
        d.text((bx + 24, byy), lines[0] if lines else "", font=F(AR, 9), fill=INK)
    y += 12 * 10 + 4
    # footer
    d.line([8, y, W - 8, y], fill=PURPLE, width=2)
    d.text((8, y + 4),
           "Sources: Reuters · AP · BBC · CNN · Times · WSJ · Guardian · CoinPaprika · HS/WicketPulse · IANS · Gadgets360 · HK News TV · JagranJosh · ObserverVoice · salonvision · Mint · ActiveInvestorMag",
           font=F(AR, 9), fill=GREY)
    d.text((8, y + 16),
           "Tags: REPORTED = confirmed by named source. Every story first reported 23-24 Nov 2026. Pictures and map: original, drawn in code.",
           font=F(AR_B, 9), fill=PURPLE_D)
    img.save(out, optimize=True)
    return out

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    a = build("A", os.path.join(outdir, "variantA.png"))
    b = build("B", os.path.join(outdir, "variantB.png"))
    for p in (a, b):
        im = Image.open(p)
        im.resize((300, 300)).save(p.replace(".png", "-300.png"))
        print(p, im.size, os.path.getsize(p))
