import cv2, pickle
import numpy as np
import tensorflow as tf
#from cnn_tf import cnn_model_fn
import os
from gestures import get_pred_text
from keras.models import load_model
import time
import pyttsx3
import operator
from util import Counter

#text to speach setup
engine = pyttsx3.init()
engine.setProperty('rate', 125)
engine.setProperty('voice', "croatian")


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.logging.set_verbosity(tf.logging.ERROR)
#classifier = tf.estimator.Estimator(model_dir="tmp/cnn_model2", model_fn=cnn_model_fn)
prediction = None
model = load_model('cnn_model.h5')

NUM_OF_FRAMES = 30
SEQUENCE_OF_PICTURES = 30



def get_image_size():
    img = cv2.imread('gestures/0/100.jpg', 0)
    return img.shape


image_x, image_y = get_image_size()



def keras_process_image(img):
    img = cv2.resize(img, (image_x, image_y))
    img = np.array(img, dtype=np.float32)
    img = np.reshape(img, (1, image_x, image_y, 1))
    return img


def keras_predict(model, image):
    processed = keras_process_image(image)
    pred_probab = model.predict(processed)[0]
    pred_class = list(pred_probab).index(max(pred_probab))
    return max(pred_probab), pred_class


def split_sentence(text, num_of_words):
    list_words = text.split(" ")
    length = len(list_words)
    splitted_sentence = []
    b_index = 0
    e_index = num_of_words
    while length > 0:
        part = ""
        for word in list_words[b_index:e_index]:
            part = part + " " + word
        splitted_sentence.append(part)
        b_index += num_of_words
        e_index += num_of_words
        length -= num_of_words
    return splitted_sentence


def put_splitted_text_in_blackboard(blackboard, splitted_text):
    y = 200
    for text in splitted_text:
        cv2.putText(blackboard, text, (4, y), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 255, 255))
        y += 50


def get_hand_hist():
    with open("hist", "rb") as f:
        hist = pickle.load(f)
    return hist



def recognize_with_hist():
    global prediction
    cam = cv2.VideoCapture(1)
    if cam.read()[0] == False:
        cam = cv2.VideoCapture(0)
    hist = get_hand_hist()
    x, y, w, h = 300, 100, 300, 300
    while True:
        text = ""
        img = cam.read()[1]
        img = cv2.flip(img, 1)
        imgCrop = img[y:y + h, x:x + w]
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([imgHSV], [0, 1], hist, [0, 180, 0, 256], 1)
        disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
        cv2.filter2D(dst, -1, disc, dst)
        blur = cv2.GaussianBlur(dst, (11, 11), 0)
        blur = cv2.medianBlur(blur, 15)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        thresh = cv2.merge((thresh, thresh, thresh))
        thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
        thresh = thresh[y:y + h, x:x + w]
        contours = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[1]
        if len(contours) > 0:
            contour = max(contours, key=cv2.contourArea)
            # print(cv2.contourArea(contour))
            if cv2.contourArea(contour) > 10000:
                x1, y1, w1, h1 = cv2.boundingRect(contour)
                save_img = thresh[y1:y1 + h1, x1:x1 + w1]

                if w1 > h1:
                    save_img = cv2.copyMakeBorder(save_img, int((w1 - h1) / 2), int((w1 - h1) / 2), 0, 0,
                                                  cv2.BORDER_CONSTANT, (0, 0, 0))
                elif h1 > w1:
                    save_img = cv2.copyMakeBorder(save_img, 0, 0, int((h1 - w1) / 2), int((h1 - w1) / 2),
                                                  cv2.BORDER_CONSTANT, (0, 0, 0))

                pred_probab, pred_class = keras_predict(model, save_img)
                print(pred_class, pred_probab)

                if pred_probab * 100 > 80:

                    text = get_pred_text(pred_class)
                    print(text)

        blackboard = np.zeros((480, 640, 3), dtype=np.uint8)
        splitted_text = split_sentence(text, 2)
        put_splitted_text_in_blackboard(blackboard, splitted_text)
        # cv2.putText(blackboard, text, (30, 200), cv2.FONT_HERSHEY_TRIPLEX, 1.3, (255, 255, 255))
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        res = np.hstack((img, blackboard))
        cv2.imshow("Recognizing gesture", res)
        #cv2.imshow("Display", blackboard)
        cv2.imshow("thresh", thresh)
        if cv2.waitKey(1) == 27:
            break

def recognize_with_background_substraction():
    restart = True
    while restart:
        cam = cv2.VideoCapture(1)
        if cam.read()[0] == False:
            cam = cv2.VideoCapture(0)

        _, first_frame = cam.read()
        first_frame = cv2.flip(first_frame, 1)
        first_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
        first_gray = cv2.GaussianBlur(first_gray, (5, 5), 0)

        fgbg = cv2.createBackgroundSubtractorMOG2()
        text = ""
        word = ""
        oldText=""
        textMode = False
        testMode = False
        frameCounter = 0
        pictureCounter = 0
        counter = Counter()

        while True:
            frame = cam.read()[1]
            frame = cv2.flip(frame, 1)
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_frame = cv2.GaussianBlur(gray_frame, (11, 11), 0)
            gray_frame = cv2.medianBlur(gray_frame, 15)
            difference = cv2.absdiff(first_gray, gray_frame)
            _, difference = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)
            difference = difference[80:350, 350:600]

            contours = cv2.findContours(difference.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[1]
            if len(contours) > 0:
                contour = max(contours, key = cv2.contourArea)
                x1, y1, w1, h1 = cv2.boundingRect(contour)
                save_img = difference[y1:y1 + h1, x1:x1 + w1]

                if cv2.contourArea(contour) > 5000:
                    #frameCounter=0
                    if w1 > h1:
                        save_img = cv2.copyMakeBorder(save_img, int((w1 - h1) / 2), int((w1 - h1) / 2), 0, 0,
                                                      cv2.BORDER_CONSTANT, (0, 0, 0))
                    elif h1 > w1:
                        save_img = cv2.copyMakeBorder(save_img, 0, 0, int((h1 - w1) / 2), int((h1 - w1) / 2),
                                                      cv2.BORDER_CONSTANT, (0, 0, 0))


                    pred_probab, pred_class = keras_predict(model, save_img)
                    print(pred_probab, pred_class)
                    if pred_probab * 100 > 80:
                        oldText=text
                        text = get_pred_text(pred_class)
                        #print(text)

                        # uhvati NUM_OF_PICTURES frameova i na temelju toga vidjet najvise pojavljivanja slova
                        if testMode:
                            counter[text]+=1



            #ako je isto slovo, nakon 30 frameova appendaj slovo
            if textMode:
                if text==oldText:
                    frameCounter+=1
                else:
                    frameCounter=0

                if frameCounter>NUM_OF_FRAMES:
                    if text == "razmak":
                        word+=" "
                    elif text == "obrisi":
                        word = word[:-1]
                    else:
                        engine.say(text)
                        word+=text
                    frameCounter=0


                splitted_text = split_sentence(word, 2)


            elif testMode:
                if sum(counter.values()) > SEQUENCE_OF_PICTURES:
                    newText = max(counter.items(), key=operator.itemgetter(1))[0]
                    splitted_text=split_sentence(newText,2)
                    #print (counter.get(sum(counter.values())))
                    print(newText)
                    #print (counter.argMax())
                    counter.clear()

            else:
                splitted_text = split_sentence(text, 2)
            blackboard = np.zeros((480, 640, 3), dtype=np.uint8)
            #splitted_text = text #ovo izbacit eventualno
            put_splitted_text_in_blackboard(blackboard, splitted_text)
            #cv2.putText(blackboard, text, (30, 200), cv2.FONT_HERSHEY_TRIPLEX, 1.3, (255, 255, 255))
            #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.rectangle(frame, (350, 80), (600, 350), (0, 255, 0), 2)
            res = np.hstack((frame, blackboard))
            cv2.imshow("Prepoznavanje geste", res)
            # cv2.imshow("Display", blackboard)
            cv2.imshow("difference", difference)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                restart = False
                break
            if k == ord("t"):
                textMode = True if not textMode else False
                print("text mode je "+str(textMode))

            if k == ord("r"):
                cam.release()
                cv2.destroyAllWindows()
                break
            if k == ord(str(0x08)) and textMode and "".__eq__(word):
                word = word[:-1]
            if k == ord(" ") and textMode:
                word+=" "
            if k == ord("s"):
                testMode = not textMode
                print("test mode je "+str(testMode))


    cam.release()
    cv2.destroyAllWindows()

def main():
    keras_predict(model, np.zeros((50, 50), dtype=np.uint8))
    # recognize_with_hist()
    recognize_with_background_substraction()

if __name__ == '__main__':
    main()