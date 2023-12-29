import numpy as np
import dlib
import cv2
import imutils
from threading import Thread
import face_recognition
from datetime import datetime
import os


# from robowars.speaker import speaker
# import pyttsx3

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
        img_dir = os.chdir(r"C:\Users\hp\PycharmProjects\pythonProject34\dev\trydjango\src\Pictures")
        path = os.path.join(img_dir, img_name)
        cv2.imwrite(path, frame)


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
            #
            # self.face_locations = faceCascade.detectMultiScale(
            #  gray,
            #  scaleFactor=1.1,
            #  minNeighbors=5,
            #  minSize=(30, 30)
            #  #flags = cv2.CV_HAAR_SCALE_IMAGE
            # )
            # recognize = Recognize()

            self.face_names = Recognize.process(frame=frame, face_locations=self.face_locations,
                                                known_face_encodings=self.known_encodings,
                                                known_face_names=self.known_names)
            print(self.face_names)

    def stop(self):
        self.stopped = True


class Duplicate:
    def duplicate():
        # base_dir = os.getcwd()
        img_dir = os.chdir(os.path.Pic)
        current_names = []
        current_encodings = []

        for images in os.listdir(img_dir):
            image = face_recognition.load_image_file(os.path.join(img_dir, images))
            face_encodings = face_recognition.face_encodings(image)[0]
            current_encodings.append(face_encodings)
            current_names.append(images)
        # n = len(known_face_encodings)
        # print(n)

        count = 0
        faces_to_delete = []
        while count < len(current_encodings):
            temp_array = list(current_encodings)
            temp_array.pop(count)

            same = face_recognition.compare_faces(temp_array, current_encodings[count])
            # print(same)

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
        # print(faces_to_delete)
        known_face_encodings = current_encodings
        known_face_names = current_names
        return known_face_encodings, known_face_names


# Retrain - TODO
class Retrain:
    def retrain():
        base_dir = os.getcwd()
        img_dir = os.chdir(r"C:\Users\hp\PycharmProjects\pythonProject34\dev\trydjango\src\Pictures")
        known_face_encodings = []
        known_face_names = []
        for images in os.listdir(img_dir):
            image = face_recognition.load_image_file(os.path.join(img_dir, images))
            face_encoding = face_recognition.face_encodings(image)
            known_face_encodings.append(face_encoding[0])
            known_face_names.append(images)
            return known_face_encodings, known_face_names


class Recognize:
    def process(frame, face_locations, known_face_encodings, known_face_names):
        face_encodings = []
        face_names = []

        [known_face_encodings, known_face_names] = Duplicate.duplicate()
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        # print(face_locations)
        for face_encoding in face_encodings:

            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                name1 = name.split('.')[0]
                # speaker(name1, 100, 0)
            if len(face_locations) == 1:
                if name == "Unknown":
                    CaptureImage.take_photo(frame)
            face_names.append(name)

        return face_names


def main():
    # # Load a sample picture and learn how to recognize it.
    # favour_image = face_recognition.load_image_file("images/favour.jpg")
    # favour_face_encoding = face_recognition.face_encodings(favour_image)[0]

    # # Load a second sample picture and learn how to recognize it.
    # donald_image = face_recognition.load_image_file("images/donald.jpg")
    # donald_face_encoding = face_recognition.face_encodings(donald_image)[0]

    # # Create arrays of known face encodings and their names
    # known_face_encodings = [
    #     favour_face_encoding,
    #     donald_face_encoding
    # ]
    # known_face_names = [
    #     "Favour Odiyo",
    #     "Donald Mkpanam"
    # ]
    # Duplicate.duplicate()
    known_face_encodings, known_face_names = Duplicate.duplicate()

    capture = CaptureVideo().start()  # Start the capturing thread
    face_detector = DetectFace(capture=capture, known_encodings=known_face_encodings,
                               known_names=known_face_names).start()  # Start the face detection thread

    while True:
        if capture.stopped:
            capture.stop()
            break

        frame = capture.read()  # read a frame from the capturing thread
        # frame = imutils.resize(frame, width=450)
        face_locations = face_detector.face_locations  # ask the face detector to send you locations if any
        frame = imutils.resize(frame, width=450)  # resize the frame because the detector is also resizing the frame

        for top, right, bottom, left in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)  # Draw the rectangles

        # for (x, y, w, h) in face_locations:
        #           cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow('Video', frame)  # Show the video
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    capture.stop()  # kill the capture thread
    face_detector.stop()  # kill the detect thread
    cv2.destroyAllWindows()


main()