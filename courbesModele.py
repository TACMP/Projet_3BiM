import Tkinter as Tk    
from Tkinter import *     
import pylab                 
from Numeric import *  
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from numpy import *
from scipy import integrate
import time

global t,dt,temps,valeurs,courbe
fen = Tk()

nbcell=100
r2=1
b2=1
c4=1
r1=1.5
b1=1
c2=0.5
c3=1
s=0.33
rho=0.01
alpha=0.3
c1=1
d1=0.2
d2=1
a1=0.2
a2=0.3
a3=0.1
v=0.0
pn=0.8
pt=0.2
pi=0.15 #nb de cell immunitaire
cell=[0]*int(nbcell*pt)+[1]*int(nbcell*pn)

def dX_dt(X,t=0):
	return array([r2*X[0]*(1-X[0]*b2)-c4*X[1]*X[0]-a3*(1-exp(-X[3]))*X[0],
	r1*X[1]*(1-b1*X[1])-c2*X[2]*X[1]-c3*X[1]*X[0]-a2*(1-exp(-X[3]))*X[1],
	s+rho*X[1]*X[2]/(alpha+X[1])-c1*X[2]*X[1]-d1*X[2]-a1*(1-exp(-X[3]))*X[2],
	v-d2*X[3]])


fig = pylab.figure()
b = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(fig, master=fen)
canvas.show()
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
toolbar = NavigationToolbar2TkAgg(canvas, fen)
toolbar.update()
canvas._tkcanvas.pack()

global t,temps,nnf,ttf,uuf,iif,n,tt,ii,u
temps=[]
nnfStock=[]
ttfStock=[]
uufStock=[]
iifStock=[]
temps.append(0)

t=linspace(0,10,100)
t2=0
dt=0.01
X0=array([pn,pt,pi,0.0])

X,infodict=integrate.odeint(dX_dt,X0,t,full_output=True)
n,tt,ii,u=X.T

nnfStock.append(n[0])
ttfStock.append(tt[0])
uufStock.append(u[0])
iifStock.append(ii[0])

b.plot(temps,nnfStock,'r-',label='N')
b.plot(temps,ttfStock,'b-',label='T')
b.plot(temps,iifStock,'g-',label='I')

canvas.show()


for j in range(len(n)):
	#global t,temps,nnf,ttf,uuf,iif,n,tt,ii,u
	t2=t2+dt
	temps.append(t2)
	nnfStock.append(n[j])
	ttfStock.append(tt[j])
	uufStock.append(u[j])
	iifStock.append(ii[j])
	b.plot(temps,nnfStock,'r-',label='N')
	b.plot(temps,ttfStock,'b-',label='T')
	b.plot(temps,iifStock,'g-',label='I')
	pylab.axis([min(temps)-0.1,max(temps)+0.1,min(min(nnfStock),min(ttfStock),min(iifStock))-0.1,max(max(nnfStock),max(ttfStock),max(iifStock))+0.1])
	canvas.draw()

fen.mainloop()

"""
nnf=n[:]
ttf=tt[:]
iif=ii[:]
uuf=u[:]


t=0
dt = 0.1
nbboucle =10
fonction =sin(t)
temps=[]
valeurs=[]
#tableaux pour srocker valeurs
temps.append(t)
valeurs.append(fonction)

b.plot(temps,valeurs)

canvas.show()

def run():
	global t,dt,temps,valeurs,courbe
	t=t+dt
	fonction=sin(t)
	#ajout
	temps.append(t)
	valeurs.append(fonction)

	
	b.plot(temps,valeurs)
	pylab.axis([min(temps)-0.1,max(temps)+0.1,min(valeurs)-0.1,max(valeurs)+0.1])

	canvas.draw()


def run():
	global nnf,ttf,uuf,iif,n,tt,ii,u
	X0=[n[-1],tt[-1],ii[-1],u[-1]]
	X,infodict=integrate.odeint(dX_dt,X0,t,full_output=True)
	n,tt,ii,u=X.T
	temps=linspace(0,10*nbboucle,100*nbboucle)
	nnf=nnf+n
	ttf=ttf+tt
	iif=iif+i
	uuf=uuf+u
	
	b.plot(temps,nnf,'r-',label='N')
	b.plot(temps,ttf,'b-',label='T')
	b.plot(temps,iif,'g-',label='I')
	#p.plot(t,u,'p-',label='U')
	#p.show()
	time.sleep(0.5)
	#pylab.axis([min(temps)-0.1,max(temps)+0.1,min(valeurs)-0.1,max(valeurs)+0.1])
	canvas.draw()

for  i in range(nbboucle):
	run()
"""




