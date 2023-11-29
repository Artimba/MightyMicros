import json
import cv2
import math
import os

def convert_to_corners(rotation, x, y, width, height):
    """
    Convert the center coordinates (x, y), dimensions (width, height), and rotation (in degrees)
    to corner coordinates (x1, y1, x2, y2, x3, y3, x4, y4) of the oriented bounding box.
    """
    # Convert rotation to radians
    theta = math.radians(rotation)

    # Calculate the corner points
    corner_dx = width / 2
    corner_dy = height / 2

    # Corner 1 (Top-Left)
    x1 = x - corner_dx * math.cos(theta) + corner_dy * math.sin(theta)
    y1 = y - corner_dx * math.sin(theta) - corner_dy * math.cos(theta)

    # Corner 2 (Top-Right)
    x2 = x + corner_dx * math.cos(theta) + corner_dy * math.sin(theta)
    y2 = y + corner_dx * math.sin(theta) - corner_dy * math.cos(theta)

    # Corner 3 (Bottom-Right)
    x3 = x + corner_dx * math.cos(theta) - corner_dy * math.sin(theta)
    y3 = y + corner_dx * math.sin(theta) + corner_dy * math.cos(theta)

    # Corner 4 (Bottom-Left)
    x4 = x - corner_dx * math.cos(theta) - corner_dy * math.sin(theta)
    y4 = y - corner_dx * math.sin(theta) + corner_dy * math.cos(theta)

    return x1, y1, x2, y2, x3, y3, x4, y4

def extract_frames(video_path, frame_indices, output_folder):
    cap = cv2.VideoCapture(video_path)
    frames = {}
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"Video: {video_path} - Resolution: {width}x{height}")
    if width != 1280 or height != 720:
        print("Mixed resolution not supported yet :(")
        cap.release()
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_index = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        if frame_index in frame_indices:
            frames[frame_index] = frame
    cap.release()
    
    for frame_index, frame in frames.items():
        cv2.imwrite(f"{output_folder}/{frame_index:04d}.jpg", frame)

def process_json(json_file, image_output_folder, label_output_folder):
    with open(json_file, 'r') as file:
        data = json.load(file)

    for item in data:
        video_path = item['video']
        frame_indices = set()
        labels_per_frame = {}

        # Accumulate all labels for each frame
        for box in item.get('box', []):
            for frame_data in box.get('sequence', []):
                if frame_data.get('enabled', False):
                    frame_index = frame_data['frame']
                    frame_indices.add(frame_index)
                    corners = convert_to_corners(frame_data['rotation'], frame_data['x'], frame_data['y'], frame_data['width'], frame_data['height'])
                    label_str = f"{corners[0]} {corners[1]} {corners[2]} {corners[3]} {corners[4]} {corners[5]} {corners[6]} {corners[7]} slice 1"
                    
                    if frame_index not in labels_per_frame:
                        labels_per_frame[frame_index] = []
                    labels_per_frame[frame_index].append(label_str)

        # Extract frames
        extract_frames(video_path, frame_indices, image_output_folder)

        # Write labels to files
        for frame_index, labels in labels_per_frame.items():
            label_file = f"{label_output_folder}/{frame_index:04d}.txt"
            with open(label_file, 'w') as f:
                for label in labels:
                    f.write(label + '\n')

# Specify your paths
json_file = 'data/mighty-tracking-annotated-11-18-23.json'
image_output_folder = '/home/sky/datasets/obb/images'
label_output_folder = '/home/sky/datasets/obb/labelTxt'

# Create directories if they don't exist
os.makedirs(image_output_folder, exist_ok=True)
os.makedirs(label_output_folder, exist_ok=True)

# Process the JSON file
process_json(json_file, image_output_folder, label_output_folder)
