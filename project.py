import cv2
import numpy as np

img = cv2.imread("profile.jpg")
frameheight = 640
farmewidth = 680
img_ball = cv2.imread("ball.jpg")

img_shape = cv2.imread("shapes.jpg")
img_shape = cv2.resize(img_shape,(640,640))



vid = cv2.VideoCapture(1)
vid.set(3, farmewidth)
vid.set(4,frameheight)
vid.set(10,150)


#points to draw cirlces (plot pen tip)

mypoints = [

]

color_BGR = [
        [243,217,111]
    ]

#cv2.imshow("output",img)
#cv2.waitKey(0)

def empty(a):
    pass


def select_color():

    cv2.namedWindow("Trackbar")
    cv2.resizeWindow("Trackbar", 1000, 500)
    cv2.createTrackbar("hue min","Trackbar",0,179,empty)
    cv2.createTrackbar("hue max", "Trackbar", 179, 179, empty)
    cv2.createTrackbar("sat min", "Trackbar", 0, 255, empty)
    cv2.createTrackbar("sat max", "Trackbar", 255, 255, empty)
    cv2.createTrackbar("val min", "Trackbar", 0, 255, empty)
    cv2.createTrackbar("val max", "Trackbar", 255, 255, empty)


    while True:
        success, img_cam = vid.read()
        hue_min = cv2.getTrackbarPos("hue min", "Trackbar")
        hue_max = cv2.getTrackbarPos("hue max", "Trackbar")
        sat_min = cv2.getTrackbarPos("sat min", "Trackbar")
        sat_max = cv2.getTrackbarPos("sat max", "Trackbar")
        val_min = cv2.getTrackbarPos("val min", "Trackbar")
        val_max = cv2.getTrackbarPos("val max", "Trackbar")

        print(hue_min,sat_min,val_min,hue_max,sat_max,val_max)

        lower = np.array([hue_min,sat_min,val_min])
        upper = np.array([hue_max,sat_max,val_max])

        img_hsv = cv2.cvtColor(img_cam,cv2.COLOR_BGR2HSV)
        img_mask =cv2.inRange(img_hsv,lower,upper)
        fin_img = cv2.bitwise_and(img_cam,img_cam,mask=img_mask)
        cv2.imshow("output",img_cam)
        cv2.imshow("mask",img_mask)
        cv2.imshow("FINAL_IMG",fin_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



def select_color_img(img_b):

    mycolors = np.array([
        [88,108,129,113,234,254]
    ])



    count = len(mycolors)

    for i in range(0,count):

        lower = np.array(mycolors[0][0:3])
        upper = np.array(mycolors[0][3:6])

        img_hsv = cv2.cvtColor(img_b, cv2.COLOR_BGR2HSV)
        img_mask = cv2.inRange(img_hsv, lower, upper)
        fin_img = cv2.bitwise_and(img_b, img_b, mask=img_mask)

        #cv2.imshow(str(i), img_mask)


        get_shapes(fin_img,i)



def get_shapes(img,col):

    img_bw = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_bw,(7,7),0)
    img_canny = cv2.Canny(img_blur,50,50)   # VERY IMP TO CONVERT THIS TO CANNY ELSE IT WILL NOT WORK

    contours,hierarchy = cv2.findContours(img_canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)



    for con in contours:

        area = cv2.contourArea(con)
        #print(area)

        x=0
        y=0
        w=0
        h=0

        if area> 500 : #ignore if shape is too small
            cv2.drawContours(img,con,-1,(0,255,0),2)

            perimeter = cv2.arcLength(con,True ) #our shape is closed, True
            points = cv2.approxPolyDP(con,0.01*perimeter,True)

            x,y,w,h = cv2.boundingRect(points)

            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),2)

            if x!=0 and y!=0:
                mypoints.append([x+w/2,y,col])
                print(x+w/2,y)

    #cv2.imshow("shapes",img)
    #cv2.imshow("canny",img_canny)


#select_color()

#select_color_img(img_ball)

#get_shapes(img_shape)

def plot_tip(image):

    count = len(mypoints)
    print("HERE",count)

    for i in range(0,count):
        cv2.circle(image,(int(mypoints[i][0]),int(mypoints[i][1])),10,color_BGR[mypoints[i][2]],cv2.FILLED)
        print("DONE")


while True:

    success,raw_img = vid.read()
    img_copy = raw_img.copy()

    select_color_img(img_copy)

    plot_tip(img_copy)

    cv2.imshow("paint",img_copy)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


















