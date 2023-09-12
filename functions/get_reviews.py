"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from cloudant.client import Cloudant
from cloudant.result import QueryResult
from cloudant.error import CloudantException
import requests
import json


def main(param_dict):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """
    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )
        print(f"Databases: {client.all_dbs()}")
        db = client['reviews']
        print(f"Connected to reviews")
        dictionary_header = {"Content-Type":"application/json"}
        if "id" not in param_dict:
            dictionary_return = {"status": "400", "headers":  dictionary_header, "body": {"error": "Missing 'id' parameter in the URL"}}
            return dictionary_return
        dealership_id = param_dict["id"]
       # print(f"The dealershipId is: " + dealership_id)
        dealership_id = int(dealership_id)
        # Define the query based on the 'dealership' ID
        selector = {'dealership': dealership_id}
        print(f"Defined the selector")
        # Execute the query using the query method
        result = db.get_query_result(selector)
        #query_result = QueryResult(result)
        #data_list = []
        # Iterate through the results and add documents to the list
        
        #for doc in result:
            #data_list.append(doc)
        # Return the data as JSON
           
    except CloudantException as cloudant_exception:
        print("unable to connect")
        dictionary_return = {"status": "500", "headers":  dictionary_header, "body": {"error":cloudant_exception}}
        return dictionary_return
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        dictionary_return = {"status": "500", "headers":  dictionary_header, "body": {"error":err}}
        return dictionary_return
    except ValueError:
       dictionary_return = {"status": "400", "headers":  dictionary_header, "body": {"error": "'id' parameter must be an integer"}}
       return dictionary_return
   
    dictionary_return = {"status": "200", "headers":  dictionary_header, "body": result.all()}
    print(result)
    return dictionary_return
    
