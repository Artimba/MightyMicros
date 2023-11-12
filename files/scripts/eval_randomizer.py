"""
This script randomly picks 20% of the images and their corresponding labels and moves them to the validation directories. The other 80% moves to training directories. 
"""

import os
import shutil
import random
from glob import glob

# Set seed for reproducibility
random.seed(42)

# Paths
origin_path = 'converter/images/'
train_images_path = 'training/images/train/'
val_images_path = 'training/images/val/'
train_labels_path = 'training/labels/train/'
val_labels_path = 'training/labels/val/'

# Make sure destination folders exist
os.makedirs(train_images_path, exist_ok=True)
os.makedirs(val_images_path, exist_ok=True)
os.makedirs(train_labels_path, exist_ok=True)
os.makedirs(val_labels_path, exist_ok=True)

# Get all image files
image_files = glob(os.path.join(origin_path, 'frame_*.jpg'))

# Determine how many images will be in the validation set (20% of the dataset)
val_size = int(len(image_files) * 0.2)

# Randomly select validation images
val_images = random.sample(image_files, val_size)

# Function to move image and label to the destination
def move_file(image_path, label_path, img_dest, lbl_dest):
    # Move image
    shutil.move(image_path, img_dest)
    
    # Move label if it exists
    if os.path.exists(label_path):
        shutil.move(label_path, lbl_dest)
    else:
        # Create an empty label file if it does not exist
        open(os.path.join(lbl_dest, os.path.basename(label_path)), 'a').close()

# Move selected images and their corresponding labels to validation directories
for image_path in val_images:
    base_filename = os.path.basename(image_path).replace('.jpg', '.txt')
    label_path = os.path.join(origin_path.replace('images', 'labels'), base_filename)
    move_file(image_path, label_path, val_images_path, val_labels_path)

# Move the remaining images and their labels to the training directories
remaining_image_files = glob(os.path.join(origin_path, 'frame_*.jpg'))
for image_path in remaining_image_files:
    base_filename = os.path.basename(image_path).replace('.jpg', '.txt')
    label_path = os.path.join(origin_path.replace('images', 'labels'), base_filename)
    move_file(image_path, label_path, train_images_path, train_labels_path)
