from figi_api.figi import api_call
import json




def get_figi_mappings(identifier_data: dict) -> list[dict]:
    """
    Receives identifier_data (dict) containing idType and idValue
    Return a result (dict) containing result_number, figi, name, exchCode, securityType2
    """
    mapping_request = [
        {"idType": identifier_data["idType"], "idValue": identifier_data["idValue"]},
    ]
    mapping_response = api_call("/v3/mapping", mapping_request)

    results = []
    i = 0
    
    for item in mapping_response:
        if 'data' in item and item['data']: #If there is a 'data' key and it is not empty
            for data_item in item['data']:  #For every item in the 'data' key
                i = i+1
                filtered_data = {
                    'result_number': i,
                    'original_id_type': identifier_data["idType"],
                    'original_id': identifier_data["idValue"],
                    'figi': data_item.get('figi'),
                    'name': data_item.get('name'),
                    'exchCode': data_item.get('exchCode'),
                    'securityType2': data_item.get('securityType2')
                }
                results.append(filtered_data)
                print(json.dumps(filtered_data, indent=2)) #Dumps converts dictionary into JSON.
    
    return results


def select_from_multiple_figi_mapping_results(results: list[dict], selection: int) -> dict:

    choice = None
    for item in results:
        if item["result_number"] == selection:
            choice = item
            choice.pop("result_number") # Remove the result number, no longer needed
            break
    
    print(f"\n\n {json.dumps(choice, indent=2)}")



def main():
    # Input comes from another function as JSON
    user_input = {
        "idType": "ID_ISIN",
        "idValue": "IE0032126645"
    }
    
    # Search for figi mappings with the user input
    results = get_figi_mappings(user_input)

    # Choose one of the results
    choice = select_from_multiple_figi_mapping_results(results, 3)
    
    

if __name__ == "__main__":
    main()