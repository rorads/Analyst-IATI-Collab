import xml.etree.ElementTree as ET
import requests
import sys

'''README: to use this script, you must include 2 or more arguments when calling it. The first must be the IATI identifier of the Organisation
you wish to examine, and then one or more country codes afterwards. For each counry code provided, a row will be appended into the csv terminal output.'''

org = sys.argv[1]
start = '2015-01-01'

# Print the header for csv output
print("headings")

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
	#start_date = None <---Input date (YYYY-MM-DD)
	#end_date = None <-----Input date (YYYY-MM-DD)


	#For each activity
	for activity in activities:
		
		#count total number of activities
		number_of_activities += 1

		#Extract budget elements and print how many there are
		budget_elements = activity.findall("budget")
		
		#Are there budget elements?
		if len(budget_elements) > 0:
			
			# Create a budget dictionary so that we can compare revised / non-revised budgets and insert the approapriate one
			found_budgets = {}
			for budget in budget_elements:
				if not found_budgets[budget.date]:
					found_budgets[budget.date] = budget

			#are there revised figures?
				#Yes - use them
				#No - use the originals

			#For each budget element used
				#Is its start period after start_date?
					#Yes, then is its end period after end_date?	
						#Yes, then add its amount to the total

		#If there aren't any budget elements, exclude the activity, and add a number to the count of non-budgeted activities
		else:
			activities_without_budgets += 1

					
	#Output the total, activities_without_budgets
	percent = float(number_of_activities - activities_without_budgets) / float(number_of_activities) * 100
	print "%s,%s,%s,%i,%i,%f,%s" % (org, country, start, number_of_activities, activities_without_budgets, percent, response.url)
