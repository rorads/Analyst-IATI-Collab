import xml.etree.ElementTree as ET
import requests
import sys
import pdb

'''README: outputs all of the listed locations in DFID's data.'''


# Print the header for csv output
#print("orgID, country, location-start, location-end, value, currency, valuation_date")
print("IATI-Identifier\tlocation name\tdescription\tpoint srs name\tcoordinates")


# The following lines translate the user provided arguments into an html api call for the IATI registry, download an xml response,
# and then parse it into memory
result = ET.parse('all-DfID-data-2015-09-24.xml')
#result = ET.parse('dfid_dummy.xml')
activities = result.findall("./iati-activities/iati-activity")

# Set our initial values
number_of_activities = 0
num_activities_location = 0
num_activities_no_location = 0


# If there are any activites published by this organisation for this country
if len(activities) > 0:
	# Then for each of those activies, output all individual location objects along with there values, value dates, and ranges.
	for activity in activities:

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
				output.append(activity_identifier.text) 
				output.append('\t')

				output.append(location_element.find('name').text) 
				output.append('\t')

				output.append(location_element.find('description').text) 
				output.append('\t')

				output.append(location_element.find('point').attrib['srsName']) 
				output.append('\t')

				output.append(location_element.find('point').find('pos').text)
				
				print ''.join(output)
			
			# ET.tostring(location_elements)
			num_activities_location += 1

	
