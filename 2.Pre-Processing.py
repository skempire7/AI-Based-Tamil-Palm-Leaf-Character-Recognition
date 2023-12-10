import cv2
import numpy as np
import os
import subprocess

# Define the folder containing your images
folder_path = "Split Images"

# Loop through all image files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".png"):  # Assuming your images are in PNG format
        # Construct the full path to the image file
        image_path = os.path.join(folder_path, filename)

        # Read the original image using OpenCV
        image = cv2.imread(image_path)

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Threshold the grayscale image
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Remove horizontal lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(image, [c], -1, (255, 255, 255), 5)

        # Remove vertical lines
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
        remove_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
        cnts = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            cv2.drawContours(image, [c], -1, (255, 255, 255), 5)

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Applying median filter for salt and pepper/impulse noise
        filter1 = cv2.medianBlur(gray, 3)

        # Applying Gaussian blur to smoothen out the image edges
        filter2 = cv2.GaussianBlur(filter1, (3, 3), 0)

        # Applying non-local means for final denoising of the image
        dst = cv2.fastNlMeansDenoising(filter2, None, 15, 7, 15)

        # Converting the image to binarized form using adaptive thresholding
        th1 = cv2.adaptiveThreshold(dst, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        # Save the preprocessed image with a new filename
        output_filename = os.path.splitext(filename)[0] + "_processed.png"
        output_path = os.path.join('Pre-Pocessed_Images', output_filename)
        cv2.imwrite(output_path, th1)
        print("pre-process completed")

subprocess.run(["python", "3.Join_Image.py"])