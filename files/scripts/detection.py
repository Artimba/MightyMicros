""" 
This is a quick script that can be used to take an image and run one of our models on it after training.
"""

import cv2
from ultralytics import YOLO

from src.pipeline.model import Model


model = Model('runs/detect/train4/weights/best.pt')
video_path = "data/20231017_120545.mp4"
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        cv2.namedWindow('YOLOv8 Inference', cv2.WINDOW_NORMAL)
        desired_width = 1920
        desired_height = 1080
        cv2.resizeWindow('YOLOv8 Inference', desired_width, desired_height)
        frame = model.predict(frame)
        print("Detections:", len(model.manager.detections))

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