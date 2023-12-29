import numpy as np
import dlib
import cv2
import imutils
from threading import Thread
import face_recognition
from datetime import datetime
import os
import requests
import base64
import json

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

class CaptureImage:
    def take_photo(frame):
        now = datetime.now()
        dt_string = now.strftime("%d%m%Y%H%M%S")
        img_name = "{}.png".format(dt_string)
        img_dir = 'Pictures'
        path = os.path.join(img_dir, img_name)
        cv2.imwrite(path, frame)
        return path
    
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
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            if len(face_locations) == 1:
                if name == "Unknown":
                    hash_face = hash(face_encoding.tostring())
                    print(hash_face)
                    img_path = CaptureImage.take_photo(frame)
                    print(img_path)
                    print("begin API call")

                    with open(img_path, "rb") as f:
                        im_bytes = f.read()
                    print("reading complete")
                    im_b64 = base64.b64encode(im_bytes).decode("utf8")

                    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

                    url = 'http://127.0.0.1:8000/register_new_face/'
                    obj = {
                        'name': 'unknown',
                        'image': im_b64,
                        'hash': hash_face
                    }
                    json_object = json.dumps(obj)

                    response = requests.post(url, data=json_object, headers=headers)
                    print(response.text)
                    # try:
                    #     data = response.json()
                    #     print("API Call Success")
                    #     print(data)
                    # except:
                    #     print("API Call Failure")
                    #     print(response.text)

            face_names.append(name)

        return face_names   
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
        face_locations = face_detector.face_locations  # ask the face detector to send you locations if any
        frame = imutils.resize(frame, width=450)  # resize the frame because the detector is also resizing the frame

        for top, right, bottom, left in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)  # Draw the rectangles


        cv2.imshow('Video', frame)  # Show the video
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    capture.stop()  
    cv2.destroyAllWindows()

main()