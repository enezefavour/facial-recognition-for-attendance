import numpy as np
import dlib
import cv2
import imutils
from threading import Thread
import face_recognition
from datetime import datetime
import os
import requests

class CaptureVideo:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return

            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
        self.stream.release


# Capture Image - Incomplete
class CaptureImage:
    def take_photo(frame):
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y%H%M%S")
        img_name = "{}.png".format(dt_string)
        img_dir = 'Pictures'
        path = os.path.join(img_dir, img_name)
        cv2.imwrite(path, frame)
        return path

def main():

    capture = CaptureVideo().start()  # Start the capturing thread
    
    while True:
        if capture.stopped:
            capture.stop()
            break

        frame = capture.read()  # read a frame from the capturing thread
    
        cv2.imshow('Video', frame)  # Show the video
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    capture.stop()  # kill the capture thread
    cv2.destroyAllWindows()

main()