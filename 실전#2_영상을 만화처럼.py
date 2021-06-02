import cv2

def onChange(pos):
    pass

cv2.namedWindow("frame_win")
cv2.namedWindow("sketch_win")
cv2.createTrackbar("trackbar_sigma", "sketch_win", 1, 20, onChange)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    sigma = cv2.getTrackbarPos('trackbar_sigma','sketch_win')
    
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_gray_blur = cv2.GaussianBlur(img_gray, (0, 0), sigma)
    img_sketch_img = cv2.divide(img_gray, img_gray_blur, scale=255)
    
    cv2.imshow('frame_win', frame)
    cv2.imshow('sketch_win', img_sketch_img)
    
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()