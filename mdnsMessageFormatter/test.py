from MDNSRR import *
from MDNSMessage import *
from MDNSCommon import *
import select
import time

m = MDNSMessage()
m.setFlag(kMDNSFlagResponse | kMDNSFlagAuthoritativeAnswer)

answer = MDNSRRPTR("_printer._tcp.local",1,4500,{'domainname':'fake._printer._tcp.local'})
m.addResponseRecord(answer)

answer2 = MDNSRRPTR("_ipp._tcp.local",1,4500,{'domainname':'fake._ipp._tcp.local'})
m.addResponseRecord(answer2)

adda = MDNSRRA("ilab1.cs.byu.edu",1,120,{'address':0xc0a81565})
adda.setCacheFlushBit(True)
m.addAdditionalRecord(adda)

addaaaa = MDNSRRAAAA("ilab1.cs.byu.edu",1,120,{'address':0xfe80000000000000be5ff4fffe8b7d13})
addaaaa.setCacheFlushBit(True)
m.addAdditionalRecord(addaaaa)

addsrv = MDNSRRSRV("fake._printer._tcp.local",1,120,{'priority':0,'weight':0,'port':515,'target':'ilab1.cs.byu.edu'})
addsrv.setCacheFlushBit(True)
m.addAdditionalRecord(addsrv)

addtxt = MDNSRRTXT("fake._printer._tcp.local",1,4500,{'txtvers':1,
														'qtotal':4,
														'rp':'RAW',
														'pdl':'application/postscript,application/vnd.hp-PCL,application/vnd.hp-PCLXL',
														'ty':'Fake Printer',
														'product':'(HP LaserJet P4015)',
														'priority':52,
														'adminurl':'http://ilab1.cs.byu.edu'})
addtxt.setCacheFlushBit(True)
m.addAdditionalRecord(addtxt)

addtxt2 = MDNSRRTXT("fake._printer._tcp.local",1,4500,{'txtvers':1,
														'qtotal':4,
														'rp':'TEXT',
														'pdl':'text/plain',
														'ty':'Fake Printer',
														'product':'(HP LaserJet P4015)',
														'priority':53,
														'adminurl':'http://ilab1.cs.byu.edu'})
addtxt2.setCacheFlushBit(True)
m.addAdditionalRecord(addtxt2)

addtxt3 = MDNSRRTXT("fake._printer._tcp.local",1,4500,{'txtvers':1,
														'qtotal':4,
														'rp':'AUTO',
														'pdl':'application/postscript,application/vnd.hp-PCL,application/vnd.hp-PCLXL,text/plain',
														'ty':'Fake Printer',
														'product':'(HP LaserJet P4015)',
														'priority':51,
														'adminurl':'http://ilab1.cs.byu.edu'})
addtxt3.setCacheFlushBit(True)
m.addAdditionalRecord(addtxt3)

addtxt4 = MDNSRRTXT("fake._printer._tcp.local",1,4500,{'txtvers':1,
														'qtotal':4,
														'rp':'BINPS',
														'pdl':'application/postscript',
														'ty':'Fake Printer',
														'product':'(HP LaserJet P4015)',
														'priority':30,
														'adminurl':'http://ilab1.cs.byu.edu',
														'Transparent':'T',
														'Binary':'T'})
addtxt4.setCacheFlushBit(True)
m.addAdditionalRecord(addtxt4)

addsrv2 = MDNSRRSRV("fake._ipp._tcp.local",1,120,{'priority':0,'weight':0,'port':631,'target':'ilab1.cs.byu.edu'})
addsrv2.setCacheFlushBit(True)

sock = getMDNSSocket()

read, write, x = select.select([sock],[],[])

time.sleep(.05)
m.send()

raw_input("Press any key to send ipp TXT record...")

m2 = MDNSMessage()
m2.setFlag(kMDNSFlagResponse | kMDNSFlagAuthoritativeAnswer)
answer = MDNSRRTXT("fake._ipp._tcp.local", 1, 4500,{'txtvers':1,
													'qtotal':1,
													'pdl':'application/postscript,application/vnd.hp-PCL,application/vnd.hp-PCLXL',
													'rp':'NPI7F45A6',
													'ty':'Fake Printer',
													'product':'(HP LaserJet P4015)',
													'priority':60,
													'adminurl':'http://ilab1.cs.byu.edu'})
answer.setCacheFlushBit(True)

m2.addResponseRecord(answer)

m2.send()

raw_input("Press any key to send ipp SRV record again...")

m3 = MDNSMessage()
m3.setFlag(kMDNSFlagResponse | kMDNSFlagAuthoritativeAnswer)

m3.addResponseRecord(addsrv2) # I don't know why this is being asked twice...

m3.send()
