# -*- coding: utf-8 -*

import Tkinter
import profile
import math
import random
import time
import interface

#random.seed(255)

# -__-__-__-__-__-__-__-  Glossary  -__-__-__-__-__-__-__- #

# State of cells :
# 'H' : healthy
# 'T' : tumor
# 'Q' : quiescent
# 'D' : dead
# 'I' : immune system cell

# 10 iterations of time = 1 day

# -__-__-__-__-__-__-__-__-__-_-_-__-__-__-__-__-__-__-__- #

pillis_parameters = {'a1':0.2,'a2':0.3,'a3':0.1,'b1':1,'b2':1,'c1':1,'c2':0.5,'c3':1,'c4':1,'d1':0.2,'d2':1,'r1':1.5,'r2':1,'s':0.33,'alpha':0.3,'rho':0.01,'v':0}
default_parameters = {'a1':0.2,'a2':0.3,'a3':0.1,'b1':1,'b2':1,'c1':1,'c2':0.4,'c3':1,'c4':1,'d1':0.2,'d2':1,'r1':1.6,'r2':1,'s':0.33,'alpha':0.3,'rho':0.2,'v':0}

simul_step = 0.01
simul_length = 10000
simul_time = 0


#          |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||          #


class Woman :

	def __init__ (self) :

		self.alive = True                          # becomes False and stops the program if woman dies from cancer (too many tumor cells in one organ)
		self.healthy = False  						# becomes True if all tumor cells are removed
		self.body = {'Breast' : Organ('Breast',65,default_parameters), 'Liver' : Organ('Liver',65,default_parameters), 'Lung' : Organ('Lung',65,default_parameters), 'Skin' : Organ('Skin',65,default_parameters)}      # dictionary of organs

		# -__-__-__-__-   Probabilities of tumor apparition / metastasis departure (from the concerned site) / metastasis arrival   -__-__-__-__- #
		self.tumor_probs = {'Breast' : 0.3, 'Liver' : 0.15, 'Lung' : 0.45, 'Skin' : 0.1}
		self.mts_appear_probs = {'Breast' : 0.001, 'Liver' : 0.0001, 'Lung' : 0.0004, 'Skin' : 0.002}
		self.mts_transfer_probs = {'Breast_Breast' : 0.05, 'Breast_Liver' : 0.6, 'Breast_Lung' : 0.3, 'Breast_Skin' : 0.05, 'Liver_Breast' : 0.05, 'Liver_Liver' : 0.4, 'Liver_Lung' : 0.45, 'Liver_Skin' : 0.1, 'Lung_Breast' : 0.1, 'Lung_Liver' : 0.5, 'Lung_Lung' : 0.25, 'Lung_Skin' : 0.15, 'Skin_Breast' : 0.05, 'Skin_Liver' : 0.4, 'Skin_Lung' : 0.35, 'Skin_Skin' : 0.2}

		self.initiate_tumor()						# creating primary tumor

		self.I = interface.frame()

		for org in (self.body).values() :
			self.I.draw_organ(org.name,org.cells,org)



	# -__-__-__-__-   Only called by __init__, this method chooses the first affected organ, and then calls a method to effectively create the initial tumor   -__-__-__-__- #
	def initiate_tumor (self) :

		doomed_organ = random.random()

		if doomed_organ < self.tumor_probs['Breast'] :
			self.body['Breast'].create_tumor()

		elif doomed_organ < self.tumor_probs['Breast'] + self.tumor_probs['Liver'] :
			self.body['Liver'].create_tumor()

		elif doomed_organ < self.tumor_probs['Breast'] + self.tumor_probs['Liver'] + self.tumor_probs['Lung'] :
			self.body['Lung'].create_tumor()

		else :
			self.body['Skin'].create_tumor()


	# -__-__-   Called whenever a "Woman" is printed, returns the proportion of tumor cells in each organ   -__-__-__-__- #
	def __repr__ (self) :

		result = []
		for name,org in (self.body).items() :
			result.append([name,org.status])
		return "\n".join([str(element) for element in result])


	#-__-__-__-__- Methode qui renvoie la tumeur primaire (ie l'organe le plus atteint) -__-__-__-__-
	def primary_tumor(self):
		pTumor=self.body['Breast']
		for org in (self.body).values() :
				if org.status['T']>pTumor.status['T']:
					pTumor=org
		return pTumor
		
	#-__-__-__-__- Methode qui verifie si la patiente est guerie -__-__-__-__-
	def isHealthy(self):
		Tumor=0
		for org in (self.body).values():
			Tumor+=org.status['T']
		if Tumor<0.002: #Je ne sais pas quel seuil mettre
			self.healthy=True

	# -__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__- #
	#												Main function, acting as a near-infinite loop											  	  #
	# -__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__- #

	def simul_RK (self) :
		check=0			#Permet de ne plus rentrer dans les if tout en maintenant la fenetre une fois que la patiente est guerie
		simul_time = 0
		while (self.I.see==True):
			if self.healthy==True and check==0:
				s = "".join(["Félicitations ! \n La patiente a guéri après ",str(simul_time/10)," jours."])
				print s
				check=1
				self.I.death_message(s)
			elif (self.alive == True) and (simul_time < simul_length) and check==0:					# simulation (currently) ends after a long time, or once the woman has died
				self.generate_metastasis(simul_time)
				for org in (self.body).values() :
					if org.status['T'] != 0:
						if org.status['H']<0.7 or org.status['I']<0.1:											# if there's too many tumor cells, we consider that the woman just died, thus the simulation ends
							self.alive = False
							if org.status['H']<0.7:
								s = "".join(["La patiente est morte au bout de ",str(simul_time/10)," jours\n d'un cancer généralisé."])
							elif org.status['I'] < 0.1:
								s = "".join(["La patiente est morte au bout de ",str(simul_time/10)," jours\n d'une maladie opportuniste\n (Système immunitaire trop faible)."])
							self.I.death_message(s)
							print s
							print org.status
						else :																# else we update her status, according to the model (one iteration)
							org.rK4(org.status['H'], org.status['T'], org.status['I'], org.status['U'], org.fh, org.ft, org.fi, org.fu, simul_step)
						org.update_layout(simul_time)	
						if org.name=='Lung':
							self.I.run2(org)											# we then update the layout (the grid drawn in the window) according to the values predicted by the equations
						self.I.draw_organ(org.name,org.cells,org)
						org.parameters['v'] = self.I.update_treatment()

				simul_time += 1
				
				if self.I.buttonSurgery==True:
					result=self.primary_tumor()
					self.I.surgery(result)
				
				self.isHealthy()
				if simul_time%50==0 :
					print simul_time
				#time.sleep(0.5)

	# -__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__- #
	#																																		  	  #
	# -__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__- #		



	# -__-__-__-__-   Called by the main loop, determines whether or not a metastasis appears, and where   -__-__-__-__- #
	def generate_metastasis (self, simul_time) :

		for name,org in (self.body).items() :

			if org.status['T'] != 0 :									# a metastasis can only come from an affected organ

				here_it_comes = random.random() * (1-1.5*org.status['T'])

				if here_it_comes < self.mts_appear_probs[name] :

					location = random.random()

					if location < self.mts_transfer_probs['_'.join([name,'Breast'])] :
						(self.body['Breast']).create_metastasis()							# if a metastasis appears, we call "create_metastasis()" which effectively creates it in the concerned organ
						print simul_time, name, '-> Breast'
					elif location < self.mts_transfer_probs['_'.join([name,'Breast'])] + self.mts_transfer_probs['_'.join([name,'Liver'])] :
						(self.body['Liver']).create_metastasis()
						print simul_time, name, '-> Liver'
					elif location < self.mts_transfer_probs['_'.join([name,'Breast'])] + self.mts_transfer_probs['_'.join([name,'Liver'])] + self.mts_transfer_probs['_'.join([name,'Lung'])] :
						(self.body['Lung']).create_metastasis()
						print simul_time, name, '-> Lung'
					else :
						(self.body['Skin']).create_metastasis()
						print simul_time, name, '-> Skin'



#          |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||          #



class Organ :

	def __init__ (self, x_name, x_size, x_parameters) :

		self.name = x_name

		self.size = x_size													# size of an organ = length of a side of the grid (thus, an organ has size**2 cells)					

		self.cells = []														# organ viewed as a 2D-grid of cells (coded as a long list of strings)
		
		for j in xrange(0,self.size**2,1) :
			(self.cells).append('H')										# at first, all cells are halthy

		# alternative way using a list of lists
		#for j in xrange(0,self.size,1) :
			#(self.cells).append(['H' for k in xrange (0,self.size,1)])     # at first, all cells are healthy

		self.status = {'H' : 1, 'T' : 0, 'Q' : 0, 'I' : 0.1	, 'U' : 0}       # status of the organ at any given simul_time (with proportion (0<p<1) of each type of cell)

		# parameters of the model, specific to each organ
		self.parameters = x_parameters



	# -__-__-__-__-   Method creating the initial tumor   -__-__-__-__-
	def create_tumor (self) :

		# -__-__- Randomized initial size -__-__-
		self.status['T'] = 0.001 + random.random()/50 						 # number of initial tumor cells, normalized
		self.status['H'] = 1 - self.status['T']

		# print int(self.status['T'] * self.size**2)                         # displays the number of initial tumor cells

		if self.size%2 == 0 :												 # finds the center (or a nearby cell) of the grid of cells forming the organ
			center = self.size**2/2 + self.size/2
		else :
			center = int(self.size**2/2)

		self.create_tumor_grid(center, int(self.status['T'] * self.size**2))     # "create_tumor_grid" effectively creates the initial tumor on the grid of cells, for it to appear once the grid is drawn
		#print self.cells



	# -__-__-__-__-   Method creating a metastasis at a given organ  -__-__-__-__-
	def create_metastasis (self) :

		metastasis_count = 0.001 + random.random()/50
		# print metastasis_count
		self.status['T'] += metastasis_count
		self.status['H'] -= metastasis_count

		self.cells[int(self.size**2 * (0.1+4*random.random()/5))] = 'T'


		# unfinished part, about adding the metastasis to the grid

		# x_location = int(random.random() * self.size)
		# y_location = int(random.random() * self.size)
		# location = x_location + self.size * y_location
		# mts_size = int(metastasis_count * self.size**2)

		# while self.cells[location] == 'T' :

		# 	x_location = int(random.random() * self.size)
		# 	y_location = int(random.random() * self.size)
			
		# #self.cells[x_location + self.size*y_location] = 'T'

		# print mts_size

		# #self.create_tumor_grid(50, mts_size)



	# -__-__-__-__-__-__-__-__-__-   Methods dealing with the grid which is being drawn   -__-__-__-__-__-__-__-__-__- #

	# -__-__-__-__-   Method adding a tumor (primary or metastasis) to an organ, with its center (near) at the given location, with a given size   -__-__-__-__-
	def create_tumor_grid (self, location, size_in_cells) :

		cells_added = 0
		square_length = int(math.sqrt(size_in_cells))      # as tumor cells will create a square/rectangular shape, this is the length of a side
		print square_length, size_in_cells
		x_shift = 0
		y_shift = 0

		# -__-__-   Tumor is created by forming rows of tumor cells around the center location, until the required number of cells have been added   -__-__-
		while cells_added < size_in_cells :

			# print location-int(square_length/2)-self.size*int(square_length/2) + x_shift + y_shift*self.size            # un-comment this to know where the tumor is created
			self.cells[location-int(square_length/2)-self.size*int(square_length/2) + x_shift + y_shift*self.size] = 'T'
			x_shift += 1
			cells_added += 1

			if x_shift >= square_length :
				x_shift = 0
				y_shift += 1

	
	# -__-__-__-__-   Method updating the grid to reflect the real status of the organ   -__-__-__-__-
	def update_layout (self, simul_time) :
	
	
		new_tumor_cells = int(self.status['T'] * self.size**2) - (self.cells).count('T')  # evaluating the number of tumor cells to add or remove

		if new_tumor_cells > 0 :														  # if we need to add tumor cells :

			#print new_tumor_cells

			possible_locations = []															# we search all possible locations of expansion (i.e. healthy cells close to a tumor cell)

			for position in xrange(0,len(self.cells),1) :

				if self.cells[position] == 'T' :											# meaning that for each tumor cell, we memorize the healthy neighbouring cells, while being sure not to look outside of the grid

					if position % self.size != 0 :											# healthy cells close to several tumor cells are counted several simul_times (which seems legit)
						if self.cells[position - 1] == 'H' :
							possible_locations.append(position - 1)

					if (position+1) % self.size != 0 :
						if self.cells[position + 1] == 'H' :
							possible_locations.append(position + 1)

					if position - self.size >= 0 :
						if self.cells[position - self.size] == 'H' :
							possible_locations.append(position - self.size)

					if position + self.size < self.size**2 :
						if self.cells[position + self.size] == 'H' :
							possible_locations.append(position + self.size)

			#print possible_locations													 # un-comment this to check the locations found

			for t_cell in xrange(0,new_tumor_cells,1) :									 # we can then add the required tumor cells by choosing randomly among all the possible locations

				if possible_locations != [] :

					chosen_location = random.randint(0,len(possible_locations)-1)
					#print possible_locations[chosen_location]							 # un-comment to get the chosen position
					self.cells[possible_locations[chosen_location]] = 'T'
					del possible_locations[chosen_location]


		elif new_tumor_cells < 0 :														 # if we need to remove tumor cells :

			#print new_tumor_cells

			possible_locations = []

			for position in xrange(0,len(self.cells),1) :								 # same logic, but we remove a tumor cell on the outside of the tumor (i.e. with at least 1 neighbouring healthy cell)

				if self.cells[position] == 'T' :											

					if position % self.size != 0 :											
						if self.cells[position - 1] == 'H' :
							possible_locations.append(position)

					if (position+1) % self.size != 0 :
						if self.cells[position + 1] == 'H' :
							possible_locations.append(position)

					if position - self.size >= 0 :
						if self.cells[position - self.size] == 'H' :
							possible_locations.append(position)

					if position + self.size < self.size**2 :
						if self.cells[position + self.size] == 'H' :
							possible_locations.append(position)


			for t_cell in xrange(new_tumor_cells,0,1) :

				if possible_locations != [] :

					chosen_location = random.randint(0,len(possible_locations)-1)
					self.cells[possible_locations[chosen_location]] = 'H'
					del possible_locations[chosen_location]

				else :
					print simul_time, new_tumor_cells
					#print simul_time, new_tumor_cells
					#print position
					#print self.cells
					





	# -__-__-__-__-__-__-__-__-__-__-__-__-  Model and numeric simulation using RK4  -__-__-__-__-__-__-__-__-__-__-__-__- #

	def fh(self, h, t, i, u) :

		return self.parameters['r2'] * h * (1-self.parameters['b2']*h)  -  self.parameters['c4']*t*h - self.parameters['a3'] * (1-math.exp(-u)) * h

	def ft(self, h, t, i, u) :

		return self.parameters['r1'] * t * (1-self.parameters['b1']*t)  -  self.parameters['c2']*i*t - self.parameters['c3']*t*h - self.parameters['a2'] * (1-math.exp(-u)) * t

	def fi(self, h, t, i, u) :

		return self.parameters['s'] + self.parameters['rho'] * (i*t)/float(self.parameters['alpha']+t) - self.parameters['c1']*i*t - self.parameters['d1']*i - self.parameters['a1'] * (1-math.exp(-u)) * i

	def fu(self, h, t, i, u) :

		return self.parameters['v'] - self.parameters['d2']*u

	def rK4(self, h, t, i, u, fh, ft, fi, fu, simul_step):
		h1 = self.fh(h, t, i, u)*simul_step
		t1 = self.ft(h, t, i, u)*simul_step
		i1 = self.fi(h, t, i, u)*simul_step
		u1 = self.fu(h, t, i, u)*simul_step
		hk = h + h1*0.5
		tk = t + t1*0.5
		ik = i + i1*0.5
		uk = u + u1*0.5
		h2 = self.fh(hk, tk, ik, uk)*simul_step
		t2 = self.ft(hk, tk, ik, uk)*simul_step
		i2 = self.fi(hk, tk, ik, uk)*simul_step
		u2 = self.fu(hk, tk, ik, uk)*simul_step
		hk = h + h2*0.5
		tk = t + t2*0.5
		ik = i + i2*0.5
		uk = u + u2*0.5
		h3 = self.fh(hk, tk, ik, uk)*simul_step
		t3 = self.ft(hk, tk, ik, uk)*simul_step
		i3 = self.fi(hk, tk, ik, uk)*simul_step
		u3 = self.fu(hk, tk, ik, uk)*simul_step
		hk = h + h3
		tk = t + t3
		ik = i + i3
		uk = u + u3
		h4 = self.fh(hk, tk, ik, uk)*simul_step
		t4 = self.ft(hk, tk, ik, uk)*simul_step	
		i4 = self.fi(hk, tk, ik, uk)*simul_step
		u4 = self.fu(hk, tk, ik, uk)*simul_step
		h = h + (h1 + 2*(h2 + h3) + h4)/6
		t = t + (t1 + 2*(t2 + t3) + t4)/6
		i = i + (i1 + 2*(i2 + i3) + i4)/6
		u = u + (u1 + 2*(u2 + u3) + u4)/6
		#print h, t, i, u
		self.status['H'] = h
		self.status['T'] = t
		self.status['I'] = i
		self.status['U'] = u

	# -__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-    -__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__-__- #


	# --------------------------------------------  Simulation with Euler  --------------------------------------------- #
	# def simul_Euler (self) :

	# 	dh = 0
	# 	dt = 0
	# 	di = 0
	# 	h = 0.8
	# 	t = 0.2
	# 	i = 0.1
	# 	print "pouet"
	# 	for j in xrange(0, simul_length, 1) :
	# 		dh = self.parameters['r2'] * h * (1-self.parameters['b2']*h)  -  self.parameters['c4']*t*h
	# 		dt = self.parameters['r1'] * t * (1-self.parameters['b1']*t)  -  self.parameters['c2']*i*t - self.parameters['c3']*t*h
	# 		di = self.parameters['s'] + self.parameters['rho'] * (i*t)/float(self.parameters['alpha']+t) - self.parameters['c1']*i*t - self.parameters['d1']*i
	# 		h += simul_step * dh
	# 		t += simul_step * dt
	# 		i += simul_step * di
	# 		print h,t,i
	# ------------------------------------------------------------------------------------------------------------------- #


#          |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||          #

	def Test():
		print "coucou coucou"

Poor_girl = Woman()
print Poor_girl
Poor_girl.simul_RK()
print Poor_girl
