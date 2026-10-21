# -*- coding: utf-8 -*-
"""生成 App 图标：蓝色渐变圆角方块 + 白色书本"""
from PIL import Image, ImageDraw
import os, math

BASE = r'C:\Users\zzy\AppData\Local\Temp\apkbuild\res'
SIZES = {'mipmap-mdpi': 48, 'mipmap-hdpi': 72, 'mipmap-xhdpi': 96,
         'mipmap-xxhdpi': 144, 'mipmap-xxxhdpi': 192}

def rounded(draw, box, r, fill):
    draw.rounded_rectangle(box, radius=r, fill=fill)

def make(size):
    S = size * 8  # 超采样
    img = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # 背景：Apple 蓝渐变
    for y in range(S):
        t = y / S
        r = int(0 + (10 - 0) * t)
        g = int(113 + (132 - 113) * t)
        b = int(227 + (255 - 227) * t)
        d.line([(0, y), (S, y)], fill=(r, g, b, 255))
    # 圆角遮罩
    mask = Image.new('L', (S, S), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * 0.225), fill=255)
    img.putalpha(mask)
    d = ImageDraw.Draw(img)
    # 白色书本
    w = S * 0.50
    h = S * 0.36
    cx, cy = S / 2, S / 2
    x0, y0 = cx - w / 2, cy - h / 2
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=int(S * 0.035), fill=(255, 255, 255, 255))
    # 书脊
    d.rectangle([cx - S * 0.012, y0, cx + S * 0.012, y0 + h], fill=(0, 113, 227, 255))
    # 三条文字线
    lw = w * 0.30
    for i in range(3):
        yy = y0 + h * (0.28 + i * 0.18)
        d.rounded_rectangle([x0 + w * 0.12, yy, x0 + w * 0.12 + lw, yy + S * 0.022],
                            radius=int(S * 0.008), fill=(0, 113, 227, 255))
        d.rounded_rectangle([cx + w * 0.08, yy, cx + w * 0.08 + lw, yy + S * 0.022],
                            radius=int(S * 0.008), fill=(0, 113, 227, 255))
    return img.resize((size, size), Image.LANCZOS)

for folder, px in SIZES.items():
    p = os.path.join(BASE, folder)
    os.makedirs(p, exist_ok=True)
    make(px).save(os.path.join(p, 'ic_launcher.png'))
    print(folder, px, 'ok')
