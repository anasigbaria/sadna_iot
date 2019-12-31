import socket
import face_recognition
from PIL import Image
import glob
import time
import numpy as np

#HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
#PORT = 65432        # Port to listen on (non-privileged ports are > 1023)



def compare_faces(picname):
	print picname,"--"
	unknown=face_recognition.load_image_file('./unknown/'+picname)#the image that we got from the bell
	unknown_encoding=face_recognition.face_encodings(unknown)

	person_name='UnknownPerson'
	for filename in glob.glob('./known/*.png'): #assuming png
		print "*"
		known_person=face_recognition.load_image_file(filename)
		known_person_encoding=face_recognition.face_encodings(known_person)
		if face_recognition.compare_faces(np.array(unknown_encoding),known_person_encoding)[0]:
			print "gotcha"
			return filename[8:len(filename)-4]#i should delete the photo if we find a match
	print "ok"
	return person_name







def main():	
	TCP_IP = '127.0.0.1'
	TCP_PORT = 5005
	BUFFER_SIZE = 40960000  # picture size

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