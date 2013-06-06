import numpy
import math
import operator

# Methods common to both the transmitter and receiver.
def hamming(s1,s2):
    # Given two binary vectors s1 and s2 (possibly of different 
    # lengths), first truncate the longer vector (to equalize 
    # the vector lengths) and then find the hamming distance
    # between the two. Also compute the bit error rate  .
    # BER = (# bits in error)/(# total bits )
    diffs = 0
    for int1, int2 in zip(s1,s2):
    	if (int1 != int2):
    		diffs += 1

    hamming_d = diffs
    ber = diffs*1.0/len(s1)
    return hamming_d, ber
