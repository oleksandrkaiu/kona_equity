# This file contains mapping from Hubspot variable names to MySQL column names.
# The mapping is divided according to data types for cleaning and structuring.

import hashlib
from django.conf import settings

ints = {
    "hs_object_id": "id",
    "alexa_rank": "rank",
    "current_employees": "current_employees",
    "g_count": "g_true",
    "g_nope": "g_false",
    "g_total": "g_total",
    "numberofemployees": "num_emp",
    "test1": "test"
}

floats = {
    "alexa_bounce_rate": "bounce_rate",
    "alexa_pageviews_per_visitor": "page_views",
    "annual_revenue_growth_since_founding": "a_revenue_since_founding",
    "employee_growth_rate_from_first_known_quarter_to_current": "emp_growth_first_to_current",
    "revenue_growth_rate_from_first_known_quarter_to_current": "revenue_growth_first_to_current",
    "revenue_per_employee": "revenue_per_employee",
    "variance_of_revenue_growth": "revenue_variance",
    "annualrevenue": "annual_revenue",
    "churn_percentage_6_23": "churn_rate",
    "churn_employees": "churn_employees",
}

bools = {
    "g1": "g1",
    "g2": "g2",
    "g3": "g3",
    "g4": "g4",
    "g5": "g5",
    "g6": "g6",
    "g7": "g7",
    "g8": "g8",
}

strings = {
    "alexa_daily_time": "daily_time",
    "best_private_equity": "best_equity",
    "city": "city",
    "country": "country",
    "current_private_equity": "current_equity",
    "industry": "industry",
    "state": "state",
    "address": "address",
    "address2": "address_2",
    "domain": "domain",
    "google_places_industry": "google_industry",
    "founded_year": "year_founded",
    "description": "description",
    "zip": "postal",
    "categories": "categories",
    "naics": "naics",
    "sic": "sic",
    "facebook_company_page": "fb_page",
    "linkedin_company_page": "li_page",
    "twitterhandle": "twitter_handle",
    "total_money_raised": "t_money_raised"
}

def remove_punc(string):
    '''Removes punctuation from a string
    '''
    punctuations = r'''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for char in punctuations:
        string = string.replace(char, "")
    return string

def validate_request(request):
    '''Validates wether the POST request received at /hook is from Huubspot.
    See https://developers.hubspot.com/docs/api/webhooks/validating-requests for more info.
    '''

    source_string = settings.HUBSPOT_SECRET + request.body.decode('utf-8')
    secure = hashlib.sha256(source_string.encode('utf-8')).hexdigest()
    if secure == str(request.headers.get("X-HubSpot-Signature")):
        return True
    return False
