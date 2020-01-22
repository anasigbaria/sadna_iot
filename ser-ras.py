import socket
import face_recognition
from PIL import Image
import glob
import time
import numpy as np
import os


#HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
#PORT = 65431        # Port to listen on (non-privileged ports are > 1023)


#the func takes a photo of a person and returns his name if there is a match in the database
def compare_faces(picname):
	unknown=face_recognition.load_image_file('./unknown/'+picname)#the image that we got from the bell
	num=face_recognition.face_locations(np.array(pic))
	if len(num)!=1:
		return 'error'
	unknown_encoding=face_recognition.face_encodings(unknown)


	person_name='UnknownPerson'
	for filename in glob.glob('./known/*.png'): #assuming png
		known_person=face_recognition.load_image_file(filename)
		known_person_encoding=face_recognition.face_encodings(known_person)
		if face_recognition.compare_faces(np.array(unknown_encoding),known_person_encoding)[0]:
			os.remove('./unknown/'+picname)#delete the photo from the unkown persons file
			return filename[8:len(filename)-4]
	return person_name #returns unknown


def phone(name):

	phon=""
	if name=='error':
		return 'error'

	for filename1 in glob.glob('./accounts/*.txt'):
		myfile = open("filename1", 'w+')
		lines=myfile.readlines()
		for line in lines:
			if name in line:
				phon=filename1[11:-4]
				break
			

		myfile.close()
		return phon
		





def main():	
	TCP_IP = '40.112.52.200'
	TCP_PORT = 25

	c=0
	for filename in glob.glob('./unknown/*.png'): #assuming jpg
		if int(filename[16:len(filename)-4])>c:
			c=int(filename[16:len(filename)-4])
	c+=1

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(1)

	conn, addr = s.accept()
	data=""
	print 'Connection address:', addr
	while 1:
		while 1:
			temp = conn.recv(1024)
			data+=temp
			if (not temp) or ('finished' in data): break
			print "received data:", len(data)
		if data:
			print len(data)
			data=data.replace('finished','')
			print len(data)
			myfile = open("./unknown/"+'person'+str(c)+'.png', 'wb')
			myfile.write(data)
			myfile.close()
			name=compare_faces('person'+str(c)+'.png')
			print name
			conn.sendall(name)
			data=""
			c+=1


	conn.close()



if __name__== "__main__":
	main()
