from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Company
from .constants import us_state_abbrev, industries
from itertools import product

class Static_Sitemap(Sitemap):
    priority = 1.0
    changefreq = 'monthly'


    def items(self):
        return ['home', 'about', 'contact', 'privacy']

    def location(self, item):
        return reverse(item)

class Company_Sitemap(Sitemap):
    changefreq = "monthly"
    limit = 5000

    def items(self):
        return Company.objects.all().order_by("-g_true").values("identifier", "g_true")

    def priority(self,obj):
        if obj["g_true"] in [7, 8]:
            return 0.8
        else:
            return (obj["g_true"] + 1)/10

    def location(self, obj):
        return "/company/" + obj["identifier"] + "/"

class State_Sitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return list(us_state_abbrev.keys())

    def location(self, obj):
        return f"/find/--{obj}/"

class City_Sitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6
    limit = 50000

    def items(self):
        return Company.objects.all().values_list("city").distinct()

    def location(self, obj):
        return f"/find/?city={obj}"

class Industry_Sitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7
    limit = 50000

    def items(self):
        return list(industries.values())

    def location(self, obj):
        return f"/find/{obj}--/"

class GIndustry_Sitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6
    limit = 50000

    def items(self):
        return Company.objects.all().distinct().values_list("google_industry", flat = True)

    def location(self, obj):
        return f"/find/?google_industry={obj}"

class StateCrossIndustry_Sitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8
    limit = 50000

    def items(self):
        return list(product(list(industries.values()), list(us_state_abbrev.keys())))

    def location(self, obj):
        return f"/find/{obj[0]}-{obj[1]}/"

class StateCrossGIndusrty_Sitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8
    limit = 50000

    def items(self):
        return list(product(list(us_state_abbrev.keys()), list(Company.objects.all().distinct().values_list("google_industry", flat = True))))

    def location(self, obj):
        return f"/find/--{obj[0]}/?google_industry={obj[1]}"