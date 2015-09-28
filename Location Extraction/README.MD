# Location Extraction Script

This project is a hacky script with the following methodology:

1. Retrieve all of the requested organisation's activity xml from [the datastore api](http://datastore.iatistandard.org/docs/api/). To set the organisation, the script should be run in from the following terminal command:`python analysis-location.py GB-1 2013` where 'GB-1' is the organisation's [IATI identifier](http://iatistandard.org/201/organisation-identifiers/) - in this case [DFID](http://iatiregistry.org/publisher/dfid), and 2013 is the year we're interested in (currently mandatory and limited to one whole year - do fork and alter if you like!).
2.  The script will then exclude any activities that start after the end of the given year, or end before the start of it. It **will not** exclude activities which do not declare an end date, regardless of their activity status (this again could be fixed if desired).
3. From the filtered activities, the location name, description, point srs name, and location coordinates are extracted from the `<location>` elements (where the activities have them) and are outputted in CSV.
4. Future steps: use the coordinates to use the [Google Maps Geocoding API](https://developers.google.com/maps/documentation/geocoding/intro?csw=1) to retrieve detailed location data and return that alonside the above.

> NOTES: This script pulls up to 20MB of data from a datastore that isn't terribly fast, so it can be*slow* when you run it with a publisher like DFID, to the tune of a couple of minutes.