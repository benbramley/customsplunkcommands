import csv,sys,time
import urllib
import os
from itertools import izip

# Add fields here to lookup against Redis
FIELDS = [ "INSERT", "FIELDS", "HERE" ]

def redis_connect():

	# Connect to redis - replace localhost with Redis server details if required
	red = redis.Redis(host='localhost', port=6379, db=0)
	return red

# Helper function taken from Splunk Python examples
def output_results(results, mvdelim = '\n', output = sys.stdout):
	"""Given a list of dictionaries, each representing
	a single result, and an optional list of fields,
	output those results to stdout for consumption by the
	Splunk pipeline"""

	# We collect all the unique field names, as well as
	# convert all multivalue keys to the right form
	fields = set()
	for result in results:
		for key in result.keys():
			if(isinstance(result[key], list)):
				result['__mv_' + key] = encode_mv(result[key])
				result[key] = mvdelim.join(result[key])
		fields.update(result.keys())

	# convert the fields into a list and create a CSV writer
	# to output to stdout
	fields = sorted(list(fields))

	writer = csv.DictWriter(output, fields)

	# Write out the fields, and then the actual results
	writer.writerow(dict(zip(fields, fields)))
	writer.writerows(results)

# Helper function taken from Splunk Python examples
def encode_mv(vals):
	"""For multivalues, values are wrapped in '$' and separated using ';'
	Literal '$' values are represented with '$$'"""
	s = ""
	for val in vals:
		val = val.replace('$', '$$')
		if len(s) > 0:
			s += ';'
		s += '$' + val + '$'

	return s

def main(input, output, redp, argv):
	csv_in = csv.DictReader(input)

	result = list()

	# LUA function to return a hash from a set key
	lua = """
	local matches = redis.call('SMEMBERS', KEYS[1])
	local val = {}
	for count = 1, #matches do
		val[count] = redis.call('HGETALL', matches[count])
	end
	return { val }
	"""
	# Register LUA script
	gethashfromkey = redp.register_script(lua)

	for row in csv_in:

		# Automatically get the input field we are looking up - Splunk sends all fields but we just want the one with values set
		for (k,v) in row.items():
			if v:
				field = k

		key = row[field]

		# Grab hashresults using set key - this comes back as an array of arrays
		hashresults = gethashfromkey(keys=[key])

		if hashresults:
			for hashresult in hashresults:
				for h in hashresult:
					# LUA returns a list so convert into a dictionary
					i = iter(h)
					resdict = dict(izip(i, i))
					resdict[field] = key

					result.append(resdict)

	output_results(result)

if __name__ == '__main__':
    import redis
    redp = redis_connect()
    main(sys.stdin, sys.stdout, redp, sys.argv)
