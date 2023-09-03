import cv2
import numpy as np

def compare_images(img1_path, img2_path):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    
    # Calculate the absolute difference between the two images
    diff = cv2.absdiff(img1, img2)
    
    # Convert the difference to grayscale
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    
    # Sum the differences
    sum_diff = np.sum(gray_diff)
    
    return sum_diff

# Example usage
img1_path = "image1.png"
img2_path = "image2.png"
sum_diff = compare_images(img1_path, img2_path)

if sum_diff < 1000:  # You can adjust this threshold
    print("The images are similar.")
else:
    print("The images are different.")
