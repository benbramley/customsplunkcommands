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

makotransform.py
----------------

This is a custom search command which takes any field as an input (defaults to _raw) and runs a Mako transform on the field producing a new field with the transformed output as it's value. 

To use copy the makotransform.py file to either an application or the default search application into the bin folder e.g. $SPLUNK_HOME/etc/app/search/bin

Edit commands.conf to tell Splunk where to find this command:

[makotransform]
filename = makotransform.py

Templates should be placed in the $APP_HOME/templates and named <templatename>.txt e.g. $SPLUNK_HOME/etc/app/search/templates/mytemplate.txt

Then restart Splunk for the changes to take effect.

This command has a number of uses for example you could create a html email message template and populate it with an error message e.g.

search index=someindex error=* | makotransform template=mytemplate fields="host,error" outfield=emailtosend

<html>
<body>
    <p>An error has occurred - ${error} on host ${host}</p>
</body>
</html>

This will produce a field for each error event called emailtosend which could then be piped to an alert command.

