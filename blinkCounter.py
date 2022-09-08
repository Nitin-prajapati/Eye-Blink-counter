import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector


cap = cv2.VideoCapture(0)  # open video or camera
detector = FaceMeshDetector(maxFaces=1)
EyeBlinkCounter = 0
frameCounter = 0
while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    # img = cv2.resize(img, (720, 1000))
    # img = cv2.rotate(img, cv2.ROTATE_180)
    img, faces = detector.findFaceMesh(img)
    if faces:
        face = faces[0]
        xtreamRR = face[130]
        xtreamRL = face[243]

        upR = face[159]
        downR = face[145]

        cv2.line(img, upR, downR, (0, 255, 255), 3)
        cv2.line(img, xtreamRL, xtreamRR, (255, 0, 0), 3)
        lengthVer, _ = detector.findDistance(upR, downR)
        lengthHor, _ = detector.findDistance(xtreamRR, xtreamRL)
        # print((lengthVer/lengthHor))
        ratio = int((lengthVer/lengthHor)*100)
        if ratio < 20 and frameCounter == 0:
            EyeBlinkCounter += 1
            frameCounter = 1
        if frameCounter > 0:
            frameCounter += 1
            if frameCounter == 8:
                frameCounter = 0

    cvzone.putTextRect(img, f'Blink Counter: {EyeBlinkCounter}', (50, 100))
    cv2.imshow("face", img)

    cv2.waitKey(2)
