""" 
This is a quick script that can be used to take an image and run one of our models on it after training.
"""

# from ultralytics import YOLO
# import cv2
# from PIL import Image

# # Path to the image you want to predict on
# image_path = 'data/frame_0.jpg'

# # Load a pretrained model (specify the correct path or model name)
# model = YOLO('runs/detect/train3/weights/best.pt')  # Replace with the path to your model weights

# # Load image
# image = cv2.imread(image_path)

# # Run YOLO model prediction
# results = model.predict(image)

# # Show the results
# for r in results:
#     im_array = r.plot(line_width=0.5, labels=False, probs=False)  # plot a BGR numpy array of predictions
#     im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
#     im.show()  # show image

import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('runs/detect/train7/weights/best.pt')

# Open the video file
video_path = "data/20231017_132531.mp4"
cap = cv2.VideoCapture(video_path)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        frame = cv2.resize(frame, (640, 480)) 
        # Run YOLOv8 inference on the frame
        results = model(frame, verbose=False)

        # Visualize the results on the frame
        annotated_frame = results[0].plot(labels=False, masks=False)

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