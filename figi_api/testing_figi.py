from figi import api_call
import json


# Example 1: Map a third party identifier to a FIGI
idType = "ID_BB_GLOBAL"
idValue = "BBG000BLNNH6"

mapping_request = [
    {"idType": idType, "idValue": idValue},
]
mapping_response = api_call("/v3/mapping", mapping_request)
print("\n\nMapping response:", json.dumps(mapping_response, indent=2))




# Example 2: Search for FIJIs using key words and other filters.
#/v3/filter is better than /v3/search because it includes number of results.
# Important: when the answer ends in 'next', read documentation on what to do.
query = "BBG00NL1J164"
# exchCode = "EU"

search_request = {"query": query}
search_response = api_call("/v3/filter", search_request)
print("\n\nSearch response:", json.dumps(search_response, indent=2))

