import cv2
import easygui
import math
import numpy as np
import operator

global pt_list

def paint_window(img_org):
    img_bg = img_org.copy()
    for pt in pt_list:
        cv2.circle(img_bg, ( pt[0], pt[1]), 5, (0, 0, 255), 2)
    cv2.imshow('IMG_ORG_VIEW', img_bg)

def mouse_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pt_list.append((x,y))
        paint_window(param)

    elif event == cv2.EVENT_RBUTTONDOWN:
        for pt in pt_list:
            #원의 방정식 if ((x - pt[0]) ** 2 + (y - pt[1]) ** 2) < 25:
            if math.sqrt((x - pt[0]) ** 2 + (y - pt[1]) ** 2) < 5: #유클리드 거리
                pt_list.remove(pt)
                paint_window(param)


pt_list = []
cv2.namedWindow("IMG_ORG_VIEW")

#file_name = easygui.fileopenbox(default="*.jpg",filetypes = ["*.jpg", "*.png"  ])
file_name = easygui.fileopenbox()

#imread 함수를 사용할 때는 파일 경로 및 파일 이름에 한글이 있으면 에러가 나니,
#imread 함수 대신에 아래와 같이 2개의 함수로 사용하세요
#img_array = np.fromfile(file_name, np.uint8)
#img_org = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

img_org = cv2.imread(file_name)

cv2.imshow("IMG_ORG_VIEW", img_org)

cv2.setMouseCallback("IMG_ORG_VIEW", mouse_event, img_org)

ret = easygui.buttonbox("작업을 선택하세요.", "이미지 처리", ("처리하기", "취소"))

if ret == "처리하기" and len( pt_list) == 4:

    #좌표점 순서 정렬 1번점 y 좌표 2개 중 x좌표 작은 것, 2번점 x좌표 큰 것, 
    # 3번점 x좌표 큰 것 2개 중 y좌표 작은 것
    pt_list.sort(key=operator.itemgetter(1))
    pt_list_clockwise = []
    if pt_list[0][0] < pt_list[1][0] :
        pt_list_clockwise.append(pt_list[0])
        pt_list_clockwise.append( pt_list[1])
    else:
        pt_list_clockwise.append(pt_list[1])
        pt_list_clockwise.append( pt_list[0])
    
    if pt_list[2][0] > pt_list[3][0] :
        pt_list_clockwise.append(pt_list[2])
        pt_list_clockwise.append( pt_list[3])
    else:
        pt_list_clockwise.append(pt_list[3])
        pt_list_clockwise.append( pt_list[2])

    w,h=720,400
    #너비 및 높이 결정
    
    w_1 = int ( math.dist(pt_list_clockwise[0], pt_list_clockwise[1]))
    w_2 = int ( math.dist(pt_list_clockwise[3], pt_list_clockwise[2]))

    w = int( (w_1 + w_2) / 2 )
    
    h_1 = int ( math.dist(pt_list_clockwise[0], pt_list_clockwise[3]))
    h_2 = int ( math.dist(pt_list_clockwise[1], pt_list_clockwise[2]))
     
    h = int ( (h_1 + h_2) / 2 )

    srcPts = np.array( [pt_list_clockwise[0], pt_list_clockwise[1], pt_list_clockwise[2], pt_list_clockwise[3]], np.float32)
    dstPts = np.array ([ [0,0], [w-1,0], [w-1, h-1], [0, h-1]], np.float32)

    #indexError 처리
    transM = cv2.getPerspectiveTransform(srcPts, dstPts)
    dst = cv2.warpPerspective(img_org, transM, (w,h))
    
    cv2.imshow("IMG_DST_VIEW", dst)

cv2.waitKey()
cv2.destroyAllWindows()