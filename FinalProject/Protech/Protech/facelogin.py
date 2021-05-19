import face_recognition
import cv2
from PIL import Image
import os

# Make web cam take a picture
web_cam = cv2.VideoCapture(0) 
success, captured_user_image = web_cam.read()

if success:
    # Get current dir of app
    cwd = os.getcwd()

    # This is the image from the database
    user_image_db = face_recognition.load_image_file(cwd + "\images\\face2.jpeg")
    user_image_db_encodings = face_recognition.face_encodings(user_image_db)[0]

    # Reduce user image size 25%
    resized_user_image = cv2.resize(captured_user_image, (0, 0), fx = 0.25, fy = 0.25)
    resized_rgb_user_image = resized_user_image[:, :, ::-1]

    # With the recently captured image, get the face location and the encondings
    captured_user_image_locations = face_recognition.face_locations(resized_rgb_user_image)
    captured_user_image_encodings = face_recognition.face_encodings(resized_rgb_user_image)

    #Compare the image in out databse with the recently captured one to see if its the same person
    check = face_recognition.compare_faces(user_image_db_encodings, captured_user_image_encodings)

    # Get the positions of where the recently captured image's user face is located
    top, right, bottom, left = (face_recognition.face_locations(captured_user_image))[0]

    # Print only for debug to see were the face is
    # print("found face at top: {}, left: {}, bottom {}, right {}".format(top, left, bottom, right))
    
    # For debug, save an image that corresponds only to the image that has only the detected user's face
    captured_user_face_image = captured_user_image[top:bottom, left:right]
    pil_image = Image.fromarray(captured_user_face_image)
    pil_image.save(cwd + "\images\\result.jpg")

    if check[0]:
        print("You have been authenticated")
    else:
        print("Not Authenticated. User's face doesn't match with our registers")


