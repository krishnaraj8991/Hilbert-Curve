import cv2
import numpy as np
import imageio
import colorsys
# PROGRAM TO GENERATE A SPACE FILLING CURVE CALLED HILBERT CURVE
# reference of hilbert curve 
# link:-https://en.wikipedia.org/wiki/Hilbert_curve
# coder:-krishnaraj solanki


# animation print funciton
def printFull():
    global full_img
    global delay
    global animation
    if animation:
        cv2.imshow("img",full_img)
        k=cv2.waitKey(delay)
        if k==ord('q'):
            exit()
        if k==ord(' '):
            animation=False
# curve generators functions (A,B,C,D) based on wikipedia page on  Hilbert curve
# inputs
# image:-image to draw curve on
def A(img):
    global thickness_const 
    global r,g,b   
    global full_img
    img[:,:]=(0,0,0)
    height=img.shape[0]
    width=img.shape[1]
    points=[]
    points.append((int(height*1/4),int(width*3/4)))
    points.append((int(height*1/4),int(width*1/4)))
    points.append((int(height*3/4),int(width*1/4)))
    points.append((int(height*3/4),int(width*3/4)))
    
    return points
def B(img):
    global thickness_const
    global r,g,b  
    img[:,:]=(0,0,0)
    height=img.shape[0]
    width=img.shape[1]
    points=[]
    points.append((int(height*3/4),int(width*1/4)))
    points.append((int(height*1/4),int(width*1/4)))
    points.append((int(height*1/4),int(width*3/4)))
    points.append((int(height*3/4),int(width*3/4)))
    return points
def C(img):
    global thickness_const
    global full_img
    global r,g,b  
    img[:,:]=(0,0,0)
    height=img.shape[0]
    width=img.shape[1]
    points=[]
    points.append((int(height*3/4),int(width*1/4)))
    points.append((int(height*3/4),int(width*3/4)))
    points.append((int(height*1/4),int(width*3/4)))
    points.append((int(height*1/4),int(width*1/4)))
    
    return points
def D(img):
    global full_img
    global thickness_const
    global r,g,b  
    img[:,:]=(0,0,0)
    height=img.shape[0]
    width=img.shape[1]
    points=[]
    points.append((int(height*1/4),int(width*3/4)))
    points.append((int(height*3/4),int(width*3/4)))
    points.append((int(height*3/4),int(width*1/4)))
    points.append((int(height*1/4),int(width*1/4)))
    
    return points

# master generator function
# inputs
# image:-image to draw hilbert curve on
# order:- order of hilbert curve to be drawn
# draw:- decides the direction of the curve 
def generator(img,order=1,draw="A"):
    global r,g,b,gradient
    all_points=[]
    if order==0:
        return (0,0)
    height=img.shape[0]
    width=img.shape[1]
    switcher={
        "A":A,
        "B":B,
        "C":C,
        "D":D
    }
    func=switcher.get(draw,lambda:"A")
    if order==1:
        if gredient:
            r+=1
            r%=255
            g+=1
            g%=255
            b+=1
            b%=255
        point=func(img)
        return point
    if order>1:
        half_h=int(height/2)
        half_w=int(width/2)
        if draw=="A":
            points=generator(img[half_h:,:half_w],order-1,draw="D")
            if points!=[]:
                 for point in points:
                    all_points.append((point[0],point[1]+half_h))
            points=generator(img[:half_h,:half_w],order-1,draw="A")
            if points!=[]:
                 for point in points:
                    all_points.append((point[0],point[1]))
            points=generator(img[:half_h,half_w:],order-1,draw="A")
            if points!=[]:
                 for point in points:
                    all_points.append((point[0]+half_w,point[1]))
            points=generator(img[half_h:,half_w:],order-1,draw="B")
            if points!=[]:
                 for point in points:
                    all_points.append((point[0]+half_w,point[1]+half_h))

        elif draw=="B":
            points=generator(img[:half_h,half_w:],order-1,draw="C")
            if points!=[]:
                 for point in points:
                    all_points.append((point[0]+half_w,point[1]))

            points=generator(img[:half_h,:half_w],order-1,draw="B")
            if points!=[]:
                 for point in points:
                    all_points.append((point[0],point[1]))
            points=generator(img[half_h:,:half_w],order-1,draw="B")
            if points!=[]:
                 for point in points:
                    all_points.append((point[0],point[1]+half_h))
            points=generator(img[half_h:,half_w:],order-1,draw="A")
            if points!=[]:
                 for point in points:
                    all_points.append((point[0]+half_w,point[1]+half_h))
        elif draw=="C":
            points=generator(img[:half_h,half_w:],order-1,draw="B")
            if points!=[]:
                 for point in points:
                    all_points.append((point[0]+half_w,point[1]))
            points=generator(img[half_h:,half_w:],order-1,draw="C")
            if points!=[]:
                 for point in points:
                    all_points.append((point[0]+half_w,point[1]+half_h))
            points=generator(img[half_h:,:half_w],order-1,draw="C")
            if points!=[]:
                 for point in points:
                    all_points.append((point[0],point[1]+half_h))
            points=generator(img[:half_h,:half_w],order-1,draw="D")
            if points!=[]:
                 for point in points:
                    all_points.append((point[0],point[1]))
        elif draw=="D":
            points=generator(img[half_h:,:half_w],order-1,draw="A")
            if points!=[]:
                 for point in points:
                    all_points.append((point[0],point[1]+half_h))
            points=generator(img[half_h:,half_w:],order-1,draw="D")
            if points!=[]:
                 for point in points:
                    all_points.append((point[0]+half_w,point[1]+half_h))
            points=generator(img[:half_h,half_w:],order-1,draw="D")
            if points!=[]:
                 for point in points:
                    all_points.append((point[0]+half_w,point[1]))
            points=generator(img[:half_h,:half_w],order-1,draw="C")
            if points!=[]:
                 for point in points:
                    all_points.append((point[0],point[1]))
    return all_points
# main program 
if __name__ == "__main__":
    global full_img
    global thickness_const
    global delay,animation
    global r,g,b,gredient
     
    # constants which determine behaviour of the program
    # ----------------------------------------------------------------
    # SET RGB
    # gradient rgb  
    r=0
    g=85
    b=170
    # const_rgb
    r=249
    g=176
    b=93
    gredient=True               # SET GREDIENT
    thickness_const=40         # SET LINE THICKNESS
    thickness_decent_content=0.5
    height=512               #SET SIZE OF CANVAS(height) height should be 50> then width for the text
    width=512                   #SET SIZE OF CANVAS(width)
    delay=1                     #SET DELAY FOR ANIMATION
    animation=True              #sets animation ON or OFF
    max_order=11                #max order for the curve
    # text consts
    # ___________________________________________
    # font
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (0,40)
    fontScale              = 1
    fontColor              = (255,255,255)
    lineType               = 2
    # ___________________________________________
    # ----------------------------------------------------------------

    # image setup
    img = np.zeros((50,width,3), np.uint8)
    img[:,:]=(0,0,0)
    img2 = np.zeros((height,width,3), np.uint8)
    img2[:,:]=(0,0,0)

    # full_img=np.zeros((height+50,width,3), np.uint8)
    for j in range(1,10):
        # filename='small_order'+str(j)+'.jpg'
        # text to print order of hilbert curve   
        # _______________________________________________________________________
        img[:50,:500]=(0,0,0)
        img2[:,:]=(0,0,0)
        cv2.putText(img,'order :-'+str(j)+"   working", bottomLeftCornerOfText, font, 
            fontScale,
            fontColor,
            lineType,cv2.LINE_AA)
        cv2.imshow("order",img[:50,:])
        k=cv2.waitKey(10)
        # _______________________________________________________________________

        # hilbert curve generator
        points=generator(img2,j,"A")

        for i in range(len(points)-1):
            rgb=colorsys.hsv_to_rgb(points[i+1][0]/width, (points[i+1][1]/height)%1, 1)
            r=rgb[0]*255
            g=rgb[1]*255
            b=rgb[2]*255
            cv2.line(img2,points[i],points[i+1],(b,g,r),thickness_const)
            k='w'
            if animation:
                cv2.imshow("img2",img2)
                k=cv2.waitKey(delay)
            if k==ord('q'):
                exit()
            if k==ord(' '):
                animation= not animation
        # text to print order of hilbert curve and process DONE    
        # _______________________________________________________________________
        img[:50,:500]=(0,0,0)
        cv2.putText(img,'order :-'+str(j)+"", bottomLeftCornerOfText, font, 
            fontScale,
            fontColor,
            lineType,cv2.LINE_AA)
        # _______________________________________________________________________
        # full_img[:50,:]=img
        # full_img[50:,:]=img2
        
        cv2.imshow("order",img[:50,:])
        cv2.imshow("img2",img2)
        # cv2.imwrite(filename,full_img)
        # out.write(img)
        k=cv2.waitKey()
        if k==ord('q'):
            exit()
        if k ==ord(' '):
            animation=True
        # version=0
        # count+=10
        # line thickness decrement by 50%
        thickness_const-=int(thickness_const*thickness_decent_content)
        if thickness_const<2:
            thickness_const=2


