import os
import sys
import glob
from PIL import Image

def scale_to_width(img, width): # アスペクト比を固定して、幅が指定した値になるようリサイズする。
    height = round(img.height * width / img.width)
    return img.resize((width, height))

files = glob.glob('./images/*')#全てのファイルのパスを取得
dst_dir = "./resize_images/"
os.makedirs(dst_dir, exist_ok=True)

try:
    os.makedirs('./sample.jpg', exist_ok=True)
except FileExistsError as e:
    print(e.strerror)  # エラーメッセージ ('Cannot create a file when that file already exists')
    print(e.errno)     # エラー番号 (17)
    print(e.filename)  # 作成できなかったディレクトリ名 ('foo')
    print("ERROR: makedirs")
    sys.exit(1)





for f in files:
    try: # ファイルがPillowの読み込みに対応しているとき
        img = Image.open(f)
        img_resize = scale_to_width(img, 256) # 幅を指定したリサイズ
        #img_resize = img.resize((int(img.width / 2), int(img.height / 2)))# ２分の１のサイズへ
        root, ext = os.path.splitext(f)
        file_name = os.path.basename(root)
        img_resize.save(os.path.join(dst_dir, file_name + ext))
        print("Success Resize: " + dst_dir + file_name + ext)
    except OSError as e:
        print("Error: " + f.title)
        pass