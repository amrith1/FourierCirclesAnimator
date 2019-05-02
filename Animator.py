import numpy as np
import matplotlib.pyplot as plt

harmonics = 10


def animate (xlist, ylist):
	period = len(xlist)
	xtrans = [x/period for x in np.fft.fft(xlist)]
	ytrans = [y/period for y in np.fft.fft(ylist)]
	xphasors = []
	yphasors = []
	
	for i in range(harmonics + 1):
		x_cos_scalar = (xtrans[i] + xtrans[-1*i]).real
		x_sin_scalar = ((xtrans[i] - xtrans[-1*i])*1j).real
		xphasors.append(x_cos_scalar + -1j*x_sin_scalar)
	
	for i in range(harmonics):
		y_cos_scalar = (ytrans[i] + ytrans[-1*i]).real
		y_sin_scalar = ((ytrans[i] - ytrans[-1*i])*1j).real
		yphasors.append(y_sin_scalar + 1j*y_cos_scalar)
		
		
	for i in range(11):
		if(abs(xphasors[i]) > 1E-7):
			print(i, ": ", xphasors[i])
		else:
			print(i, ": ", 0)




freq = 1
period = 240.0
array = []
for x in range(int(period)):
	array.append(np.cos(2*np.pi*x*freq/period - np.pi/4) + np.cos(2*4*np.pi*x*freq/period - np.pi/6))

animate(array, range(240))




		
	


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