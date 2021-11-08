import os
import glob
from PIL import Image, ImageDraw
import numpy as np

def select_color(color):
    mean = np.array(color).mean(axis=0)
    return (255,255,255,0) if mean >= 205 else color

def transparent(img):
    w, h = img.size
    transparent_img = Image.new('RGBA', (w, h))
    np.array([[transparent_img.putpixel((x, y), select_color(img.getpixel((x,y)))) for x in range(w)] for y in range(h)])
    return transparent_img

files = glob.glob('./resize_images/*')# 全てのファイルのパスを取得
dst_dir = "./transparent_images/"
os.makedirs(dst_dir, exist_ok=True)

for f in files:
    try:
        original_img = Image.open(f).convert("RGB")
        root, ext = os.path.splitext(f)
        file_name = os.path.basename(root)
        transparent(original_img).save(os.path.join(dst_dir, file_name + ".png"))
        print("Success Transparent: " + dst_dir + file_name + ".png")
    except OSError as e:
        print("Error: " + f.title)
        pass