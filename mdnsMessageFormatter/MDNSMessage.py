__author__ = 'crunk'

from MDNSCommon import *
from MDNSRR import *
from MDNSQuery import *


class MDNSMessage(object):
	def __init__(self, m_id=0, flags=0):
		checkUInt16(m_id)
		checkUInt16(flags)
		self.id = m_id
		self.flags = flags
		self.questions = []
		self.answers = []
		self.authrrs = []
		self.addrrs = []

	def addQuery(self, q):
		checkClass(q, MDNSQuery)
		self.questions.append(q)
		pass

	def addResponseRecord(self, rr):
		checkClass(rr, MDNSRR)
		self.flags |= kMDNSFlagResponse # TODO: I believe the presence of an answer automatically makes this a response
		self.answers.append(rr)
		pass

	def addAuthoritativeRecord(self, rr):
		checkClass(rr, MDNSRR)
		self.authrrs.append(rr)
		pass

	def addAdditionalRecord(self, rr):
		checkClass(rr, MDNSRR)
		self.addrrs.append(rr)
		pass

	def toByteArray(self):
		result = uInt16ToByteArray(self.id)
		result += uInt16ToByteArray(self.flags)
		result += uInt16ToByteArray(len(self.questions))
		result += uInt16ToByteArray(len(self.answers))
		result += uInt16ToByteArray(len(self.authrrs))
		result += uInt16ToByteArray(len(self.addrrs))

		for q in self.questions:
			result += q.toByteArray()
		for rr in self.answers:
			result += rr.toByteArray()
		for rr in self.authrrs:
			result += rr.toByteArray()
		for rr in self.addrrs:
			result += rr.toByteArray()

		return result

	def addFlag(self, flag):
		checkUInt16(flag)
		self.flags |= flag

	def clearFlag(self, flag):
		checkUInt16(flag)
		self.flags &= ~flag

	def send(self):
		sock = getMDNSSendSocket()
		sock.send(self.toByteArray())