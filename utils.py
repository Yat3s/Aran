#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, os, pygame, io
from PIL import Image, ImageFont, ImageDraw
def jsonify(source_dict):
    if isinstance(source_dict, dict):
        return json.dumps(dict([(k, v) for k, v in source_dict.iteritems() if(v) ]), ensure_ascii=False, indent=4, sort_keys=True)
    return str(source_dict)

def drawPic(text):
    processed_text = ''
    max_line_len = 20
    font_size = 18
    length = len(text)
    line = int(length / max_line_len) + 1
    width = (max_line_len * 20 if length > max_line_len else length * 20) + 20
    for i in range(0, line):
        processed_text += text[i * max_line_len : (i+1) * max_line_len] + '\n'
    im = Image.new("RGB", (width, line * 35), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype("FZGLJW.TTF", font_size)
    dr.text((20, 5), processed_text, font=font, fill="#000000")
    im.save("assets/draw_pic.png")
