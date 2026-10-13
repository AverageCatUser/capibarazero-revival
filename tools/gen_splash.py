#!/usr/bin/env python3
"""Generate a CyberMeow cat-head bitmap for the boot splash.
Outputs include/icons/home/splash.h (1-bit, MSB-first) + a preview PNG."""
import math
from PIL import Image, ImageDraw

W, H = 96, 80           # final bitmap size
S = 8                   # supersample
CW, CH = W * S, H * S
FG, BG = 255, 0


def draw_cat():
    img = Image.new("L", (CW, CH), BG)
    d = ImageDraw.Draw(img)
    cx = CW // 2
    # head (rounded)
    hw, hh = int(CW * 0.34), int(CH * 0.33)
    cyc = int(CH * 0.60)
    d.rounded_rectangle([cx - hw, cyc - hh, cx + hw, cyc + hh],
                        radius=int(CW * 0.16), fill=FG)
    # ears (triangles)
    ear = int(CW * 0.16)
    d.polygon([(cx - hw + 6, cyc - hh + 10),
               (cx - hw - ear // 2, cyc - hh - int(CH * 0.26)),
               (cx - int(CW * 0.06), cyc - hh - 4)], fill=FG)
    d.polygon([(cx + hw - 6, cyc - hh + 10),
               (cx + hw + ear // 2, cyc - hh - int(CH * 0.26)),
               (cx + int(CW * 0.06), cyc - hh - 4)], fill=FG)
    # eyes (cut out -> background), slightly angled
    ew, eh = int(CW * 0.075), int(CH * 0.11)
    for sgn in (-1, 1):
        ex = cx + sgn * int(CW * 0.14)
        ey = cyc - int(CH * 0.05)
        d.ellipse([ex - ew, ey - eh, ex + ew, ey + eh], fill=BG)
    # nose
    d.polygon([(cx, cyc + int(CH * 0.10)),
               (cx - int(CW * 0.04), cyc + int(CH * 0.04)),
               (cx + int(CW * 0.04), cyc + int(CH * 0.04))], fill=BG)
    # whiskers (cut)
    for sgn in (-1, 1):
        base_x = cx + sgn * int(CW * 0.10)
        for k, dy in enumerate((-6, 6)):
            d.line([(base_x, cyc + int(CH * 0.10) + dy),
                    (cx + sgn * int(CW * 0.46), cyc + int(CH * 0.02) + dy * 3)],
                   fill=BG, width=5)
    return img.resize((W, H), Image.LANCZOS).point(
        lambda p: 255 if p >= 120 else 0, mode="L")


def pack_msb(img):
    bytew = (W + 7) // 8
    data = bytearray(bytew * H)
    px = img.load()
    for y in range(H):
        for x in range(W):
            if px[x, y] >= 128:
                data[y * bytew + (x >> 3)] |= (0x80 >> (x & 7))
    return data


def main():
    import os
    img = draw_cat()
    data = pack_msb(img)
    vals = ["0x%02x" % v for v in data]
    lines = ['#include "Arduino.h"', "", "#ifndef CM_SPLASH_H",
             "#define CM_SPLASH_H", "",
             "#define CM_CAT_W %d" % W, "#define CM_CAT_H %d" % H, "",
             "const uint8_t cm_cat[] = {"]
    for i in range(0, len(vals), 12):
        lines.append("    " + ", ".join(vals[i:i + 12]) + ",")
    lines += ["};", "", "#endif"]
    os.makedirs("include/icons/home", exist_ok=True)
    with open("include/icons/home/splash.h", "w") as f:
        f.write("\n".join(lines))
    print("wrote include/icons/home/splash.h")
    # preview (magenta cat on black)
    prev = Image.new("RGB", (W * 3, H * 3), (0, 0, 0))
    big = img.resize((W * 3, H * 3), Image.NEAREST)
    mag = Image.new("RGB", big.size, (255, 46, 136))
    prev.paste(mag, (0, 0), big)
    prev.save("tools/splash_preview.png")
    print("wrote tools/splash_preview.png")


if __name__ == "__main__":
    main()
