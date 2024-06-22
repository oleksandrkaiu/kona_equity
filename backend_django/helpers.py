from auth_app.models import Profile, Favourite, Visited
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
import smtplib
from django.core.mail import EmailMultiAlternatives
from email.mime.text import MIMEText 
from email.mime.image import MIMEImage 
from email.mime.multipart import MIMEMultipart
import requests
import json


class Chart:
    """ Handle the chart data representation a.k.a Annual Revenue and Employee Count.
    NOTE: Both annual revenue and employee data are up-to-date manually
    correlated to the HubSpot API 2021 data, you may want to add extra fields
    for future new data
    e.g. employee_q1_2021: data.get('properties').get('employee_count_2020_q2'),
    """

    def __init__(self, company_id, data_type=None):
        """ company_id --> integer
        data_type --> string"""

        url = f"https://api.hubapi.com/companies/v2/companies/{company_id}"
        querystring = {"hapikey": "2f0e2171-0a87-413e-81cb-e0435ab583d5"}
        response = requests.get(url=url, params=querystring)
        data = json.loads(response.content)

        self.data_type = data_type
        self.annual_revene = {
            '2019_q1': data.get('properties').get('revenue_2019_q1'),
            '2019_q2': data.get('properties').get('revenue_2019_q2'),
            '2019_q3': data.get('properties').get('revenue_2019_q3'),
            '2019_q4': data.get('properties').get('revenue_2019_q4'),

            '2020_q1': data.get('properties').get('revenue_2020_q1'),
            '2020_q2': data.get('properties').get('revenue_2020_q2'),
            '2020_q3': data.get('properties').get('revenue_2020_q3'),
            '2020_q4': data.get('properties').get('revenue_2020_q4'),
        }

        self.employees = {
            '2019_q1': data.get('properties').get('employee_count_q1_2019'),
            '2019_q2': data.get('properties').get('employee_count_q2_2019'),
            '2019_q3': data.get('properties').get('employee_count_q3_2019'),
            '2019_q4': data.get('properties').get('employee_count_q4_2019'),

            '2020_q1': data.get('properties').get('employee_count_2020_q1'),
            '2020_q2': data.get('properties').get('employee_count_2020_q2'),
            '2020_q3': data.get('properties').get('employee_count_2020_q3'),
            '2020_q4': data.get('properties').get('employee_count_2020_q2'),
        }

    def __extract(self, data):
        for k in data:
            value = data.get(k)
            if value:
                data[k] = value.get('value')

        return data

    def execute(self):
        if self.data_type == 'revenue_data':
            return self.__extract(self.annual_revene)
        elif self.data_type == 'employee_count':
            return self.__extract(self.employees)

def getAuth(request):
    auth = None
    if request.user.is_authenticated:
        try:
            auth = Profile.objects.get(user=request.user).profile_photo
        except Exception as e:
            print(e)
            # auth = None
    return auth

def getFavs(request):
    favourites = []
    if request.user.is_authenticated:
        favourites = Favourite.objects.filter(user=request.user).values_list("company_id", flat=True)
    return favourites

def addToVisited(request, company):
    if request.user.is_authenticated:
        v = Visited.objects.filter(user=request.user, company=company)
        if v.exists():
            v = v[0]
            v.timestamp = timezone.now()
            v.save()
        else:
            Visited.objects.create(user=request.user, company=company)

def createHeadline(industry, g_industry, state, city):
    choose = ""
    if industry:
        choose = str.capitalize(industry)
    elif g_industry:
        choose = str.capitalize(g_industry)

    if choose:
        fHalf = f"{choose} Companies "
        sHalf = f"Find {choose} Companies "
        tHalf = f"{choose} companies "
    else:
        fHalf = f"Company Search "
        sHalf = "Find Companies "
        tHalf = "companies "

    choose = ""
    if state:
        choose = str.capitalize(state)
    if city:
        ch = str.capitalize(city)
        if choose:
            choose = f"{ch}, {choose}"
        else:
            choose = ch

    if choose:
        fHalf += f"in {choose}"
        sHalf += f"in {choose}"
        tHalf += f"in {choose}"
    else:
        fHalf += "in the United States"
        tHalf += "in the United States"
        if not industry and not g_industry:
            sHalf += "in Industry or State"
        else:
            sHalf += "in the United States"

    return fHalf, sHalf, tHalf

def checkPop(session, auth):
    if auth.is_authenticated:
        return False
    if session.get("pop") is None:
        session["pop"] = 1
    if session["pop"] == settings.POPUP_WAIT:
        return True
    session["pop"] += 1
    return False


class MessagesService():
  def __init__(self) -> None:
    pass
      
  @staticmethod 
  def send_email(to_address, subject, body):
      send_mail(
      subject=subject,
      message=body,
      from_email=settings.EMAIL_HOST_USER,
      recipient_list=[to_address],
      fail_silently=False,
    )

  @staticmethod 
  def send_results_data(email):
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'Konaequity Premium'
    msgRoot['From'] = settings.EMAIL_HOST_USER
    msgRoot['To'] = email

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText('Sweellc.')
    msgAlternative.attach(msgText)

    msgText = MIMEText('<br><img src="cid:image1"><br>', 'html')
    msgAlternative.attach(msgText)

    # msgImage = MIMEImage(myfile.read())

    # msgImage.add_header('Content-ID', '<image1>')
    # msgRoot.attach(msgImage)
    

    smtp = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    smtp.sendmail(settings.EMAIL_HOST_USER, email, msgRoot.as_string())
    smtp.quit()

# send_results_data("testaliaxghar@gmail.com")
# MessagesService.send_email("testaliaxghar@gmail.com", "hello", "body")
