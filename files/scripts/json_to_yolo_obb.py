import json
import cv2
import math
import os
import numpy as np
from decimal import Decimal, ROUND_DOWN

video_num = 0




def convert_to_corners(top_left_x, top_left_y, width, height, rotation, img_width, img_height):
    # Convert from percentages to coordinates
    top_left_x = top_left_x / 100.0 * img_width
    top_left_y = top_left_y / 100.0 * img_height
    width = width / 100.0 * img_width
    height = height / 100.0 * img_height
    
    # Get center of box
    center_x = top_left_x + width / 2
    center_y = top_left_y + height / 2
    
    # Calculate the half-dimensions of the box
    half_width = width / 2
    half_height = height / 2

    # Define the rotation matrix
    theta = np.radians(rotation)  # Convert to radians
    cos = np.cos(theta)
    sin = np.sin(theta)
    rotation_matrix = np.array([[cos, -sin], [sin, cos]])

    # Define the corners relative to the center
    corners = np.array([
        [half_width, half_height],
        [half_width, -half_height],
        [-half_width, -half_height],
        [-half_width, half_height]
    ])

    # Rotate and translate the corners
    rotated_corners = []
    for corner in corners:
        # Apply rotation and then translate to original center
        rotated_corner = np.dot(rotation_matrix, corner) + np.array([center_x, center_y])
        rotated_corner = Decimal(str(rotated_corner[0])), Decimal(str(rotated_corner[1]))
        rotated_corner = (rotated_corner[0].quantize(Decimal('0.0'), rounding=ROUND_DOWN), rotated_corner[1].quantize(Decimal('0.0'), rounding=ROUND_DOWN))
        rotated_corners.append(rotated_corner)

    # Ensure the corners are within image bounds for plotting
    for i, corner in enumerate(rotated_corners):
        x, y = corner
        x = max(0, min(img_width, x))
        y = max(0, min(img_height, y))
        rotated_corners[i] = (x, y)

    return rotated_corners





def extract_frames(video_path, frame_indices, output_folder):
    global video_num
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file {video_path}")
        return
    frames = {}
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"Video: {video_path} - Resolution: {width}x{height}")
    i = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"Reached end of video, exiting on iteration {i}.")
            break
        frame_index = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        if frame_index in frame_indices:
            frames[frame_index] = frame
        i += 1
    cap.release()
    print(f"Extracted {len(frames)} frames from {video_path}")
    print(f"Saving frames to {output_folder}")
    for frame_index, frame in frames.items():
        cv2.imwrite(f"{output_folder}/video_{video_num}_{frame_index:04d}.png", frame)
    return width, height

def process_json(json_file, image_output_folder, label_output_folder, project_dir):
    global video_num
    with open(json_file, 'r') as file:
        data = json.load(file)

    for item in data:
        video_path = os.path.join(project_dir, item['video'])
        frame_indices = set()
        labels_per_frame = {}

        # First accumulate all frame indices
        for box in item.get('box', []):
            for frame_data in box.get('sequence', []):
                if frame_data.get('enabled', False):
                    frame_indices.add(frame_data['frame'])

        # Then extract frames
        img_width, img_height = extract_frames(video_path, frame_indices, image_output_folder)

        # Now process each frame
        for box in item.get('box', []):
            for frame_data in box.get('sequence', []):
                if frame_data.get('enabled', False):
                    frame_index = frame_data['frame']

                    # Include image dimensions in the function call
                    corners = convert_to_corners(rotation=frame_data['rotation'], 
                                                 top_left_x=frame_data['x'], 
                                                 top_left_y=frame_data['y'], 
                                                 width=frame_data['width'], 
                                                 height=frame_data['height'], 
                                                 img_width=img_width, 
                                                 img_height=img_height)
                    label_str = f"{corners[0][0]} {corners[0][1]} {corners[1][0]} {corners[1][1]} {corners[2][0]} {corners[2][1]} {corners[3][0]} {corners[3][1]} slice 1"

                    if frame_index not in labels_per_frame:
                        labels_per_frame[frame_index] = []
                    labels_per_frame[frame_index].append(label_str)

        # Write labels to files
        for frame_index, labels in labels_per_frame.items():
            label_file = f"{label_output_folder}/video_{video_num}_{frame_index:04d}.txt"
            with open(label_file, 'w') as f:
                for label in labels:
                    f.write(label + '\n')
        video_num += 1


# Specify your paths
json_file = 'data/mighty-tracking-annotated-11-18-23.json'
image_output_folder = '/home/sky/datasets/obb/images'
label_output_folder = '/home/sky/datasets/obb/labelTxt'

# Create directories if they don't exist
os.makedirs(image_output_folder, exist_ok=True)
os.makedirs(label_output_folder, exist_ok=True)

# Process the JSON file
process_json(json_file, image_output_folder, label_output_folder, project_dir = '/home/sky/MightyMicros')
