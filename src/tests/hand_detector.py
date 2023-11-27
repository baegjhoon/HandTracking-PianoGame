import cv2
import mediapipe as mp

class handDetector():
    def __init__(self, mode=True, maxHands=2, detectionCon=0.5, trackCon=0.5):
        # 손 감지 모드 및 관련 매개변수 초기화
        self.mode = mode  # 정적 이미지 모드 활성화 여부
        self.maxHands = maxHands  # 최대 손 감지 수
        self.detectionCon = detectionCon  # 최소 감지 신뢰도
        self.trackCon = trackCon  # 최소 추적 신뢰도

        # Mediapipe 손 모델 초기화
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon)

        # Mediapipe 그리기 유틸리티 초기화
        self.mp_drawing = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        # 이미지 좌우 반전
        img = cv2.flip(img, 1)
        # 이미지를 RGB 형식으로 변환
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # 손 감지 수행
        self.results = self.hands.process(img_rgb)
        # 감지된 손이 있을 경우 감지 결과를 이미지에 그림
        if self.results.multi_hand_landmarks is not None:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_drawing.draw_landmarks(
                        img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                    )
        return img

    def findPositions(self, img, handNo=0, draw=True):
        # 손의 랜드마크 위치를 저장할 리스트 초기화
        lmList = []
        # 감지된 손이 있을 경우 해당 손의 랜드마크 가져오기
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            # 각 랜드마크의 좌표를 이미지 상의 좌표로 변환하여 리스트에 추가
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                lmList.append([id, cx, cy])

                # 랜드마크를 이미지에 원으로 표시 (옵션)
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return lmList