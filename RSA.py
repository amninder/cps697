import miller_rabin
import mersenne
from fabric.colors import *
import gmpy2
from gmpy2 import *
from datetime import datetime



def seed():
	return datetime.now().microsecond

def getRandomPrime():
	n = mersenne.retRandom(seed())
	if miller_rabin.millerRabin(n, 4):
		return n
	else:
		return getRandomPrime()

def getRandom():
	return mersenne.retRandom(seed())

def step2(p, q, r, s):
	_n      = mul(p,q)
	_m      = mul(r,s)
	_phi    = mul((p-1),(q-1))
	_lambda = mul((r-1),(s-1))
	return (_n, _m, _phi, _lambda)


"""
Derived from Pseudocode: http://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Iterative_method_2
"""
def extended_gcd(a, b):
	lastremainder, remainder = abs(a), abs(b)
	x, lastx, y, lasty = 0, 1, 1, 0
	while remainder:
		lastremainder, (quotient, remainder) = \
			remainder, divmod(lastremainder, remainder)
		x, lastx = lastx - quotient*x, x
		y, lasty = lasty - quotient*y, y
		
	return lastremainder, lastx * \
		(-1 if a<0 else 1), lasty * (-1 if b < 0 else 1)

def modinv(a, m):
	g, x, y = extended_gcd(a, m)
	if g != 1:
		raise ValueError
	return x%m

"""
Euclid's algorithm to find GCD: http://en.wikipedia.org/wiki/Euclidean_algorithm
"""
def GCD(a, b):
	while a!=b:
		if a>b:
			a -= b
		else:
			b -= a
	return a

def str2NumList(strn):
	"""Converts a string to a list of integers based on ASCII values"""
	return [ord(chars) for chars in strn]

def numList2String(l):
	"""Converts a list of integers to a string bsed on ASCII values"""
	return ''.join(map(chr, l))

def generateLargePrime(p):
	n = (gmpy2.xmpz(getRandom())**gmpy2.xmpz(p))+(gmpy2.xmpz(getRandom())**gmpy2.xmpz(p)-1)
	while not miller_rabin.millerRabin(n, 2):
		n = (gmpy2.xmpz(getRandom())**gmpy2.xmpz(p))+(gmpy2.xmpz(getRandom())**gmpy2.xmpz(p)-1)
	return n

def encrypt(_g, _s, _e, _n, _m):
	r = gmpy2.xmpz(1)
	g = gmpy2.xmpz(_g)
	s = gmpy2.xmpz(_s)
	e = gmpy2.xmpz(_e)
	n = gmpy2.xmpz(_n)
	m = gmpy2.xmpz(_m)

	b1 = f_mod(e, n)
	b1 = pow(g, pow(s, b1))
	b1 = mul(b1, f_mod(pow(r,m), pow(m,2)))
	return b1

def decrypt(_c, _lambda, _m, _d, _mu, _n):
	c    = gmpy2.xmpz(_c)
	lmda = gmpy2.xmpz(_lambda)
	m    = gmpy2.xmpz(_m)
	d    = gmpy2.xmpz(_d)
	mu   = gmpy2.xmpz(_mu)
	n    = gmpy2.xmpz(_n)
	b1   = f_mod(pow((f_mod(mul((((pow(c, lmda) \
		% (pow(m, 2))-1))/m), mu), m)),d), n)
	return b1

"""http://www.wojtekrj.net/2008/09/pythonalgorithms-fast-modular-exponentiation-script/"""
def modularExp(a, n, m):
	bits = []
	while n:
		bits.append(n%2)
		n /= 2
	solution = 1
	bits.reverse()
	for x in bits:
		solution = (solution*solution) % m
		if x:
			solution = (solution*a) % m
	return solution

def expo(u, m):
	q = m
	prod = 1
	current = u
	while q>0:
		if (q%2)==1:
			prod = current * prod
			q -= 1
			print prod
	current = current * current
	q = q/2
	return prod

# modInv 2
#
def extEuclideanAlg(a, b):
	if b==0:
		return 1, 0, a
	else:
		x, y, gcd = extEuclideanAlg(b, a%b)
		return y, x-y*(a//b), gcd

def modInvEuclid(a, m):
	x, y, gcd = extEuclideanAlg(a, m)
	if gcd==1:
		return x%m
	else:
		return None

# Second RSA
p   = 0
q   = 0
n   = 0
phi = 0
e   = 0
d   = 0
m   = 133
c   = 0
drc = 0

def selectPrime():
	global p
	global q
	global n
	global phi
	global e
	global d
	global m
	global c
	global drc
	p = getRandom()
	
	while not miller_rabin.millerRabin(p, 2):
		p = getRandom()
	q = getRandom()
	while not miller_rabin.millerRabin(q, 2):
		q = getRandom()
	n = mul(p, q)
	phi = (p-1) * (q-1)
	e = getRandom()
	while gcd(e, phi)!=1:
		e=getRandom()
	d = divm(1, e, phi)
	c = pow(m, e, n)
	drc = pow(c, d, n)


# selectPrime()
# print "p: %d"%p
# print "q: %d"%q
# print "n: %d"%n
# print "phi: %d"%phi
# print "e: %d"%e
# print "d: %d"%d
# print "message: %d"%m
# print "cipher: %d"%c
# print "decrypted: %d"%drc

			# Karatsuba multiplication #

_CUTOFF = 1536

def k_multiply(x, y):
	if x.bit_length()<= _CUTOFF or y.bit_length <= _CUTOFF:
		return x*y
	else:
		n 		= max(b.bit_length(), y.bit_length)
		half 	= (n+32) // mul(64, 32)
		mask 	= (1 << half) - 1
		xlow 	= x & mask
		ylow 	= y & mask
		xhigh 	= x >> half
		yhigh 	= y >> half

		a 		= k_multiply(xhigh, yhigh)
		b 		= k_multiply(xlow + xhigh, ylow + yhigh)
		c 		= k_multiply(xlow, ylow)
		d 		= b - a - c
		return (((a << half) + d) << half) + c
