import cv2
import numpy as np
import pickle
#from hand_hist import build_squares, get_hand_hist

def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping, drawing

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False
        drawing=True

def build_squares(img, a,b):
    #x, y, w, h = 420, 140, 10, 10
    x,y=a[0], a[1]
    w=int((b[0]-x)/6)
    h=int((b[1]-y)/6)
    #w,h= 10,10
    d = int(min(w,h)/3)
    imgCrop = None
    crop = None
    for j in range(int(5)):
        for i in range(int(5)):
            if np.any(imgCrop == None):
                imgCrop = img[y:y + h, x:x + w]
            else:
                imgCrop = np.hstack((imgCrop, img[y:y + h, x:x + w]))
            # print(imgCrop.shape)k
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
            x += w + d
        if np.any(crop == None):
            crop = imgCrop
        else:
            crop = np.vstack((crop, imgCrop))
        imgCrop = None
        y += h + d
        x=a[0]
    return crop

if __name__ == '__main__':
    f = True
    while f:
        drawing=False
        cv2.namedWindow("preview")
        vc = cv2.VideoCapture(0)

        #cap = cv2.VideoCapture(0)
        refPt = []
        cropping = False
        remove_function=True
        flag=False
        flagPressedK=False
        imgCrop = None
        flagPressedC=False


        if vc.isOpened(): # try to get the first frame
            rval, frame = vc.read()
        else:
            rval = False

        cv2.setMouseCallback("preview", click_and_crop)
        while rval:

            #frame = cv2.flip(frame, 1)#OBRNUTI SLIKU JER KOD FLIPA NE MOGU LIJEPO ISCRTAT RECT
            cv2.imshow("preview", frame)
            rval, frame = vc.read()
            key = cv2.waitKey(20)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            if key == ord('k'):
                flagPressedK = True
            if flagPressedK:
                imgCrop = build_squares(frame,refPt[0], refPt[1])


            if key == ord('c'):
                hsvCrop = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2HSV)
                flagPressedC = True
                hist = cv2.calcHist([hsvCrop], [0, 1], None, [180, 256], [0, 180, 0, 256])
                cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
            if flagPressedC:
                dst = cv2.calcBackProject([hsv], [0, 1], hist, [0, 180, 0, 256], 1)
                dst1 = dst.copy()
                disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
                cv2.filter2D(dst, -1, disc, dst)
                blur = cv2.GaussianBlur(dst, (11, 11), 0)
                blur = cv2.medianBlur(blur, 15)
                ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                thresh = cv2.merge((thresh, thresh, thresh))
                # cv2.imshow("res", res)
                cv2.imshow("Thresh", thresh)

            if drawing:
                #print(refPt)
                cv2.rectangle(frame, refPt[0], refPt[1], (0, 255, 0), 2)
                cv2.imshow("preview", frame)
                remove_function = False

            if remove_function == False:
                cv2.setMouseCallback("preview", lambda *args : None)

            # exit on ESC
            if key == 27:
                f = False
                break
            # on r reset the video and enable to draw new rectangle, DOESNT WORK
            # treba dodati da se postavi setMouseCallback nazad na funckiju ili drugu funkciju
            # i ocistit ekran, odnosno maknuti rectagnle
            if key == ord("r"):
                vc.release()
                break
                #cv2.setMouseCallback("preview", click_and_crop)

    vc.release()
    cv2.destroyWindow("preview")



