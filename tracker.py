import cv2

# Normally this is how we hook into a live feed
# cv2.VideoCapture(0)

# This is how we do it for now
video_data = "data/20231017_120545.mp4"
capture = cv2.VideoCapture(video_data)

# Ensure the video file was opened successfully
if not capture.isOpened():
    print(f"Failed to open video {video_data}")
    exit(1)

tracker = cv2.TrackerCSRT.create()

# Detection
bbox = None

while True:
    ret, frame = capture.read()

    # Break out of the loop if the end of the video is reached or frame could not be read
    if not ret:
        print("Failed to read a frame from the video or end of video reached.")
        break

    if bbox is not None:
        ret, bbox = tracker.update(frame)
        if ret:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        else:
            cv2.putText(frame, "Tracking Failed.", (100, 80), cv2.FONT_HERSHEY_PLAIN, 0.75, (0, 0, 255), 2)

    cv2.imshow("Tracking", frame)

    key = cv2.waitKey(40)

    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('s') and frame is not None:
        bbox = cv2.selectROI("Tracking", frame, False)
        print(bbox)
        print(type(bbox))
        tracker.init(frame, bbox)

capture.release()
cv2.destroyAllWindows()







