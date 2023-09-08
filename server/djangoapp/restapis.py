import requests
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from .models import CarDealer,DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                             params=kwargs)
        if api_key:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                            params=kwargs,auth=HTTPBasicAuth('apikey', api_key))
            
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    state = kwargs.get("state")
    if state:
        json_result = get_request(url, state=state)
    else:
        json_result = get_request(url)

    if json_result:
        # Get the row list in JSON as dealers
        print(json_result)
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # print(dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                   full_name=dealer_doc["full_name"],id=dealer_doc["id"], 
                                   lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],st=dealer_doc["st"], 
                                   zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

    results = []
    dealer_id = dealerId
    json_result = get_request(url, dealership_id=dealer_id)
    if json_result:
        # Get the row list in JSON as reviews
        print(json_result)
        reviews = json_result
        # For each review object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review
            
            # Create a DealerReview object with values in `doc` object
            review_obj = DealerReview(dealership = review_doc["dealership"],name = review_doc["name"],
            purchase = review_doc["purchase"],review = review_doc["review"],
            purchase_date = review_doc["purchase_date"],car_make = review_doc["car_make"],
            car_model = review_doc["car_model"],car_year = review_doc["car_year"],
            id = review_doc["id"])
            review_obj.sentiment =  analyze_review_sentiments(review_doc["review"])
            results.append(review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(review,**kwargs):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

    authenticator = IAMAuthenticator('hOCc4dGDLIQjLxG5uwtnZjBCe0LkUK2kGV81pUf1dTkB')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator)
    print("Text to review is " + review)
    natural_language_understanding.set_service_url('https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/facce2d4-930d-4afc-87af-d8d67f2ef6fa')
    response = natural_language_understanding.analyze(text=review,language='en',
        features=Features(entities=EntitiesOptions(sentiment=True, limit=1),
        keywords=KeywordsOptions(sentiment=True,
                                 limit=1))).get_result()
   
    sentiment = response["keywords"][0]["sentiment"]["label"]
    print("The sentiment is " + sentiment) 
    
    print(json.dumps(response, indent=2))
    return sentiment
    #params = dict()
    #params["text"] = text
    #params["version"] = "2022-04-07"
    #params["features"] = "sentiment"
    #params["return_analyzed_text"] = "true"
    #response = requests.get("https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/facce2d4-930d-4afc-87af-d8d67f2ef6fa", params=params, headers={'Content-Type': 'application/json'},
           #                         auth=HTTPBasicAuth('apikey', "hOCc4dGDLIQjLxG5uwtnZjBCe0LkUK2kGV81pUf1dTkB"))
    #print(response)
    #return response

