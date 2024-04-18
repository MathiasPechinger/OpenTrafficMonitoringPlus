import os
import cv2
import csv
import numpy as np
import ast
from tqdm import tqdm  # Import the tqdm function

# Paths
image_dir = './out/trimmed_video/temp/preprocessed_images'
csv_dir = './out/trimmed_video/temp/contours'
output_dir = './out/trimmed_video/temp/newContours'

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# List all image files in the directory
image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Check if there are any image files to process
if not image_files:
    print("No image files to process.")
else:
    # Initialize tqdm progress bar for image files
    for image_file in tqdm(image_files, desc='Processing image files'):
        # Load the image
        image = cv2.imread(os.path.join(image_dir, image_file))

        # Construct the corresponding CSV file path
        csv_file = os.path.join(csv_dir, f"{os.path.splitext(image_file)[0]}_masks_contours.csv")

        # Read contours from CSV file
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            contours = [np.array([ast.literal_eval(point) for point in row]) for row in reader]

        # Check if contours were found and draw them
        if contours:
            cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

        # Save the image to the output directory
        cv2.imwrite(os.path.join(output_dir, image_file), image)

    print("Finished processing all images.")
