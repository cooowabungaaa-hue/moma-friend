from PIL import Image
import os

img_path = r"c:\Users\小野明子\Desktop\moma-friend-lp\room-bg-v2.png"
if os.path.exists(img_path):
    with Image.open(img_path) as img:
        print(f"Dimensions: {img.width}x{img.height}")
else:
    print("File not found.")
