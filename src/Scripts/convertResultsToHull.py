import os
import cv2
import csv
import numpy as np
from tqdm import tqdm  # Import the tqdm function

# Paths
masks_dir = './out/trimmed_video/temp/images_after_network'
output_dir = './out/trimmed_video/temp/contours'

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# List of files to process
files = [f for f in os.listdir(masks_dir) if f.endswith('_masks.npy')]

# Initialize tqdm progress bar
for file_name in tqdm(files, desc='Processing files'):
    # Load the masks from the file
    masks = np.load(os.path.join(masks_dir, file_name))
    
    # Initialize a list to hold contours for all masks in this file
    contours_list = []
    
    # Process each mask
    for mask in tqdm(masks, desc='Finding contours', leave=False):
        # Find contours in the mask
        contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Collect all contours
        for contour in contours:
            # Append the contour coordinates to the list
            contours_list.append(contour.tolist())  # Convert numpy array to list for csv writer
    
    # Save the contours to a CSV file
    csv_file = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}_contours.csv")
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(contours_list)
