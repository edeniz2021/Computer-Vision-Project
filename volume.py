import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
colorR = (255, 0, 255)
cap = cv2.VideoCapture(0)
ax, ay, aw, ah = 100, 100, 200, 200

with mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                cursor = hand_landmarks.landmark[8]
                middle_finger = hand_landmarks.landmark[12]
                distance = ((middle_finger.x - cursor.x)**2 + (middle_finger.y - cursor.y)**2 + (middle_finger.z - cursor.z)**2)**0.5
                if distance<30:
                    if ax - aw//2 < cursor.x * img.shape[1] < ax + aw//2 and ay - ah//2 < cursor.y * img.shape[0] < ay + ah//2:
                        colorR = (0, 255, 0)
                        ax, ay = int(cursor.x * img.shape[1]), int(cursor.y * img.shape[0])
                    else:
                        colorR = (255, 0, 255)
                    #for id, lm in enumerate(hand_landmarks.landmark):
                    #    h, w, c = img.shape
                    #    cx, cy = int(lm.x * w), int(lm.y * h)
                    #    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

                    mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.rectangle(img, (ax - aw//2, ay - ah//2), (ax + aw//2, ay + ah//2), colorR, cv2.FILLED)
        #cv2.rectangle(img, (2*ax - aw//2, 2*ay - ah//2), (2*ax + aw//2, 2*ay + ah//2), colorR, cv2.FILLED)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
