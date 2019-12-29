import socket
import face_recognition
from PIL import Image
import glob
import time

#HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
#PORT = 65432        # Port to listen on (non-privileged ports are > 1023)



def compare_faces(picname):
	print picname,"--"
	unknown=face_recognition.load_image_file('./unknown/'+picname)#the image that we got from the bell
	print "OO"
	unknown_encoding=face_recognition.face_encodings(unknown)

	person_name="?"
	for filename in glob.glob('./known/*.png'): #assuming png
		print "*"
		known_person=face_recognition.load_image_file(filename)
		known_person_encoding=face_recognition.face_encodings(known_person)
		if face_recognition.compare_faces([unknown_encoding],known_person_encoding)[0]:
			print "gotcha"
			return filename[:len(filename)-4]#i should delete the photo if we find a match
	print "ok"
	return 'UnknownPerson'







def main():	
	TCP_IP = '127.0.0.1'
	TCP_PORT = 5005
	BUFFER_SIZE = 40960000  # picture size

	c=0
	for filename in glob.glob('./unknown/*.png'): #assuming jpg
		if int(filename[-5])>c:
			c=int(filename[-5])
	c+=1

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(1)

	conn, addr = s.accept()
	print 'Connection address:', addr
	while 1:
		try:
			data = conn.recv(BUFFER_SIZE)
			if not data: break
			#print "received data:", data
			myfile = open("./unknown/"+'person'+str(c)+'.png', 'wb')
			myfile.write(data)
			myfile.close()
			conn.sendall(compare_faces('person'+str(c)+'.png'))
			c+=1
		except:
			time.sleep(0.1)

	conn.close()



if __name__== "__main__":
	main()


