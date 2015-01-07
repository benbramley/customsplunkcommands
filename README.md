customsplunkcommands
====================

Collection of custom built Splunk commands 

cacheget.py

This is a custom lookup command which enables Splunk to connect to a Redis cache lookp field values.

To use copy the cacheget.py either to an application folder or the default search application e.g. $SPLUNK_HOME/etc/app/search/bin

Edit transforms.conf to tell Splunk to use the cacheget.py file as a lookup command
