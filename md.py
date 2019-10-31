# motion detector

import cv2, time, pandas
from datetime import datetime

#first frame should be a background image
first_frame = None
video = cv2.VideoCapture(0)

status_list = [None, None]
times = []
df = pandas.DataFrame(columns=["Start", "End"])

while True:
    check, frame = video.read()
    status = 0

    if check:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # blur the gray image
        gray = cv2.GaussianBlur(gray,(21,21),0)
        if first_frame is None:
            first_frame = gray
            # go to the beginning of the loop
            continue
        # Compare the first frame with the current frame, gray, blurred
        # save the absolute difference - if the difference is more than 30 = 
        # movement = assign white (threshold is the function where 30 is used)
        delta_frame = cv2.absdiff(first_frame, gray)
        thresh_frame = cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
        #smooth the threshold frame, delay the areas, remove the black holes - dilate
        #white areas are smoother
        thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
        # find contours
        (cnts,_) = cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for contour in cnts:
            if cv2.contourArea(contour) < 10000:
                continue
            #for areas smaller than 10000 area skip draw contour
            status = 1 
            
            (x, y, w, h) = cv2.boundingRect(contour)
            # draw a white rectangle
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 3)
        
        status_list.append(status)
        if status_list[-1] == 1 and status_list[-2] == 0:
            times.append(datetime.now())
        if status_list[-1] == 0 and status_list[-2] == 1:
            times.append(datetime.now())

        cv2.imshow("Capturing webcam", gray)
        cv2.imshow("Delta frame", delta_frame)
        cv2.imshow("Threshold Frame", thresh_frame)
        cv2.imshow("Color frame", frame)    
        #cv2.imwrite("imgcapt"+str(countFrames)+".jpg", gray)
        #print(delta_frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            if status ==1:
                times.append(datetime.now())
            break
        #print(status)
    else:
        break
print(status_list)
print (times)
for i in range(0,len(times),2):
    df = df.append({"Start":times[i], "End":times[i+1]}, ignore_index=True)
df.to_csv("Times.csv")

video.release()


