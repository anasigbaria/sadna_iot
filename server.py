import face_recognition
from PIL import Image
import glob

unknown="image"#the image that we got from the bell
unknown_encoding=fr.face_encodings(unknown)

person_name="?"
for filename in glob.glob('yourpath/*.gif'): #assuming gif
    known_person=fr.load_image_file(filename)
    known_person_encoding=fr.face_encodings(known_person)
    if fr.compare_faces([unknown_encoding],known_person_encoding)[0]:#compare faces
        person_name=filename[:len(filename)-4]
        break





