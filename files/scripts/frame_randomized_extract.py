import cv2
import numpy as np
import os
import random
from glob import glob

def extract_frames(videos, output_dir, total_frames=2000):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    frames_per_video = total_frames // len(videos)
    for video_path in videos:
        cap = cv2.VideoCapture(video_path)
        total_video_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_indices = random.sample(range(total_video_frames), min(frames_per_video, total_video_frames))

        for frame_idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            if not ret:
                continue
            cv2.resize(frame, (1280, 960))
            # Randomly rotate the frame
            if random.choice([True, False]):
                angle = random.choice([90, 180, 270])
                frame = rotate_image(frame, angle)

            # Save the frame
            frame_filename = os.path.join(output_dir, f"{os.path.basename(video_path).split('.')[0]}_frame{frame_idx}.jpg")
            cv2.imwrite(frame_filename, frame)

        cap.release()

def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

# Usage
video_files = glob('data/*.mp4')  # Adjust the path and file type as needed
output_directory = 'data/extracted_frames'
extract_frames(video_files, output_directory, total_frames=2000)
