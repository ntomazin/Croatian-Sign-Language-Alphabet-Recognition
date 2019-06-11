import cv2
import os
from gestures import add_gesture
image_x, image_y = 50, 50



def init_create_folder():
    if not os.path.exists("gestures"):
        os.mkdir("gestures")


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

def flip_images(g_id):
	gest_folder = "gestures"
	for g in os.listdir(gest_folder):
            if int(g_id) == int(g):
                for i in range(1200):
                    path = gest_folder+"/"+g_id+"/"+str(i+1)+".jpg"
                    new_path = gest_folder+"/"+g_id+"/"+str(i+1+1200)+".jpg"
                    print(path)
                    img = cv2.imread(path, 0)
                    img = cv2.flip(img, 1)
                    cv2.imwrite(new_path, img)

def store_images(g_id):
    flag = True
    while flag:
        total_pics = 1200

        cam = cv2.VideoCapture(1)
        if not cam.read()[0]:
            cam = cv2.VideoCapture(0)

        _, first_frame = cam.read()
        first_frame = cv2.flip(first_frame, 1)
        first_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
        first_gray = cv2.GaussianBlur(first_gray, (5, 5), 0)

        create_folder("gestures/" + str(g_id))
        pic_no = 0
        flag_start_capturing = False
        frames = 0

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
                contour = max(contours, key=cv2.contourArea)
                if cv2.contourArea(contour) > 10000 and frames > 50:
                    x1, y1, w1, h1 = cv2.boundingRect(contour)
                    pic_no += 1
                    save_img = difference[y1:y1 + h1, x1:x1 + w1]

                    if w1 > h1:
                        save_img = cv2.copyMakeBorder(save_img, int((w1 - h1) / 2), int((w1 - h1) / 2), 0, 0,
                                                      cv2.BORDER_CONSTANT, (0, 0, 0))
                    elif h1 > w1:
                        save_img = cv2.copyMakeBorder(save_img, 0, 0, int((h1 - w1) / 2), int((h1 - w1) / 2),
                                                      cv2.BORDER_CONSTANT, (0, 0, 0))

                    save_img = cv2.resize(save_img, (image_x, image_y))
                    save_img = cv2.flip(save_img, 1)
                    cv2.putText(frame, "Capturing...", (30, 60), cv2.FONT_HERSHEY_TRIPLEX, 2, (127, 255, 255))
                    cv2.imwrite("gestures/" + str(g_id) + "/" + str(pic_no) + ".jpg", save_img)

            cv2.rectangle(frame, (350, 80), (600, 350), (0, 255, 0), 2)
            cv2.putText(frame, str(pic_no), (30, 400), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (127, 127, 255))
            cv2.imshow("Capturing gesture", frame)
            cv2.imshow("difference", difference)
            k = cv2.waitKey(1)
            if k == ord('c'):
                if flag_start_capturing == False:
                    flag_start_capturing = True
                    print("start")
                else:
                    flag_start_capturing = False
                    print("stop")
                    frames = 0
            if flag_start_capturing == True:
                frames += 1
            if pic_no == total_pics:
                flag = False
                break
            if k == 27:
                flag = False
                break
            if k == ord('r'):
                break

def main():
    init_create_folder()
    g_id = input("Enter gesture no.: ")
    g_name = input("Enter gesture name/text: ")
    add_gesture(g_id, g_name)
    store_images(g_id)
    flip_images(g_id)

if __name__ == '__main__':
    main()