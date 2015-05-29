# -*- coding: utf-8 -*

from Tkinter import*
import math
import time


class frame:

	def __init__(self):
		self.fenetre = Tk()
		self.fenetre.geometry("900x900")

		self.cells_memorize = []
		for i in xrange(4) :
			self.cells_memorize.append([])
			for j in xrange(10000) :
				self.cells_memorize[i].append('x')


		champ_label = Label(self.fenetre, text="Projet TACMP!")


		#Pour afficher le label dans la fenetre
		#pack permet de positionner la fenetre
		champ_label.pack()


		######################################################################################
		#                             Separation de la fenetre                               #
		######################################################################################

		pHaut = PanedWindow(self.fenetre,orient=HORIZONTAL,height=710,width=810)

		#pHaut.pack(fill=BOTH)
		pHaut.pack()


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

		pHaut.pack()

		pBas = PanedWindow(self.fenetre, orient=HORIZONTAL)
		pBas.pack(side=TOP)
		pBas1 = PanedWindow(pBas, orient=VERTICAL,height=200,width=300)
		pBas2 = PanedWindow(pBas, orient=VERTICAL,height=200,width=300)
		pBas3 = PanedWindow(pBas, orient=VERTICAL,height=200,width=300)


		# Canvas #



		pBas.add(pBas1)
		pBas.add(pBas2)
		pBas.add(pBas3)


		self.Slider = Scale(self.fenetre, from_ = 0, to = 10, resolution = 0.01)
		self.Slider.pack()
		pHaut.add(self.Slider)

		######################################################################################
		#                                     Boutons                                        #
		######################################################################################

		

		bouton1= Button(self.fenetre, text="1", command=self.fonction, height=3, width=3)
		bouton1.pack()
		bouton2= Button(self.fenetre, text="2", command=self.fonction, height=3, width=3)
		bouton2.pack()

		pBas1.add(bouton1)
		pBas1.add(bouton2)


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

		pBas.pack()
	

	def fonction(self):
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