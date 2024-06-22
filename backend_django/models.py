from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .utils import human_format, returnEpirationDate, defaultValues, defaultCompetitorValues
from django.utils import timezone
import json
import sys
from django.contrib.auth.models import User

# This model should be in auth_app but because of a db conflict that's impossible to do now
# This model serves to store email verification tokens in order to let people verify their emails from
# a different browser than the one they initially signed up with
class Verification(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)

class Company(models.Model):

    id = models.BigIntegerField(primary_key = True)
    name = models.CharField(max_length = 255, null = True, db_index = True)
    identifier = models.CharField(max_length = 255, null = True, db_index = True)
    domain = models.CharField(max_length = 255, null = True, db_index = True)
    year_founded = models.CharField(max_length = 8, null = True, db_index = True)
    description = models.TextField(null = True)
    address_2 = models.CharField(max_length = 500, null = True)
    address = models.CharField(max_length = 500, null = True)
    city = models.CharField(max_length = 255, null = True, db_index = True)
    state = models.CharField(max_length = 255, null = True, db_index = True)
    postal = models.CharField(max_length = 100, null = True)
    country = models.CharField(max_length = 255, null = True, db_index = True)
    industry = models.CharField(max_length = 255, null = True, db_index = True)
    google_industry = models.CharField(max_length = 255, null = True, db_index = True)
    current_equity = models.CharField(max_length = 255, null = True)
    best_equity = models.CharField(max_length = 255, null = True)
    categories = models.CharField(max_length = 255, null = True, db_index = True)
    bounce_rate = models.FloatField(null = True)
    daily_time = models.CharField(max_length = 200, null = True)
    page_views = models.FloatField(null = True)
    rank = models.BigIntegerField(null = True)
    is_public = models.BooleanField(null = True)
    naics = models.CharField(max_length = 200, null = True)
    sic = models.CharField(max_length = 200, null = True)
    fb_page = models.CharField(max_length = 1000, null = True)
    twitter_handle = models.CharField(max_length = 1000, null = True)
    li_page = models.CharField(max_length = 1000, null = True)
    t_money_raised = models.CharField(max_length = 200, null = True)
    competitors = models.JSONField(default = defaultCompetitorValues)
    g1 = models.BooleanField(null = True)
    g2 = models.BooleanField(null = True)
    g3 = models.BooleanField(null = True)
    g4 = models.BooleanField(null = True)
    g5 = models.BooleanField(null = True)
    g6 = models.BooleanField(null = True)
    g7 = models.BooleanField(null = True)
    g8 = models.BooleanField(null = True)
    g_true = models.IntegerField(validators=[MaxValueValidator(8), MinValueValidator(0)], db_index = True, default = 0)
    g_false = models.IntegerField(validators=[MaxValueValidator(8), MinValueValidator(0)], default = 0)
    g_total = models.IntegerField(validators=[MaxValueValidator(8), MinValueValidator(0)], default = 0)
    annual_revenue = models.FloatField(null = True, db_index = True)
    num_emp = models.BigIntegerField(null = True, db_index = True)
    churn_employees = models.FloatField(null = True)
    churn_rate = models.FloatField(null = True)
    revenue_per_employee = models.FloatField(null = True)
    revenue_variance = models.FloatField(null = True)
    a_revenue_since_founding = models.FloatField(null = True)
    revenue_growth_first_to_current = models.FloatField(null = True)
    emp_growth_first_to_current = models.FloatField(null = True)
    current_employees = models.IntegerField(null = True)
    revenue_quarter_chart = models.JSONField(default = defaultValues)
    employee_quarter_chart = models.JSONField(default = defaultValues)
    is_premium = models.BooleanField(default = False, db_index = True)
    is_disabled = models.BooleanField(default = False, db_index = True)
    test = models.IntegerField(null = True, db_index = True)
    last_modified = models.JSONField(default = defaultValues)

    class Meta:
        ordering = ('annual_revenue',)

    def setValue(self, field, value, occuredAt):
        '''Updates fields according to data received from Hubspot. Since data received from Hubspot is not ordered, timestamps are saved.
        '''
        lmod = self.last_modified
        if field in lmod:
            timestamp = lmod[field]
        else:
            timestamp = 0

        if occuredAt > timestamp:
            self.__dict__[field] = value
            lmod.update(
                {
                    field: occuredAt
                }
            )
            self.last_modified = lmod

    def updateModifiedTime(self, field, occuredAt):
        '''Updates modified time for a specific field.
        '''
        self.last_modified.update({
            field: occuredAt
            })

    def __str__(self):
        if self.year_founded:
            return str(f"{self.name} founded in {self.year_founded}")
        else:
            return str(self.name)

    def banner(self):
        '''Text to be displayed in popup
        '''
        if len(self.name) <= 30:
            return f"Get updates on {self.name}"
        else:
            return f"Get updates on this company"

    def addr(self):
        '''Address for heading
        '''
        if self.city and self.state:
            return f"{self.city}, {self.state}"
        elif self.state:
            return self.state
        elif self.city:
            return self.city
        else:
            return None

    def keyInfo(self):
        key = {}
        back = ["name", "categories", "industry", "domain", "google_industry", "li_page", "t_money_raised", "fb_page", "sic", "twitter_handle", "naics"]
        front = ["Name", "Tags", "Category", "Website", "Industry", "LinkedIn", "Funding Amount", "Facebook", "SIC", "Twitter", "NAICS"]
        for i in range(len(back)):
            if self.__dict__[back[i]]:
                key[front[i]] = self.__dict__[back[i]]
        if key.get("Website"):
            key["Website"] = "https://www." + key["Website"]
        if key.get("Tags", None):
            key["splitTags"] = key["Tags"].split(";")
        return key

    def cleanForFront(self):
        '''Cleaning required for P3
        '''
        if self.annual_revenue:
            self.annual_revenue = int(self.annual_revenue)

        if self.a_revenue_since_founding:
            self.a_revenue_since_founding = int(self.a_revenue_since_founding)

        if self.revenue_per_employee:
            self.revenue_per_employee = int(self.revenue_per_employee)

        if(self.address is None):
            self.address = ""
        if(self.address_2 is None):
            self.address_2 = ""

        if not self.daily_time:
            self.daily_time = "-"

        if self.rank:
            self.rank = human_format(self.rank)
        else:
            self.rank = "-"

        if self.bounce_rate:
            self.bounce_rate = str(self.bounce_rate) + " %"
        else:
            self.bounce_rate = "-"

        if self.revenue_variance:
            self.revenue_variance = round(float(self.revenue_variance), 2)
        else:
            self.revenue_variance = "-"

        if not self.churn_employees:
            self.churn_employees = "-"

        else:
            self.churn_employees = int(self.churn_employees)

        if self.churn_rate:
            self.churn_rate = round(float(self.churn_rate), 2)
        else:
            self.churn_rate = "-"

        if self.revenue_growth_first_to_current:
            self.revenue_growth_first_to_current = round(float(self.revenue_growth_first_to_current) * 100, 1)
        else:
            self.revenue_growth_first_to_current = "-"

        if self.emp_growth_first_to_current:
            self.emp_growth_first_to_current = round(float('%.3f'%(self.emp_growth_first_to_current)) * 100, 1)
        else:
            self.emp_growth_first_to_current = "-"

        if self.industry:
            self.industry = str.capitalize(" ".join(str.lower(self.industry).split("_")))

        if not self.current_employees:
            self.current_employees = "-"

        if not self.page_views:
            self.page_views = "-"

        return self

class CompanyLike(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    company = models.ForeignKey(Company, on_delete = models.CASCADE)
    date_added = models.DateTimeField(default = timezone.now)
    liked= models.BooleanField(default = True)


class IP(models.Model):
    id = models.AutoField(primary_key=True)
    ip_addr = models.GenericIPAddressField(db_index=True, unique=False)
    state = models.CharField(db_index=True, unique=False, max_length=60, null=True)
    city = models.CharField(db_index=True, unique=False, max_length=600, null=True)
    expiration = models.DateTimeField(default=returnEpirationDate)

    def __str__(self):
        return str(f"{self.ip_addr}: {self.state}. Expires on {str(self.expiration)}")

    def hasExpired(self):
        if timezone.now() > self.expiration:
            return True
        return False

class Tasks(models.Model):
    id = models.AutoField(primary_key=True)
    arg = models.TextField(null = True)

    def to_list(self):
        try:
            return json.loads(self.arg)
        except Exception as e:
            print("Webhook JSON parsing exception", e, file=sys.stderr)
            return []
