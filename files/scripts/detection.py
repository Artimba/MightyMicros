""" 
This is a quick script that can be used to take an image and run one of our models on it after training.
"""



import cv2
from ultralytics import YOLO
from src.pipeline.model import Model
import subprocess

# Load the YOLOv8 model
model = Model()


# Open the video file
video_path = "A:/MightyMicros/data/20231017_120545_30fps.mp4"
cap = cv2.VideoCapture(video_path)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        frame = cv2.resize(frame, (640, 480)) 
        # Run YOLOv8 inference on the frame
        annotated_frame = model.predict(frame)

        # Visualize the results on the frame
        # annotated_frame = results[0].plot(labels=False, masks=False)

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        key = cv2.waitKey(-1)
        if key == ord("q"):
            break
        elif key == 32:
            continue
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()