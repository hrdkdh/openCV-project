import cv2
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)

img_fg = cv2.imread("glasses.png", cv2.IMREAD_UNCHANGED);
img_fg = cv2.resize(img_fg,(300,130))

_,mask = cv2.threshold(img_fg[:,:,3],1,255,cv2.THRESH_BINARY) #mask = img_fg[:,:,3]

mask_inv = cv2.bitwise_not(mask)


img_fg = cv2.cvtColor(img_fg,cv2.COLOR_BGRA2BGR)
img_bg = cv2.imread("jr.jpg")


roi = img_bg[250:380, 120:420]

#cv2.bitwise_and(src1, src2, mask) 는 mask의 값이 0이 아닌 부분만 src1과 src2를 AND 연산 합니다. 
# mask의 값이 0인 부분은 mask로 그대로 씌워두는 것이죠.
#cv2.bitwise_and() 함수의 인자로 사용되는 mask는 1채널 값이어야 하므로 대부분 흑백 이미지입니다. 
# mask의 값이 0이 아닌 부분은 곧 흰색 부분을 말하므로 
# mask의 검정색 부분은 연산을 하지 않고 검정색 그대로 이미지에 놓여지게 됩니다.

masked_fg= cv2.bitwise_and(img_fg,img_fg, mask=mask)

masked_bg = cv2.bitwise_and(roi,roi,mask=mask_inv)


added = cv2.add(masked_bg, masked_fg) #added = masked_bg + masked_fg


img_bg [250:380,120:420] = added

cv2.imshow("win_main",img_bg)
cv2.waitKey()
cv2.destroyAllWindows()
