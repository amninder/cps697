"""
####################################################################

	written for Mersenne twister BY M. Matsumoto and T. Nishimura 
	for the values of MT19937 from table II  of section 8.

###################################################################

AND
  |	0 	1
--|-------
0 |	0 	0
1 |	0 	1

OR
  |	0 	1
--|-------
0 |	0 	1
1 |	1 	1

XOR
  |	0 	1
--|-------
0 |	0 	1
1 |	1 	0


from:
	Table II: Parameters and k-distribution of Mersenne Twisters for MT19937
"""
_w = 32
_n = 624
_m = 397
_r = 31
_a = 0x9908b0df # a = 2567483615
_u = 11
_s = 7
_b = 0x9d2c5680 # b = 2636928640
_t = 15
_c = 0xefc60000 # c = 4022730752
_l = 18

MT 		= [1 for i in xrange(_n)]
index 	= 0

# last 32 bits
bitmask_upper = (2**_w)-1

# last 31 bit
bitmask_lower = (2**_r)

# to get last 31 bits
get_last_31_bit = (2**_r)-1

def initialize_generator(seed):
	MT[0] = seed
	for i in xrange(1, 624):
		MT[i] = ((1812433253 *MT[i-1])^((MT[i-1]>>30) +1)) \
		& bitmask_upper

def generate_numbers():
	for i in xrange(624):
		y = (MT[i] & bitmask_lower) + (MT[(i+1) % 624] \
			& get_last_31_bit)
		MT[i] = MT[(i+_m) % 624]^(y>>1)
		if y%2 !=0:
			MT[i] ^= _a

def extract_number():
	global index
	global MT
	if index==0:
		generate_numbers()
	y  = MT[index]
	y ^= y>>_u
	y ^= (y<<_s) & _b 	# 2636928640 is b and 7 is s
	y ^= (y<<_t) & _c 	# 4022730752 is c and 15 is t
	y ^= y >> _l 				# 18 is l

	index = (index+1) % 624 # step 5 of the algorithm
	return y

def retRandom(seed):
	initialize_generator(seed)
	return extract_number()
