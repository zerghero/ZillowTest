ZillowTest
==========

Test Python script to get home value data by zip code or address using Zillow API.

<b>Zip code: </b>
Use GetDemographics API from Zillow plus zip code list to compile home values for properties of different sizes (single family, condo, by bedroom count, $/sq ft).  Prints table of results.

<b>Address: </b>
Import address list from address_list.csv, output detailed address-level data.  Uses GetDeepSearchResults API from Property Details API from Zillow.

Next step: Merge with US Census zip code extents to display average market values on map?
