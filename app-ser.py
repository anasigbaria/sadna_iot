import socket
import face_recognition
from PIL import Image
import glob
import time
import numpy as np
import os



def add_account(data,conn):
    name=data[11:data.find(':',9,len(data))]
    for filename1 in glob.glob('./accounts/*.txt'):
        if name in filename1:
            conn.sendall('user_exists')
            return
    f= open('./accounts/'+name+'.txt',"w+")
    f.write(data[11+len(name)+1:])
    f.close()
    conn.sendall('success')
    

def vistors_accounts(data,conn):
    #first we delete similar faces so there is no duplications for the same person
    for filename1 in glob.glob('./unknown/*.png'): #assuming png
        try:
            if filename1 not in glob.glob('./unknown/*.png'):
                continue
            person1=face_recognition.load_image_file(filename1)
            person1_encoding=face_recognition.face_encodings(person1)
            for filename2 in glob.glob('./unknown/*.png'): #assuming png
                if filename1!=filename2:
                    person2=face_recognition.load_image_file(filename2)
                    person2_encoding=face_recognition.face_encodings(person2)
                    if face_recognition.compare_faces(np.array(person2_encoding),person1_encoding)[0]:
                        os.remove(filename2)#delete the photo from the unkown persons file
        except:
            continue


    b="#"+len(glob.glob('./unknown/*.png'))+"$"#send the number of pics
    conn.sendall(b)
    b=""

    #now we send the picyures to the app
    for filename1 in glob.glob('./unknown/*.png'): #assuming png
        with open(filename1, "rb") as image:
                f = image.read()
                b = bytearray(f)
        #print len(b)
        b+="finished"
        conn.sendall(b)
        b=""
def manage_vistors(data,conn):
    b=""
    #first we delete similar faces so there is no duplications for the same person
    for filename1 in glob.glob('./unknown/*.png'): #assuming png
        try:
            if filename1 not in glob.glob('./unknown/*.png'):
                continue
            person1=face_recognition.load_image_file(filename1)
            person1_encoding=face_recognition.face_encodings(person1)
            for filename2 in glob.glob('./unknown/*.png'): #assuming png
                if filename1!=filename2:
                    person2=face_recognition.load_image_file(filename2)
                    person2_encoding=face_recognition.face_encodings(person2)
                if face_recognition.compare_faces(np.array(person2_encoding),person1_encoding)[0]:
                    os.remove(filename2)#delete the photo from the unkown persons file
        except:
            continue

    b="#"+len(glob.glob('./unknown/*.png'))+"#"
    conn.sendall(b)
    b=""

    #now we send the picyures to the app
    for filename1 in glob.glob('./unknown/*.png'): #assuming png
        with open(filename1, "rb") as image:
                f = image.read()
                b = bytearray(f)
        #print len(b)
        b+="##"+filename1+"$$"
        conn.sendall(b)
        b=""
    
    #now we send the uers accounts and $ sign at the end
    myfile=open("./accounts.txt")
    acc=myfile.read()
    myfile.close()
    conn.sendall(acc+'$')

def manage_accounts(data,conn):
    #send users with phones
    acc=''
    for filename1 in glob.glob('./accounts/*.txt'):
        acc+=filename1[11:-4]
        acc+=':'
        f=open(filename1)
        acc+=f.readline()
        acc+='-'
        f.close()
    conn.sendall(acc)
    

def delete_acc(data):
    name=data[10:]
    os.remove("./accounts/"+name+".txt")

def update_acc(data):
    name=data[10:data.find(':')]
    myfile=open("./accounts/"+name+".txt")
    lines=myfile.readlines()
    flag=0
        
    for line in lines:
        if flag:
            myfile.write(line)
        else:
            myfile.write(data[10+len(name):]+'\n','w+')
            flag=1
    myfile.close()


def add_vistor_to_acc(data):
    name=data[17:data.find(':')]
    phone=data[data.find(':')+1:]
    myfile=open("./accounts/"+name+".txt")
    lines=myfile.readlines()
    flag=0
    for line in lines:
        if not flag:
            myfile.write(line)
            flag=1
        else:
            myfile.write(name+':'+phone)
            flag=1
    myfile.close()

def name_to(data):
    filename=data[7:data.find('#')]
    name=data[:data.find('#')+1:]
    old_file = os.path.join("unknown", filename+'.png')
    new_file = os.path.join("known", name+'.png')
    os.rename(old_file, new_file)









def main():	
    TCP_IP = ''
    TCP_PORT = 80

    c=0
    for filename in glob.glob('./unknown/*.png'): #assuming jpg
        if int(filename[16:len(filename)-4])>c:
            c=int(filename[16:len(filename)-4])
        c+=1
    while 1:

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)

        conn, addr = s.accept()
        data=""
        print ('Connection address:', addr)
        while 1:
            while not conn._closed():
                temp = conn.recv(1024)
                data+=temp
                if (not temp) or ('finished' in data): break
            print ("received data:", len(data))
            if data:
                #print len(data)
                data=data.replace('finished','')

                if 'add_account' in data:
                    add_account(data,conn)

                elif 'manage_vistors' in data:
                    manage_vistors(data,conn)

                elif 'vistors_accounts' in data:
                    vistors_accounts(data,conn)

                elif 'manage_accounts' in data:
                    manage_accounts(data,conn)

                elif 'delete_acc' in data:
                    delete_acc(data)

                elif 'update_acc' in data:
                    update_acc(data)
                
                elif 'add_vistor_to_acc' in data:
                    add_vistor_to_acc(data)
                
                elif 'name_to' in data:
                    name_to(data)



        conn.close()



if __name__== "__main__":
	main()