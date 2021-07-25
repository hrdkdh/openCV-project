import cv2

img_hat = cv2.imread("hat.png", cv2.IMREAD_UNCHANGED);
img_hat = cv2.resize(img_hat,(200,100))
_,mask = cv2.threshold(img_hat[:,:,3],1,255,cv2.THRESH_BINARY)

mask_inv = cv2.bitwise_not(mask)
img_hat = cv2.cvtColor(img_hat,cv2.COLOR_BGRA2BGR)

face_cascade = cv2.CascadeClassifier("xml/haarcascade_frontalface_alt2.xml")

cap = cv2.VideoCapture(0)

while True:
	ret, frame = cap.read()
	img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(img_gray, 1.3, 5)
	for (x,y,w,h) in faces:
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0 ),2)

		x1=int((x+(w/2))-(img_hat.shape[1]/2))
		x2=int((x+(w/2))+(img_hat.shape[1]/2))
		y1 = y - img_hat.shape[0] - 10
		y2 = y - 10
		if x1 < 0 or y1 < 0 or x2 >= frame.shape[1] or y2 >= frame.shape[0]:
			continue
		roi = frame[y1:y2, x1:x2]
		masked_fg = cv2.bitwise_and(img_hat, img_hat, mask=mask)
		masked_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

		added = masked_fg + masked_bg

		frame[y1:y2, x1:x2] = added
		#frame[y1:y2, x1:x2]= img_hat

		cv2.imshow('frame_win', frame)

	if cv2.waitKey(1) == 32:
		break
	
cap.release()
cv2.destroyAllWindows()