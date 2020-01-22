import time
import socket
import os

import pygame, sys
from pygame.locals import *
import pygame.camera

import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)

GPIO.setup(12,GPIO.IN,pull_up_down=GPIO.PUD_UP)



def main():
    TCP_IP = '40.112.58.200'
    TCP_PORT = 25
    BUFFER_SIZE = 1024
    img_counter = 0
   


    s = socket.socket()
    s.connect((TCP_IP, TCP_PORT))

    while 1:
        input_state=GPIO.input(12)


        if input_state == False:
            img_name = "opencv_frame_{}.png".format(img_counter)
            
            pygame.init()
            pygame.camera.init()
            cam = pygame.camera.Camera("/dev/video0",(640,480))
            cam.start()
            image= cam.get_image()
            pygame.image.save(image,img_name)
            cam.stop()

            print("{} written!".format(img_name))

            #convert the image to binary and send it to the server
            with open(img_name, "rb") as image:
                f = image.read()
                b = bytearray(f)
            b+="finished"
            s.sendall(b)
            
            
            #wait for the server respone with the person name or unknown
            data = s.recv(BUFFER_SIZE)
            print str(data)
            
    
    
    s.close()







if __name__== "__main__":
	main()
