import numpy as np
import time
import matplotlib.pyplot as plt
from tkinter import *
import random

harmonics = 100
canvas_width = 1000
canvas_height = 1000
phase_multiples = []

def xcoord(x):
	scaled_x = 2 *x
	return scaled_x + canvas_width/2

def ycoord(y):
	scaled_y = 2*y
	return -1*scaled_y + canvas_height/2
		
def createCircles(canvas, counter_circles, clock_circles, phasors):
	prev_xloc = 0
	prev_yloc = 0
	for i in range(1, harmonics + 1):
		radius = abs(phasors[i])
		counter_circles.append(canvas.create_oval(xcoord(prev_xloc - radius), ycoord(prev_yloc - radius), xcoord(prev_xloc + radius), ycoord(prev_yloc + radius)))
		prev_xloc += phasors[i].real
		prev_yloc += phasors[i].imag
		radius = abs(phasors[-1*i])
		clock_circles.append(canvas.create_oval(xcoord(prev_xloc - radius), ycoord(prev_yloc - radius), xcoord(prev_xloc + radius), ycoord(prev_yloc + radius)))
		prev_xloc += phasors[-1*i].real
		prev_yloc += phasors[-1*i].imag		
	
def initPhaseMults(period):
	for i in range(harmonics + 1):
		phase_multiples.append(np.exp(i*np.pi*2j/period))

def update_positions(canvas, counter_circles, clock_circles, firstpass, firstpoint, phase_tracker, drawX, drawY):
	for i in range(1, harmonics + 1):
		phase_tracker[i] *= phase_multiples[i]
		phase_tracker[-1*i] *= np.conj(phase_multiples[i])
	prev_xloc = 0
	prev_yloc = 0
	for i in range(1, harmonics + 1):
		radius = abs(phase_tracker[i])
		canvas.coords(counter_circles[i], xcoord(prev_xloc - radius), ycoord(prev_yloc - radius), xcoord(prev_xloc + radius), ycoord(prev_yloc + radius))
		prev_xloc += phase_tracker[i].real
		prev_yloc += phase_tracker[i].imag
		radius = abs(phase_tracker[-1*i])
		canvas.coords(clock_circles[i], xcoord(prev_xloc - radius), ycoord(prev_yloc - radius), xcoord(prev_xloc + radius), ycoord(prev_yloc + radius))
		prev_xloc += phase_tracker[-1*i].real
		prev_yloc += phase_tracker[-1*i].imag
	if(firstpass):
		if(not firstpoint):
			canvas.create_oval(xcoord(prev_xloc -1 ), ycoord(prev_yloc- 1), xcoord(prev_xloc + 1), ycoord(prev_yloc + 1))
	drawX = prev_xloc
	drawY = prev_yloc
	
def animate (xlist, ylist):
	plt.scatter(xlist, ylist)
	plt.axis('scaled')
	plt.show(block=False)
	period = len(xlist)
	values = [xlist[i] + 1j*ylist[i] for i in range(period)]
	phasors = [x/period for x in np.fft.fft(values)]
	master = Tk()
	canvas = Canvas(master, width=canvas_width, height=canvas_height)
	counter_circles = [None]
	clock_circles = [None]
	createCircles(canvas, counter_circles, clock_circles, phasors)
	canvas.pack()
	initPhaseMults(period)
	firstpass = True
	drawX = 0
	drawY = 0
	while True:
		phase_tracker = phasors.copy()
		for phase in range(period):
			firstpoint = (phase == 0)
			update_positions(canvas, counter_circles, clock_circles, firstpass, firstpoint, phase_tracker, drawX, drawY)
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




