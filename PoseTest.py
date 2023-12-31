#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from just_playback import Playback
playback = Playback()
playback.load_file(r"C:\Users\Sanskar\Downloads\lowdrum.mp3")
playback2 = Playback()
playback2.load_file(r"C:\Users\Sanskar\Downloads\highdrumsnare.mp3")
import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# For static images:
IMAGE_FILES = []
BG_COLOR = (192, 192, 192) # gray
with mp_pose.Pose(
    static_image_mode=True,
    model_complexity=2,
    enable_segmentation=True,
    min_detection_confidence=0.5) as pose:
  for idx, file in enumerate(IMAGE_FILES):
    image = cv2.imread(file)
    image_height, image_width, _ = image.shape
    # Convert the BGR image to RGB before processing.
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    image_height, image_width, _ = image.shape

    if not results.pose_landmarks:
      continue
    print(
        f'Nose coordinates: ('
        f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * image_width}, '
        f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_height})'
    )

    annotated_image = image.copy()
    # Draw segmentation on the image.
    # To improve segmentation around boundaries, consider applying a joint
    # bilateral filter to "results.segmentation_mask" with "image".
    condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
    bg_image = np.zeros(image.shape, dtype=np.uint8)
    bg_image[:] = BG_COLOR
    annotated_image = np.where(condition, annotated_image, bg_image)
    # Draw pose landmarks on the image.
    mp_drawing.draw_landmarks(
        annotated_image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)
    # Plot pose world landmarks.
    mp_drawing.plot_landmarks(
        results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

varcount1 = 0
varcount2 = 0

    
# For webcam input:
cap = cv2.VideoCapture(0)
logo1 = cv2.imread(r"C:\Users\Sanskar\Downloads\snare.png")
img2gray = cv2.cvtColor(logo1, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)
logo2 = cv2.imread(r"C:\Users\Sanskar\Downloads\drumbass.png")
img2gray2 = cv2.cvtColor(logo2, cv2.COLOR_BGR2GRAY)
ret2, mask2 = cv2.threshold(img2gray2, 1, 255, cv2.THRESH_BINARY)

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    image_height, image_width, _ = image.shape

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    lm = results.pose_landmarks
    lmPose = mp_pose.PoseLandmark
    rwrist_x = int(lm.landmark[lmPose.RIGHT_WRIST].x * image_width)
    rwrist_y = int(lm.landmark[lmPose.RIGHT_WRIST].y * image_height)
    lwrist_x = int(lm.landmark[lmPose.LEFT_WRIST].x * image_width)
    lwrist_y = int(lm.landmark[lmPose.LEFT_WRIST].y * image_height)
    print(rwrist_x, rwrist_y, lwrist_x, lwrist_y)
    if(lwrist_y>300):
        if(varcount1==0):
            playback.play()
            varcount1=1
    else:
        varcount1=0
    if(rwrist_y>300):
        if(varcount2==0):
            playback2.play()
            varcount2=1
    else:
        varcount2=0
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()

