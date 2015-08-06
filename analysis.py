import xml.etree.ElementTree as ET
import requests
import sys

# Canada, WFP, Unicef

'''README: '''

org = sys.argv[1]
start = '2015-01-01'

# Print the header for csv output
print("titles")

# Repeat this process for every country given
for i in range(2,len(sys.argv)):

	country = sys.argv[i]

	payload = {'reporting-org': org, 'recipient-country': country, 'end-date__gt': start, 'stream':'True'}
	response = requests.get("http://datastore.iatistandard.org/api/1/access/activity.xml", params=payload)
	result = ET.fromstring(response.content)
	activities = result.findall("./iati-activities/iati-activity")

	number_of_activities = 0
	activities_without_budgets = 0
	total_committed = 0
	budget_collisions = 0


	# If there are any activites published by this organisation for this country
	if len(activities) > 0:
		# Then for each of those activies, output all individual budget objects along with there values, value dates, and ranges.
		for activity in activities:
			
			#counter for the budget collisions found in this activity
			current_budget_collisions = 0

			#count total number of activities
			number_of_activities += 1

			#Extract budget elements and print how many there are
			budget_elements = activity.findall("budget")
			
			#Are there budget elements?
			if len(budget_elements) > 0:
				# Create a budget dictionary so that we can compare revised / non-revised budgets and insert the approapriate one
				non_colliding_budgets = {}
				# For each budget element
				for budget in budget_elements:
					# Store whether it's revised or original
					b_type = budget.attrib['type']
					# For each detail of the budget
					for child in budget:
						# look at the budgets start and end dates to make sure that it's unique
						date_string = ""
						# if the detail is not the value element
						if child.tag != 'value':
							# make a key out of the start and end dates of the budget
							date_string = date_string + child.attrib['iso-date']
							# if the key isn't already there, then store this budget agains the key
							if date_string not in non_colliding_budgets.keys():
								non_colliding_budgets[date_string] = budget
							# otherwise
							else:
								# record the collision
								current_budget_collisions += 1
								# and if the budget type is 'revised', overwrite the value in the dictionary
								if b_type == 'revised':
									non_colliding_budgets[date_string] = budget
			else:
				activities_without_budgets += 1
			
			count = 0
			for prime_budget in non_colliding_budgets:
				count += 1
				print count, prime_budget.text

			#add the budget collisions to the total
			budget_collisions += current_budget_collisions
		
						
		#Output the total, activities_without_budgets
		percent = float(number_of_activities - activities_without_budgets) / float(number_of_activities) * 100
		print "%s,%s,%s,%i,%i,%f,%i,%s" % (org, country, start, number_of_activities, activities_without_budgets, percent, budget_collisions, response.url)

	# If there are no activities, output and error message
	else: print "%s has no activities for %s!" % (org, country)
