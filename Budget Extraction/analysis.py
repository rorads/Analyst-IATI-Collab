import xml.etree.ElementTree as eT
import requests
import sys

org = sys.argv[1]

# Print the header for csv output
print("orgID, country, budget-start, budget-end, value, currency, valuation_date")

# Repeat this process for every country given
for i in range(2, len(sys.argv)):

    # The following lines translate the user provided arguments into an html api call for the IATI
    # registry, download an xml response, and then parse it into memory
    country = sys.argv[i]
    payload = {'reporting-org': org, 'recipient-country': country, 'stream': 'True'}
    response = requests.get("http://datastore.iatistandard.org/api/1/access/activity.xml", params=payload)
    result = eT.fromstring(response.content)
    activities = result.findall("./iati-activities/iati-activity")

    # Set our initial values
    number_of_activities = 0
    activities_without_budgets = 0
    total_committed = 0
    budget_collisions = 0

    # If there are any activites published by this organisation for this country
    if len(activities) > 0:
        # Then for each of those activies, output all individual budget objects
        # along with there values, value dates, and ranges.
        for activity in activities:

            currency = activity.attrib['default-currency']

            # count total number of activities
            number_of_activities += 1

            # percentage of this activity that applies to the country of interest
            country_weighting = 100
            recipient_countries = activity.findall("recipient-country")
            if len(recipient_countries) > 1:
                for countries in recipient_countries:
                    if countries.attrib['code'] == country:
                        country_weighting = (countries.attrib['percentage'])

            # Extract budget elements
            budget_elements = activity.findall("budget")

            # If there are any budget elements
            if len(budget_elements) > 0:
                # then iterate through each budget element
                for budget in budget_elements:
                    # then iterate through each detail of the given budget
                    for child in budget:
                        # and record the values we're interested in
                        if child.tag == 'period-start':
                            budget_start = child.attrib['iso-date']
                        elif child.tag == 'period-end':
                            budget_end = child.attrib['iso-date']
                        elif child.tag == 'value':
                            valuation_date = child.attrib['value-date']
                            budget_value = float(child.text) / 100.0 * float(country_weighting)
                    # Output the relevant information for each budget
                    print "%s,%s,%s,%s,%f,%s,%s" % (
                        org, country, budget_start, budget_end, budget_value, currency, valuation_date)

    # If there are no activities, output and error message
    else:
        print "%s has no activities for %s!" % (org, country)
