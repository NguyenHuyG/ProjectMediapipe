import cv2 as cv

cap = cv.VideoCapture(0)
while True:
    ret, image = cap.read()
    if not ret:
        break

    cv.imshow("Test1", image)

    if cv.waitKey(1) == 27:
        break

cap.release()
cv.destroyAllWindows()
