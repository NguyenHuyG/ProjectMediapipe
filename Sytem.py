import time
import cv2
import cv2 as cv
import mediapipe as mp
import pandas as pd
import pygame as pg
import configparser as cf
import os
import datetime as datetime
from mutagen.mp3 import MP3

parent_folder = os.getcwd()

Alert_sound = os.path.join(parent_folder, "Sound.mp3")
Alert_Audio = MP3(os.path.join(parent_folder, "Sound.mp3"))

config = cf.ConfigParser()
config.read(os.path.join(parent_folder,"Setting.ini"))

Setting1 = [config.getint("Sensitivity", "nose"), config.getint("Sensitivity", "shoulder"), config.getint("Sensitivity", "eye"), config.getint("Sensitivity", "back")]
Setting2 = [config.getboolean("SaveConfig", "cap"), config.getboolean("SaveConfig", "excel")]
CD_1 = int(round((Alert_Audio.info.length / 2),0)) + 1
print(CD_1)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

pg.mixer.init()
pg.mixer.music.load(Alert_sound)
Alert_LT = 0
Alert_CD = CD_1

Reason = ["Cui dau thap", "Ngoi lech vai", "Gan mang hinh", "Gap lung"]
Fix = ["Cui dau vua du", "Ngoi dung tu the", "Xa man hinh hon", "Ngoi Thang lung"]
data = []

LT_1 = 0

File_path = os.path.join(parent_folder, "File")
os.makedirs(File_path, exist_ok=True)

folder_path = os.path.join(File_path, "Capture")
os.makedirs(folder_path, exist_ok=True)

excel_folder = os.path.join(File_path, "Logs")
os.makedirs(excel_folder, exist_ok=True)

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

    now = datetime.datetime.now()
    time_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{reason}_{time_str}.jpg"
    file_path = os.path.join(folder_path, file_name)

    cv.imwrite(file_path,img)

def AppendData(str1, str2):
    data.append([datetime.datetime.now().strftime("%H:%M:%S"), str1, str2])

def save_exel():
    df = pd.DataFrame(data, columns=["Thời gian","Lý do","Khắc phục"])
    df.to_excel(file_name, index=False)

cap = cv.VideoCapture(0)

now = datetime.datetime.now()
file_name = os.path.join(excel_folder, now.strftime("log_%Y-%m-%d_%H-%M-%S.xlsx"))

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

        current_time = time.time()

        if nose - l_shoulder_y > Setting1[0] or nose - r_shoulder_y > Setting1[0]:
            texthide(Reason[0])
            play_alert()
            print("1", nose, l_shoulder_y, nose - l_shoulder_y)
            print("2", nose, r_shoulder_y, nose - r_shoulder_y)
            if current_time - LT_1 >= CD_1:
                LT_1 = time.time()
                if Setting2[0]:
                    SaveImg(img, Reason[0])
                if Setting2[1]:
                    AppendData(Reason[0],Fix[0])

        if shoulder_diff > Setting1[1]:
            texthide(Reason[1])
            play_alert()
            if current_time - LT_1 >= CD_1:
                LT_1 = time.time()
                if Setting2[0]:
                    SaveImg(img, Reason[1])
                if Setting2[1]:
                    AppendData(Reason[1],Fix[1])

        if eye_dist_px > Setting1[2]:
            texthide(Reason[2])
            play_alert()
            if current_time - LT_1 >= CD_1:
                LT_1 = time.time()
                if Setting2[0]:
                    SaveImg(img, Reason[2])
                if Setting2[1]:
                    AppendData(Reason[2],Fix[2])

        if L_back_dy < Setting1[3] and L_back_dx > Setting1[3] or R_back_dy < Setting1[3] and R_back_dx > Setting1[3]:
            texthide(Reason[3])
            play_alert()
            if current_time - LT_1 >= CD_1:
                LT_1 = time.time()
                if Setting2[0]:
                    SaveImg(img, Reason[3])
                if Setting2[1]:
                    AppendData(Reason[3],Fix[3])

    cv.imshow("T1", img)

    if cv.waitKey(1) == 27:
        break

cap.release()
cv.destroyAllWindows()
pg.mixer.quit()
save_exel()
