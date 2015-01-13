# Splunk command to transform results using a mako template
# Created - 22/07/2013
# Author - BB
 
import splunk.Intersplunk as si
import StringIO
from mako.template import Template
from mako.runtime import Context
 
if __name__ == '__main__':
    try:
        keywords,options = si.getKeywordsAndOptions()
        defaultval = options.get('default', None)
        field = options.get('field', '_raw')
        template = options.get('template', None)
        outfield = options.get('outfield', 'transformed')
        filetemplate = Template(filename='../templates/'+template+'.txt')
 
        if len(keywords) != 1:
            si.generateErrorResults('Requires exactly one template argument.')
            exit(0)
 
        results,dummyresults,settings = si.getOrganizedResults()
        # for each results
        for result in results:
            # get field value
            myresult = result.get(field, None)
            added = False
            if myresult != None:
                try:
                    values = filetemplate(myresult)
                    result[outfield] = values
                except Exception, e:
                    pass # consider throwing exception and explain path problem
 
            if not added and defaultval != None:
                result[outfield] = defaultval
 
        si.outputResults(results)
    except Exception, e:
        import traceback
        stack =  traceback.format_exc()
        si.generateErrorResults("Error '%s'. %s" % (e, stack))
