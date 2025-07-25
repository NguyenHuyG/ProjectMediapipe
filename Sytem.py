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
now = datetime.datetime.now()

Alert_sound = os.path.join(parent_folder, "Sound.mp3")
Alert_Audio = MP3(os.path.join(parent_folder, "Sound.mp3"))

window_name = "T1"
cv.namedWindow(window_name, cv.WINDOW_NORMAL)
cv.resizeWindow(window_name, 640, 480)

config = cf.ConfigParser()
config.read(os.path.join(parent_folder,"Setting.ini"))

Setting1 = [config.getint("Sensitivity", "nose"), config.getint("Sensitivity", "shoulder"), config.getint("Sensitivity", "eye"), config.getint("Sensitivity", "back")]
Setting2 = [config.getboolean("SaveConfig", "cap"), config.getboolean("SaveConfig", "excel"),config.getboolean("SaveConfig","top")]
CD_1 = int(round((Alert_Audio.info.length / 2),0)) + 1

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

pg.mixer.init()
pg.mixer.music.load(Alert_sound)
Alert_LT = 0
Alert_CD = CD_1

Reason = ["Cui dau thap", "Ngoi lech vai trai","Ngoi lech vai phai", "Gan mang hinh", "Gap lung"]
Fix = ["Cui dau vua du", "Ngoi dung tu the", "Xa man hinh hon", "Ngoi Thang lung"]
data = []

LT_1 = [0,0,0,0,0]

File_path = os.path.join(parent_folder, "File")
os.makedirs(File_path, exist_ok=True)

folder_path = os.path.join(File_path, "Capture")
os.makedirs(folder_path, exist_ok=True)

timestr = now.strftime("%Y-%m-%d_%H-%M-%S")
Folder_B_path = os.path.join(folder_path, timestr)
os.makedirs(Folder_B_path, exist_ok=True)

excel_folder = os.path.join(File_path, "Logs")
os.makedirs(excel_folder, exist_ok=True)

if Setting2[2]:
    cv.setWindowProperty(window_name, cv.WND_PROP_TOPMOST, 1)

def play_alert():
    global Alert_LT
    now = time.time()
    if now - Alert_LT > Alert_CD:
        pg.mixer.music.play()
        Alert_LT = now

def texthide(str,x,y,s):
    cv.putText(img, str, (x, y), cv.FONT_HERSHEY_SIMPLEX, s, (0, 0, 255), 2)

def SaveImg(img, reason):
    time_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{reason}_{time_str}.jpg"
    file_path = os.path.join(Folder_B_path, file_name)

    cv.imwrite(file_path,img)

def AppendData(str1, str2):
    data.append([datetime.datetime.now().strftime("%H:%M:%S"), str1, str2])

def save_exel():
    if Setting2[1]:
        file_name = os.path.join(excel_folder, now.strftime("log_%Y-%m-%d_%H-%M-%S.xlsx"))

        df = pd.DataFrame(data, columns=["Thời gian","Lý do","Khắc phục"])
        df.to_excel(file_name, index=False)

cap = cv.VideoCapture(0)

while True:
    if Setting2[2]:
        ret, img = cap.read()
    else:
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

        nose_y       = lm[mp_pose.PoseLandmark.NOSE].y * h
        nose_x       = lm[mp_pose.PoseLandmark.NOSE].x * w
        l_shoulder_y = lm[mp_pose.PoseLandmark.LEFT_SHOULDER].y * h
        l_shoulder_x = lm[mp_pose.PoseLandmark.LEFT_SHOULDER].x * w
        r_shoulder_y = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * h
        r_shoulder_x = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * w
        l_eye        = lm[mp_pose.PoseLandmark.LEFT_EYE].x * w
        r_eye        = lm[mp_pose.PoseLandmark.RIGHT_EYE].x * w
        l_hip_x      = lm[mp_pose.PoseLandmark.LEFT_HIP].x * w
        l_hip_y      = lm[mp_pose.PoseLandmark.LEFT_HIP].y * h
        r_hip_x      = lm[mp_pose.PoseLandmark.RIGHT_HIP].x * w
        r_hip_y      = lm[mp_pose.PoseLandmark.RIGHT_HIP].y * h

        shoulder_diff = abs(l_shoulder_y - r_shoulder_y)
        eye_dist_px   = abs(l_eye - r_eye)
        L_back_dx     = abs(l_shoulder_x - l_hip_x)
        L_back_dy     = abs(l_shoulder_y - l_hip_y)
        R_back_dx     = abs(l_shoulder_x - l_hip_x)
        R_back_dy     = abs(r_shoulder_y - l_hip_y)

        current_time = time.time()

        if nose_y - l_shoulder_y > Setting1[0] or nose_y - r_shoulder_y > Setting1[0]:
            texthide(Reason[0], int(round(nose_x,0) + 25), int(round(nose_y,0) - 25), 0.7)
            play_alert()
            if current_time - LT_1[0] >= CD_1:
                LT_1[0] = time.time()
                if Setting2[0]:
                    SaveImg(img, Reason[0])
                if Setting2[1]:
                    AppendData(Reason[0],Fix[0])

        if shoulder_diff > Setting1[1]:
            play_alert()
            if l_shoulder_y > r_shoulder_y:
                texthide(Reason[1], int(round(r_shoulder_x) - 80), int(round(r_shoulder_y) - 35), 0.7)
            else:
                texthide(Reason[2], int(round(l_shoulder_x) - 80), int(round(l_shoulder_y) - 35), 0.7)

            if Setting2[0] and current_time - LT_1[1] >= CD_1:
                LT_1[1] = time.time()
                SaveImg(img, Reason[1])
            if Setting2[1] and current_time - LT_1[2] >= CD_1:
                LT_1[2] = time.time()
                AppendData(Reason[2],Fix[1])

        if eye_dist_px > Setting1[2]:
            texthide(Reason[3], int(round(nose_x) - 200), int(round(nose_y) - 100),1.5)
            play_alert()
            if current_time - LT_1[3] >= CD_1:
                LT_1[3] = time.time()
                if Setting2[0]:
                    SaveImg(img, Reason[2])
                if Setting2[1]:
                    AppendData(Reason[2],Fix[2])

        if L_back_dy < Setting1[3] and L_back_dx > Setting1[3] or R_back_dy < Setting1[3] and R_back_dx > Setting1[3]:
            texthide(Reason[4], 20, 40, 0.7)
            play_alert()
            if current_time - LT_1[4] >= CD_1:
                LT_1[4] = time.time()
                if Setting2[0]:
                    SaveImg(img, Reason[4])
                if Setting2[1]:
                    AppendData(Reason[4],Fix[3])

    cv.imshow(window_name, img)

    if cv.waitKey(1) == 27:
        break

cap.release()
cv.destroyAllWindows()
pg.mixer.quit()
save_exel()
