# MDNS Message Formatting Library
This library is an object oriented approach for generating, formatting, and sending mDNS Protocol messages. This is particularly useful for security and reliability testing of mDNS discoverable services. 

## Contained in this Library
The library is constituted of the following classes:

* MDNSMessage
* MDNSMessageEntity (abstract base class)
* MDNSQuery (subclass of MDNSMessageEntity)
* MDNSRR (an abstract base class for mDNS resource records; subclass of MDNSMessageEntity)
* subclasses of MDNSRR in the form MDNSRR<type> based on record type (A, AAAA, NS, PTR, TXT, SRV)

In addition, the file MDNSCommon.py contains a number of mDNS constants and supportive functions.

## Using the Library

### Creating an MDNSMessage
Each message begins with an MDNSMessage. If no parameters are given to the MDNSMessage constructor, the message is instantiated with a transaction ID of 0 and no flags set.  

### Adding queries to an MDNSMessage
The client must create an MDNSQuery and then add it to the MDNSMessage as follows:

	m = MDNSMessage()
	query = MDNSQuery(name, type, class)
	m.addQuestion(query)

Default values for type and class are kMDNSRRTypeANY and kMDNSRRClassIN by default, respectively.

### Adding Response, Authoritative, and Additional Resource Records (RRs)
Response, authoritative, and additional records are all created using MDNSRR objects. Once the object is created, the object is added with the appropriate MDNSMessage method from the following methods:

	m.addResponse(responseRR)
	m.addAuthoritativeRecord(authRR)
	m.addAdditionalRecord(addRR)

Please Note: if a response is added to the MDNSMessage, the kMDNSFlagResponse (0x8000) will be set automatically in the message flags.  
