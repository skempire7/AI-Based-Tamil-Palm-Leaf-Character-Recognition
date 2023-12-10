from PIL import Image
import subprocess
# Open the three separate images
img_part1 = Image.open("Pre-Pocessed_Images\Part1_processed.png")
img_part2 = Image.open("Pre-Pocessed_Images\Part2_processed.png")
img_part3 = Image.open("Pre-Pocessed_Images\Part3_processed.png")

# Get the dimensions of the individual images
width1, height1 = img_part1.size
width2, height2 = img_part2.size
width3, height3 = img_part3.size

# Calculate the total width and height of the combined image
total_width = width1 + width2 + width3
max_height = max(height1, height2, height3)

# Create a new blank image with the calculated dimensions
combined_img = Image.new('RGB', (total_width, max_height))

# Paste each part into the combined image
combined_img.paste(img_part1, (0, 0))
combined_img.paste(img_part2, (width1, 0))
combined_img.paste(img_part3, (width1 + width2, 0))

# Save the combined image
combined_img.save("10.Joined_image.jpg")
print("joining completed")

subprocess.run(["python", "4.Segmentation.py"])
