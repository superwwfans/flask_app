#! usr/bin/env python
# coding=utf-8
# FileName = ''
# time:
# author: huang-xin-dong
# about:
# ---------------------------------------------------------
"""
    生成图片验证码
"""
from random import randint
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from uuid import uuid4


def create_captcha():
    """
    生成验证码图片,将随机生成的验证码绘制在图片上
    :return: 返回图片，验证码
    """
    uu = str(uuid4())
    text = uu[:4]
    t = [ord(i) for i in uu]

    font_color = (t[1], t[2], t[3])  # rgb (255,0,0)
    # 线颜色
    line_color = (t[4], t[5], t[6])
    # 点颜色
    point_color = (t[7], t[8], t[9])
    width, height = 100, 40
    image = Image.new('RGB', (width, height), (200, 200, 200))
    font_path = "utils/captcha/font/Arial.ttf"
    font = ImageFont.truetype(font_path, height-10)
    draw = ImageDraw.Draw(image)
    draw.text((10, 8), text, font=font, fill=font_color)
    # 绘制线条
    for i in range(0, 5):
        draw.line(((t[1]-50, t[2]-30),
                   (t[11]+50, t[13])),
                  fill=line_color,
                  width=3)
    # #绘制点
    for i in range(1000):
        draw.point((randint(0, width), randint(0, height)), fill=point_color)
    # 输出
    try:
        out = BytesIO()  # 在内存中创建了一个文件
        image.save(out, format='jpeg')
        content = out.getvalue()
        out.close()
        return text, content
    except Exception:
       return None










