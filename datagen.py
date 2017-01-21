from PIL import Image, ImageDraw, ImageFont
from random import randrange
from io import BytesIO
import threading

import time
import pyapi

OUT_PATH = "gendata/"
IMAGE_SIZE = (300, 200)

BACK_COLORS = [(255, 165, 165), (255, 183, 124), (255, 253, 173), (167, 249, 182), (184, 221, 249), (235, 206, 255), (255, 255, 255)]
TEXT_COLORS = [(181, 41, 41), (237, 128, 26), (221, 218, 11), (14, 186, 46), (11, 114, 193), (109, 13, 173), (0, 0, 0)]
BACK_COLORS_NAME = ["Red", "Orange", "Yellow", "Green", "Blue", "Purple", "White"]
TEXT_COLORS_NAME = ["Red", "Orange", "Yellow", "Green", "Blue", "Purple", "Black"]
FONTS = [ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40), ImageFont.truetype('Pillow/Tests/fonts/DejaVuSans.ttf', 40)]
FONTS_NAME = ["FreeMono", "DejaVuSans"]


project = pyapi.Client().create_fproject(OUT_PATH + "project.meta")


def task():

    for i in range(50000):

        ids = {}
        numericf = {}
        discretef = {}
        backno = randrange(7)
        textno = randrange(7)
        fontno = randrange(2)

        textlen = randrange(10) + 1
        ypos = randrange(160)
        alphaval = 0
        text = ""
        for c in range(textlen):
            charval = randrange(26)
            alphaval += (charval + 1)
            text += chr(ord('A')+charval)

        ids["rand"] = randrange(100000)
        ids["time"] = time.time()
        numericf["CharCount"] = textlen
        numericf["AlphaSum"] = alphaval
        numericf["TextY"] = ypos
        discretef["BackColor"] = BACK_COLORS_NAME[backno]
        discretef["TextColor"] = TEXT_COLORS_NAME[textno]
        discretef["Font"] = FONTS_NAME[fontno]

        img = Image.new('RGB', IMAGE_SIZE, BACK_COLORS[backno])
        d = ImageDraw.Draw(img)

        d.text((10, ypos), text, font=FONTS[fontno], fill=TEXT_COLORS[textno])

        output = BytesIO()
        img.save(output, format="png")
        #project.add_data(output.getvalue(), ids, numericf, discretef)
        output.close()


threads = []
for i in range(10):
    t = threading.Thread(target=task)
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()
