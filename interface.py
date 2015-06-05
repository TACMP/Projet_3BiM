# -*- coding: utf-8 -*

from Tkinter import*
import math
import time
import intTest
import pylab      
import random       



#from Numeric import *  
    

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

class frame:

	def __init__(self):
		self.fenetre = Tk()
		self.fenetre.geometry("1400x1400")
		
		"""
		self.sickWoman = TACMP.Woman()
		print Poor_girl
		self.sickWoman.simul_RK()
		print Poor_girl
		"""

		self.cells_memorize = []
		for i in xrange(4) :
			self.cells_memorize.append([])
			for j in xrange(10000) :
				self.cells_memorize[i].append('x')

		self.txt=StringVar()
		self.txt.set("Projet TACMP!")
		self.champ_label = Label(self.fenetre, textvariable=self.txt)

		
		#Pour afficher le label dans la fenetre
		#pack permet de positionner la fenetre
		self.champ_label.pack()
		
		
		#Pour que la fenetre reste ouverte a la fin:
		self.see=True
		
		
		

		######################################################################################
		#                             Separation de la fenetre                               #
		######################################################################################
		panneau1 = PanedWindow(self.fenetre,orient=HORIZONTAL,height=710,width=1400)
		
		pHaut = PanedWindow(self.fenetre,orient=HORIZONTAL,height=710,width=800)
		pDroite = PanedWindow(self.fenetre,orient=VERTICAL,height=710,width=400)

		pHaut1 = PanedWindow(pHaut, orient=VERTICAL)
		pHaut2 = PanedWindow(pHaut, orient=VERTICAL)
		

		self.Canvas1 = Canvas(self.fenetre, width=350, height=350,bg='white')
		self.Canvas1.create_rectangle(1,1,349,349) 
		self.Canvas2= Canvas(self.fenetre, width=350, height=350,bg='white')
		self.Canvas2.create_rectangle(1,1,349,349)  
		self.Canvas3= Canvas(self.fenetre, width=350, height=350,bg='white') 
		self.Canvas3.create_rectangle(1,1,349,349) 
		self.Canvas4= Canvas(self.fenetre, width=350, height=350,bg='white') 
		self.Canvas4.create_rectangle(1,1,349,349) 
		
		pHaut1.add(self.Canvas1)
		pHaut1.add(self.Canvas2)
		pHaut2.add(self.Canvas3)
		pHaut2.add(self.Canvas4)

		pHaut.add(pHaut1)
		pHaut.add(pHaut2)
		
		
		################################"""
		#self.CanvasCourbes = Canvas(self.fenetre, width=600, height=300,bg='white')
		self.fig = pylab.figure()
		self.b = self.fig.add_subplot(111)
		self.canvas = FigureCanvasTkAgg(self.fig, master=pDroite)
		self.canvas.show()
		self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
		toolbar = NavigationToolbar2TkAgg(self.canvas, self.fenetre)
		toolbar.update()
		self.canvas._tkcanvas.pack()
	
		global t,dt,nbT,nbH,temps,valT,valH
		t=0
		dt = 0.1
		temps=[]
		valT=[]
		valH=[]
		temps.append(t)
		nbT=0
		nbH=0
		valT.append(nbT)
		valH.append(nbH)
		print len(temps), len(valT)
		self.b.plot(temps,valT,'r-')
		self.b.plot(temps,valH,'b-')

		self.canvas.show()
		
		################################"

		panneau1.add(pHaut)
		panneau1.add(pDroite)
		
		panneau1.pack()
		
		
		
		self.Slider = Scale(self.fenetre, from_ = 0, to = 10, resolution = 0.01)
		self.Slider.pack()
		pHaut.add(self.Slider)
		
		

		pBas = PanedWindow(self.fenetre, orient=HORIZONTAL)
		pBas.pack(side=TOP)
		pBas1 = PanedWindow(pBas, orient=VERTICAL,height=200,width=300)
		pBas2 = PanedWindow(pBas, orient=VERTICAL,height=200,width=300)

		pBas.add(pBas1)
		pBas.add(pBas2)

		

		######################################################################################
		#                                     Boutons                                        #
		######################################################################################

		

		bouton1= Button(self.fenetre, text="Tracer courbes", command=self.fonction, height=3, width=3)
		bouton1.pack()
		

		pBas1.add(bouton1)
		
		#Bouton pour intervention chirurgicale
		self.buttonSurgery=False
		bSurgery=Button(self.fenetre,text="Intervention chirurgicale",command=self.setSurgery, height=3, width=3)
		bSurgery.pack()
		pBas1.add(bSurgery)

		"""
		######################################################################################
		#                                     CheckBoxs                                      #
		######################################################################################

		var_case1 = IntVar()
		case1 = Checkbutton(self.fenetre, text="Ne plus poser cette question", variable=var_case1)
		case1.pack()

		var_case2 = IntVar()
		case2 = Checkbutton(self.fenetre, text="Poser encore cette question", variable=var_case2)
		case2.pack()

		pBas2.add(case1)
		pBas2.add(case2)
		
"""
		
		
		pBas.pack()

	def run2(self,org):
		global  t,dt,nbT,nbH,temps,valT,valH
		
		self.b.clear()
		#if t==0
		t=t+dt
		temps.append(t)
		
		nbT = org.status['T']
		nbH = org.status['H']
		valT.append(nbT)
		valH.append(nbH)
		"""
		self.b.plot(temps,valT,'r-')
		self.b.plot(temps,valH,'b-')
		
		self.b.plot(t,nbT,'r-')
		self.b.plot(t,nbH,'b-')
		
		self.canvas._tkcanvas.create_oval(t, nbT,t+0.1,nbT+0.1, 'r-')
		self.canvas._tkcanvas.create_oval(t, nbH,t+0.1,nbH +0.1, 'b-')
		"""
		self.b.plot(temps,valT,'r-')
		self.b.plot(temps,valH,'b-')

		"""
		if len(temps)>=100:
			pylab.axis([max(temps)-5,max(temps)+0.1,min(min(valT),min(valH))-0.1,max(max(valT),max(valH))+0.1])
		else:
			pylab.axis([min(temps)-0.1,max(temps)+0.1,min(min(valT),min(valH))-0.1,max(max(valT),max(valH))+0.1])
		"""
		self.canvas.draw()

	def fonction(self):
		f= intTest.fenetre2(0.8,0.2,0.15)
		TACMP.test()
		print "coucou"
			
	def draw_organ(self,name,org,orgEntier):
		
		cs = 5
		if name=='Lung':
			
			for i in xrange(len(org)):
				x=i%int(math.sqrt(len(org)))
				y=i/int(math.sqrt(len(org)))
				if org[i] != self.cells_memorize[0][i] :	
					if org[i]=='H':
						self.Canvas1.create_oval(cs*x+10,cs*y+10,cs*x+11,cs*y+11,outline='green')
					elif org[i]=='T':
						self.Canvas1.create_oval(cs*x+10,cs*y+10,cs*x+11,cs*y+11,outline='red')
			self.cells_memorize[0] = list(org)

		elif name=='Liver':
			for i in xrange(len(org)):
				x=i%int(math.sqrt(len(org)))
				y=i/int(math.sqrt(len(org)))
				if org[i] != self.cells_memorize[1][i] :	
					if org[i]=='H':
						self.Canvas2.create_oval(cs*x+10,cs*y+10,cs*x+11,cs*y+11,outline='green')
					elif org[i]=='T':
						self.Canvas2.create_oval(cs*x+10,cs*y+10,cs*x+11,cs*y+11,outline='red')			
			self.cells_memorize[1] = list(org)

		elif name=='Breast':
			
			for i in xrange(len(org)):
				x=i%int(math.sqrt(len(org)))
				y=i/int(math.sqrt(len(org)))
				if org[i] != self.cells_memorize[2][i] :	
					if org[i]=='H':
						self.Canvas3.create_oval(cs*x+10,cs*y+10,cs*x+11,cs*y+11,outline='green')
					elif org[i]=='T':
						self.Canvas3.create_oval(cs*x+10,cs*y+10,cs*x+11,cs*y+11,outline='red')
			self.cells_memorize[2] = list(org)

		elif name=='Skin':
			for i in xrange(len(org)):
				x=i%int(math.sqrt(len(org)))
				y=i/int(math.sqrt(len(org)))
				if org[i] != self.cells_memorize[3][i] :	
					if org[i]=='H':
						self.Canvas4.create_oval(cs*x+10,cs*y+10,cs*x+11,cs*y+11,outline='green')
					elif org[i]=='T':
						self.Canvas4.create_oval(cs*x+10,cs*y+10,cs*x+11,cs*y+11,outline='red')
			self.cells_memorize[3] = list(org)

		# prise en compte actions utilisateur
		self.fenetre.update_idletasks()
		self.fenetre.update()


	def update_treatment(self) :
		return self.Slider.get()
		
	def death_message(self,message):
		t=Toplevel()
		s=StringVar()
		s.set(message)
		death=Label(t, textvariable=s)
		death.pack()
		self.fenetre.mainloop()
		#a faire : un reset quand on ferme la fenetre message
		
	def setSurgery(self):
		self.buttonSurgery=True
		
	def surgery(self,org): # Idee : mettre un nombre max et un temps entre les interventions? Sinon il suffit de faire plein d'interventions pour guerir la patiente
		p=0.90+random.random()*0.05 #calcul le pourcentage de tumeur qui sera enleve
		remove=p*org.status['T']
		org.status['T']-=remove
		org.status['H']+=remove
		self.buttonSurgery=False
		
