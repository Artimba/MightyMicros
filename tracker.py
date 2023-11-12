import cv2

# Normally this is how we hook into a live feed
# cv2.VideoCapture(0)

# This is how we do it for now
video_data = "20231017_132900.mp4"
capture = cv2.VideoCapture(video_data)

tracker = cv2.TrackerCSRT.create()

# Detection
bbox = None

while True:

    ret, frame = capture.read()

    if bbox is not None:
        ret, bbox = tracker.update(frame)

        # This is return value from tracker
        if ret:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else:
            cv2.putText(frame, "Tracking Failed.", (100,80), cv2.FONT_HERSHEY_PLAIN, 0.75, (0,0,255), 2)

    cv2.imshow("Tracking", frame)

    key = cv2.waitKey(40)

    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('s'):
        bbox = cv2.selectROI("Tracking", frame, False)
        tracker.init(frame, bbox)


capture.release()
cv2.destroyAllWindows()







