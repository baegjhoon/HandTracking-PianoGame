import pygame, time, os, random
import cv2, sys, math
import numpy as np
import keyboard

import hand_detector as ht

pygame.init()

w = 1600
h = w * (9/16)

screen = pygame.display.set_mode((w, h))

clock = pygame.time.Clock()

main = True
ingame = True

# KEY 입력 감지 Lists
keys = [0, 0, 0, 0, 0]
keyset = [0, 0, 0, 0, 0]

maxframe = 60
fps = 0

gst = time.time()
Time = time.time() - gst

ty = 0 # note
tst = Time # note 생성 시간

t1 = []
t2 = []
t3 = []
t4 = []
t5 = []

Cpath = os.path.dirname(__file__)
Fpath = os.path.join(Cpath, 'assets/fonts')
ingame_font_path = os.path.join(Fpath, 'LeferiPointSpecialItalic.ttf')

rate = "Ready"

ingame_font_rate = pygame.font.Font(ingame_font_path, int(w / 26))

# note 생성 함수
def sum_note(n):
    if n == 1:
        ty = 0
        tst = Time + 2
        t1.append([ty, tst])
    if n == 2:
        ty = 0
        tst = Time + 2
        t2.append([ty, tst])
    if n == 3:
        ty = 0
        tst = Time + 2
        t3.append([ty, tst])
    if n == 4:
        ty = 0
        tst = Time + 2
        t4.append([ty, tst])
    if n == 5:
        ty = 0
        tst = Time + 2
        t5.append([ty, tst])

speed = 1

notesumt = 0

a = 0
aa = 0

spin = 0

combo =  0
combo_effect = 0
combo_effect2 = 0
miss_anim = 0
last_combo = 0

combo_time = Time + 1.2

rate_data = [0, 0, 0, 0, 0]

def rating(n):
    global combo, miss_anim, last_combo, combo_effect, combo_effect2, combo_time, rate
    if abs((h/12) * 9 - rate_data[n - 1] < 950 * speed * (h / 900) and (h / 12) * 9 - rate_data[n - 1] >= 200 * speed * (h / 900)):
        last_combo = combo
        miss_anim = 1
        combo = 0
        combo_effect = 0.2
        combo_time = Time + 1
        combo_effect2 = 1.3
        rate = "Worst"
    if abs((h/12) * 9 - rate_data[n - 1] < 200 * speed * (h / 900) and (h / 12) * 9 - rate_data[n - 1] >= 100 * speed * (h / 900)):
        last_combo = combo
        miss_anim = 1
        combo = 0
        combo_effect = 0.2
        combo_time = Time + 1
        combo_effect2 = 1.3
        rate = "Bad"
    if abs((h/12) * 9 - rate_data[n - 1] < 100 * speed * (h / 900) and (h / 12) * 9 - rate_data[n - 1] >= 50 * speed * (h / 900)):
        combo += 1
        combo_effect = 0.2
        combo_time = Time + 1
        combo_effect2 = 1.3
        rate = "Good"
    if abs((h/12) * 9 - rate_data[n - 1] < 50 * speed * (h / 900) and (h / 12) * 9 - rate_data[n - 1] >= 15 * speed * (h / 900)):
        combo += 1
        combo_effect = 0.2
        combo_time = Time + 1
        combo_effect2 = 1.3
        rate = "Great"
    if abs((h/12) * 9 - rate_data[n - 1] < 15 * speed * (h / 900) and (h / 12) * 9 - rate_data[n - 1] >= 0 * speed * (h / 900)):
        combo += 1
        combo_effect = 0.2
        combo_time = Time + 1
        combo_effect2 = 1.3
        rate = "Perfect"

###### START :: 웹캠, Hand detector ######

# 2개의 랜드마크 사이의 거리 계산
def get_distance(p1, p2):
    return math.dist((p1[1], p1[2]), (p2[1], p2[2]))

wCam = 320
hCam = 240
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("카메라를 사용할 수 없는 상태입니다.")
    sys.exit(
        "카메라 연결을 확인해주세요."
    )

cap.set(3, wCam)
cap.set(4, hCam)

detector = ht.handDetector(detectionCon = 0.6)

# 엄지, 검지, 중지, 약지, 새끼 손가락의 끝 좌표
index_fingers = [4, 8, 12, 16, 20]

###### END :: 웹캠, Hand detector ######
while main:
    while ingame:
        ########## START :: 웹캠, Hand detector ##########
        ret, frame = cap.read() # 카메라 데이터 읽기

        frame = detector.findHands(frame)
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # OpenCV의 BGR을 Pygame의 RGB로 변환
        # frame = np.rot90(frame)  # 화면을 90도 회전
        # frame = pygame.surfarray.make_surface(frame)

        lmList = detector.findPositions(frame, draw=False)

        ########## END :: 웹캠, Hand detector ##########
        
        if len(t1) > 0:
            rate_data[0] = t1[0][0]
        if len(t2) > 0:
            rate_data[1] = t2[0][0]
        if len(t3) > 0:
            rate_data[2] = t3[0][0]
        if len(t4) > 0:
            rate_data[3] = t4[0][0]
        if len(t5) > 0:
            rate_data[4] = t5[0][0]

        # 노트 생성, 생성 시간 설정
        if Time > 0.7 * notesumt:
            notesumt += 1
            
            while a == aa:
                a = random.randint(1, 5)
            sum_note(a)
            aa = a

        Time = time.time() - gst

        fps = clock.get_fps()

        ingame_font_combo = pygame.font.Font(ingame_font_path, int((w / 38) * combo_effect2))
        combo_text = ingame_font_combo.render(str(combo), True, (255, 255, 255))

        rate_text = ingame_font_rate.render(str(rate), True, (255, 255, 255))
        rate_text = pygame.transform.scale(rate_text, (int(w / 110 * len(rate) * combo_effect2), int((w/58 * combo_effect * combo_effect2))))

        ingame_font_miss = pygame.font.Font(ingame_font_path, int(w/38 * miss_anim))
        miss_text = ingame_font_miss.render(str(last_combo), True, (255, 0, 0))

        if fps == 0:
            fps = maxframe


        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    keyset[0] = 1
                    if len(t1) > 0:
                        if t1[0][0] > h/3:
                            rating(1)
                            del t1[0]
                if event.key == pygame.K_s:
                    keyset[1] = 1
                    if len(t2) > 0:
                        if t2[0][0] > h/3:
                            rating(2)
                            del t2[0]
                if event.key == pygame.K_d:
                    keyset[2] = 1
                    if len(t3) > 0:
                        if t3[0][0] > h/3:
                            rating(3)
                            del t3[0]
                if event.key == pygame.K_l:
                    keyset[2] = 1
                    if len(t3) > 0:
                        if t3[0][0] > h/3:
                            rating(3)
                            del t3[0]
                if event.key == pygame.K_SEMICOLON: # KEY: ;
                    keyset[3] = 1
                    if len(t4) > 0:
                        if t4[0][0] > h/3:
                            rating(4)
                            del t4[0]
                if event.key == pygame.K_QUOTE: # KEY: '
                    keyset[4] = 1
                    if len(t5) > 0:
                        if t5[0][0] > h/2:
                            rating(5)
                            del t5[0]
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    keyset[0] = 0
                if event.key == pygame.K_s:
                    keyset[1] = 0
                if event.key == pygame.K_d:
                    keyset[2] = 0
                if event.key == pygame.K_l:
                    keyset[2] = 0
                if event.key == pygame.K_SEMICOLON: # KEY: ;
                    keyset[3] = 0
                if event.key == pygame.K_QUOTE: # KEY: '
                    keyset[4] = 0

            
        # '''
        if len(lmList) != 0:
            for i in index_fingers:
                x, y = lmList[i][1], lmList[i][2]
                # 엄지
                if get_distance(lmList[4], lmList[5]) < get_distance(lmList[3], lmList[5]):
                    # print("엄지 접힘")
                    keyset[0] = 1
                    if len(t1) > 0:
                        if t1[0][0] > h/3:
                            rating(1)
                            del t1[0]
                else:
                    # print("엄지 펴짐")
                    keyset[0] = 0
                
                # 검지
                if get_distance(lmList[8], lmList[1]) < get_distance(lmList[7], lmList[1]):
                    # print("검지 접힘")
                    keyset[1] = 1
                    if len(t2) > 0:
                        if t2[0][0] > h/3:
                            rating(2)
                            del t2[0]
                else:
                    # print("검지 펴짐")
                    keyset[1] = 0
                
                # 중지
                if get_distance(lmList[12], lmList[0]) < get_distance(lmList[11], lmList[0]):
                    # print("중지 접힘")
                    keyset[2] = 1
                    if len(t3) > 0:
                        if t3[0][0] > h/3:
                            rating(3)
                            del t3[0]
                else:
                    # print("중지 펴짐")
                    keyset[2] = 0
                
                # 약지
                if get_distance(lmList[16], lmList[0]) < get_distance(lmList[15], lmList[0]):
                    # print("약지 접힘")
                    keyset[3] = 1
                    if len(t4) > 0:
                        if t4[0][0] > h/3:
                            rating(4)
                            del t4[0]
                else:
                    # print("약지 펴짐")
                    keyset[3] = 0
                
                # 소지
                if get_distance(lmList[20], lmList[0]) < get_distance(lmList[19], lmList[0]):
                    # print("소지 접힘")
                    keyset[4] = 1
                    if len(t5) > 0:
                        if t5[0][0] > h/2:
                            rating(5)
                            del t5[0]
                else:
                    # print("소지 펴짐")
                    keyset[4] = 0
        # '''

        screen.fill((0, 0, 0))
        
        # 프레임에 따라 움직임 최적화(감속)
        for i in range(len(keys)):
            keys[i] += (keyset[i] - keys[i]) / (2 * (maxframe / fps))

        # 텍스트의 움직임
        if Time > combo_time:
            combo_effect += (0 - combo_effect) / (2 * (maxframe / fps))
        if Time < combo_time:
            combo_effect += (1 - combo_effect) / (2 * (maxframe / fps))

        combo_effect2 += (2 - combo_effect2) / (2 * (maxframe / fps))

        miss_anim += (4 - miss_anim) / (4 * (maxframe / fps))

        # gaer background
        pygame.draw.rect(screen, (0, 0, 0), (w/2 - w/8 - 110, -int(w/100), w/4 + 110, h + int(w/50)))
        
        # key fx
        for i in range(7):
            i += 1
            pygame.draw.rect(screen, (200 - ((200 / 7) * i), 200 - ((200 / 7) * i), 200 - ((200 / 7) * i)), (w/2 - w/8 + w/32 - (w / 32) - 110 * keys[0], (h / 12) * 9 - (h / 30) * keys[0] * i + 10, w/16 * keys[0], (h / 35) / i))
        for i in range(7):
            i += 1
            pygame.draw.rect(screen, (200 - ((200 / 7) * i), 200 - ((200 / 7) * i), 200 - ((200 / 7) * i)), (w/2 - w/16 + w/32 - (w / 32) - 110 * keys[1], (h / 12) * 9 - (h / 30) * keys[1] * i + 10, w/16 * keys[1], (h / 35) / i))
        for i in range(7):
            i += 1
            pygame.draw.rect(screen, (200 - ((200 / 7) * i), 200 - ((200 / 7) * i), 200 - ((200 / 7) * i)), (w/2 + w/32 - (w / 32) - 110 * keys[2], (h / 12) * 9 - (h / 30) * keys[2] * i + 10, w/16 * keys[2], (h / 35) / i))
        for i in range(7):
            i += 1
            pygame.draw.rect(screen, (200 - ((200 / 7) * i), 200 - ((200 / 7) * i), 200 - ((200 / 7) * i)), (w/2 + w/16 + w/32 - (w / 32) - 110 * keys[3], (h / 12) * 9 - (h / 30) * keys[3] * i + 10, w/16 * keys[3], (h / 35) / i))
        for i in range(7):
            i += 1
            pygame.draw.rect(screen, (200 - ((200 / 7) * i), 200 - ((200 / 7) * i), 200 - ((200 / 7) * i)), (w/2 + w/8 + w/32 - (w / 32) - 110 * keys[4], (h / 12) * 9 - (h / 30) * keys[4] * i + 10, w/16 * keys[4], (h / 35) / i))

        #gear line
        pygame.draw.rect(screen, (255, 255, 255), (w/2 - w/8 - 110, -int(w/100), w/4 + 110, h + int(w/50)), int(w/160))

        # note
        for tile_data in t1:
            tile_data[0] = (h / 12) * 9 + (Time - tile_data[1]) * 350 * speed * (h / 900)
            pygame.draw.rect(screen, (255, 255, 255), (w/2 - w/8 - 110, tile_data[0] - h/100, w/16, h/50))
            if tile_data[0] > h - h/9:
                last_combo = combo
                miss_anim = 1
                combo = 0
                combo_effect = 0.2
                combo_time = Time + 1
                combo_effect2 = 1.3
                rate = "Miss"
                t1.remove(tile_data)

        for tile_data in t2:
            tile_data[0] = (h / 12) * 9 + (Time - tile_data[1]) * 350 * speed * (h / 900)
            pygame.draw.rect(screen, (255, 255, 255), (w/2 - w/16 - 110, tile_data[0] - h/100, w/16, h/50))
            if tile_data[0] > h - h/9:
                last_combo = combo
                miss_anim = 1
                combo = 0
                combo_effect = 0.2
                combo_time = Time + 1
                combo_effect2 = 1.3
                rate = "Miss"
                t2.remove(tile_data)

        for tile_data in t3:
            tile_data[0] = (h / 12) * 9 + (Time - tile_data[1]) * 350 * speed * (h / 900)
            pygame.draw.rect(screen, (255, 255, 255), (w/2 - 110, tile_data[0] - h/100, w/16, h/50))
            if tile_data[0] > h - h/9:
                last_combo = combo
                miss_anim = 1
                combo = 0
                combo_effect = 0.2
                combo_time = Time + 1
                combo_effect2 = 1.3
                rate = "Miss"
                t3.remove(tile_data)

        for tile_data in t4:
            tile_data[0] = (h / 12) * 9 + (Time - tile_data[1]) * 350 * speed * (h / 900)
            pygame.draw.rect(screen, (255, 255, 255), (w/2 + w/16 - 110, tile_data[0] - h/100, w/16, h/50))
            if tile_data[0] > h - h/9:
                last_combo = combo
                miss_anim = 1
                combo = 0
                combo_effect = 0.2
                combo_time = Time + 1
                combo_effect2 = 1.3
                rate = "Miss"
                t4.remove(tile_data)

        for tile_data in t5:
            tile_data[0] = (h / 12) * 9 + (Time - tile_data[1]) * 350 * speed * (h / 900)
            pygame.draw.rect(screen, (255, 255, 255), (w/2 + w/8 - 110, tile_data[0] - h/100, w/16, h/50))
            if tile_data[0] > h - h/9:
                last_combo = combo
                miss_anim = 1
                combo = 0
                combo_effect = 0.2
                combo_time = Time + 1
                combo_effect2 = 1.3
                rate = "Miss"
                t5.remove(tile_data)

        # 판정선
        pygame.draw.rect(screen, (0, 0, 0), (w/2 - w/8 - 110, (h / 12) * 9, w/4 + 110, h/2))
        pygame.draw.rect(screen, (255, 255, 255), (w/2 - w/8 - 110, (h / 12) * 9, w/4 + 110, h/2), int(w/160))

        # 조작키
        # a
        pygame.draw.rect(screen, (255 - 100 * keys[0],255 - 100 * keys[0], 255 - 100 * keys[0]), (w / 2 - w / 9 - 110, (h / 24) * 19 + (h / 48) * keys[0], w / 27, h / 8), int(h / 150))
        # d, l
        pygame.draw.rect(screen, (255 - 100 * keys[2],255 - 100 * keys[2], 255 - 100 * keys[2]), (w / 2 - 90, (h / 24) * 19 + (h / 48) * keys[2], w / 27, h / 8), int(h / 150))
        # '
        pygame.draw.rect(screen, (255 - 100 * keys[4],255 - 100 * keys[4], 255 - 100 * keys[4]), (w / 2 + w / 13.5 - 5 , (h / 24) * 19 + (h / 48) * keys[4], w / 27, h / 8), int(h / 150))

        # s
        pygame.draw.rect(screen, (255 - 100 * keys[1], 255 - 100 * keys[1], 255 - 100 * keys[1]), (w / 2 - w / 18 - 100, (h / 48) * 39 + (h / 48) * keys[1], w / 27, h / 8))
        pygame.draw.rect(screen, (50, 50, 50), (w / 2 - w / 18 - 100, (h / 48) * 39 + (h / 48) * keys[1], w / 27, h / 8), int(h / 150))
        pygame.draw.rect(screen, (25, 25, 25), (w / 2 - w / 18 - 100, (h / 48) * 43 + (h / 48) * (keys[1] * 1.2), w / 27, h / 64), int(h / 150))

        # ;
        pygame.draw.rect(screen, (255 - 100 * keys[3], 255 - 100 * keys[3], 255 - 100 * keys[3]), (w / 2 + w / 13.5 - 107, (h / 48) * 39 + (h / 48) * keys[3], w / 27, h / 8))
        pygame.draw.rect(screen, (50, 50, 50), (w / 2 + w / 13.5 - 107, (h / 48) * 39 + (h / 48) * keys[3], w / 27, h / 8), int(h / 150))
        pygame.draw.rect(screen, (25, 25, 25), (w / 2 + w / 13.5 - 107, (h / 48) * 43 + (h / 48) * (keys[3] * 1.2), w / 27, h / 64), int(h / 150))

        # 중앙 동그라미
        pygame.draw.circle(screen, (180, 180, 180), (w / 2 - 60, (h / 24) * 20), (w / 240), int(h / 320))
        
        # 중앙 동그라미 선
        # line_length = 25 * (w / 1600) # 선의 길이 계산
        
        # start_point = (w / 2 - 110 - math.sin(spin) * line_length + 80, (h / 24) * 21 - math.cos(spin) * line_length)
        # end_point = (w / 2 + math.sin(spin) * line_length - 80, (h / 24) * 21 + math.cos(spin) * line_length)
        # pygame.draw.line(screen, (202, 202, 202), start_point, end_point, int(w / 800))
       
        # spin += (speed / 20 * (maxframe / fps))
        
        miss_text.set_alpha(255 - (255 / 4) * miss_anim)

        screen.blit(combo_text, (w/2 - combo_text.get_width() / 2 - 50, (h / 12) * 4 - combo_text.get_height() / 2))
        screen.blit(rate_text, (w/2 - rate_text.get_width() / 2 - 50, (h / 12) * 8 - rate_text.get_height() / 2))
        screen.blit(miss_text, (w/2 - miss_text.get_width() / 2 - 50, (h / 12) * 4 - miss_text.get_height() / 2))
        
        # screen.blit(frame, (w/2, h/2)) # 웹캠 화면 출력

        pygame.display.flip()

        clock.tick(maxframe)

        # cv2.imshow("Image", frame)
        cv2.imshow("Image", cv2.resize(frame, (320, 240)))

ingame = False
main = False

cap.release() # 비디오 캡처 객체 해제
cv2.destroyAllWindows() # 영상 창 닫기
pygame.quit()