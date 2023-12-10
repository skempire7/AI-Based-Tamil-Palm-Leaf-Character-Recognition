import cv2
import numpy as np
import imutils
import os
import subprocess

# Define the folder where you want to save segmented images
output_folder = "Segmented_Letters"

# Delete all files in the output folder before saving new images
for filename in os.listdir(output_folder):
    file_path = os.path.join(output_folder, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)

image = cv2.imread("10.Joined_image.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)
ret, thresh1 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
dilate = cv2.dilate(thresh1, None, iterations=2)

# Apply morphological operations to separate overlapping characters
kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(dilate, cv2.MORPH_OPEN, kernel, iterations=1)

# Find contours and hierarchy (for OpenCV version 3+)
cnts, hierarchy = cv2.findContours(opening.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Use the following line for OpenCV version 2
# cnts = cv2.findContours(opening.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

orig = image.copy()
i = 1000

for cnt in cnts:
    if cv2.contourArea(cnt) < 200:
        continue

    x, y, w, h = cv2.boundingRect(cnt)
    roi = image[y:y + h, x:x + w]
    
    cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imwrite(os.path.join(output_folder, str(i) + ".png"), roi)
    i += 1

cv2.imwrite("11.Segmented_Image.jpg", orig)
print("segmented completed")
subprocess.run(["python", "5.Recognition.py"])