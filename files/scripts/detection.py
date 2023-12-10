""" 
This is a quick script that can be used to take an image and run one of our models on it after training.
"""

import cv2
# from ultralytics import YOLO

from src.pipeline.model import Model


model = Model('epoch_30.pth')
video_path = "data/20231017_122937.mp4"
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        cv2.namedWindow('RMMCV Inference', cv2.WINDOW_NORMAL)
        desired_width = 1920
        desired_height = 1080
        cv2.resizeWindow('RMMCV Inference', desired_width, desired_height)
        frame = model.predict(frame)
        frame = cv2.resize(frame, (desired_width, desired_height))
        print("Detections:", len(model.manager.detections))

        cv2.imshow("RMMCV Inference", frame)

        key = cv2.waitKey(1)  # Wait indefinitely for a key press
        if key == ord("q"):
            break
        # elif key == 32:
        #     continue
        elif key == ord("s"):
            cv2.imwrite("output.png", frame)
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()