__author__ = 'crunk'

from MDNSMessageEntity import *

class MDNSQuery(MDNSMessageEntity):
	def __init__(self, qname, qtype = kMDNSRRTypeANY, qclass = kMDNSRRClassIN):
		super(MDNSQuery, self).__init__(qname, qtype, qclass)