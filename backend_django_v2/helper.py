import re
from urllib.parse import urlparse
from datetime import datetime
import pytz
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
import threading
import json
import requests

EDIT_KEYS = {
    "summary": ["id", "name", "domain", "identifier", "description", "year_founded"],
    "location": ["id", "name", "identifier", "domain", "city", "state", "address", "postal"],
    "keys": ["id", "identifier", "name", "categories", "industry", "domain", "google_industry", "li_page", "t_money_raised", "fb_page", "sic", "twitter_handle", "naics"],
    "annual_rev": ["id", "name", "domain", "identifier", "revenue_quarter_chart"],
    "Employee Count": ["id", "name", "domain", "identifier", "employee_quarter_chart"],
}

def convert_key(key):
    return key.replace("_", " ").title()

def get_email_user_data(user):
    user_data = []
    if user.email:
        user_data.append(("Email", user.email))
    if user.profile:
        if user.profile.first_name:
            user_data.append(("First Name", user.profile.first_name))
        if user.profile.last_name:
            user_data.append(("Last Name", user.profile.last_name))
    return user_data


def get_time_now(timezone="US/Hawaii"):
    utc_now = pytz.utc.localize(datetime.utcnow())
    local_now = utc_now.astimezone(pytz.timezone(timezone))
    return local_now.strftime("%Y-%m-%d %H:%M:%S")

def get_company_info(company, edit_type):
    fields = EDIT_KEYS[edit_type]
    company_info = []
    for field in fields:
        company_info.append((convert_key(field), str(getattr(company, field))))
    company_info.append(("URL", reverse('backend_django_v2:company', args=[company.identifier])))
    return company_info


def get_contact_info(company_id):
    contact_info = []
    apiKey = '2f0e2171-0a87-413e-81cb-e0435ab583d5'
    associationUri = 'https://api.hubapi.com/crm-associations/v1/associations/' + str(company_id)
    associationUri = associationUri + '/HUBSPOT_DEFINED/2?hapikey=' + apiKey
    associatedContactResponse = requests.get(associationUri)
    if associatedContactResponse.content:
        contactIdPayload = json.loads(associatedContactResponse.content)
        if contactIdPayload and contactIdPayload['results'] and len(contactIdPayload['results']) > 0:
            contactIds = contactIdPayload['results']
            for contactId in contactIds:
                firstName = ''
                lastName = ''
                jobTitle = ''
                email = ''
                contactUri = 'https://api.hubapi.com/contacts/v1/contact/vid/' + str(contactId) + '/profile?hapikey=' + apiKey
                contactResponse = requests.get(contactUri)
                contactPayload = json.loads(contactResponse.content)
                try:
                    if contactPayload['properties']['firstname']:
                        firstName = contactPayload['properties']['firstname']['value']
                    if contactPayload['properties']['email']:
                        email = contactPayload['properties']['email']['value']
                    if contactPayload['properties']['lastname']:
                        lastName = contactPayload['properties']['lastname']['value']
                    if contactPayload['properties']['jobtitle'] and contactPayload['properties']['jobtitle']['value'] != 'No Title Available':
                        jobTitle = contactPayload['properties']['jobtitle']['value']
                    if firstName and lastName and jobTitle:
                        contact_info.append({'firstName': firstName, 'lastName': lastName, 'email':email, 'jobTitle': jobTitle, 'contactId': contactId})
                except:
                    pass

    return contact_info

# print(get_contact_info(company_id))


def send_edit_email(sub, body, from_email, to, html):
    if html:
        send_mail(
            sub,
            body,
            from_email,
            [to],
            html_message=body,
        )
    else:
        send_mail(
            sub,
            body,
            from_email,
            [to],
        )


def send_edit_email_thread(sub, body, from_email, to, html):
    thread = threading.Thread(target=send_edit_email, args=(sub, body, from_email, to, html), daemon=True)
    thread.start()

def format_url(url):
    if not re.match('(?:http|ftp|https)://', url):
        return 'https://{}'.format(url)
    return url

def get_domain(url):
    url = format_url(url)
    try:
        return urlparse(url).netloc
    except:
        return None

def get_email_domain(email):
    try:
        return re.search('@((\w|\w[\w\-]*?\w)\.\w+)', email).group(1)
    except:
        return None
