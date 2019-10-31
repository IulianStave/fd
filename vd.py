import cv2, time

video = cv2.VideoCapture(0)

countFrames = 1
while True:
    countFrames = countFrames+1
    check, frame = video.read()

    print(check)
    print(frame)
    print(type(frame))

    if check:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Capturing webcam", gray)
        cv2.imwrite("imgc"+str(countFrames)+".jpg",gray)
        key = cv2.waitKey(1000)
        if key == ord('q'):
            break
    else:
        break
video.release()