# -*- coding: utf-8 -*

from Tkinter import*
import math
import time
import intTest
import pylab                 
#from Numeric import *  
    

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

class frame:

	def __init__(self):
		self.fenetre = Tk()
		self.fenetre.geometry("1400x1400")

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
		
		

		self.see=True
		
		
		

		######################################################################################
		#                             Separation de la fenetre                               #
		######################################################################################
		panneau1 = PanedWindow(self.fenetre,orient=HORIZONTAL,height=710,width=1400)
		
		pHaut = PanedWindow(self.fenetre,orient=HORIZONTAL,height=710,width=800)
		pDroite = PanedWindow(self.fenetre,height=710,width=400)

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
		fig = pylab.figure()
		self.b = fig.add_subplot(111)
		self.canvas = FigureCanvasTkAgg(fig, master=pDroite)
		self.canvas.show()
		self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
		toolbar = NavigationToolbar2TkAgg(self.canvas, self.fenetre)
		toolbar.update()
		self.canvas._tkcanvas.pack()
		global t,dt,temps,valeurs,courbe


		t=0
		dt = 0.1
		interval_temps =100
		fonction =math.sin(t)
		temps=[]
		valeurs=[]
		#tableaux pour srocker valeurs
		temps.append(t)
		valeurs.append(fonction)

		self.b.plot(temps,valeurs)

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

	def run(self):
		global t,dt,temps,valeurs,courbe
		t=t+dt
		fonction=math.sin(t)
		#ajout
		temps.append(t)
		valeurs.append(fonction)

		
		self.b.plot(temps,valeurs)
		pylab.axis([min(temps)-0.1,max(temps)+0.1,min(valeurs)-0.1,max(valeurs)+0.1])

		self.canvas.draw()

	def fonction(self):
		f= intTest.fenetre2()
		print "coucou"
			
	def draw_organ(self,name,org):
		
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
						self.run()
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
		self.fenetre.update_idletasks()
		self.fenetre.update()
		
