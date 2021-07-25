import cv2
import pytesseract
import numpy as np
import easygui

global ptr_list

def onMouse(event, x, y, flag, param):
    if ( event == cv2.EVENT_MOUSEMOVE):
        for p in ptr_list:
            x_min = min(p[0][0][0],p[1][0][0],p[2][0][0],p[3][0][0] )
            x_max = max (p[0][0][0],p[1][0][0],p[2][0][0],p[3][0][0] )
            y_min = min(p[0][0][1], p[1][0][1], p[2][0][1], p[3][0][1])
            y_max = max(p[0][0][1], p[1][0][1], p[2][0][1], p[3][0][1])
            if ( x_min < x and x_max > x and y_min < y and y_max > y):
                cv2.polylines(param, [p], True, (0, 0, 255), 2, cv2.LINE_AA)
                cv2.imshow("src_win", param)
            else:
                cv2.polylines(param, [p], True, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.imshow("src_win", param)
                   
    if (event== cv2.EVENT_LBUTTONDOWN):
        for p in ptr_list:
            x_min = min(p[0][0][0],p[1][0][0],p[2][0][0],p[3][0][0] )
            x_max = max (p[0][0][0],p[1][0][0],p[2][0][0],p[3][0][0] )
            y_min = min(p[0][0][1], p[1][0][1], p[2][0][1], p[3][0][1])
            y_max = max(p[0][0][1], p[1][0][1], p[2][0][1], p[3][0][1])
            if ( x_min < x and x_max > x and y_min < y and y_max > y and \
                easygui.buttonbox("이 구역을 문자인식합니다.", "@_@", ("처리하기", "취소"))== "처리하기"):
                print( pytesseract.image_to_string(src[y_min:y_max, x_min:x_max],lang="kor+eng") )

src = cv2.imread("two_namecards.jpg")
src = cv2.resize(src,(600,600))

#dw, dh = src.shape[1], src.shape[0]

# 입력 영상 전처리
src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
_, src_bin = cv2.threshold(src_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
#_, src_bin = cv2.threshold(src_gray, 100, 255, cv2.THRESH_BINARY )

ptr_list = []
cv2.namedWindow("src_win")

# 외곽선 검출 및 명함 검출
contours, _ = cv2.findContours(src_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

for pts in contours:
    # 너무 작은 객체는 무시
    if cv2.contourArea(pts) < 1000:
        continue

    # 외곽선 근사화
    approx = cv2.approxPolyDP(pts, cv2.arcLength(pts, True)*0.04, True) #0.02

    # 컨벡스가 아니고, 사각형이 아니면 무시
    if not cv2.isContourConvex(approx) or len(approx) != 4:
        continue

    cv2.polylines(src, [approx], True, (0, 255, 0), 2, cv2.LINE_AA)
    ptr_list.append(approx)

cv2.setMouseCallback("src_win",onMouse, src)

cv2.imshow('src_win', src)

cv2.waitKey()
cv2.destroyAllWindows()