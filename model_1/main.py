import numpy as np
import matplotlib.pyplot as plt
from time import sleep
import random

### Clases
class Individual:
	def __init__(self,box):
		len_x = box[0] - box[2]
		len_y = box[1] - box[3]
		self.r = 1.5 # Size of the particle
		self.x = np.random.rand()*len_x - box[0]
		self.y = np.random.rand()*len_y - box[1]
		self.vx = np.random.rand()*10 - 5
		self.vy = np.random.rand()*10 - 5
		self.alpha = np.arctan2(self.vy,self.vx) # *180/np.pi
		self.m = 1

		self.px = self.m*self.vx
		self.py = self.m*self.vy
		self.kin = 0.5*self.m*(self.vx*self.vx+self.vy*self.vy)

		self.infected = 0
		self.inmune = 0
		self.time_infected = 0
		self.recovery_time = np.abs(np.random.randn() + 1)*14



	def update_speed(self,theta, rand=0):
		if rand == 0:
			# print(self.vx)
			gamma = theta - self.alpha
			self.alpha = theta + gamma
			v = (self.vx*self.vx+self.vy*self.vy)**0.5
			self.vx = v*np.cos(self.alpha)
			self.vy = v*np.sin(self.alpha)
			# print(self.vx)
		elif rand == 1:
			self.alpha = np.random.rand()*(np.pi)-np.pi/2
			v = np.random.rand()*10 - 5
			self.vx = v*np.cos(self.alpha)
			self.vy = v*np.sin(self.alpha)

	def update_location(self,dt):
		self.x = self.x + self.vx*dt
		self.y = self.y + self.vy*dt
		if self.infected == 1:
			self.time_infected += dt
		if self.time_infected >= self.recovery_time:
			self.infected = 0
			self.inmune = 1


	def update(self,dt,theta=None):
		if theta != None:
			update_speed(theta)
		update_location(dt)


class Population:
	def __init__(self,n):
		self.n = n
		self.individuals = [Individual(box) for i in range(n) ]
		self.x = np.array([self.individuals[i].x for i in range(n) ])
		self.y = np.array([self.individuals[i].y for i in range(n) ])
		self.infection = [self.individuals[i].infected for i in range(n) ]
		self.color = np.zeros((n,3))
		for i in range(n):
			if self.infection[i] == 1:
				self.color[i,: ] = np.array([1, 0.0 , 0. ])

	def update(self):
		n = self.n
		self.x = np.array([self.individuals[i].x for i in range(n) ])
		self.y = np.array([self.individuals[i].y for i in range(n) ])
		self.infection = [self.individuals[i].infected for i in range(n) ]
		for i in range(n):
			if self.infection[i] == 1:
				self.color[i,: ] = np.array([1, 0.0 , 0. ])
			else:
				self.color[i,: ] = np.array([0, 0.0 , 0. ])
	# def append(self)


# Functions

def calculate_distance(ind):
	n = len(ind)
	d = [ ]
	pairs = [  [ (j,i) for i in range(j+1,n) ] for j in range(0,n) ]
	for p in pairs:
		for i,j in p:
			d.append(( i, j, ((ind[i].x-ind[j].x)**2 + (ind[i].y-ind[j].y)**2)**0.5 ) )
	return d

def collision_particle(indi,indj,rand=0):
	bisec = (indi.alpha + indj.alpha)/2
	indi.update_speed(bisec,rand)
	indj.update_speed(bisec,rand)
	contagion(indi,indj)

def contagion(indi,indj):
	check = 1
	if indi.infected > 0 and check == 1:
		if indj.inmune == 0 : # random.uniform(0, 1) > 0.2 and :
			indj.infected = 1
			check = 0
	if indj.infected > 0 and check == 1 :
		if indi.inmune == 0 : # random.uniform(0, 1) > 0.2:
			indi.infected = 1

def collision_wall(ind,box):
	if ((ind.x + ind.r) >= (box[0])*0.99) or ((ind.x + ind.r) <= (box[2])*0.99):
		ind.update_speed(np.pi/2,rand=0)
	if ((ind.y + ind.r) >= (box[1])*0.99) or ((ind.y + ind.r) <= (box[3])*0.99):
		ind.update_speed(np.pi,rand=0)


# --------------- # --------------- # --------------- # --------------- # --------------- #

# --------------- # --------------- # --------------- # --------------- # --------------- #
plot_simulation = 0
n = 500

dt = 0.5
t = 0
total_time = 100

box = [100,100,-100,-100]

pop = Population(n)

pop.individuals[5].infected = 1
pop.individuals[1].infected = 1

#print(pop.individuals[5].recovery_time)
#print(pop.individuals[1].recovery_time)
pop.update()

if plot_simulation==1:
	plt.show()
	axes = plt.gca()
	axes.set_xlim(box[2], box[0])
	axes.set_ylim(box[3], box[1])
	#dot, = axes.plot(pop.x, pop.y,'o', markersize=2,markeredgecolor='black',markerfacecolor='blue')
	dot = axes.scatter(pop.x, pop.y, s=6, c = pop.color)


ncases = []
while t < total_time:

	dist = calculate_distance(pop.individuals)

	# Distance
	for i,j,dij in dist:
		indi = pop.individuals[i]
		indj = pop.individuals[j]
		if dij <= (indi.r+indj.r):
			# print('cillisions')
			collision_particle(indi,indj,rand=0)
		elif dij <= 5:
			contagion(indi,indj)


	for ind in pop.individuals:
		ind.update_location(dt)
		collision_wall(ind,box)

	t += dt


	pop.update()

	# Ensemble variables
	ncases.append(np.sum(pop.infection))

	if plot_simulation==1:
		dot = axes.scatter(pop.x, pop.y, s=6, c = pop.color)
		plt.title(t)
		axes.set_xlim(box[2], box[0])
		axes.set_ylim(box[3], box[1])
		plt.draw()
		plt.pause(1e-10)
		axes.cla()
	#sleep(0.0001)

	if 1:
		print(t/total_time*100)



if plot_simulation==1:
	plt.show()
	plt.close()

plt.plot(ncases)
plt.show()
