# encode.py - Utility to populate the database

import cv2
import face_recognition
import pickle
import os

folderPath = 'static/faces'
modelPathList = os.listdir(folderPath)

imgList = []
imgIds = []

for path in modelPathList:
    img = cv2.imread(os.path.join(folderPath, path))
    if img is not None:
        imgList.append(img)
        imgIds.append(os.path.splitext(path)[0])
   
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)
        if encodings:
            encodeList.append(encodings[0])
    return encodeList

encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, imgIds]

with open("Encodefile.p", 'wb') as file:
    pickle.dump(encodeListKnownWithIds, file)

print("Encoding saved successfully.")
