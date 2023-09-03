import os
import subprocess
import logging
from PIL import Image
from PIL import ImageChops

# Initialize variables
image_list = []
batch_list = []
logging.basicConfig(level=logging.DEBUG)

# Initialize counter for screenshot filenames
i = 1
prev_center_pixels = None

# Step 1 & 2: Take initial screenshot and scroll down
while True:
    result = subprocess.run(["adb", "exec-out", "screencap", "-p"], capture_output=True)
    with open(f"screen{i}.png", "wb") as f:
        f.write(result.stdout)
    curr_img = Image.open(f"screen{i}.png")

    # Crop images to only compare the area that should change
    crop_box = (0, int(curr_img.height * 0.28), curr_img.width, int(curr_img.height * 0.90))
    cropped_curr = curr_img.crop(crop_box)
    image_list.append(cropped_curr)

    # Take a small sample of pixels from the center
    center_box = (int(cropped_curr.width * 0.45), int(cropped_curr.height * 0.45), 
                  int(cropped_curr.width * 0.55), int(cropped_curr.height * 0.55))
    center_crop = cropped_curr.crop(center_box)
    center_pixels = list(center_crop.getdata())

    if prev_center_pixels:
        diff_sum = sum(abs(a[i] - b[i]) for a, b in zip(center_pixels, prev_center_pixels) for i in range(3))
        logging.debug(f"Iteration {i}: diff_sum = {diff_sum}")

        if diff_sum < 1000:  # Very low threshold to detect nearly identical images
            logging.info("Reached end of scrollable content.")
            break

    prev_center_pixels = center_pixels
    i += 1  # Increment counter for next iteration

    # Scroll action
    subprocess.run(["adb", "shell", "input", "swipe", "500", "1444", "500", "675"])

    # Check if it's time to process a batch
    if len(image_list) == 5:
        # Step 3: Stitch images in the current batch
        stitched_img = Image.new("RGB", (image_list[0].width, image_list[0].height * len(image_list)))
        y_offset = 0
        for img in image_list:
            stitched_img.paste(img, (0, y_offset))
            y_offset += img.height

        batch_list.append(stitched_img)
        image_list = []  # Clear the list for the next batch

# Step 4: OCR each batch
for idx, batch_img in enumerate(batch_list):
    batch_img.save(f"stitched_batch_{idx}.png")
    subprocess.run(["tesseract", f"stitched_batch_{idx}.png", f"output_batch_{idx}.txt"])

# Clean up
for i in range(1, i+1):
    os.remove(f"screen{i}.png")
