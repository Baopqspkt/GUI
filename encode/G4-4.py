from Tkinter import *
import tkMessageBox
from PIL import ImageTk, Image
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

root  = Tk()
root.title("Encode file")
root.geometry("400x400+100+50")

a = StringVar()
b = StringVar()
t = Text(root,height=400,width=40)

def dataset_adress():
	c = a.get()
	c = c.replace('\\','/')
	return c
	
def encode_adress():
    c = b.get()
    c = c.replace('\\','/')
    return c

def clicked():
	check = 0
	c = dataset_adress()
	d = encode_adress()
	#check path:
	print (c)
	print (d)
	if os.path.isdir(c) and os.path.isdir(d):
		check = 1
	if check == 1:
		imagePaths = list(paths.list_images(c))
		knownEncodings = []
		knownNames = []

		for (i, imagePath) in enumerate(imagePaths):
			name = imagePath.split(os.path.sep)[-2]

			image = cv2.imread(imagePath)
			rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

			boxes = face_recognition.face_locations(rgb,
				model="hog")

			encodings = face_recognition.face_encodings(rgb, boxes)

			for encoding in encodings:
				knownEncodings.append(encoding)
				knownNames.append(name)

		data = {"encodings": knownEncodings, "names": knownNames}
		f = open(d + '/' + "encoding.pickle", "wb")
		f.write(pickle.dumps(data))
		f.close()
	if (check == 1):
		tkMessageBox.showinfo('Information','Complie complette')	
	else:
		tkMessageBox.showerror('Information','Link error please input by hand')
noidung = """ Encode  file from image to file pickle.
1. Select path of image file
2. Select path of output file
3. Press Encode to start Encode
4. Press Quit to exit process
Let's start
Author: baopq.spkt@gmail.com """
img =ImageTk.PhotoImage(Image.open('logo.png'))
Button(root, text='Quit', command=root.destroy).pack(fill=X)
Label(root,text='Link dataset').pack(fill=X)
Entry(root,textvariable=a).pack(fill=X)
Label(root,text='Adress File output').pack(fill=X)
text = Entry(textvariable=b).pack(fill=X)
Button(root, text='Encode File', command=clicked).pack(fill=X)
panel = Label(root,image = img)
panel.pack(side = "bottom",fill = "both", expand = "yes")
t.pack(fill=X)
t.insert(END,noidung)

root.mainloop()
