import xml.etree.ElementTree as ET
import requests
import sys
import pdb
import dateutil.parser
import pdb

f = open('output.csv', 'w')
'''README: outputs all of the listed locations in DFID's data.'''


# Print the header for csv output
#print("orgID, country, location-start, location-end, value, currency, valuation_date")
f.write("IATI-Identifier,location name,description,point srs name,coordinates,\n")


# The following lines translate the user provided arguments into an html api call for the IATI registry, download an xml response,
# and then parse it into memory
result = ET.parse('all-DfID-data-2015-09-24.xml')
#result = ET.parse('dfid_2013_activities.xml')
#result = ET.parse('dfid_dummy.xml')
activities = result.findall("./iati-activities/iati-activity")

# Set our initial values
number_of_activities = 0
num_activities_location = 0
num_activities_no_location = 0

def out_of_scope(dates):

	for date in dates:
		#pdb.set_trace()

		if date.attrib['type'] == 'start-actual':
			if dateutil.parser.parse(date.attrib['iso-date']).year > 2013:
				return True
		elif date.attrib['type'] == 'end-actual':
			if dateutil.parser.parse(date.attrib['iso-date']).year < 2013:
				return True
		else:
			if date.attrib['type'] == 'start-planned':
				if dateutil.parser.parse(date.attrib['iso-date']).year > 2013:
					return True
			elif date.attrib['type'] == 'end-planned':
				if dateutil.parser.parse(date.attrib['iso-date']).year < 2013:
					return True
			else:
				return False



# If there are any activites published by this organisation for this country
if len(activities) > 0:
	# Then for each of those activies, output all individual location objects along with there values, value dates, and ranges.
	for activity in activities:

		date_list = activity.findall('activity-date')

		if out_of_scope(date_list) or len(date_list) < 1:
			#print '-\t-\t-\t-\t-\t'
			continue

		activity_identifier = activity.find('iati-identifier')
		
		# count total number of activities
		number_of_activities += 1
		
		# Extract location elements
		location_elements = activity.findall('location')
		
		# If there are any location elements
		if len(location_elements) > 0:

			for location_element in location_elements:

				# Build the output string
				output = []
				output.append('\"')
				output.append(activity_identifier.text) 
				output.append('\",\"')
				output.append(location_element.find('name').text) 
				output.append('\",\"')
				output.append(location_element.find('description').text) 
				output.append('\",\"')
				output.append(location_element.find('point').attrib['srsName']) 
				output.append('\",\"')
				output.append(location_element.find('point').find('pos').text)
				output.append('\"\n')

				
				f.write(''.join(output).encode('ascii', 'ignore'))
			
			# ET.tostring(location_elements)


	
