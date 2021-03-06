import random, re,  subprocess, sys, os, math ,numpy,shutil
import matplotlib.pyplot as plt
import stl
from stl import mesh
from distutils.dir_util import copy_tree
from multiprocessing import Pool
import scipy.interpolate as si


def read_integers(filename,t):
	with open(filename) as f:
		if t=='f':
			z=[float(x) for x in f]
			if len(z)==1:
				return z[0]
			else:
				return z
		if t=='i':
			z=[int(x) for x in f]
			if len(z)==1:
				return z[0]
			else:
				return z

def randf(x,y):
    a=1000
    return float(random.randrange(int(x*a),int(y*a)))/a


def myRound(x,base,prec=2):
    return round(base * round(float(x)/base),prec)

def cartesian(R,A):
    X=[];Y=[]
    for i in range(len(R)):
        X.append(R[i]*math.cos(math.radians(A[i])))
        Y.append(R[i]*math.sin(math.radians(A[i])))
    return X,Y

def polar(X,Y):
    R=[];A=[]
    for i in range(len(X)):
        R.append((X[i]**2+Y[i]**2)**0.5)
        print Y[i],X[i]
        A.append(math.degrees(math.atan(float(Y[i])/X[i])))
    return R,A


def run(I):
	def bspline(cv, n=100, degree=2, periodic=True):
	    """ Calculate n samples on a bspline

	        cv :      Array ov control vertices
	        n  :      Number of samples to return
	        degree:   Curve degree
	        periodic: True - Curve is closed
	                  False - Curve is open
	    """

	    # If periodic, extend the point array by count+degree+1
	    cv = numpy.asarray(cv)
	    count = len(cv)

	    if periodic:
	        factor, fraction = divmod(count+degree+1, count)
	        cv = numpy.concatenate((cv,) * factor + (cv[:fraction],))
	        count = len(cv)
	        degree = numpy.clip(degree,1,degree)

	    # If opened, prevent degree from exceeding count-1
	    else:
	        degree = numpy.clip(degree,1,count-1)


	    # Calculate knot vector
	    kv = None
	    if periodic:
	        kv = numpy.arange(0-degree,count+degree+degree-1,dtype='int')
	    else:
	        kv = numpy.array([0]*degree + range(count-degree+1) + [count-degree]*degree,dtype='int')

	    # Calculate query range
	    u = numpy.linspace(periodic,(count-degree),n)


	    # Calculate result
	    arange = numpy.arange(len(u))
	    points = numpy.zeros((len(u),cv.shape[1]))
	    for i in xrange(cv.shape[1]):
	        points[arange,i] = si.splev(u, (kv,cv[:,i],degree))

	    return points

	def insert(X,Y,R,A):
	    X.append(R)
	    Y.append(A)
	    #n+=1
	    #X.append(R*math.cos(math.radians(A)))
	    #Y.append(R*math.sin(math.radians(A)))
	    

	def dis(r1,a1,r2,a2):
	    #d1=math.sqrt((r2-r1)**2+(a2-a1)**2) //Cartesian
	    d1=math.sqrt(r1**2+r2**2-2*r1*r2*math.cos(math.radians(a1-a2)))
	            
	    return d1
	
	from Constants import Rmax,Rmin, Angle
	coorArrX = []
	coorArrY = []
	R=randf(Rmin,Rmax)
	A=0
	insert(coorArrX,coorArrY,R,A)
	for i in range(180/Angle):
		R=randf(Rmin,Rmax)
		A=(i+randf(0,1))*Angle
		#print R,(A-i*Angle)
		insert(coorArrX,coorArrY,R,A)
	R=randf(Rmin,Rmax)
	A=180
	insert(coorArrX,coorArrY,R,A)
	'''
	thefile = open('../Genes', 'w')
	for i in range(len(coorArrX)):
		thefile.write("%.2f %.2f\n" %(coorArrX[i],coorArrY[i]))
	thefile.close()
	
	'''
	n=len(coorArrX)
	os.makedirs('../Results/Generation_0/Specie_%i'%I)
	thefile = open('../Results/Generation_0/Specie_%i/Genes'%I, 'a+')
	for i in range(len(coorArrX)):
		thefile.write("%.2f\t%.2f\n" %(coorArrX[i],coorArrY[i]))#randf(random.randrange(random.randrange(-150,-145),-70),0))
	thefile.close()
	
	def graph(coorArrX,coorArrY):
		#print coorArrY
		#print read_integers('../Results/Generation_0/Specie_%i/Genes'%I,'fxy')
		
		#coorArrX,coorArrY=read_integers('../Results/Generation_0/Specie_%i/Genes'%I,'fxy')
		numSteps = 500    
		n=len(coorArrY)
		for i in range(n-2):
			coorArrX.append(coorArrX[(n-i-2)])
			coorArrY.append(-coorArrY[(n-i-2)])

		X,Y=cartesian(coorArrX,coorArrY)
		coorArrX=X;coorArrY=Y
		XY=bspline(numpy.array(zip(coorArrX,coorArrY)),numSteps,2)
		#print XY
		x1=[XY[i][0] for i in range(len(XY))]
		y1=[XY[i][1] for i in range(len(XY))]
	    
	    #print R,A

		'''
		#print x,y
		plt.xlim(-100,500)  
		plt.ylim(-300,300) 
		plt.scatter(coorArrX,coorArrY,s=2)
		plt.scatter(coorArrX[0],coorArrY[0],c='k',s=2)
		plt.scatter(coorArrX[n-1],coorArrY[n-1],c='k',s=2)
		#n=["%s" %i for i in range(len(coorArrX))]
		#for i, txt in enumerate(n):
		#    plt.annotate(txt, (coorArrX[i],coorArrY[i]),size="10")

		x=[];y=[]
		res=1000
		R=[Rmin for i in range(res+1)]
		A=[(Amax-Amin)*z/res+Amin for z in range(res+1)]


		for i in range(len(R)):
		    x.append(R[i]*math.cos(math.radians(A[i])))
		    y.append(R[i]*math.sin(math.radians(A[i])))
		plt.plot(x,y,c='r', linewidth=0.5)

		x=[];y=[]
		R=[Rmax for i in range(res+1)]
		A=[(Amax-Amin)*i/res+Amin for i in range(res+1)]
		for i in range(len(R)):
		    x.append(R[i]*math.cos(math.radians(A[i])))
		    y.append(R[i]*math.sin(math.radians(A[i])))
		plt.plot(x,y,c='r', linewidth=0.5)

		x=[];y=[]
		R=[(Rmax-Rmin)*i/res+Rmin for i in range(res+1)]
		A=[Amin for i in range(res+1)]
		for i in range(len(R)):
		    x.append(R[i]*math.cos(math.radians(A[i])))
		    y.append(R[i]*math.sin(math.radians(A[i])))
		plt.plot(x,y,c='r', linewidth=0.5)

		x=[];y=[]
		R=[(Rmax-Rmin)*i/res+Rmin for i in range(res+1)]
		A=[Amax for i in range(res+1)]
		for i in range(len(R)):
		    x.append(R[i]*math.cos(math.radians(A[i])))
		    y.append(R[i]*math.sin(math.radians(A[i])))
		plt.plot(x,y,c='r', linewidth=0.5)
		    





		plt.plot(x1,y1,c='k', linewidth=1)

		thefile = open('../Results/Generation_0/Specie_%i/Points'%I, 'a+')
		for i in range(len(x1)):
		    
		    thefile.write("%.6f %.6f\n" %(x1[i],y1[i]))#randf(random.randrange(random.randrange(-150,-145),-70),0))
		    
		thefile.close()
		'''
		plt.plot(x1,y1)
		plt.savefig('../Results/Generation_0/Fig%i.svg'%(I))
		plt.close()

	graph(coorArrX,coorArrY)
	

	
    #plt.show()
    #os.remove('Points')

'''
for i in xrange(1,10):
    run(i)

'''
def Gen1_run(nPop0):
	
	if(not os.path.isdir("../Results")):
		os.mkdir('../Results')
	else:
		shutil.rmtree('../Results')
		os.mkdir('../Results')
	
	#os.makedirs('../Results/Generation_0/Specie_%i'%(1))
	y = Pool()
	result = y.map(run,range(nPop0))
	y.close()
	y.join()    

#run(1)

Gen1_run(20)
#run()