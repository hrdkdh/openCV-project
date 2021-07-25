import cv2
import glob



img_files = glob.glob("images/*.jpg")
img_files.extend(glob.glob("images/*.png"))

if not img_files:
    print("There are no jpg files in 'images' folder")
    sys.exit()

cv2.namedWindow('img_view', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('img_view', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

for f in img_files:
    img = cv2.imread( f )
    if img is None:
        print('Image load failed!')
        break
    
    cv2.imshow("img_view", img) 
    if cv2.waitKey(2000) == 27:
        break
    
    #페이드 아웃
    img_bg = img.copy()
    img_bg.fill(0)
    for i in range(1,11):
        alpha = 1 - ( i / 10.0)
        dst = cv2.addWeighted(img, alpha, img_bg, 1-alpha, 0)
        cv2.imshow("img_view", dst)
        cv2.waitKey(100)

cv2.destroyAllWindows()