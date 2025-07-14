import time
import cv2
import cv2 as cv
import mediapipe as mp
import pygame as pg
import configparser as cf
import os
import datetime as dt

parent_folder = os.getcwd()

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

pg.mixer.init()
Alert_sound = os.path.join(parent_folder, "Sound.mp3")
pg.mixer.music.load(Alert_sound)
Alert_LT = 0
Alert_CD = 3

Reason = ["Cui dau thap", "Ngoi lech vai", "Gan mat", "Gap lung"]

config = cf.ConfigParser()
config.read(os.path.join(parent_folder,"Setting.ini"))

def play_alert():
    global Alert_LT
    now = time.time()
    if now - Alert_LT > Alert_CD:
        pg.mixer.music.stop()
        pg.mixer.music.play()
        Alert_LT = now

def texthide(str):
    cv.putText(img, str, (20, 40), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

def SaveImg(img, reason):
    folder_path = os.path.join(parent_folder,"Capture")
    os.makedirs(folder_path, exist_ok=True)

    now = dt.datetime.now()
    time_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{reason}_{time_str}.jpg"
    file_path = os.path.join(folder_path, file_name)

    cv.imwrite(file_path,img)

cap = cv.VideoCapture(0)

while True:
    ret, img = cap.read()

    if not ret:
        break

    img = cv.flip(img,1)
    h, w = img.shape[:2]

    img_rgb = cv.cvtColor(img, cv2.COLOR_BGR2RGB)
    res = pose.process(img_rgb)

    if res.pose_landmarks:
        lm = res.pose_landmarks.landmark
        mp_draw.draw_landmarks(img, res.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        nose         = lm[mp_pose.PoseLandmark.NOSE].y * h
        l_shoulder_y = lm[mp_pose.PoseLandmark.LEFT_SHOULDER].y * h
        l_shoulder_x = lm[mp_pose.PoseLandmark.LEFT_SHOULDER].x * w
        r_shoulder_y = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * h
        r_shoulder_x = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * w
        l_eye        = lm[mp_pose.PoseLandmark.LEFT_EYE].x * w
        r_eye        = lm[mp_pose.PoseLandmark.RIGHT_EYE].x * w
        l_hip_x      = lm[mp_pose.PoseLandmark.LEFT_HIP].x * w
        l_hip_y      = lm[mp_pose.PoseLandmark.LEFT_HIP].y * h
        r_hip_x      = lm[mp_pose.PoseLandmark.RIGHT_EYE].x * w
        r_hip_y      = lm[mp_pose.PoseLandmark.RIGHT_EYE].y * h

        shoulder_diff = abs(l_shoulder_y - r_shoulder_y)
        eye_dist_px   = abs(l_eye - r_eye)
        L_back_dx     = abs(l_shoulder_x - l_hip_x)
        L_back_dy     = abs(l_shoulder_y - l_hip_y)
        R_back_dx     = abs(l_shoulder_x - l_hip_x)
        R_back_dy     = abs(r_shoulder_y - l_hip_y)

        Setting1 = [config.getint("Sensitivity","nose"), config.getint("Sensitivity","shoulder"), config.getint("Sensitivity","eye"), config.getint("Sensitivity","back")]
        Setting2 = config.getboolean("SaveConfig","turn")

        pose_wrong = False
        if nose - l_shoulder_y > Setting1[0] or nose - r_shoulder_y > Setting1[0]:
            texthide(Reason[0])
            play_alert()
            if Setting2:
                SaveImg(img, Reason[0])

        if shoulder_diff > Setting1[1]:
            texthide(Reason[1])
            play_alert()
            if Setting2:
                SaveImg(img, Reason[1])

        if eye_dist_px > Setting1[2]:
            texthide(Reason[2])
            play_alert()
            if Setting2:
                SaveImg(img, Reason[2])

        if L_back_dy < Setting1[3] and L_back_dx > Setting1[3] and not pose_wrong or R_back_dy < Setting1[3] and R_back_dx > Setting1[3]:
            texthide(Reason[3])
            play_alert()
            if Setting2:
                SaveImg(img, Reason[3])

    cv.imshow("T1", img)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv.destroyAllWindows()
pg.mixer.quit()
