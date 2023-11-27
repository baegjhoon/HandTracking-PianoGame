import cv2, sys, math
import hand_detector as ht

def get_distance(p1, p2):
    return math.dist((p1[1], p1[2]), (p2[1], p2[2]))

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("카메라를 사용할 수 없는 상태입니다.")
    sys.exit()

cap.set(3, wCam)
cap.set(4, hCam)

detector = ht.handDetector(detectionCon = 0.7)

# 엄지, 검지, 중지, 약지, 새끼 손가락의 끝 좌표
index_fingers = [4, 8, 12, 16, 20]

while True:
    res, frame = cap.read() # 카메라 데이터 읽기

    if not res: # 프레임 읽었는지 확인
        print("카메라를 사용할 수 없는 상태입니다.")
        break

    frame = detector.findHands(frame)
    lmList = detector.findPositions(frame, draw=False)

    if len(lmList) != 0:
        for i in index_fingers:

            x, y = lmList[i][1], lmList[i][2]

            if get_distance(lmList[4], lmList[5]) < get_distance(lmList[3], lmList[5]):
                # fingers = "0" # 접혔으면 0
                print("엄지 접힘")
            else:
                # fingers = "1" # 퍼졌으면 1
                print("엄지 펴짐")
            
            if get_distance(lmList[8], lmList[10]) < get_distance(lmList[8], lmList[11]):
                # fingers = "0" # 접혔으면 0
                print("검지 접힘")
            else:
                # fingers = "1" # 퍼졌으면 1
                print("검지 펴짐")

            if get_distance(lmList[12], lmList[6]) < get_distance(lmList[12], lmList[7]):
                # fingers = "0" # 접혔으면 0
                print("중지 접힘")
            else:
                # fingers = "1" # 퍼졌으면 1
                print("중지 펴짐")

            if get_distance(lmList[16], lmList[18]) < get_distance(lmList[16], lmList[19]):
                # fingers = "0" # 접혔으면 0
                print("약지 접힘")
            else:
                # fingers = "1" # 퍼졌으면 1
                print("약지 펴짐")
            
            if get_distance(lmList[19], lmList[15]) < get_distance(lmList[20], lmList[15]):
                # fingers = "0" # 접혔으면 0
                print("소지 접힘")
            else:
                # fingers = "1" # 퍼졌으면 1
                print("소지 펴짐")

    # if len(lmList) != 0:
    #     # 특정 손가락의 위치에 따라 출력
    #     for i in index_fingers:
    #         x, y = lmList[i][1], lmList[i][2]

    #         if y > hCam - 10:
    #             print("엄지")
    #         elif y > hCam - 50:
    #             print("검지")
    #         elif y > hCam - 100:
    #             print("중지")
    #         elif y > hCam - 150:
    #             print("약지")
    #         elif y > hCam - 200:
    #             print("소지")

    cv2.imshow("Image", frame)

    key = cv2.waitKey(5) & 0xFF # 키보드 입력 받기
    if key == 27 or key == ord('q'): # ESC or q 를 누르면 종료
        break

cv2.destroyAllWindows() # 영상 창 닫기
cap.release() # 비디오 캡처 객체 해재