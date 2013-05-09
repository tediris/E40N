# audiocom library: Source and sink functions
import common_srcsink as common
import Image
from graphs import *
import binascii
import random



class Source:
    def __init__(self, monotone, filename=None):
        # The initialization procedure of source object
        self.monotone = monotone
        self.fname = filename
        #print 'Source: '

    def process(self):
            # Form the databits, from the filename 
            if self.fname is not None:
                databits = self.file2bits(self.fname)
                
                if self.fname.endswith('.png') or self.fname.endswith('.PNG'):
                    #databits =
                    payload = self.get_header(len(databits), "image")
                else:           
                    # Assume it's text  
                    #databits = self.text2bits(self.fname)
                    payload = self.get_header(len(databits), "text")                  
            else:               
                # Send monotone (the payload is all 1s for 
                # monotone bits)   
                databits = [1]*self.monotone   
                payload = self.get_header(self.monotone, "monotone")


            bytes = self.bitToByte(databits) #note that this is for testing purposes
            f = open("test.txt", "w")
            for b in range (0, len(bytes)):
                #print bytes[b]
                f.write(chr(bytes[b]))

            f.close()
            return numpy.array(databits), numpy.array(payload + databits)

    def text2bits(self, filename):
        bits = [];
        f = open(filename)
        chars = f.read();
        for c in chars:
            #print c
            str = bin(ord(c))[2:]
            while len(str) < 8:
                str = '0' + str
            #print str
            for c in str:
                bits.append(int(c))

        return bits

    def bits(self, filename):
        bytes = (ord(b) for b in filename.read())
        for b in bytes:
            for i in xrange(8):
                yield (b >> i) & 1

    def file2bits(self, filename):
        bitArray = [];
        for b in self.bits(open(filename, 'r')):
            bitArray.append(b);
        return bitArray;

    def bits_from_image(self, filename):
        # Given an image, convert to bits
        return bits

    def get_header(self, payload_length, srctype): 
        # Given the payload length and the type of source 
        # (image, text, monotone), form the header
        src = []
        if srctype == "image":
            src.append(0)
            src.append(0)
        elif srctype == "text":
            src.append(0)
            src.append(1)
        elif srctype == "monotone":
            src.append(1)
            src.append(0)
        length = self.convertToBinaryList(payload_length)
        while(len(src) + len(length) < 32): #makes length of header consistent
            src.append(0)
        return src + length

    def convertToBinaryList(self, x):
        if x <= 0: return [0]
        bit = []
        while x:
            bit.append(x % 2)
            x >>= 1
        return bit[::-1]

    def bitToByte(self, bits):
        bytes = []
        while (len(bytes) < len(bits)/8):
            pos = len(bytes)
            byteString = ""
            byteAsArray = bits[pos*8: pos*8 + 8]
            for b in byteAsArray:
                byteString += str(b)

            byteString = byteString[::-1]
            #print byteString
            byte = int(byteString, 2)
            #print chr(byte)
            bytes.append(byte)
        return bytes

