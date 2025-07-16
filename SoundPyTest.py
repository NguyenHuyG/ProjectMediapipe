# -------------- Khai báo thư viện -------------
import pygame as pg
import time
import keyboard

# ---------- Khởi tạo và nạp âm thanh -----------
pg.mixer.init()
ALERT_SOUND = "alert1.mp3"
pg.mixer.music.load(ALERT_SOUND)

# ----------- Kiểm soát thời gian ---------------
Lasttime = 0
timeCD = 3

# -------------- Phát âm thanh ------------------
while True:
    current_time = time.time() # lấy thời gian hiện tại

    if current_time - Lasttime > timeCD: # so sánh thời gian để tránh lặp
        pg.mixer.music.stop() # tắt âm thanh
        pg.mixer.music.play() # phát âm thanh
        Lasttime = current_time # cập nhật thời gian lasttime

    if keyboard.is_pressed('esc'): # điều kiện thoát vòng lặp khi ấn esc
        break

    time.sleep(0.1) # thời gian nghỉ giúp giảm tài nguyên
