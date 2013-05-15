__author__ = 'crunk'

from MDNSCommon import *
from MDNSMessageEntity import *

class MDNSRR(MDNSMessageEntity):
	def __init__(self, rrname, rrtype, rrclass, rrttl, rrdataArgMap):
		super(MDNSRR, self).__init__(rrname, rrtype, rrclass)
		checkUInt32(rrttl)
		self.ttl = rrttl
		self.formattedRRData = self.formatRRData(rrdataArgMap)
		if len(self.formattedRRData) >= 2**16:
			raise Exception("formattedrrdata must be smaller than 2^16 in length")

	def toByteArray(self):
		result = super(MDNSRR, self).toByteArray()
		result += uInt32ToByteArray(self.ttl)
		result += uInt16ToByteArray(len(self.formattedRRData))
		result += self.formattedRRData
		return result

	def setCacheFlushBit(self, boolean):
		checkClass(boolean, bool)
		if boolean:
			self.rrclass |= 0x8000
		else:
			self.rrclass &= 0x7fff

	def formatRRData(self, rrdataArgMap):
		raise Exception("Virtual Method")

class MDNSRRA(MDNSRR):
	def __init__(self, rrname, rrclass, rrttl, rrdataArgMap):
		""" ## rrdataArgMap keys and value types ##
		'address': uint32 """
		super(MDNSRRA, self).__init__(rrname, kMDNSRRTypeA, rrclass, rrttl, rrdataArgMap)

	def formatRRData(self, rrdataArgMap):
		return uInt32ToByteArray(rrdataArgMap['address'])


class MDNSRRNS(MDNSRR):
	def __init__(self, rrname, rrclass, rrttl, rrdataArgMap):
		""" ## rrdataArgMap keys and value types ##
		'domainname': a valid domain name string """
		super(MDNSRRNS, self).__init__(rrname, kMDNSRRTypeNS, rrclass, rrttl, rrdataArgMap)

	def formatRRData(self, rrdataArgMap):
		return encodeRRName(rrdataArgMap['domainname'])


class MDNSRRPTR(MDNSRR):
	def __init__(self, rrname, rrclass, rrttl, rrdataArgMap):
		""" ## rrdataArgMap keys and value types ##
		'domainname': a valid domain name string """
		super(MDNSRRPTR, self).__init__(rrname, kMDNSRRTypePTR, rrclass, rrttl, rrdataArgMap)

	def formatRRData(self, rrdataArgMap):
		return encodeRRName(rrdataArgMap['domainname'])


class MDNSRRTXT(MDNSRR):
	def __init__(self, rrname, rrclass, rrttl, rrdataArgMap):
		""" ## rrdataArgMap: a map of key value pairs. For each pair,
		a text entry is added to the record in the string form '<key>=<value>' """
		super(MDNSRRTXT, self).__init__(rrname, kMDNSRRTypeTXT, rrclass, rrttl, rrdataArgMap)

	def formatRRData(self, rrdataArgMap):
		result = bytearray()
		for (k, v) in rrdataArgMap.items():
			result += encodeString(str(k) + "=" + str(v))
		return result


class MDNSRRAAAA(MDNSRR):
	def __init__(self, rrname, rrclass, rrttl, rrdataArgMap):
		""" ## rrdataArgMap keys and value types ##
		'address': ulong128 """
		super(MDNSRRAAAA, self).__init__(rrname, kMDNSRRTypeAAAA, rrclass, rrttl, rrdataArgMap)

	def formatRRData(self, rrdataArgMap):
		return uLong128ToByteArray(rrdataArgMap['address'])


class MDNSRRSRV(MDNSRR):
	def __init__(self, rrname, rrclass, rrttl, rrdataArgMap):
		""" ## rrdataArgMap keys and value types ##
		'priority': uint16,
		'weight': uint16,
		'port': uint16,
		'target': a valid hostname string (<hostname>.local.) """
		super(MDNSRRSRV, self).__init__(rrname, kMDNSRRTypeSRV, rrclass, rrttl, rrdataArgMap)

	def formatRRData(self, rrdataArgMap):
		result = bytearray(uInt16ToByteArray(rrdataArgMap['priority']))
		result += uInt16ToByteArray(rrdataArgMap['weight'])
		result += uInt16ToByteArray(rrdataArgMap['port'])
		result += encodeRRName(rrdataArgMap['target'])
		return result


class MDNSRRNSEC(MDNSRR):
	def __init__(self, rrname, rrclass, rrttl, rrdataArgMap):
		""" MDNSRRNSEC is currently unimplemented
		"""
		super(MDNSRRNSEC, self).__init__(rrname, kMDNSRRTypeNSEC, rrclass, rrttl, rrdataArgMap)

	def formatRRData(self, rrdataArgMap):
		raise Exception("Unimplemented Method")