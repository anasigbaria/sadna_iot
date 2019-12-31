import time
import cv2
import socket



def main():
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5005
    BUFFER_SIZE = 1024
    img_counter = 0
    cam = cv2.VideoCapture(0)


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            img_counter += 1
            with open(img_name, "rb") as image:
                f = image.read()
                b = bytearray(f)
            print len(b)
            b+="finished"
            s.sendall(b)
            #s.shutdown(socket.SHUT_WR)


            data = s.recv(BUFFER_SIZE)
            print str(data)
    
    
    s.close()







if __name__== "__main__":
	main()