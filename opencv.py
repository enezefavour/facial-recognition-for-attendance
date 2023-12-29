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

class Duplicate:
    def duplicate():
        img_dir = 'Pictures'
        current_names = []
        current_encodings = []

        for images in os.listdir(img_dir):
            image = face_recognition.load_image_file(os.path.join(img_dir, images))
            face_encodings = face_recognition.face_encodings(image)[0]
            current_encodings.append(face_encodings)
            current_names.append(images)
       
        count = 0
        faces_to_delete = []
        while count < len(current_encodings):
            temp_array = list(current_encodings)
            temp_array.pop(count)

            same = face_recognition.compare_faces(temp_array, current_encodings[count])

            if True in same:
                filepath = os.path.join(img_dir, current_names[count])
                # print(filepath)
                # os.remove(filepath)
                # faces_to_delete.append(known_face_names[count])
                # known_face_names.pop(count)
                # known_face_encodings.pop(count)

            face_distances = face_recognition.face_distance(temp_array, current_encodings[count])
            best_match_index = np.argmin(face_distances)
            if same[best_match_index]:
                filepath2 = os.path.join(img_dir, current_names[count])
                os.remove(filepath2)
                faces_to_delete.append(current_names[count])
                current_names.pop(count)
                current_encodings.pop(count)

            count = count + 1
        known_face_encodings = current_encodings
        known_face_names = current_names
        return known_face_encodings, known_face_names

class DetectFace:
    def __init__(self, capture, known_encodings, known_names):
        self.capture = capture
        self.stopped = False
        self.face_locations = []
        self.face_names = []
        self.known_encodings = known_encodings
        self.known_names = known_names

    def start(self):
        Thread(target=self.process, args=()).start()
        return self

    def process(self):
        while not self.stopped:
            frame = self.capture.read()

            frame = imutils.resize(frame, width=450)

            frame = frame[:, :, ::-1]

            self.face_locations = face_recognition.face_locations(frame)

            # print(self.face_locations)
            # faceCascade = cv2.CascadeClassifier("haarcascade.xml")
            # gray = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2GRAY)
            
            try:
                self.face_names = Recognize.process(frame=frame, face_locations=self.face_locations,
                                                    known_face_encodings=self.known_encodings,
                                                    known_face_names=self.known_names)
            except:
                print("no faces to recognize")
            print(self.face_names)

    def stop(self):
        self.stopped = True

def main():
    known_face_encodings, known_face_names = Duplicate.duplicate()
    capture = CaptureVideo().start()  # Start the capturing thread
    face_detector = DetectFace(capture=capture, known_encodings=known_face_encodings,
                               known_names=known_face_names).start()
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