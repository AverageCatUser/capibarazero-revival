# CyberMeow firmware (CapibaraZero re-skin) — T-Embed CC1101

A restyled build of the CapibaraZero firmware for the **LilyGO T-Embed CC1101 / CC1101 Plus**.
This is the stock CapibaraZero v0.5.2 firmware with a reworked home-screen UI and a
turnkey build pipeline that produces a single flashable `.bin`.

---

## What changed

**Real home-screen icons (new)**
- Each tile now has a proper glyph: WiFi, Bluetooth, USB (BadUSB), Sub-GHz tower, NFC, IR remote, JS, and a settings gear. The stock home screen had colour blocks with text only — no icons.
- Icons are 32×32 1-bit bitmaps in `include/icons/home/home_icons.h`, drawn through GFXForms' `Bitmap` widget (white glyph, transparent background).
- They're generated from `tools/gen_icons.py` (edit that and re-run to tweak any glyph).

**UI theme (`lib/UI/style.h`)**
- New cohesive **CyberMeow palette**: teal tiles, magenta selection highlight, cyan status text — replacing the stock raw-magenta-on-black look.
- All colours are pre-computed RGB565 literals (`CM_TEAL`, `CM_MAGENTA`, `CM_CYAN`, …) so they drop into any GFXForms/Adafruit_GFX colour argument.
- Rounder tiles (corner radius 8 → 10).

**Tile widget (`lib/UI/widgets/RectText.hpp` + `.cpp`)**
- Tiles are now drawn as **outlines** with the icon + label inside, and selection **recolours the outline** (teal → magenta). This replaces the stock behaviour of *filling* the box.
- **Bug fix:** the stock firmware filled *deselected* tiles black, so they visually **vanished** as you scrolled the menu. Every tile now stays visible.
- The `radius` and `font_size` constructor arguments are now actually honoured (they were previously ignored and hardcoded to `8` / `2`).
- The widget changes were syntax-checked against the real GFXForms headers, but **not** run on hardware here — the GitHub build (below) is the real verification.

**Build pipeline (`.github/workflows/cybermeow-build.yml`)**
- New workflow that builds **only** the T-Embed target and merges the output into one flashable image, `CyberMeow-TEmbed-factory.bin`.
- The original upstream workflow (`main.yml`) was set to manual-only — its release step needs a secret and an external repo, so it fails on a fork.

> Nothing in the attack/radio code was changed — this is a UI + packaging pass only.

---

## Getting a `.bin`

You have three options. **Option A (GitHub Actions) is the easiest** and needs no toolchain on your machine.

### A. Build it on GitHub (recommended)
1. Push this repo to your GitHub account (`AverageCatUser`), e.g. a repo named `cybermeow-fw`.
2. Open the **Actions** tab → the run titled *Build CyberMeow firmware (T-Embed CC1101)* starts automatically. (Or hit **Run workflow**.)
3. When it's green, open the run and download the **`CyberMeow-TEmbed-firmware`** artifact from the Artifacts section.
4. Inside you get:
   - `CyberMeow-TEmbed-factory.bin` — the single merged image (flash at `0x0`)
   - `bootloader.bin`, `partitions.bin`, `boot_app0.bin`, `firmware.bin` — the individual images

### B. Build it locally
This is a **PlatformIO** project (not Arduino IDE). Two ways:

**B1 — VS Code (easiest, GUI):**
1. Install [VS Code] + the **PlatformIO IDE** extension.
2. Install **GNU Bison** and **Flex** (the JS/Duktape step needs them):
   - Windows: `winget install GnuWin32.Bison GnuWin32.Flex` (or use MSYS2 `pacman -S bison flex`)
   - macOS: `brew install bison flex`
   - Linux: `sudo apt install bison flex`
3. Open this folder in VS Code.
4. Run `bash init_libs.sh` once in the terminal (fetches Duktape).
5. PlatformIO sidebar → **Project Tasks → env:lilygo_t_embed_cc1101 → Build** (and **Upload** with the board plugged in).

**B2 — Command line:**
```bash
pip install platformio          # PlatformIO Core
bash init_libs.sh               # fetch Duktape (needs bison + flex installed)
pio run  -e lilygo_t_embed_cc1101           # build
pio run  -e lilygo_t_embed_cc1101 -t upload # flash (board connected)
```
Output `.bin`s land in `.pio/build/lilygo_t_embed_cc1101/`.

> First build downloads the ESP32-S3 toolchain (~hundreds of MB) and all the
> CapibaraZero attack libs from GitHub — give it a few minutes. If `init_libs.sh`
> can't reach duktape.org, grab `duktape-2.7.0.tar.xz` from the
> [Duktape GitHub releases](https://github.com/svaarala/duktape/releases) and
> extract it to `lib/duktape-2.7.0/` yourself.

### C. Why not a prebuilt .bin in this zip?
The environment this was prepared in blocks the ESP32-S3 toolchain hosts
(`dl.espressif.com`, the PlatformIO registry) and `duktape.org` by policy, so the
firmware couldn't be compiled there. The CI above does the compile on GitHub's
runners, which have open network access.

---

## Flashing

**Offsets** (ESP32-S3, 16 MB):

| File | Offset |
|------|--------|
| bootloader.bin | 0x0 |
| partitions.bin | 0x8000 |
| boot_app0.bin | 0xe000 |
| firmware.bin | 0x10000 |

### Single merged image (simplest)
```bash
esptool.py --chip esp32s3 --port <PORT> --baud 460800 \
  write_flash -z --flash_mode dio --flash_freq 80m --flash_size 16MB \
  0x0 CyberMeow-TEmbed-factory.bin
```

### Or the four separate images
```bash
esptool.py --chip esp32s3 --port <PORT> --baud 460800 \
  write_flash -z --flash_mode dio --flash_freq 80m --flash_size detect \
  0x0 bootloader.bin 0x8000 partitions.bin 0xe000 boot_app0.bin 0x10000 firmware.bin
```

### Or no command line at all
Open https://espressif.github.io/esptool-js/ in Chrome/Edge, connect the board over USB,
add `CyberMeow-TEmbed-factory.bin` at offset `0x0`, and click Program.

---

## Easy next step (optional)
Sub-menus (NFC/IR/SubGHz `List` buttons) still use the stock blue accent
(`ST77XX_BLUE` in `lib/UI/pages/**`). Swapping those for `HOME_ICON_COLOR` makes the
whole UI match the home screen. Left undone on purpose because it spans ~8 files and
wasn't compile-tested here — say the word and I'll do the sweep.
