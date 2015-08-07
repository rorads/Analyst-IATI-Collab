# Analyst-IATI-Collab
Scripts written to help Analysts use IATI data

--------------------
### Introduction
This repository contains two hastily made scripts to interpret IATI data. Together, they allow someone (with a working python environment & [requests installed](http://www.python-requests.org/en/latest/)) to analyse a given publisher's budget spending for a set of recipient countries.

### Using this code
For the time being there are two scripts: one that checks the given pairings for missing budgets, and budget collisions (see below), and one that aggregates all of the budgets that have been declared for a given pairing _from within an activity_.
Both scripts are called in the same way, by calling the following in bash:
```bash
python analysis.py orgId countryCode1 ... countryCodeN
```
or
```bash
python initial_coverage_review.py orgId countryCode1 ... countryCodeN
```

### initial_coverage_review.py
This script produces results in csv by printing them to the console. This means that the inital output is looks like this:
```csv
org, country, start, number_of_activities, activities_without_budgets, percent, total_budgets, budget_collisions, response.url
CA-3,AF,01/01/15,33,0,100,99,0,http://datastore.iatistandard.org/api/1/access/activity.xml?reporting-org=CA-3&recipient-country=AF&stream=True&end-date__gt=2015-01-01
```
Once this is saved into a [name].csv format, however, it can be opened as a spreadsheet and then manipulated, which would look more like this:
<table border="1">
<tbody><tr><td>org</td>
<td> country</td>
<td> start</td>
<td> number_of_activities</td>
<td> activities_without_budgets</td>
<td> percent</td>
<td> total_budgets</td>
<td> budget_collisions</td>
<td> response.url</td>
</tr>
<tr><td>CA-3</td>
<td>AF</td>
<td>01/01/15</td>
<td>33</td>
<td>0</td>
<td>100</td>
<td>99</td>
<td>0</td>
<td>http://datastore.iatistandard.org/api/1/access/activity.xml?reporting-org=CA-3&amp;recipient-country=AF&amp;stream=True&amp;end-date__gt=2015-01-01</td>
</tr>
</tbody></table>

### analysis.py
This script is similar - publishing csv to the console, and taking arguments in the same way - but instead of printing out at the organisation-country pairing level, will output at the budget-in-activity level for a given set of pairings (i.e. organisation:country1, organisaiton:country2, ...).
The csv output looks like this:
```csv
orgID, country, budget-start, budget-end, value, currency, valuation_date
CA-3,TZ,2010-04-01,2011-03-31,278522.420000,CAD,2010-04-01
CA-3,TZ,2011-04-01,2012-03-31,292448.170000,CAD,2010-04-01
...
```
The resulting spreadsheet looks like this:
<table border="1">
<tbody><tr><td>orgID</td>
<td> country</td>
<td> budget-start</td>
<td> budget-end</td>
<td> value</td>
<td> currency</td>
<td> valuation_date</td>
</tr>
<tr><td>CA-3</td>
<td>TZ</td>
<td>2010-04-01</td>
<td>2011-03-31</td>
<td>278522.420000</td>
<td>CAD</td>
<td> 2010-04-01</td>
</tr>
<tr><td>CA-3</td>
<td>TZ</td>
<td>2011-04-01</td>
<td>2012-03-31</td>
<td>292448.170000</td>
<td>CAD</td>
<td> 2010-04-01</td>
</tr>
<tr><td>...</td>
<td>...</td>
<td>...</td>
<td>...</td>
<td>...</td>
<td>...</td>
<td>...</td>
</tr>
</tbody></table>

### Current Bugs
* initial_coverage_review.py breaks if there is no activity between a given publisher and a given country
