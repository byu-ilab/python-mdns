__author__ = 'crunk'

from MDNSCommon import *

class MDNSMessageEntity(object):
	def __init__(self, rrname, rrtype, rrclass):
		checkUInt16(rrtype)
		checkUInt16(rrclass)
		checkRRName(rrname)
		self.rrname = rrname
		self.rrtype = rrtype
		self.rrclass = rrclass

	def toByteArray(self):
		result = bytearray(encodeRRName(self.rrname))
		result += uInt16ToByteArray(self.rrtype)
		result += uInt16ToByteArray(self.rrclass)
		return result