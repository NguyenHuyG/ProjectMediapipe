import pygame as pg
import time
import keyboard

pg.mixer.init()
ALERT_SOUND = "alert1.mp3"
pg.mixer.music.load(ALERT_SOUND)

Lasttime = 0
timeCD = 3

while True:
    current_time = time.time()

    if current_time - Lasttime > timeCD:
        pg.mixer.music.play()
        Lasttime = current_time

    if keyboard.is_pressed('esc'):
        break

    time.sleep(0.1)

