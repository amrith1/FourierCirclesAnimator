import numpy as np
import time
import matplotlib.pyplot as plt
from tkinter import *
import random

harmonics = 15
canvas_width = 1000
canvas_height = 1000
phase_multiples = []
xphase_tracker = []
yphase_tracker = []

def xcoord(x):
	return x + canvas_width/2

def ycoord(y):
	return -1*y + canvas_height/2

def prodPhasors(xlist, ylist, xphasors, yphasors):
	period = len(xlist)
	xtrans = [x/period for x in np.fft.fft(xlist)]
	ytrans = [y/period for y in np.fft.fft(ylist)]	
	for i in range(harmonics + 1):
		x_cos_scalar = (xtrans[i] + xtrans[-1*i]).real
		x_sin_scalar = ((xtrans[i] - xtrans[-1*i])*1j).real
		xphasors.append(x_cos_scalar + -1j*x_sin_scalar)
	for i in range(harmonics + 1):
		y_cos_scalar = (ytrans[i] + ytrans[-1*i]).real
		y_sin_scalar = ((ytrans[i] - ytrans[-1*i])*1j).real
		yphasors.append(y_sin_scalar + 1j*y_cos_scalar)
		
def createCircles(c, xcircles, ycircles, xphasors, yphasors):
	prev_xloc = 0
	prev_yloc = 0
	for i in range(1, harmonics + 1):
		radius = abs(xphasors[i])
		if(i == 1):
			xcircles.append(c.create_oval(xcoord(0 - radius), ycoord(-3/10 * canvas_height - radius), xcoord(0 + radius), ycoord(-3/10*canvas_height + radius)))
			prev_xloc = xphasors[i].real
			prev_yloc = xphasors[i].imag - 3/10 * canvas_height
		else:
			xcircles.append(c.create_oval(xcoord(prev_xloc - radius), ycoord(prev_yloc - radius), xcoord(prev_xloc + radius), ycoord(prev_yloc + radius)))
			prev_xloc += xphasors[i].real
			prev_yloc += xphasors[i].imag
	xcircles.append(c.create_line(xcoord(prev_xloc), ycoord(prev_yloc), xcoord(prev_xloc), 0, fill = "green"))
	prev_xloc = 0
	prev_yloc = 0
	for i in range(1, harmonics + 1):
		radius = abs(yphasors[i])
		if(i == 1):
			ycircles.append(c.create_oval(xcoord(-3/10 * canvas_width - radius), ycoord(0 - radius), xcoord(-3/10 * canvas_width + radius), ycoord(0 + radius)))
			prev_xloc = yphasors[i].real - 3/10 * canvas_width
			prev_yloc = yphasors[i].imag
		else:
			ycircles.append(c.create_oval(xcoord(prev_xloc - radius), ycoord(prev_yloc - radius), xcoord(prev_xloc + radius), ycoord(prev_yloc + radius)))
			prev_xloc += yphasors[i].real
			prev_yloc += yphasors[i].imag
	ycircles.append(c.create_line(xcoord(prev_xloc), ycoord(prev_yloc), canvas_width, ycoord(prev_yloc), fill = "green"))
	c.pack()
	
def initPhaseMults(period):
	for i in range(harmonics + 1):
		phase_multiples.append(np.exp(i*np.pi*2j/period))

def initTrackers(xphasors, yphasors):
	for i in range(harmonics + 1):
		xphase_tracker.append(xphasors[i])
		yphase_tracker.append(yphasors[i])

def update_positions(canvas, xcircles, ycircles, firstpass):
	for i in range(1, harmonics + 1):
		xphase_tracker[i] *= phase_multiples[i]
		yphase_tracker[i] *= phase_multiples[i]
	prev_xloc = 0
	prev_yloc = 0
	for i in range(1, harmonics + 1):
		if(i == 1):
			#xcircles[i].coords(xcoord(0 - radius), ycoord(-3/10 * canvas_height - radius), xcoord(0 + radius), ycoord(-3/10*canvas_height + radius))
			prev_xloc = xphase_tracker[i].real
			prev_yloc = xphase_tracker[i].imag - 3/10 * canvas_height
		else:
			radius = abs(xphase_tracker[i])
			canvas.coords(xcircles[i], xcoord(prev_xloc - radius), ycoord(prev_yloc - radius), xcoord(prev_xloc + radius), ycoord(prev_yloc + radius))
			prev_xloc += xphase_tracker[i].real
			prev_yloc += xphase_tracker[i].imag
	prev_coords = canvas.coords(xcircles[harmonics + 1])
	finalX = prev_coords[0]
	finalNewX = xcoord(prev_xloc)
	canvas.coords(xcircles[harmonics + 1], xcoord(prev_xloc), ycoord(prev_yloc), xcoord(prev_xloc), 0)	
	prev_xloc = 0
	prev_yloc = 0
	for i in range(1, harmonics + 1):
		if(i == 1):
			#ycircles.append(c.create_oval(xcoord(-3/10 * canvas_width - radius), ycoord(0 - radius), xcoord(-3/10 * canvas_width + radius), ycoord(0 + radius)))
			prev_xloc = yphase_tracker[i].real - 3/10 * canvas_width
			prev_yloc = yphase_tracker[i].imag
		else:
			radius = abs(yphase_tracker[i])
			canvas.coords(ycircles[i], xcoord(prev_xloc - radius), ycoord(prev_yloc - radius), xcoord(prev_xloc + radius), ycoord(prev_yloc + radius))
			prev_xloc += yphase_tracker[i].real
			prev_yloc += yphase_tracker[i].imag
	prev_coords = canvas.coords(ycircles[harmonics + 1])
	if firstpass:
		canvas.create_line(finalX, prev_coords[1], finalNewX, ycoord(prev_yloc))		
	canvas.coords(ycircles[harmonics + 1], xcoord(prev_xloc), ycoord(prev_yloc), canvas_width, ycoord(prev_yloc))

def animate (xlist, ylist):
	xphasors = []
	yphasors = []
	prodPhasors(xlist, ylist, xphasors, yphasors)
	master = Tk()
	canvas = Canvas(master, width=canvas_width, height=canvas_height)
	xcircles = [None]
	ycircles = [None]
	createCircles(canvas, xcircles, ycircles, xphasors, yphasors)
	period = len(xlist)
	initPhaseMults(period)
	firstpass = True
	while True:
		initTrackers(xphasors, yphasors)
		for phase in range(period):
			update_positions(canvas, xcircles, ycircles, firstpass)
			master.update()
			time.sleep(0.002)
		firstpass = False





period = 512.0
x_array = []
y_array = []

type = ""
seed = 0
if(len(sys.argv) < 2):
	print("Illegal Arguments")
	exit()
else: 
	type = sys.argv[1][1:len(sys.argv[1])]
	if(type == "random"):
		seed = int(sys.argv[2])
		

if(type == "random"):
	xpoint = 0
	ypoint = 0
	x_array.append(xpoint)
	y_array.append(ypoint)
	xmax = 0
	xmin = 0
	ymax = 0
	ymin = 0
	random.seed(seed)
	for i in range(int(period/2)):
		xmax = (300) if (xpoint + 10 > 300) else (xpoint + 10)
		ymax = (300) if (ypoint + 10 > 300) else (ypoint + 10)
		xmin = (-300) if (xpoint - 10 < -300) else (xpoint - 10)
		ymin = (-300) if (ypoint - 10 < -300) else (ypoint - 10)
		xpoint = random.randint(xmin, xmax + 1)
		ypoint = random.randint(ymin, ymax + 1)
		x_array.append(xpoint)
		y_array.append(ypoint)
	for i in range(int(period/2)):
		x_array.append(x_array[int(period/2) - i])
		y_array.append(y_array[int(period/2) - i])






if(type == "square"):
	for x in range(int(period)):
		if (x < 128):
			x_array.append(-64 + x)
		elif (x < 256):
			x_array.append(64)
		elif (x < 384):
			x_array.append(64 - x + 256)
		else:
			x_array.append(-64)

	for y in range(int(period)):
		if (y < 128):
			y_array.append(-64)
		elif (y < 256):
			y_array.append(-64 + y -128)
		elif (y < 384):
			y_array.append(64)
		else:
			y_array.append(64 - y + 384)




animate(x_array, y_array)






"""
radius = abs(yphasors[i])
		ycircles.append(c.create_oval(xcoord(-300 - radius), ycoord(0 - radius), xcoord(-300 + radius), ycoord(0 + radius)))
"""


"""	
for i in range(11):
	if(abs(xphasors[i]) > 1E-7):
		print(i, ": ", xphasors[i])
	else:
		print(i, ": ", 0)
		
for i in range(11):
	if(abs(yphasors[i]) > 1E-7):
		print(i, ": ", yphasors[i])
	else:
		print(i, ": ", 0)
"""		
	


"""
print(np.sin(0), "\n")
freq = 5
period = 240.0
array = []
for x in range(int(period)):
	array.append(np.sin(2*np.pi*x*freq/period) + np.cos(2*np.pi*x*freq/period))


#print(array)

result = np.fft.fft(a = array)
print(len(result), "\n")

###############
for x in range(int(period)):
	if(abs(result[x]) > 1E-7):
		print("Index ", x, " is ", result[x]/period, "\n")


#plt.plot(range(64), original)
#plt.show()
"""


