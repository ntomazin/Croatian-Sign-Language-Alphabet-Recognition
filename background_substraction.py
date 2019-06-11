import numpy as np
import cv2



def main():
    cam = cv2.VideoCapture(1)
    if cam.read()[0] == False:
        cam = cv2.VideoCapture(0)

    _, first_frame = cam.read()
    first_frame = cv2.flip(first_frame, 1)

    #cam = cv2.VideoCapture('vtest.avi')
    first_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
    first_gray = cv2.GaussianBlur(first_gray, (5, 5), 0)

    fgbg = cv2.createBackgroundSubtractorMOG2()

    while True:
        frame = cam.read()[1]
        frame = cv2.flip(frame, 1)

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
        difference = cv2.absdiff(first_gray, gray_frame)
        _, difference = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)
        #difference=difference[80:350,350:600]
        cv2.rectangle(frame, (350, 80), (600, 350), (0, 255, 0), 2)

        cv2.imshow("First frame", first_frame)
        cv2.imshow("Frame", frame)
        cv2.rectangle(difference, (350, 80), (600, 350), (0, 255, 0), 2)

        cv2.imshow("difference", difference)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break



    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
