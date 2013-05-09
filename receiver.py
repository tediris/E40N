import sys
import math
import numpy
import scipy.cluster.vq
import common_txrx as common
from numpy import linalg as LA
import receiver_mil3

class Receiver:
    def __init__(self, carrier_freq, samplerate, spb):
        '''
        The physical-layer receive function, which processes the
        received samples by detecting the preamble and then
        demodulating the samples from the start of the preamble 
        sequence. Returns the sequence of received bits (after
        demapping)
        '''
        self.fc = carrier_freq
        self.samplerate = samplerate
        self.spb = spb 
        print 'Receiver: '

    def detect_threshold(self, demod_samples):
        '''
        Calls the detect_threshold function in another module.
        No need to touch this.
        ''' 
        return receiver_mil3.detect_threshold(demod_samples)
 
    def detect_preamble(self, demod_samples, thresh, one):
        '''
        Find the sample corresp. to the first reliable bit "1"; this step 
        is crucial to a proper and correct synchronization w/ the xmitter.
        '''

        '''
        First, find the first sample index where you detect energy based on the
        moving average method described in the milestone 2 description.
        '''
        # Fill in your implementation of the high-energy check procedure

        energy_offset = 0
        lower_bound = (one + thresh)/2
        print "one: " + str(one)
        print "thresh: " + str(thresh)
        while True:
            mean = numpy.average(demod_samples[energy_offset + self.spb/4:energy_offset + self.spb*3/4])
            if mean > lower_bound:
                break
            energy_offset = energy_offset + 1

        if energy_offset < 0:
            print '*** ERROR: Could not detect any ones (so no preamble). ***'
            print '\tIncrease volume / turn on mic?'
            print '\tOr is there some other synchronization bug? ***'
            sys.exit(1)

        '''
        Then, starting from the demod_samples[offset], find the sample index where
        the cross-correlation between the signal samples and the preamble 
        samples is the highest. 
        '''
        # Fill in your implementation of the cross-correlation check procedure
        preamble_bits = [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1]  
        preamble_samples = []
        for x in range(0, len(preamble_bits)):
            sample = [preamble_bits[x]]*self.spb
            #print "sample: " + str(sample)
            preamble_samples = preamble_samples + sample

        preamble_samples = numpy.array(preamble_samples)
        print "preamble_samples: " + str(preamble_samples)

        maximum = 0
        offset = 0
        for x in range(-10*self.spb,10*self.spb):
            #print "preamble_samples" + str(preamble_samples)
            test_array = demod_samples[energy_offset + x:energy_offset + x + len(preamble_samples)]
            #print "test_array: " + str(test_array)
            result = numpy.multiply(test_array, preamble_samples)
            #print "result: " + str(result)
            temp = numpy.sum(result)
            
            if temp > maximum:
                #print "temp: " + str(temp)
                #print "offset: " + str(x)
                maximum = temp
                offset = x



        preamble_offset = offset
        print "NUMBER of samples: " + str(len(demod_samples))
        print "preamble_offset: " + str(offset)
        
        '''
        [preamble_offset] is the additional amount of offset starting from [offset],
        (not a absolute index reference by [0]). 
        Note that the final return value is [offset + pre_offset]
        '''
        print "total offset: " + str(energy_offset + preamble_offset)
        return energy_offset + preamble_offset
        
    def demap_and_check(self, demod_samples, preamble_start):
        '''
        Demap the demod_samples (starting from [preamble_start]) into bits.
        1. Calculate the average values of midpoints of each [spb] samples
           and match it with the known preamble bit values.
        2. Use the average values and bit values of the preamble samples from (1)
           to calculate the new [thresh], [one], [zero]
        3. Demap the average values from (1) with the new three values from (2)
        4. Check whether the first [preamble_length] bits of (3) are equal to
           the preamble. If it is proceed, if not terminate the program. 
        Output is the array of data_bits (bits without preamble)
        '''
        preamble_bits = [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1]
        

        ones = []
        zeroes = []
        for x in range(0, len(preamble_bits)):
            mean = numpy.average(demod_samples[preamble_start + x*self.spb:x*self.spb + self.spb + preamble_start])
            if preamble_bits[x] == 1:
                ones.append(mean)
            else:
                zeroes.append(mean)

        ones_average = numpy.mean(ones)
        zeroes_average = numpy.mean(zeroes)
        print "high: " + str(ones_average)
        print "low: " + str(zeroes_average)

        # Fill in your implementation
        threshold = (ones_average + zeroes_average)/2
        offset = preamble_start + len(preamble_bits)*self.spb

        data_bits = []

        for x in range(offset/self.spb, len(demod_samples)/self.spb - 300):
            mean = 0
            #print (x - offset/self.spb)
            for y in range(0, self.spb):
                mean  = mean + demod_samples[offset + x*self.spb + y]
            mean = mean / self.spb
            if (mean > threshold):
                data_bits.append(1)
            else:
                data_bits.append(0)
            #x = x + self.spb


        return data_bits # without preamble

    def demodulate(self, samples):
        return common.demodulate(self.fc, self.samplerate, samples)
