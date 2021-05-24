import face_recognition
import cv2
from PIL import Image
import os
import numpy as np
from io import BytesIO

class FaceAuth:
    def authenticate(self, user_image_db_bytes, captured_user_image_bytes):
        # use numpy to construct an array from the bytes
        user_image_db_pil = Image.open(BytesIO(user_image_db_bytes)).convert("RGB")
        # convert to np array
        user_image_db_arr = np.array(user_image_db_pil) 
        # Convert RGB to BGR 
        user_image_db = user_image_db_arr[:, :, ::-1].copy()

        # use numpy to construct an array from the bytes
        captured_user_image_pil = Image.open(BytesIO(captured_user_image_bytes)).convert("RGB")
        # convert to np array
        captured_user_image_arr = np.array(captured_user_image_pil) 
        # Convert RGB to BGR 
        captured_user_image = captured_user_image_arr[:, :, ::-1].copy()

        user_image_db_encodings = face_recognition.face_encodings(user_image_db)[0]
        captured_user_image_encodings = face_recognition.face_encodings(captured_user_image)[0]

        #Compare the image in out databse with the recently captured one to see if its the same person
        check = face_recognition.compare_faces([user_image_db_encodings], captured_user_image_encodings)

        if check[0]:
            print("Authenticated")
            return True
        else:
            print("Unauthorized")
            return False




