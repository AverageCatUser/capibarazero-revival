/*
 * This file is part of the Capibara zero (https://github.com/CapibaraZero/fw or
 * https://capibarazero.github.io/). Copyright (c) 2024 Andrea Canale.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, version 3.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 */

#include <Adafruit_ST77xx.h>

#ifndef STYLE_H
#define STYLE_H

/*
 * CyberMeow theme (RGB565)
 * ------------------------
 * A cohesive teal + magenta palette replacing the stock magenta-on-black look.
 * Tiles are a vivid teal; the selected tile pops in magenta so the cursor is
 * always obvious. Colours are pre-computed RGB565 literals so they work with
 * any Adafruit_GFX / GFXForms colour argument.
 */
#define CM_BLACK   0x0000  // true black background
#define CM_WHITE   0xFFFF  // labels
#define CM_TEAL    0x0DDA  // #0AB8D0 - default tile colour
#define CM_MAGENTA 0xF971  // #FF2E88 - selected tile highlight
#define CM_CYAN    0x5E9C  // #5FD3E0 - secondary / info text

// Per-tile accent colours (each home tile gets its own hue for personality)
#define CM_WIFI      0x2CDF  // azure
#define CM_BLE       0x163A  // cyan
#define CM_BADUSB    0x3E8A  // green
#define CM_SUBGHZ    0xFD80  // amber
#define CM_NFC       0x9B7E  // violet
#define CM_IR        0xFAC7  // red-orange
#define CM_JS        0xFE83  // yellow
#define CM_SETTINGS  0x9D37  // slate

#define HOME_BACKGROUND_COLOR CM_BLACK    // Home background color
#define HOME_TEXT_COLOR CM_WHITE          // Icon description color
#define HOME_ICON_COLOR CM_TEAL           // Default (unselected) tile color
#define HOME_SELECT_COLOR CM_MAGENTA      // Selected tile highlight color
#define HOME_INFO_COLOR CM_CYAN           // Home info text color (battery/version)
#define HOME_ICON_RADIUS 10               // Home icon corner radius
#define HOME_ICON_HEIGHT 50               // Home icon height
#define HOME_TEXT_SIZE 2                  // Home text size

#endif