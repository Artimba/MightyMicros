""" 
This is a quick script that can be used to take an image and run one of our models on it after training.
"""

import cv2
from ultralytics import YOLO

from src.pipeline.model import Model

# Load the YOLOv8 model
model = Model('runs/detect/train4/weights/best.pt')

# Open the video file
video_path = "data/20231017_120545.mp4"
cap = cv2.VideoCapture(video_path)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        frame = model.predict(frame)
        print("Detections:", len(model.manager.detections))

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", frame)

        key = cv2.waitKey(0)  # Wait indefinitely for a key press
        if key == ord("q"):
            break
        elif key == 32:  # ASCII code for spacebar
            continue  # Go to the next iteration and thus the next frame
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()