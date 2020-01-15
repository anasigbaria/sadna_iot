import time
import cv2
import socket
import face_recognition
import numpy as np




def main():
    TCP_IP = '40.112.58.200'
    TCP_PORT = 25
    BUFFER_SIZE = 1024
    img_counter = 0
    cam = cv2.VideoCapture(0)


    s = socket.socket()
    s.connect((TCP_IP, TCP_PORT))

    while 1:
        ret, frame = cam.read()
        cv2.imshow("test", frame)
       # cv2.imshow("test", frame)
        if not ret:
            break
        time.sleep(0.1)
        k=cv2.waitKey(1)
        if k%256 == 32:
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))

            #check the number of faces if its not 1 then retake the photo
            pic=face_recognition.load_image_file(img_name)
            num=face_recognition.face_locations(np.array(pic))
            if len(num)!=1:
                continue

            #convert the image to binary and send it to the server
            img_counter += 1
            with open(img_name, "rb") as image:
                f = image.read()
                b = bytearray(f)
            #print len(b)
            b+="finished"
            s.sendall(b)
            
            
            #wait for the server respone with the person name or unknown
            data = s.recv(BUFFER_SIZE)
            print str(data)
    
    
    s.close()







if __name__== "__main__":
	main()