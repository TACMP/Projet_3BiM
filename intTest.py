#import odemedicament
import pylab as p
from Tkinter import*
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('TkAgg')
from numpy import *
import pylab as p
from scipy import integrate
from numpy import arange, sin, pi,array

class fenetre2:
	def __init__(self,pn,pt,pi,V):
		print "je fais la deuxieme fenetre"
		self.fen=Tk()
		self.fen.geometry("600x600")
		self.fen.wm_title("evolution du modele")
		#e=Entry(self.fen)
		#e.pack()
		#v=e.get()
		label =Label(self.fen,text="Value")
		label.pack()
		
		"""
		def sel():
			print (v)
			s = "Val "+ v
			label.config(text =s)
			"""
		fig = Figure(figsize=(5,4), dpi=100)
		c = FigureCanvasTkAgg(fig, master=self.fen)
		a = fig.add_subplot(111)
		c.get_tk_widget().pack()
		toolbar = NavigationToolbar2TkAgg( c, self.fen)
		toolbar.update()
		c._tkcanvas.pack()
		
		def dX_dt(X,v=0,pn=0.8,pt=0.2,t=0,nbcell=100,r2=1,b2=1,c4=1,r1=1.6,b1=1,c2=0.4,c3=1,s=0.33,rho=0.2,alpha=0.3,c1=1,d1=0.2,d2=1,a1=0.2,a2=0.3,a3=0.1):
			#if e.get()=='':
			#	v=0
			#else:
			#	v=float(e.get())
			v=V
			print("Ici v vaut"),v
			return array([r2*X[0]*(1-X[0]*b2)-c4*X[1]*X[0]-a3*(1-exp(-X[3]))*X[0],
			r1*X[1]*(1-b1*X[1])-c2*X[2]*X[1]-c3*X[1]*X[0]-a2*(1-exp(-X[3]))*X[1],
			s+rho*X[1]*X[2]/(alpha+X[1])-c1*X[2]*X[1]-d1*X[2]-a1*(1-exp(-X[3]))*X[2],
			v-d2*X[3]])
			
		def createCanvas():
			
			nbcell=100
			r2=1
			b2=1
			c4=1
			r1=1.6
			b1=1
			c2=0.4
			c3=1
			s=0.33
			rho=0.2
			alpha=0.3
			c1=1
			d1=0.2
			d2=1
			a1=0.2
			a2=0.3
			a3=0.1
			Valpn=pn
			Valpt=pt
			Valpi=pi
			v=V
			cell=[0]*int(nbcell*Valpt)+[1]*int(nbcell*Valpn)
			t=linspace(0,400,4000)
			X0=array([Valpn,Valpt,Valpi,v])
			fin=20
			pas=100
			ttf=1
			X,infodict=integrate.odeint(dX_dt,X0,t,full_output=True)
			n,tt,i,u=X.T
			a.plot(t,n,'r-',label='N')
			a.plot(t,tt,'b-',label='T')
			a.plot(t,i,'g-',label='I')
			#a.plot(t,u,'y-',label='U')
			a.legend(('cellules saines', 'cellules tumorales','cellules immunitaires'),'best')
			c.show()
		
		
		createCanvas()
		
		def clear():
			a.clear()
			
		def f():
			#clear()
			#a = fig.add_subplot(111)
			#createCanvas()
			print(v)
			
		button = Button(self.fen, text="Print v", command=f)
		button.pack()
		#self.fen.mainloop()
