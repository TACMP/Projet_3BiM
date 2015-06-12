# -*- coding: utf-8 -*

from Tkinter import*
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('TkAgg')

import math

import parameters

class fenetre2:
	def __init__(self,pn,pt,pi,V):
		self.fen=Tk()
		self.fen.geometry("600x600")
		self.fen.wm_title("Prédictions du modele")
		print "lala"
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

			
		def createCanvas():
			

			h = pn
			t = pt
			i = pi
			u = V
			time = 0
			time_list = []
			h_list = []
			t_list = []
			i_list = []

			while time < 100 :

				time_list.append(time)
				h_list.append(h)
				t_list.append(t)
				i_list.append(i)
				h,t,i,u = rK4(h,t,i,u,fh,ft,fi,fu,parameters.simul_step)
				time += parameters.simul_step

			a.plot(time_list,h_list,'r-',label='N')
			a.plot(time_list,t_list,'b-',label='T')
			a.plot(time_list,i_list,'g-',label='I')

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


params = parameters.default_parameters

def fh(h, t, i, u) :

	return params['r2'] * h * (1-params['b2']*h)  -  params['c4']*t*h - params['a3'] * (1-math.exp(-u)) * h

def ft(h, t, i, u) :

	return params['r1'] * t * (1-params['b1']*t)  -  params['c2']*i*t - params['c3']*t*h - params['a2'] * (1-math.exp(-u)) * t

def fi(h, t, i, u) :

	return params['s'] + params['rho'] * (i*t)/float(params['alpha']+t) - params['c1']*i*t - params['d1']*i - params['a1'] * (1-math.exp(-u)) * i

def fu(h, t, i, u) :

	return params['v'] - params['d2']*u

def rK4(h, t, i, u, fh, ft, fi, fu, simul_step):
	h1 = fh(h, t, i, u)*simul_step
	t1 = ft(h, t, i, u)*simul_step
	i1 = fi(h, t, i, u)*simul_step
	u1 = fu(h, t, i, u)*simul_step
	hk = h + h1*0.5
	tk = t + t1*0.5
	ik = i + i1*0.5
	uk = u + u1*0.5
	h2 = fh(hk, tk, ik, uk)*simul_step
	t2 = ft(hk, tk, ik, uk)*simul_step
	i2 = fi(hk, tk, ik, uk)*simul_step
	u2 = fu(hk, tk, ik, uk)*simul_step
	hk = h + h2*0.5
	tk = t + t2*0.5
	ik = i + i2*0.5
	uk = u + u2*0.5
	h3 = fh(hk, tk, ik, uk)*simul_step
	t3 = ft(hk, tk, ik, uk)*simul_step
	i3 = fi(hk, tk, ik, uk)*simul_step
	u3 = fu(hk, tk, ik, uk)*simul_step
	hk = h + h3
	tk = t + t3
	ik = i + i3
	uk = u + u3
	h4 = fh(hk, tk, ik, uk)*simul_step
	t4 = ft(hk, tk, ik, uk)*simul_step	
	i4 = fi(hk, tk, ik, uk)*simul_step
	u4 = fu(hk, tk, ik, uk)*simul_step
	h = h + (h1 + 2*(h2 + h3) + h4)/6
	t = t + (t1 + 2*(t2 + t3) + t4)/6
	i = i + (i1 + 2*(i2 + i3) + i4)/6
	u = u + (u1 + 2*(u2 + u3) + u4)/6
	return h,t,i,u
