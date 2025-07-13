# ------------ Khai báo thư viện ------------
import cv2 as cv

# --------- Khởi tạo camera -----------------
cap = cv.VideoCapture(0)

# ----------- Xử lý hình ảnh ----------------
while True:
    ret, image = cap.read() # Đọc camera
    if not ret: # Kiểm tra kết nối với camera
        break

    cv.imshow("Test1", image) # hiển thị khung hình trên cửa sổ Test1 

    if cv.waitKey(1) == 27: # kiểm có nhấn nút esc để thoát khỏi phần mềm
        break

# --- giải phóng tài nguyên khi thoát khỏi vòng lặp
cap.release() # thoát camera
cv.destroyAllWindows() # tắt cửa sổ
