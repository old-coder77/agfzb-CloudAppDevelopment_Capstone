"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests


def main(param_dict):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """
    dictionary_header = {"Content-Type":"application/json"}
    try:
        client = Cloudant.iam(
            account_name=param_dict["COUCH_USERNAME"],
            api_key=param_dict["IAM_API_KEY"],
            connect=True,
        )
        if "review" not in param_dict:
            dictionary_return = {"status": "400", "headers":  dictionary_header, "body": {"error": "Missing the review data"}}
            return dictionary_return
        review_data = param_dict["review"]
        db = client['reviews']
        print(f"Connected to reviews")
        required_fields = ['id', 'name', 'dealership', 'review', 'purchase', 'purchase_date', 'car_make', 'car_model', 'car_year']
        for field in required_fields:
            if field not in review_data:
                description=f'Missing required field: {field}'    
                dictionary_return = {"status": "400", "headers":  dictionary_header, "body": {"error": description}}
                return dictionary_return
        db.create_document(review_data)
    except CloudantException as cloudant_exception:
        print("unable to connect")
        dictionary_return = {"status": "500", "headers":  dictionary_header, "body": {"error": cloudant_exception}}
        return dictionary_return
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        dictionary_return = {"status": "500", "headers":  dictionary_header, "body": {"error": err}}
        return dictionary_return
    # Save the review data as a new document in the Cloudant database
    dictionary_return = {"status": "200", "headers":  dictionary_header, "body": {"message": "Your review has been posted successfully"}}
    return dictionary_return
