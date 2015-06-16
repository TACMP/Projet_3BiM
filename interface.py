# -*- coding: utf-8 -*

from Tkinter import*
import math
import time
import pylab      
import random
import os

import intTest



#from Numeric import *  
    

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

class frame:

	def __init__(self):

		self.fenetre = Tk()
		self.fenetre.title("The Amazing Cancer Modeling Project")
		self.fenetre.geometry("1400x1400")

		self.day = StringVar()
		self.day.set("Day 0")
		self.champ_label = Label(self.fenetre, textvariable=self.day)


		#Pour afficher le label dans la fenetre
		#pack permet de positionner la fenetre
		self.champ_label.pack()
			
		#Pour que la fenetre reste ouverte a la fin:
		self.see = True
		
		self.TraceCourbeLung =False
		self.TraceCourbeBreast =False
		self.TraceCourbeSkin =False
		self.TraceCourbeLiver =False


		self.surgery_used = False
		self.reset = False
		
		
		

		######################################################################################
		#                             Separation de la fenetre                               #
		######################################################################################
		panneau1 = PanedWindow(self.fenetre,orient=HORIZONTAL,height=750,width=1400)
		
		pHaut = PanedWindow(self.fenetre,orient=HORIZONTAL,height=750,width=800)
		pDroite = PanedWindow(self.fenetre,orient=VERTICAL,height=750,width=400)
		pDroite1= PanedWindow(pDroite, orient=VERTICAL,height=245,width=400)
		pDroite2= PanedWindow(pDroite, orient=HORIZONTAL,height=245,width=400)
		pDroite3= PanedWindow(pDroite, orient=VERTICAL,height=245,width=400)
		
		pDroite.add(pDroite1)
		pDroite.add(pDroite2)
		pDroite.add(pDroite3)
		
		boutonLung= Button(self.fenetre, text="Prédictions Poumon", command=self.TracerCourbeLung, height=3)

		
		boutonBreast= Button(self.fenetre, text="Prédictions Sein", command=self.TracerCourbeBreast, height=4)
		
		boutonLiver= Button(self.fenetre, text="Prédictions Foie", command=self.TracerCourbeLiver, height=3)

		boutonSkin= Button(self.fenetre, text="Prédictions Peau", command=self.TracerCourbeSkin, height=4)

		boutonReset = Button(self.fenetre, text="RESET", command=self.Reset)

		pDroite1.add(boutonLung)
		pDroite1.add(boutonBreast)
		pDroite1.add(boutonLiver)
		pDroite1.add(boutonSkin)	
		
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
		
		self.txt=StringVar()
		self.txt.set("Poumon")
		self.Poumon = Label(self.fenetre, textvariable=self.txt)
		
		self.txt2=StringVar()
		self.txt2.set("Sein")
		self.Sein = Label(self.fenetre, textvariable=self.txt2)
		
		self.txt3=StringVar()
		self.txt3.set("Foie")
		self.Foie = Label(self.fenetre, textvariable=self.txt3)
		
		self.txt4=StringVar()
		self.txt4.set("Peau")
		self.Peau = Label(self.fenetre, textvariable=self.txt4)
		
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
		
		
		
		self.Slider = Scale(self.fenetre, from_ = 0, to = 20, resolution = 0.2)
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

		

		
		
		#Bouton pour intervention chirurgicale
		self.buttonSurgery=False
		bSurgery=Button(self.fenetre,text="Intervention \n chirurgicale",command=self.setSurgery, height=1, width=28)
		pDroite2.add(bSurgery)
		pDroite2.add(boutonReset)
		
		self.fileLung = open("StockageDonneesLung.txt","w+")
		self.fileLiver = open("StockageDonneesLiver.txt","w+")
		self.fileBreast = open("StockageDonneesBreast.txt","w+")
		self.fileSkin = open("StockageDonneesSkin.txt","w+")
		
		
		######################################################################################
		#                                     CheckBoxs                                      #
		######################################################################################

		self.var_caseLung = IntVar()
		self.var_caseLung.set(1)
		caseLung = Checkbutton(self.fenetre, text="Enregistrement des données du poumon", variable=self.var_caseLung, height=4)
		
		
		self.var_caseSkin= IntVar()
		self.var_caseSkin.set(1)
		caseSkin = Checkbutton(self.fenetre, text="Enregistrement des données de la peau", variable=self.var_caseSkin, height=4)


		self.var_caseLiver = IntVar()
		self.var_caseLiver.set(1)
		caseLiver = Checkbutton(self.fenetre, text="Enregistrement des données du foie", variable=self.var_caseLiver, height=4)

		
		self.var_caseBreast = IntVar()
		self.var_caseBreast.set(1)

		caseBreast = Checkbutton(self.fenetre, text="Enregistrement des données du sein", variable=self.var_caseBreast, height=4)


		pDroite3.add(caseLung)
		pDroite3.add(caseSkin)
		pDroite3.add(caseLiver)
		pDroite3.add(caseBreast)
		

		
		
		self.pBas.pack()
	

	def run(self,org,date):

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

		self.day.set("Day " + str(date))



	def gnuplotFunction(self):
		
		#print self.fileLung.readline()
		#print self.fileBreast.readline()
		#print self.fileSkin.readline()
		#print self.fileLiver.readline()

		fichier1=open("commandeGNULung.txt","w") 
		comm2="plot 'StockageDonneesLung.txt' using 1:2 with lines title 'Evolution du nombre de cellules tumorales pour le poumon'\n" 
		
		fichier1.write(comm2) 
		fichier1.close() 
		os.system("gnuplot "+"commandeGNULung.txt --persist")
		

		fichier2=open("commandeGNUBreast.txt","w") 
		comm2="plot 'StockageDonneesBreast.txt' using 1:2 with lines title 'Evolution du nombre de cellules tumorales pour le sein' \n" 
		fichier2.write(comm2) 
		fichier2.close() 
		os.system("gnuplot "+"commandeGNUBreast.txt --persist")
		

		fichier3=open("commandeGNUSkin.txt","w") 
		comm2="plot 'StockageDonneesSkin.txt' using 1:2 with lines title 'Evolution du nombre de cellules tumorales pour la peau' \n" 
		fichier3.write(comm2) 
		fichier3.close() 
		os.system("gnuplot "+"commandeGNUSkin.txt --persist")
		

		fichier4=open("commandeLiver.txt","w") 
		comm2="plot 'StockageDonneesLiver.txt' using 1:2 with lines title 'Evolution du nombre de cellules tumorales pour le foie' \n" 
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


	def draw_organ_init(self,org) :

		cs = 5
		x_gap = 6
		y_gap = 6
		if org.name=='Lung':
			for i in xrange(len(org.cells)):
				x=i%int(math.sqrt(len(org.cells)))
				y=i/int(math.sqrt(len(org.cells)))
				if org.cells[i]=='H':
					self.Canvas1.create_oval(cs*x+x_gap,cs*y+y_gap,cs*x+x_gap+1,cs*y+y_gap+1,outline='green')
				elif org.cells[i]=='T':
					self.Canvas1.create_oval(cs*x+x_gap,cs*y+y_gap,cs*x+x_gap+1,cs*y+y_gap+1,outline='red')

		elif org.name=='Liver':
			for i in xrange(len(org.cells)):
				x=i%int(math.sqrt(len(org.cells)))
				y=i/int(math.sqrt(len(org.cells)))
				if org.cells[i]=='H':
					self.Canvas2.create_oval(cs*x+x_gap,cs*y+y_gap,cs*x+x_gap+1,cs*y+y_gap+1,outline='green')
				elif org.cells[i]=='T':
					self.Canvas2.create_oval(cs*x+x_gap,cs*y+y_gap,cs*x+x_gap+1,cs*y+y_gap+1,outline='red')			

		elif org.name=='Breast':
			for i in xrange(len(org.cells)):
				x=i%int(math.sqrt(len(org.cells)))
				y=i/int(math.sqrt(len(org.cells)))
				if org.cells[i]=='H':
					self.Canvas3.create_oval(cs*x+x_gap,cs*y+y_gap,cs*x+x_gap+1,cs*y+y_gap+1,outline='green')
				elif org.cells[i]=='T':
					self.Canvas3.create_oval(cs*x+x_gap,cs*y+y_gap,cs*x+x_gap+1,cs*y+y_gap+1,outline='red')
			
		elif org.name=='Skin':
			for i in xrange(len(org.cells)):
				x=i%int(math.sqrt(len(org.cells)))
				y=i/int(math.sqrt(len(org.cells)))
				if org.cells[i]=='H':
					self.Canvas4.create_oval(cs*x+x_gap,cs*y+y_gap,cs*x+x_gap+1,cs*y+y_gap+1,outline='green')
				elif org.cells[i]=='T':
					self.Canvas4.create_oval(cs*x+x_gap,cs*y+y_gap,cs*x+x_gap+1,cs*y+y_gap+1,outline='red')

			
	def draw_organ(self,org) :
		
		cs = 5
		x_gap = 6
		y_gap = 6
		if org.name=='Lung':
			for i in org.cells_switched :
				x=i%int(math.sqrt(len(org.cells)))
				y=i/int(math.sqrt(len(org.cells)))
				if org.cells[i]=='H':
						self.Canvas1.create_oval(cs*x+x_gap,cs*y+y_gap,cs*x+x_gap+1,cs*y+y_gap+1,outline='green')
				elif org.cells[i]=='T':
						self.Canvas1.create_oval(cs*x+x_gap,cs*y+y_gap,cs*x+x_gap+1,cs*y+y_gap+1,outline='red')

			self.txt.set(" ".join(["Poumon \t Immun. : ",str("%.3f" % org.status['I']), "\t Medic : ",str("%.3f" % org.status['U'])]))


		elif org.name=='Liver':
			for i in org.cells_switched :
				x=i%int(math.sqrt(len(org.cells)))
				y=i/int(math.sqrt(len(org.cells)))
				if org.cells[i]=='H':
						self.Canvas2.create_oval(cs*x+x_gap,cs*y+y_gap,cs*x+x_gap+1,cs*y+y_gap+1,outline='green')
				elif org.cells[i]=='T':
						self.Canvas2.create_oval(cs*x+x_gap,cs*y+y_gap,cs*x+x_gap+1,cs*y+y_gap+1,outline='red')

			self.txt3.set(" ".join(["Foie \t Immun. : ",str("%.3f" % org.status['I']), "\t Medic : ",str("%.3f" % org.status['U'])]))


		elif org.name=='Breast':
			for i in org.cells_switched :
				x=i%int(math.sqrt(len(org.cells)))
				y=i/int(math.sqrt(len(org.cells)))
				if org.cells[i]=='H':
						self.Canvas3.create_oval(cs*x+x_gap,cs*y+y_gap,cs*x+x_gap+1,cs*y+y_gap+1,outline='green')
				elif org.cells[i]=='T':
						self.Canvas3.create_oval(cs*x+x_gap,cs*y+y_gap,cs*x+x_gap+1,cs*y+y_gap+1,outline='red')

			self.txt2.set(" ".join(["Sein \t Immun. : ",str("%.3f" % org.status['I']), "\t Medic : ",str("%.3f" % org.status['U'])]))
			

		elif org.name=='Skin':
			for i in org.cells_switched :
				x=i%int(math.sqrt(len(org.cells)))
				y=i/int(math.sqrt(len(org.cells)))
				if org.cells[i]=='H':
						self.Canvas4.create_oval(cs*x+x_gap,cs*y+y_gap,cs*x+x_gap+1,cs*y+y_gap+1,outline='green')
				elif org.cells[i]=='T':
						self.Canvas4.create_oval(cs*x+x_gap,cs*y+y_gap,cs*x+x_gap+1,cs*y+y_gap+1,outline='red')

			self.txt4.set(" ".join(["Peau \t Immun. : ",str("%.3f" % org.status['I']), "\t Medic : ",str("%.3f" % org.status['U'])]))


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

		
	def surgery(self,org):
		p=0.60+random.random()*0.35 #calcule le pourcentage de tumeur qui sera enleve
		remove=p*org.status['T']
		org.status['T']-=remove
		org.status['H']+=remove
		self.buttonSurgery = False
		self.surgery_used = True


	def Reset(self) :

		self.fenetre.destroy()
		os.system("python TACMP.py")
