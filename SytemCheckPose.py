# --- import libarary ---
import time
import cv2
import cv2 as cv
import mediapipe as mp
import pygame as pg
import configparser as cf
import os

# --- started mediapipe (pose) ---
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

# --- started pygame (sound) ---
pg.mixer.init()
Alert_sound = "alert.mp3"
pg.mixer.music.load(Alert_sound)
Alert_LT = 0
Alert_CD = 3

# --- Folder parent (folder) ---
parent_folder = os.getcwd()

# --- Started config (setting) ---
config = cf.ConfigParser()
config.read(os.path.join(parent_folder,"Setting.ini"))

# --- play sound (sound) ---
def play_alert():
    global Alert_LT
    now = time.time()
    if now - Alert_LT > Alert_CD:
        pg.mixer.music.stop()
        pg.mixer.music.play()
        Alert_LT = now

# --- text hide (Text) ---
def texthide(str):
    cv.putText(img, str, (20, 40), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

# --- Open Webcame (Webcame) ---
cap = cv.VideoCapture(0)

while True:
    ret, img = cap.read()

    if not ret:
        break

    img = cv.flip(img,1)
    h, w = img.shape[:2]

    img_rgb = cv.cvtColor(img, cv2.COLOR_BGR2RGB)
    res = pose.process(img_rgb)

    # --- Check landmarks in body (body) ---
    if res.pose_landmarks:
        lm = res.pose_landmarks.landmark
        mp_draw.draw_landmarks(img, res.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # --- Landmarks position to pixel ---
        nose         = lm[mp_pose.PoseLandmark.NOSE].y * h
        l_shoulder_y = lm[mp_pose.PoseLandmark.LEFT_SHOULDER].y * h
        l_shoulder_x = lm[mp_pose.PoseLandmark.LEFT_SHOULDER].x * w
        r_shoulder_y = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * h
        r_shoulder_x = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * w
        l_eye        = lm[mp_pose.PoseLandmark.LEFT_EYE].y * h
        r_eye        = lm[mp_pose.PoseLandmark.RIGHT_EYE].y * h
        l_hip_x      = lm[mp_pose.PoseLandmark.LEFT_HIP].x * w
        l_hip_y      = lm[mp_pose.PoseLandmark.LEFT_HIP].y * h
        r_hip_x      = lm[mp_pose.PoseLandmark.RIGHT_EYE].x * w
        r_hip_y      = lm[mp_pose.PoseLandmark.RIGHT_EYE].y * h

        # --- abs (Data) ---
        shoulder_diff = abs(l_shoulder_y - r_shoulder_y)
        eye_dist_px   = abs(l_eye - r_eye)
        L_back_dx     = abs(l_shoulder_x - l_hip_x)
        L_back_dy     = abs(l_shoulder_y - l_hip_y)
        R_back_dx     = abs(l_shoulder_x - l_hip_x)
        R_back_dy     = abs(r_shoulder_y - l_hip_y)

        # --- Sensitivity in setting.ini (setting) ---
        Setting1 = [config.getint("Sensitivity","nose"), config.getint("Sensitivity","shoulder"), config.getint("Sensitivity","eye"), config.getint("Sensitivity","back")]

        # --- Check and Notification ---
        if nose - l_shoulder_y > Setting1[0] or nose - r_shoulder_y > Setting1[0]:
            texthide("Cui dau thap")
            play_alert()

        if shoulder_diff > Setting1[1]:
            texthide("Ngoi lech vai")
            play_alert()

        if eye_dist_px > Setting1[2]:
            texthide("Gan man hinh")
            play_alert()

        if L_back_dy > Setting1[3] and L_back_dx < Setting1[3] or R_back_dy > Setting1[3] and R_back_dx > Setting1[3]:
            texthide("Gap lung")
            play_alert()

    cv.imshow("T1", img)

    if cv2.waitKey(1) == 27:
        break

# Free resources when close app
cap.release()
cv.destroyAllWindows()
pg.mixer.quit()