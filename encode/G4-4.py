from Tkinter import *
import tkMessageBox
from PIL import ImageTk, Image
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
from pexpect import pxssh

root  = Tk()
root.title("Encode file")
root.geometry("400x400+100+50")

a = StringVar()
b = StringVar()
c = StringVar()
d = StringVar()
e = StringVar()
t = Text(root,height=400,width=100)

def dataset_adress():
	c = a.get()
	c = c.replace('\\','/')
	return c
	
def encode_adress():
    c = b.get()
    c = c.replace('\\','/')
    return c

def ExitApplication():
	MsgBox = tkMessageBox.askquestion('Exit Application', 'Are you want to exit', icon='warning')
	if MsgBox == 'yes':
		root.destroy()
	else:
		tkMessageBox.showinfo('Return', 'You will now return to the application screen')

def clicked():
	check = 0
	c = dataset_adress()
	d = encode_adress()
	#check path:
	print (c)
	print (d)
	if os.path.isdir(c) and os.path.isdir(d):
		check = 1
	else:
		tkMessageBox.showerror('Information','Link error please fillout')
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
		#tkMessageBox.showinfo('Information','Complie complette')
		#tkMessageBox.showinfo('Information','Complie complette')
		s = pxssh.pxssh()
		hostname = c.get()
		username = d.get()
		password = e.get()
		s.login(hostname,username,password,sync_multiplier=5, auto_prompt_reset=False)
		os.system("/Users/bpham/Desktop/code-python/scp.command")
		s.sendline('sudo reboot -h now')
		s.prompt()
		s.logout()
		tkMessageBox.showinfo('Information','Complie complette')
			
	
noidung = """ Encode  file from image to file pickle.
1. Select path of image file
2. Select path of output file
3. Press Encode to start Encode
4. Press Quit to exit process
Let's start
Author: baopq.spkt@gmail.com """

## Component
img =ImageTk.PhotoImage(Image.open('logo.png'))
Button(root, text='Quit', command=ExitApplication, fg = "Red").pack(fill=X)
Label(root,text='Link dataset').pack(fill=X)
Entry(root,textvariable=a).pack(fill=X)
Label(root,text='Adress File output').pack(fill=X)
text = Entry(textvariable=b).pack(fill=X)
Button(root, text='Encode File', command=clicked).pack(fill=X)
Label(root,text='Your IP').pack(fill=X)
text = Entry(textvariable=c).pack(fill=X)
Label(root,text='User Name').pack(fill=X)
text = Entry(textvariable=d).pack(fill=X)
Label(root,text='Password').pack(fill=X)
text = Entry(textvariable=e).pack(fill=X)

t.pack(fill=X)
t.insert(END,noidung)

root.mainloop()
