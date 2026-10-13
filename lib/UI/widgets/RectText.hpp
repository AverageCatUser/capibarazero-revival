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

#include <Arduino.h>

#include "Bitmap.hpp"
#include "GFXForms.hpp"
#include "Grid.hpp"
#include "Rect.hpp"
#include "Text.hpp"
#include "style.h"

#ifndef RECT_TEXT_H
#define RECT_TEXT_H

class RectText : public Widget {
 private:
  Rect *box;
  Text *text_widget;
  Grid *container;
  Bitmap *icon_widget = nullptr;              // optional glyph (white, on black)
  uint16_t base_color = HOME_ICON_COLOR;      // tile outline when not selected
  uint16_t select_color = HOME_SELECT_COLOR;  // tile outline when selected
  uint8_t icon_w = 0;
  uint8_t icon_h = 0;

  // Centre the glyph on the tile box. Must run after the box has been laid
  // out/displayed so its geometry is valid. Tiles are drawn as outlines (the
  // interior stays the black background), so the Bitmap widget's background
  // repaint is invisible and the glyph always renders cleanly.
  void draw_icon() {
    if (icon_widget == nullptr || box == nullptr) return;
    int ix = box->get_x() + (box->get_width() - icon_w) / 2;
    int iy = box->get_y() + (box->get_heigth() - icon_h) / 2;
    icon_widget->set_pos(ix, iy);  // set_pos() repaints the glyph for us
  };

 public:
  RectText(GFXForms *display, const char *text, int font_size,
           uint16_t font_color, int _heigth, int radius, uint16_t rect_color,
           std::function<void()> _cb, const uint8_t *_icon = nullptr,
           uint8_t _icon_w = 0, uint8_t _icon_h = 0);
  ~RectText();
  void set_pos(int _x, int _y) {
    x = _x;
    y = _y;
    container->set_pos(_x, _y);
  };
  void set_color(uint16_t _color) {};
  void display() {
    container->display();
    draw_icon();
  };
  void set_dimension(int _width, int _heigth) {
    width = _width;
    heigth = _heigth;
    container->set_dimension(_width, _heigth);
  };
  void set_selected(bool _selected) {
    selected = _selected;
    // Recolour the tile *outline* instead of filling it. The stock firmware
    // filled the box (blue when selected, black when not) which made idle
    // tiles vanish as you scrolled and would also stamp over the icon. An
    // outline keeps the interior black, so the glyph stays clean and every
    // tile stays visible.
    box->set_color(selected ? select_color : base_color);
    box->display();
    draw_icon();  // keep the glyph on top after the outline redraw
  };
  void click() {
    Serial.println("Widget clicked");
    cb();
  };
  void click(void callback()) { callback(); }
};
#endif