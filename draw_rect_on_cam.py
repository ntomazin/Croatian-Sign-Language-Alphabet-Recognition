import cv2
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

if __name__ == '__main__':
    drawing=False
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)
    #cap = cv2.VideoCapture(0)
    refPt = []
    cropping = False
    remove_function=True
    flag=False


    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    cv2.setMouseCallback("preview", click_and_crop)

    while rval:
        #frame = vc.read()[1]
        #frame = cv2.flip(frame,1)
        cv2.imshow("preview", frame)
        rval, frame = vc.read()
        key = cv2.waitKey(20)

        # draw a rectangle around the region of interest
        if drawing:
            #print(refPt)
            cv2.rectangle(frame, refPt[0], refPt[1], (0, 255, 0), 2)
            cv2.imshow("preview", frame)
            remove_function = False

        if remove_function == False:
            cv2.setMouseCallback("preview", lambda *args : None)

        # exit on ESC
        if key == 27:
            break
        # on r reset the video and enable to draw new rectangle, DOESNT WORK
        # treba dodati da se postavi setMouseCallback nazad na funckiju ili drugu funkciju
        # i ocistit ekran, odnosno maknuti rectagnle
        if key == ord("r"):
            print("radi")
            remove_function=True
            #cv2.setMouseCallback("preview", click_and_crop)

    vc.release()
    cv2.destroyWindow("preview")



