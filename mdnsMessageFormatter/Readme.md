# MDNS Message Formatting Library
This library is an object oriented approach for generating, formatting, and sending mDNS Protocol messages. This is particularly useful for security and reliability testing of mDNS discoverable services. 

## Contained in this Library
The library is constituted of the following classes:

* MDNSMessage
* MDNSMessageEntity (abstract base class)
* MDNSQuery (subclass of MDNSMessageEntity)
* MDNSRR (an abstract base class for mDNS resource records; subclass of MDNSMessageEntity)
* subclasses of MDNSRR in the form MDNSRR&amp;type&amp; based on record type (current support allows types A, AAAA, NS, PTR, TXT, and SRV)

In addition, the file MDNSCommon.py contains a number of mDNS constants and supportive functions.

## Using the Library

### Creating an MDNSMessage
Each message begins with an MDNSMessage. If no parameters are given to the MDNSMessage constructor, the message is instantiated with a transaction ID of 0 and no flags set.  

### Adding queries to an MDNSMessage
The client must create an MDNSQuery and then add it to the MDNSMessage as follows:

	m = MDNSMessage()
	query = MDNSQuery(name, type, class)
	m.addQuery(query)

Default values for type and class are kMDNSRRTypeANY and kMDNSRRClassIN by default, respectively.

### Adding Response, Authoritative, and Additional Resource Records (RRs) to an MDNSMessage
Response, authoritative, and additional records are all created using MDNSRR objects. Once the object is created, the object is added with the appropriate MDNSMessage method from the following methods:

```python
m.addResponseRecord(responseRR)
m.addAuthoritativeRecord(authRR)
m.addAdditionalRecord(addRR)
```

**Please Note**: if a response is added to the MDNSMessage, the kMDNSFlagResponse (0x8000) will be set automatically in the message flags.
MDNSRR subclass objects implicitly specify what type of RR they are. For example, an MDNSRRA object is an MDNSRR object with a record type A. MDNSRR subclass objects require 4 things:
	
* the record name
* the record class
* the record time-to-live (ttl) value
* the record data (rrdata)

The constructor for the MDNSRR subclasses is the same across all of them. For example, instantiation of an MDNSRRA object is done as follows:

```python
rr = MDNSRRA(rrname, rrclass, rrttl, rrdataArgMap)
```

The rrdataArgMap is a mapping of string keys to values. Each type of RR requires different data and thus the required key-value pairs in rrdataArgMap depends on the type of RR that is being instantiated. To find out what key-value pairs are required for each type, a call such as `help(MDNSRRA.__init__)` will return a description of the requirements. In other words, the docstrings for each MDNSRR subclass `__init__` function contain information about rrdataArgMap. Here is the return of `help(MDNSRRSRV.__init__)`:

```python
__init__(self, rrname, rrclass, rrttl, rrdataArgMap) unbound MDNSRR.MDNSRRSRV method
    ## rrdataArgMap keys and value types ##
    'priority': uint16,
    'weight': uint16,
    'port': uint16,
    'target': a valid hostname string (<hostname>.local.)
```

### Sending an MDNSMessage
After creating an MDNSMessage and adding the desired entries to the message, calling `MDNSMessage.send()` will format and send the message contents to the mDNS multicast address:

```python
m = MDNSMessage()
.
.
.
m.send()
```

Alternatively, MDNSMessage also contains the method `MDNSMessage.toByteArray()`. If you would like to manage the sending of the packet, you can use `toByteArray()` to get the formatted message in byte array form. The byte array can then be used as raw data to be sent out on a socket. 

