import xml.etree.ElementTree as ET
import requests
import sys

# Canada, WFP, Unicef

'''README: '''

org = sys.argv[1]
start = '2015-01-01'

# Print the header for csv output
print("orgID, country, budget-start, budget-end, value, currency, valuation_date")

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
			
			# percentage of this activity that applies to the country of interest
			country_weighting = 100
			recipient_countries = activity.findall("recipient-country")
			if len(recipient_countries) > 1:
				for countries in recipient_countries:
					if countries.attrib['code'] == country:
						country_weighting = (countries.attrib['percentage'])

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
						# if the detail is not the value element
						if child.tag == 'period-start':
							budget_start = child.attrib['iso-date']
						elif child.tag == 'period-end':
							budget_end = child.attrib['iso-date']
						elif child.tag == 'value':
							valuation_date = child.attrib['value-date']
							budget_value = float(child.text)/100.0* float(country_weighting)
					#Output the budgets
					print "%s,%s,%s,%s,%f,%s" % (org, country, budget_start, budget_end, budget_value, valuation_date)


			else:
				activities_without_budgets += 1
						

	# If there are no activities, output and error message
	else: print "%s has no activities for %s!" % (org, country)
