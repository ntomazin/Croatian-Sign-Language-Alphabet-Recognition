import cv2
import numpy as np
import pickle
from GUI import Settings
#from hand_hist import build_squares, get_hand_hist

def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping, drawing

    # obrnuti koordinate za flipan prozor
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    #takoder obrnuti
    elif event == cv2.EVENT_LBUTTONUP:
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

def add_text(frame, frameHeight):
    #cv2.putText(img=frame, text='Oznaci pravokutnik preko kojeg ces prepoznati histogram', org=(20, 20),
                #fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.8,
                #color=(0, 255, 0))


    cv2.putText(img=frame, text='K - stvori pravokutnike', org=(10, frameHeight-5),
                fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.8,
                color=(0, 255, 0))
    cv2.putText(img=frame, text='C - histogram', org=(10, frameHeight-30),
                fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.8,
                color=(0, 255, 0))
    cv2.putText(img=frame, text='R - reset', org=(frameWidth-150, frameHeight - 5),
                fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.8,
                color=(0, 255, 0))


if __name__ == '__main__':
    Settings()
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
        frameWidth = int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))
        frameHeight = int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))


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

            add_text(frame, frameHeight)
            """
            #"k" za popunit kvadratima oznaceni pravokutnik
            if key == ord('k') and drawing:
                flagPressedK = True
            if flagPressedK:
                imgCrop = build_squares(frame,refPt[0], refPt[1])
            """
            #"c" za otvorit histogram
            if key == ord('c'):# and flagPressedK:
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
                imgCrop = build_squares(frame, refPt[0], refPt[1])

            if remove_function == False:
                cv2.setMouseCallback("preview", lambda *args : None)

            # ESC za izlazak
            if key == 27:
                f = False
                break

            # "r" za restart
            if key == ord("r"):
                cv2.destroyWindow("Thresh")
                vc.release()
                flagPressedC=False
                break
                #cv2.setMouseCallback("preview", click_and_crop)

            if key == ord("s"):
                with open("hist", "wb") as f:
                    pickle.dump(hist, f)
                print("SAVED")


    vc.release()
    cv2.destroyWindow("preview")




