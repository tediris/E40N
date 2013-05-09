# audiocom library: Source and sink functions
import common_srcsink
import Image
from graphs import *
import binascii
import random


class Sink:
    def __init__(self):
        # no initialization required for sink 
        print 'Sink:'

    def process(self, recd_bits):
        # Process the recd_bits to form the original transmitted
        # file. 
        # Here recd_bits is the array of bits that was 
        # passed on from the receiver. You can assume, that this 
        # array starts with the header bits (the preamble has 
        # been detected and removed). However, the length of 
        # this array could be arbitrary. Make sure you truncate 
        # it (based on the payload length as mentioned in 
        # header) before converting into a file.
        
        # If its an image, save it as "rcd-image.png"
        # If its a text, just print out the text
        
        # Return the received payload for comparison purposes
        bytes = self.bitToByte(recd_bits)
        ext = ""
        if (recd_bits[0] == 0 and recd_bits[1] == 1):
            ext = "txt"
            printBytes(bytes)
        elif (recd_bits[0] == 0 and recd_bits[1] == 0):
            ext = "png"
        f = open("foo." + ext, "w")
        for b in range (4, len(bytes)):
            f.write(chr(bytes[b]))

        f.close()
        rcd_payload = recd_bits
        return rcd_payload

    def printBytes(self, bytes):
        for b in range (4, len(bytes)):
            print chr(bytes[b])

    def bits2text(self, bits):
        # Convert the received payload to text (string)
        return  text

    def image_from_bits(self, bits,filename):
        # Convert the received payload to an image and save it
        # No return value required .
        pass 

    def read_header(self, header_bits): 
        # Given the header bits, compute the payload length
        # and source type (compatible with get_header on source)
 
        print '\tRecd header: ', header_bits
        print '\tLength from header: ', payload_length
        print '\tSource type: ', srctype
        return srctype, payload_length

    def bitToByte(self, bits):
        bytes = []
        while (len(bytes) < len(bits)/8):
            pos = len(bytes)
            byteString = ""
            byteAsArray = bits[pos*8: pos*8 + 8]
            for b in byteAsArray:
                byteString += str(b)

            byteString = byteString[::-1]
            print byteString
            byte = int(byteString, 2)
            print chr(byte)
            bytes.append(byte)
        return bytes