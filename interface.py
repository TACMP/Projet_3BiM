# -*- coding: utf-8 -*

from Tkinter import*
import math
import time
import intTest
import pylab      
import random
import os



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
		
		self.TraceCourbeLung =False
		self.TraceCourbeBreast =False
		self.TraceCourbeSkin =False
		self.TraceCourbeLiver =False


		self.reset = False
		
		
		

		######################################################################################
		#                             Separation de la fenetre                               #
		######################################################################################
		panneau1 = PanedWindow(self.fenetre,orient=HORIZONTAL,height=750,width=1400)
		
		pHaut = PanedWindow(self.fenetre,orient=HORIZONTAL,height=750,width=800)
		pDroite = PanedWindow(self.fenetre,orient=VERTICAL,height=750,width=400)

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
		
		txt=StringVar()
		txt.set("Poumon")
		self.Poumon = Label(self.fenetre, textvariable=txt)
		
		txt2=StringVar()
		txt2.set("Sein")
		self.Sein = Label(self.fenetre, textvariable=txt2)
		
		txt3=StringVar()
		txt3.set("Foie")
		self.Foie = Label(self.fenetre, textvariable=txt3)
		
		txt4=StringVar()
		txt4.set("Peau")
		self.Peau = Label(self.fenetre, textvariable=txt4)
		
		pHaut1.add(self.Poumon)

		pHaut1.add(self.Canvas1)
		
		pHaut1.add(self.Foie)
		
		pHaut1.add(self.Canvas2)
		
		pHaut2.add(self.Sein)
		pHaut2.add(self.Canvas3)
		
		pHaut2.add(self.Peau)
		pHaut2.add(self.Canvas4)
		
		
		pHaut.add(pHaut1)
		pHaut.add(pHaut2)
		
		
		################################"""
	
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

		
		################################"

		panneau1.add(pHaut)
		panneau1.add(pDroite)
		
		panneau1.pack()
		
		
		
		self.Slider = Scale(self.fenetre, from_ = 0, to = 20, resolution = 0.1)
		self.Slider.pack()
		pHaut.add(self.Slider)
		
		


		self.pBas = PanedWindow(self.fenetre, orient=HORIZONTAL)
		self.pBas.pack(side=TOP)
		pBas1 = PanedWindow(self.pBas, orient=VERTICAL,height=150,width=700)
		pBas2 = PanedWindow(self.pBas, orient=VERTICAL,height=150,width=700)


		self.pBas.add(pBas1)
		self.pBas.add(pBas2)

		

		######################################################################################
		#                                     Boutons                                        #
		######################################################################################

		pBas11 = PanedWindow(pBas1, orient=HORIZONTAL,height=75,width=700)
		pBas12 = PanedWindow(pBas1, orient=HORIZONTAL,height=75,width=700)
		
		pBas1.add(pBas11)
		pBas1.add(pBas12)

		boutonLung= Button(self.fenetre, text="Tracer courbes Poumon", command=self.TracerCourbeLung)
		boutonLung.pack()
		
		boutonBreast= Button(self.fenetre, text="Tracer    courbes    Sein", command=self.TracerCourbeBreast)
		boutonBreast.pack()
		
		boutonLiver= Button(self.fenetre, text="Tracer courbes Foie", command=self.TracerCourbeLiver)
		boutonLiver.pack()
		
		boutonSkin= Button(self.fenetre, text="Tracer courbes Peau", command=self.TracerCourbeSkin)
		boutonSkin.pack()

		boutonReset = Button(self.fenetre, text="RESET", command=self.Reset)

		pBas11.add(boutonBreast)
		pBas11.add(boutonLiver)
		pBas12.add(boutonLung)
		pBas12.add(boutonSkin)
		pBas12.add(boutonReset)
		
		#Bouton pour intervention chirurgicale
		self.buttonSurgery=False
		bSurgery=Button(self.fenetre,text="Intervention chirurgicale",command=self.setSurgery, height=3, width=3)
		bSurgery.pack()
		pBas2.add(bSurgery)
		
		self.fileLung = open("StockageDonneesLung.txt","w+")
		self.fileLiver = open("StockageDonneesLiver.txt","w+")
		self.fileBreast = open("StockageDonneesBreast.txt","w+")
		self.fileSkin = open("StockageDonneesSkin.txt","w+")
		
		
		######################################################################################
		#                                     CheckBoxs                                      #
		######################################################################################

		self.var_caseLung = IntVar()
		self.var_caseLung.set(1)
		caseLung = Checkbutton(self.fenetre, text="Enregistrer les données du poumon", variable=self.var_caseLung)
		caseLung.pack()
		#print "",var_caseLung.get()
		
		
		self.var_caseSkin= IntVar()
		self.var_caseSkin.set(1)
		caseSkin = Checkbutton(self.fenetre, text="Enregistrer les données de la peau", variable=self.var_caseSkin)
		caseSkin.pack()

		self.var_caseLiver = IntVar()
		self.var_caseLiver.set(1)
		caseLiver = Checkbutton(self.fenetre, text="Enregistrer les données du foie", variable=self.var_caseLiver)
		caseLiver.pack()
		
		self.var_caseBreast = IntVar()
		self.var_caseBreast.set(1)
		caseBreast = Checkbutton(self.fenetre, text="Enregistrer les données du sein", variable=self.var_caseBreast)
		caseBreast.pack()

		pBas2.add(caseLung)
		pBas2.add(caseSkin)
		pBas2.add(caseLiver)
		pBas2.add(caseBreast)
		

		
		
		self.pBas.pack()
	

	def run(self,org):
		global  t,dt,nbT,nbH,temps,valT,valH

		t=t+dt
		temps.append(t)
		
		nbT = org.status['T']
		nbH = org.status['H']
		
		valT.append(nbT)
		valH.append(nbH)
		if org.name=="Lung" and self.var_caseLung.get()==1:
			self.fileLung.write(str(t)+ "	" +str(nbT) + "	" +  str(nbH) + "\n")
		elif org.name=="Breast" and self.var_caseBreast.get()==1:
			self.fileBreast.write(str(t)+ "	" +str(nbT) + "	" +  str(nbH) + "\n")
		elif org.name=="Skin" and self.var_caseSkin.get()==1:
			self.fileSkin.write(str(t)+ "	" +str(nbT) + "	" +  str(nbH) + "\n")
		elif org.name=="Liver" and self.var_caseLiver.get()==1:
			self.fileLiver.write(str(t)+ "	" +str(nbT) + "	" +  str(nbH) + "\n")

	def gnuplotFunction(self):
		print "Je vais dans la fonction gnuplot"
		
		print self.fileLung.readline()

		print self.fileBreast.readline()
		
		print self.fileSkin.readline()
		print self.fileLiver.readline()

		fichier1=open("commandeGNULung.txt","w") 
		comm2="plot 'StockageDonneesLung.txt' using 1:2 with lines title 'Evolution du nombre de cellule tumorales' \n" 
		#comm3="replot 'StockageDonneesLung.txt' using 1:3 with lines title 'Evolution du nombre de cellule saines' \n" 
		fichier1.write(comm2) 
		fichier1.write(comm3) 
		fichier1.close() 
		os.system("gnuplot "+"commandeGNULung.txt --persist")
		

		fichier2=open("commandeGNUBreast.txt","w") 
		comm2="plot 'StockageDonneesBreast.txt' using 1:2 with lines title 'Evolution du nombre de cellule tumorales' \n" 
		fichier2.write(comm2) 
		fichier2.close() 
		os.system("gnuplot "+"commandeGNUBreast.txt --persist")
		

		fichier3=open("commandeGNUSkin.txt","w") 
		comm2="plot 'StockageDonneesSkin.txt' using 1:2 with lines title 'Evolution du nombre de cellule tumorales' \n" 
		fichier3.write(comm2) 
		fichier3.close() 
		os.system("gnuplot "+"commandeGNUSkin.txt --persist")
		

		fichier4=open("commandeLiver.txt","w") 
		comm2="plot 'StockageDonneesLiver.txt' using 1:2 with lines title 'Evolution du nombre de cellule tumorales' \n" 
		fichier4.write(comm2) 
		fichier4.close() 
		os.system("gnuplot "+"commandeLiver.txt --persist")
			
	def TracerCourbeLung(self):
		self.TraceCourbeLung = True
		
	def TracerCourbeBreast(self):
		self.TraceCourbeBreast = True
		
	def TracerCourbeLiver(self):
		self.TraceCourbeLiver = True
		
	def TracerCourbeSkin(self):
		self.TraceCourbeSkin = True

	def fonction(self,pn,pt,pi,v):
		f= intTest.fenetre2(pn,pt,pi,v)
		self.TraceCourbeLung =False
		self.TraceCourbeBreast =False
		self.TraceCourbeSkin =False
		self.TraceCourbeLiver =False
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
		self.gnuplotFunction()
		t=Toplevel()
		s=StringVar()
		s.set(message)
		death=Label(t, textvariable=s)
		death.pack()

		while self.reset == False :

			self.fenetre.update_idletasks()
			self.fenetre.update()

		self.Reset()

		#a faire : un reset quand on ferme la fenetre message
		
	def setSurgery(self):
		self.buttonSurgery=True
		
	def surgery(self,org): # Idee : mettre un nombre max et un temps entre les interventions? Sinon il suffit de faire plein d'interventions pour guerir la patiente
		p=0.90+random.random()*0.05 #calcul le pourcentage de tumeur qui sera enleve
		remove=p*org.status['T']
		org.status['T']-=remove
		org.status['H']+=remove
		self.buttonSurgery=False


	def Reset(self) :

		self.fenetre.destroy()
		os.system("python TACMP.py")
