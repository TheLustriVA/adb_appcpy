import os
import subprocess
from PIL import Image

# Step 1: Take initial screenshot
subprocess.run(["adb", "exec-out", "screencap", "-p", "> screen1.png"])

# Initialize variables
image_list = []
image_list.append(Image.open("screen1.png"))

# Step 2 & 3: Scroll down and take subsequent screenshots
for i in range(2, 6):  # Adjust the range based on how much you need to scroll
    subprocess.run(["adb", "shell", "input", "swipe", "500", "1500", "500", "500"])
    subprocess.run(["adb", "exec-out", "screencap", "-p", f"> screen{i}.png"])
    image_list.append(Image.open(f"screen{i}.png"))

# Step 4: Stitch images
stitched_img = Image.new("RGB", (image_list[0].width, image_list[0].height * len(image_list)))

y_offset = 0
for img in image_list:
    stitched_img.paste(img, (0, y_offset))
    y_offset += img.height

stitched_img.save("stitched.png")

# Step 5: OCR
subprocess.run(["tesseract", "stitched.png", "output.txt"])

# Clean up
for i in range(1, 6):
    os.remove(f"screen{i}.png")
