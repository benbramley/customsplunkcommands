customsplunkcommands
====================

Collection of custom built Splunk commands 

rediscacheget.py
----------------

This is a custom lookup command which enables Splunk to connect to a Redis cache to lookup field values.

To use, copy the rediscacheget.py file either to an application or the default search application into the bin folder e.g. $SPLUNK_HOME/etc/app/search/bin

Edit transforms.conf to tell Splunk to use the cacheget.py file as a lookup command:

[rediscachelookup]                                                                                                                            
external_cmd = rediscacheget.py                                                                                                              
fields_list = [INSERT FIELDS TO LOOKUP HERE] 

Then restart Splunk for the changes to take effect.
