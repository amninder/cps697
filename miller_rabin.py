from random import *
from gmpy2 import *

def millerRabin(n, k=3):
	if n<2:
		return False
	if n%2==0:
		return False

	s = 0
	d = n-1

	while d%2==0:
		s 	+=	1
		d 	>>=	1
	for i in range(k):
		rand 	= randint(2, n-2)
		x 		= powmod(rand, d, n)
		if x == 1 or x == n-1:
			continue
		for r in range(s):
			isPrime = True
			x = powmod(x,2,n)
			if x==1:
				return False
			if x==n-1:
				isPrime = False
				break
		if isPrime:
			return False
	return True