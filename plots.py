# -*- coding: utf-8 -*-
import RSA
import miller_rabin
from gmpy2 import *
import gmpy2
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time
from random import randint

param = 1
previous = 0
def plotGraphMiller():
	fig   = plt.figure()
	ax1   = fig.add_subplot(1,1,1)
	plt.suptitle("Bytes VS Time")
	plt.xlabel('Bytes')
	plt.ylabel('NanoSeconds')
	xar   = []
	yar   = []
	def animate(i):
		global param
		global previous
		n = plotMillerTime(param)
		if n[1]>previous:
			previous = n[1]
			xar.append(n[1]/8)
			yar.append(n[0])
			print ("Time: %d"%n[0])
			print ("Bytes: %d"%int(n[1]/8))
			ax1.clear()
			plt.xlabel('Bytes')
			plt.ylabel('NanoSeconds')
			ax1.plot(xar, yar)
		param += 1
	ani = animation.FuncAnimation(fig, animate)
	plt.show()

def plotGraphMillerDigits():
	fig   = plt.figure()
	ax1   = fig.add_subplot(1,1,1)
	plt.suptitle("Digits VS Time")
	plt.xlabel('Digits')
	plt.ylabel('NanoSeconds')
	xar   = []
	yar   = []
	def animate(i):
		global param
		global previous
		n = plotMillerTime(param)
		if n[1]>previous:
			previous = n[1]
			xar.append(n[2])
			yar.append(n[0])
			print ("Time: %d"%n[0])
			print ("Digits: %d"%int(n[2]))
			ax1.clear()
			plt.xlabel('Digits')
			plt.ylabel('NanoSeconds')
			ax1.plot(xar, yar)
		param += 1
	ani = animation.FuncAnimation(fig, animate)
	plt.show()

def plotPrimeRange():
	r = primeRange(100)
	plt.plot(r[0], r[1])
	# plt.xticks(np.arange(min(r[0], max(r[0]), 1.0)))
	plt.ylabel('percent of primes')
	plt.xlabel('Number Range')
	plt.show()



# ______PLOT FUNCTIONS_______

def plotMillerTime(p):
	multiVar = 10000000000
	mills = int(round(time.time()*multiVar))
	n = (gmpy2.xmpz(RSA.getRandom())**gmpy2.xmpz(p))+(gmpy2.xmpz(RSA.getRandom())**gmpy2.xmpz(p)-1)
	while not miller_rabin.millerRabin(n, 2):
		n = (gmpy2.xmpz(RSA.getRandom())**gmpy2.xmpz(p))+(gmpy2.xmpz(RSA.getRandom())**gmpy2.xmpz(p)-1)
	mills = int(round(time.time()*multiVar)) - mills
	return (mills, bit_length(n), totalDigits(n))

def totalDigits(num): 
	i = 0
	while num>0:
		i += 1
		num /= 10
	return i

total_primes = []
nextP = 1
def nextPrime(p):
	power = 100
	global total_primes
	global nextP
	while nextP <= p:
		nextP = next_prime(nextP)
		total_primes.append(nextP)
	return len(total_primes)-1
	

def primeRange(j):
	x = 1
	range = []
	tot_primes = []
	while x <=j:
		range.append(x)
		tot_primes.append(float(nextPrime(x))/float(x))
		print ("%.10f in %d"%(float(nextPrime(x))/float(x), x))
		x += 1
	return (range, tot_primes)
# primeRange(10000)
