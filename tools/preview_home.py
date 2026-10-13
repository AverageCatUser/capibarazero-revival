#!/usr/bin/env python3
"""Render a representative preview of the CyberMeow home screen using the real
generated glyphs and the actual outline-tile design."""
from PIL import Image, ImageDraw, ImageFont
import gen_icons as gi

TEAL = (10, 184, 208)
MAGENTA = (255, 46, 136)
CYAN = (95, 211, 224)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# order matches MainPage grid: wifi, ble, badusb, subghz / nfc, ir, js, settings
TILES = [
    ("wifi", "WiFi", gi.icon_wifi),
    ("ble", "BLE", gi.icon_ble),
    ("badusb", "BadUSB", gi.icon_usb),
    ("subghz", "SubGHz", gi.icon_subghz),
    ("nfc", "NFC", gi.icon_nfc),
    ("ir", "IR", gi.icon_ir),
    ("js", "JS", gi.icon_js),
    ("settings", "Settings", gi.icon_settings),
]
SELECTED = 0  # WiFi selected (lower_limit)


def glyph_rgba(fn, size, color):
    """Return an RGBA image of the 1-bit glyph in `color` on transparent bg."""
    bits = gi.to_1bit(fn()).resize((size, size), Image.NEAREST)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    px = bits.load()
    op = out.load()
    for y in range(size):
        for x in range(size):
            if px[x, y] >= 128:
                op[x, y] = color + (255,)
    return out


def main():
    SCALE = 2.4
    SW, SH = int(320 * SCALE), int(170 * SCALE)  # screen px
    MX, MY_TOP = 40, 92
    W, H = SW + 2 * MX, SH + MY_TOP + 40

    img = Image.new("RGB", (W, H), (12, 15, 20))
    d = ImageDraw.Draw(img)
    f_title = ImageFont.truetype(FONT, 22)
    f_sub = ImageFont.truetype(FONT, 13)
    f_lbl = ImageFont.truetype(FONT, int(16 * SCALE / 2.0))
    f_foot = ImageFont.truetype(FONT, int(13 * SCALE / 1.6))

    d.text((W / 2, 30), "CYBERMEOW  ·  HOME", font=f_title, fill=CYAN, anchor="mm")
    d.text((W / 2, 58), "LilyGO T-Embed CC1101 · real icons · outline tiles, magenta = selected",
           font=f_sub, fill=(125, 136, 148), anchor="mm")

    # screen
    sx, sy = MX, MY_TOP
    d.rounded_rectangle([sx - 14, sy - 14, sx + SW + 14, sy + SH + 14],
                        radius=22, fill=(26, 29, 34), outline=BLACK, width=2)
    d.rectangle([sx, sy, sx + SW, sy + SH], fill=BLACK)

    cols, rows = 4, 2
    pad_x = int(10 * SCALE)
    cell_w = (SW - (cols + 1) * pad_x) // cols
    box_h = int(50 * SCALE)
    lbl_h = int(24 * SCALE)
    pad_y = int(12 * SCALE)
    icon_px = int(32 * SCALE * 0.7)

    for i, (key, label, fn) in enumerate(TILES):
        r, c = divmod(i, cols)
        bx = sx + pad_x + c * (cell_w + pad_x)
        by = sy + pad_y + r * (box_h + lbl_h + pad_y)
        col = MAGENTA if i == SELECTED else TEAL
        # outline tile
        d.rounded_rectangle([bx, by, bx + cell_w, by + box_h],
                            radius=int(10 * SCALE / 1.5), outline=col, width=3)
        # icon centred in box (white)
        g = glyph_rgba(fn, icon_px, WHITE)
        img.paste(g, (bx + (cell_w - icon_px) // 2, by + (box_h - icon_px) // 2), g)
        # label under box
        d.text((bx + cell_w / 2, by + box_h + lbl_h / 2), label,
               font=f_lbl, fill=WHITE, anchor="mm")

    # status strip just under the screen (kept off the tile labels)
    d.text((sx, sy + SH + 20), "CyberMeow v0.5.2", font=f_foot, fill=CYAN)
    d.text((sx + SW, sy + SH + 20), "BAT 100%", font=f_foot, fill=CYAN, anchor="ra")

    img.save("ui_preview.png")
    print("wrote ui_preview.png", img.size)


if __name__ == "__main__":
    main()
