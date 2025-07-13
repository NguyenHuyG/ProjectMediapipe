import cv2
import cv2 as cv
import mediapipe as mp

cap = cv.VideoCapture(0)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

while True:
    ret, img = cap.read()

    if not ret:
        break

    if cv.waitKey(1) == 27:
        break

    img_rgb = cv.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = pose.process(img_rgb)

    if result.pose_landmarks:
        mp_draw.draw_landmarks(img, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    cv.imshow("Test1", img)

    if cv.waitKey(1) == 27:
        break

cap.release()
cv.destroyAllWindows()