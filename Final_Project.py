import zipfile

from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

# the rest is up to you!

from zipfile import ZipFile
main_files=zipfile.ZipFile("images.zip","r")

main_images = main_files.infolist()
main_names = main_files.namelist()

all_imgs=[]
for img in main_images:
    img = Image.open(main_files.open(img))
    all_imgs.append(img)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

all_sheet=[]
all_text =[]
for img in all_imgs:
    img1 = np.array(img)
    gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(img.convert("L"))
    all_text.append(text)
    faces= face_cascade.detectMultiScale(gray,1.20,minNeighbors = 5,minSize=(75,85))
#     if len(faces)==0:
#         print ("But there were no faces in that file")
    if len(faces)>5:
        contact_sheet = Image.new("RGB",(500,200))
    else:
        contact_sheet = Image.new("RGB",(500,100))
    i=0
    j=0
    for x,y,w,h in faces:
        new =img.crop((x,y,x+w,y+h))
        new1= new.resize((100,100))
        contact_sheet.paste(new1,(i,j))
        if i+new1.width==contact_sheet.width:
            i=0
            j=j+new1.width
        else:
            i+=new1.width
    all_sheet.append(contact_sheet)

final_dict ={}
idx=0
for name in main_names:
    final_dict[name]= [all_sheet[idx],all_text[idx]]
    idx+=1
    
def word_search(word):
    for name in final_dict.keys():
        if word in final_dict[name][1]:
            print ("Result found in file {}".format(name))
            if len(np.nonzero(np.array(final_dict[name][0]))[0])>0:
                display(final_dict[name][0])
            else:
                print ("But there were no faces in that file")

word_search("Christopher")
#word_search("Mark")