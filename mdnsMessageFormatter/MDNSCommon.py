__author__ = 'crunk'

import socket

def getMDNSSendSocket():
	sock = socket.socket(type=socket.SOCK_DGRAM)
	sock.connect(("224.0.0.251",5353))
	return sock


class ClassException(Exception):
	def __init__(self, obj, expectedClass):
		string = "ClassError -- given: " + str(obj.__class__.__name__) + ", expected: " + str(expectedClass.__name__)
		super(ClassException, self).__init__(string)

#
#	mDNS rr types
#
kMDNSRRTypeA = 1
kMDNSRRTypeNS = 2
kMDNSRRTypePTR = 12
kMDNSRRTypeTXT = 16
kMDNSRRTypeAAAA = 28
kMDNSRRTypeSRV = 33
kMDNSRRTypeNSEC = 47
kMDNSRRTypeANY = 255

#
# mDNS rr classes
#
kMDNSRRClassIN = 1

#
#   mDNS rrType string map
#
rrtypeCodeToStr = {
	kMDNSRRTypeA: "A",
	kMDNSRRTypeNS: "NS",
	kMDNSRRTypePTR: "PTR",
	kMDNSRRTypeTXT: "TXT",
	kMDNSRRTypeAAAA: "AAAA",
	kMDNSRRTypeSRV: "SRV",
	kMDNSRRTypeNSEC: "NSEC"
}


#
#   mDNS Message Flags
#
kMDNSFlagResponse = 0x8000
kMDNSFlagAuthoritativeAnswer = 0x0400
kMDNSFlagTruncated = 0x0200
kMDNSFlagRecursionDesired = 0x0100
kMDNSFlagRecursionAvailable = 0x0080
kMDNSFlagAnswerAuthenticated = 0x0020
kMDNSFlagNonAuthenticated = 0x0010

#
#   Conversion tools
#

def uInt16ToByteArray(i):
	""" Creates a byte array from a uint16 in big endian order,
	raises exception if i not a uint16
	"""
	checkUInt16(i)
	result = bytearray()
	result.append((i & 0xff00) >> 8)
	result.append(i & 0xff)
	return result

def uInt32ToByteArray(i):
	""" Creates a byte array from a uint32 in big endian order,
	raises exception if i not a uint32
	"""
	checkUInt32(i)
	result = bytearray()
	result.append((i & 0xff000000) >> 24)
	result.append((i & 0x00ff0000) >> 16)
	result.append((i & 0x0000ff00) >> 8)
	result.append(i & 0x000000ff)
	return result

def uLong128ToByteArray(l):
	""" Creates a byte array from a ulong128 in big endian order,
	raises exception if l not a ulong128
	"""
	checkULong128(l)
	result = bytearray()
	result += uInt32ToByteArray(int((l & 0xffffffff000000000000000000000000) >> 96))
	result += uInt32ToByteArray(int((l & 0x00000000ffffffff0000000000000000) >> 64))
	result += uInt32ToByteArray(int((l & 0x0000000000000000ffffffff00000000) >> 32))
	result += uInt32ToByteArray(int( l & 0x000000000000000000000000ffffffff))
	return result

def checkULong128(l):
	""" Checks to see if parameter l is a ulong128,
	raises exception if not	"""
	checkClass(l, long)
	if l < 0 or l >= 2**128:
		raise Exception("Long outside of range [0, 2^128)")

def checkUInt32(i):
	""" Checks to see if parameter i is a uint32,
	raises exception if not	"""
	checkClass(i, int)
	if i < 0 or i >= 2**32:
		raise Exception("Int outside of range [0, 2^32)")


def checkUInt16(i):
	""" Checks to see if parameter i is a uint16,
	raises exception if not	"""
	checkClass(i, int)
	if i < 0 or i >= 2**16:
		raise Exception("Short outside of range [0, 2^16)")

def checkClass(obj, expectedClass):
	""" Checks to see if parameter obj is of class expectedClass,
	raises exception if not	"""
	if not isinstance(obj, expectedClass):
		raise ClassException(obj, expectedClass)

def checkRRName(rrname):
	check = True # TODO: regex checking of domain name _name
	if not check:
		raise Exception("Malformed record name")

def parseRRNameToSublabels(rrname):
	# TODO: compression
	checkRRName(rrname)
	name = rrname
	if name[-1] == '.':
		name = name[:-1]
	return name.split('.')

def encodeRRName(rrname, pointers=None):
	# TODO: compression
	sublabels = parseRRNameToSublabels(rrname)
	result = bytearray()
	for sublabel in sublabels:
		result.append(len(sublabel))
		for char in sublabel:
			result.append(char)
	result.append(0) # this isn't used in compression
	return result

