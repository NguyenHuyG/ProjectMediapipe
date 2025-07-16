#--------------- Khai báo thư viện ---------------
import cv2
import cv2 as cv
import mediapipe as mp

#--------------- Quay video bằng camera ----------
cap = cv.VideoCapture(0)

#--------------- Khai ba mediapipe ---------------
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

#--------------- Xử lý hình ảnh ------------------
while True:
    ret, img = cap.read() # đọc camera

    if not ret: # kiểm tra có kết nối với camera
        break

    if cv.waitKey(1) == 27: # điều kiện nhấn esc để thoát
        break

    img_rgb = cv.cvtColor(img, cv2.COLOR_BGR2RGB) # chuyển hình ảnh sang rgb
    result = pose.process(img_rgb) # thực hiện khung sương cơ thể

    if result.pose_landmarks: # Phát hiện các điểm khớp cơ thể
        mp_draw.draw_landmarks(img, result.pose_landmarks, mp_pose.POSE_CONNECTIONS) # vẽ các điểm khớp

    cv.imshow("Test1", img) # hiện khung hình trên của sổ test 1


#--------------- Giải phóng tài nguyên -------------
cap.release() # Tắt camera
cv.destroyAllWindows() # Đòng cửa sổ
