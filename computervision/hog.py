#import the necessary packages
import numpy as np
from picamera2.encoders import H264Encoder, Quality
from picamera2 import Picamera2, Preview
import time, libcamera
from PIL import Image
import cv2

import os

os.environ["LIBCAMERA_LOG_LEVELS"] = "3"
Picamera2.set_logging(Picamera2.ERROR)


# Adopted from https://medium.com/@mh_yip/opencv-detect-whether-a-window-is-closed-or-close-by-press-x-button-ee51616f7088
# Thanks to David C. for Aspect Ratio workaround to Rasberry Pi cv2 bug:
# https://stackoverflow.com/questions/66431311/python-opencv-on-raspberry-pi-detect-window-closing
def cv2_wait_for_window_to_close(window_title):
    """
    Blocks execution until the specified window has been closed. If the user
    presses the <ESC> key, the function will return immediately.
    """

    visible = cv2.getWindowProperty(window_title, cv2.WND_PROP_VISIBLE)
    aratio = cv2.getWindowProperty(window_title, cv2.WND_PROP_ASPECT_RATIO)
    while visible != 0.0 and aratio >= 0:
        visible = cv2.getWindowProperty(window_title, cv2.WND_PROP_VISIBLE)
        aratio = cv2.getWindowProperty(window_title, cv2.WND_PROP_ASPECT_RATIO)
        keyCode = cv2.waitKey(100)
        if (keyCode & 0xFF) == 27:
            print(f"Detected <ESC> Key... Quitting Program")
            cv2.destroyWindow(window_title)
            return




#sets how many pixels away from the center a person needs to be before the head stops
center_tolerance = 5; 

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

#picam = Picamera2()
#video_config = picam.create_video_configuration(
    #main={"size": (800, 600)}, 
    #lores={"size": (400, 300)}, 
    #display="lores")


#while(True):
    # Capture frame-by-frame
    
    #frame = picam.capture_array()
filename = 'portrait.jpg'
#frame = cv2.imread(filename)
picam = Picamera2()
picam.start()
time.sleep(0.5)
print("DONE")
frame = picam.capture_array()
#frame = picam.capture_image()

frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB) 

#cv2.namedWindow(filename)
#cv2.imshow(filename, frame)
#cv2.moveWindow(filename, 50, 50)
#cv2_wait_for_window_to_close(filename)

print(frame.shape)
frame = cv2.resize(frame,(320,240))
print(frame.shape)

# detect people in the image
# returns the bounding boxes for the detected objects

time_start = time.time()
boxes, weights = hog.detectMultiScale(frame, winStride=(1,1), scale = 1.05)
time_end = time.time()
time_elapsed = time_end - time_start
print(f'{filename}: detected {len(boxes)} people objects in {time_elapsed:.3f}s')

boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
centers = []
for box in boxes:
    #get the distance from the center of each box's center x cord to the center of the screen and ad them to a list
    center_x = ((box[2]-box[0])/2)+box[0]
    x_pos_rel_center = (center_x-70)
    dist_to_center_x = abs(x_pos_rel_center)
    centers.append({'box': box, 'x_pos_rel_center': x_pos_rel_center, 'dist_to_center_x':dist_to_center_x})    
if len(centers) > 0:
        #sorts the list by distance_to_center
    sorted_boxes = sorted(centers, key=lambda i: i['dist_to_center_x'])
    #draws the box
    center_box = sorted_boxes[0]['box']
    for box in range(len(sorted_boxes)):
    # display the detected boxes in the colour picture
        if box == 0:
            cv2.rectangle(frame, (sorted_boxes[box]['box'][0],sorted_boxes[box]['box'][1]), (sorted_boxes[box]['box'][2],sorted_boxes[box]['box'][3]), (0,255, 0), 2)
        else:
            cv2.rectangle(frame, (sorted_boxes[box]['box'][0],sorted_boxes[box]['box'][1]), (sorted_boxes[box]['box'][2],sorted_boxes[box]['box'][3]),(0,0,255),2)
    #retrieves the distance from center from the list and determins if the head should turn left, right, or stay put and turn lights on
    Center_box_pos_x = sorted_boxes[0]['x_pos_rel_center']  
    if -center_tolerance <= Center_box_pos_x <= center_tolerance:
        #turn on eye light
        print("center")
        #result = write_read("2")
    elif Center_box_pos_x >= center_tolerance:
        #turn head to the right
        print("right")
        #result = write_read("3")
    elif Center_box_pos_x <= -center_tolerance:
        #turn head to the left
        print("left")
        #result = write_read("1")
    print(str(Center_box_pos_x))
else:
    #prints out that no person has been detected
    #result = write_read("0")
    print("nothing detected")
#resizes the video so its easier to see on the screen
#frame = cv2.resize(frame,(640,480))
# Display the resulting frame
cv2.namedWindow(filename)
cv2.imshow(filename, frame)
cv2.moveWindow(filename, 50, 50)
cv2_wait_for_window_to_close(filename)
picam.stop()
picam.close()