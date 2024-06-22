from multiprocessing import context
from .constants import us_state_abbrev, industries, g_names, g_descriptions, g_colors, g_8_col, g_7_col, continents, links, ilinks, purposes, dropdown_content, strengthAndWeaknesses
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import human_format, sort_data, assemblePagination, createPageBook, convert_to_localtime, createPager
from django.core.cache import cache
from urllib.parse import unquote, quote
from .hubspot import validate_request
from django.shortcuts import redirect, render
from .tasks import sendEmail
import pycountry_convert as pc
from django.db.models import Q
from auth_app.models import Favourite, Profile
from django.contrib.auth.models import User
from .ip import getStateFromIp
from .forms import ContactForm
from functools import reduce
from .models import Company, Tasks
from random import shuffle
from ratelimit.decorators import ratelimit
from .helpers import MessagesService
import stripe
import sys
import os
import json

import re
from difflib import SequenceMatcher
from difflib import get_close_matches
from imdb.utils import normalizeName, normalizeTitle, build_title, \
    build_name, analyze_name, analyze_title, \
                        canonicalTitle, canonicalName, re_titleRef, \
                        build_company_name, re_episodes, _unicodeArticles, \
                        analyze_company_name, re_year_index, re_nameRef

from pathlib import Path
from django.conf import settings
from .helpers import getAuth, getFavs, addToVisited, createHeadline, checkPop

from django.core.paginator import Paginator
# from .pagination import FasterCountPaginator

from watson import search as watson

from django.db import connection

#new imports 02/05/2022
from allauth.account.models import EmailAddress

#new imports 03/05/2022
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password


@ratelimit(key='ip', block=True, rate='200/m', method=ratelimit.ALL)
def home(request):
    # Get 20 randomnly shuffled companies with g_score = 8
    res = cache.get("home.top")
    if not res:
        results = Company.objects.filter(g_true=8)
        res = list(results.values("id", "name", "domain", "annual_revenue", "num_emp", "identifier"))
        shuffle(res)
        res = res[:25]
        cache.set("home.top", res, settings.EXP_WARM)

    # Determine wether these companies are in the watchlist of the user
    favourites = getFavs(request)

    for i in res:
        i["annual_revenue"] = human_format(i["annual_revenue"])
        i["num_emp"] = human_format(i["num_emp"])
        if i["id"] in favourites:
            i["fav"] = True
        else:
            i["fav"] = False

    connection.close()
    return render(request, 'home.html', {'top': res, 'links': links, 'ilinks': ilinks, 'dc':dropdown_content, 'rauth': getAuth(request), 'pop': checkPop(request.session, request.user)})

@ratelimit(key='ip', block=True, rate='50/m', method=ratelimit.ALL)
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        ip = request.META.get('HTTP_X_REAL_IP')
        ua = request.META.get('HTTP_USER_AGENT')
        if form.is_valid():
            if not form.is_spam(ip, ua):
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                purpose = purposes[form.cleaned_data['purpose']]
                message = form.cleaned_data['message']
                subject = f"Contact request by {name} ({email}) for {purpose}"
                body = f'''
                    *** This is an automatically generated message.***

                    Contact Request Sender Information:

                    Name: {name}
                    Email Address: {email}
                    Purpose: {purpose}
                    Message: {message}
                '''
                sendEmail({
                    "subject": subject,
                    "message": body
                })
                connection.close()
                return render(request, "contact-us.html", {"submitted": 1, 'dc':dropdown_content, "rauth": getAuth(request), 'pop': checkPop(request.session, request.user)})
            else:
                connection.close()
                return render(request, "contact-us.html", {"submitted": 2, 'dc':dropdown_content, "rauth": getAuth(request), 'pop': checkPop(request.session, request.user)})
        else:
            connection.close()
            return render(request, "contact-us.html", {"submitted": 3, 'dc':dropdown_content, "rauth": getAuth(request), 'pop': checkPop(request.session, request.user)})
    connection.close()
    return render(request, "contact-us.html", {'submitted': 0, 'dc':dropdown_content, "rauth": getAuth(request), 'pop': checkPop(request.session, request.user)})

@ratelimit(key='ip', block=True, rate='50/m', method=ratelimit.ALL)
def privacy(request):
    connection.close()
    return render(request, 'privacy-policy.html', {'dc':dropdown_content, "rauth": getAuth(request), 'pop': checkPop(request.session, request.user)})

@ratelimit(key='ip', block=True, rate='50/m', method=ratelimit.ALL)
def new(request):
    connection.close()
    return render(request, 'new.html', {'dc':dropdown_content, "rauth": getAuth(request), 'pop': checkPop(request.session, request.user)})

@ratelimit(key='ip', block=True, rate='50/m', method=ratelimit.ALL)
def watch(request):
    connection.close()
    return render(request, 'watch.html', {'dc':dropdown_content, "rauth": getAuth(request), 'pop': checkPop(request.session, request.user)})

@ratelimit(key='ip', block=True, rate='50/m', method=ratelimit.ALL)
def pricing(request):
    connection.close()
    return render(request, 'pricing.html', {'dc':dropdown_content, "rauth": getAuth(request), 'pop': checkPop(request.session, request.user)})

@ratelimit(key='ip', block=True, rate='100/m', method=ratelimit.ALL)
def about(request):
    CALL_IN = settings.MAX_ACCORDION_RESULTS
    state = getStateFromIp(request)[0]
    favourites = getFavs(request)
    result = cache.get("about." + state)
    if result:
        q = result
    else:
        show = us_state_abbrev[state]
        data_get = ["id", "name", "domain", "annual_revenue", "num_emp", "identifier"]
        res = cache.get("home.top")
        if not res:
            results = Company.objects.filter(g_true=8)
            res = list(results.values(*data_get))
            shuffle(res)
        res = res[:CALL_IN]
        q = [
            {
                "text": "What are the most healthy, profitable growing companies?",
                "target": res
            },
            {
                "text": f"What are the most healthy, profitable growing companies in {show}?",
                "target": Company.objects.filter(state=state).order_by("-g_true").values(*data_get)[:CALL_IN]
            },
            {
                "text": f"What are the most healthy, profitable growing software companies in {show}?",
                "target": Company.objects.filter(state=state, industry="Computer Software").order_by("-g_true").values(*data_get)[:CALL_IN]
            },
            {
                "text": f"Which software companies in {show} generate the most revenue?",
                "target": Company.objects.filter(state=state, industry="Computer Software").order_by("-annual_revenue").values(*data_get)[:CALL_IN]
            },
            {
                "text": f"Which software companies in {show} have the most employees?",
                "target": Company.objects.filter(state=state, industry="Computer Software").order_by("-num_emp").values(*data_get)[:CALL_IN]
            }
        ]
        for i in q:
            for j in i["target"]:
                j["annual_revenue"] = human_format(j["annual_revenue"])
                j["num_emp"] = human_format(j["num_emp"])
        cache.set("about." + state, q, settings.EXP_COLD)

    # determine favourites
    for i in q:
        for j in i["target"]:
            j["fav"] = False
            if j["id"] in favourites:
                j["fav"] = True
    connection.close()
    return render(request, "about.html", {'ex': q, 'dc':dropdown_content, "rauth": getAuth(request), 'pop': checkPop(request.session, request.user)})

@ratelimit(key='ip', block=True, rate='200/m', method=ratelimit.ALL)
def company(request, id):
    try:
        company = Company.objects.get(identifier=id)
        addToVisited(request, company)
        company = company.cleanForFront()
        buffer = dict()
        buffer["g_data"] = []
        for i in range(0,8):
            if(company.__dict__["g"+str(i+1)]):
                temp_dict = dict()
                temp_dict["name"]= g_names[i]
                temp_dict["desc"]= g_descriptions[i]
                buffer["g_data"].append(temp_dict)

        if company.g_true <=6:
            setter = g_colors
        elif company.g_true ==7:
            setter = g_7_col
        else:
            setter = g_8_col
        for i in range(0, int(company.g_true)):
            buffer["g_data"][i]["color"] = setter[i]

        data = sort_data(company.revenue_quarter_chart, company.annual_revenue)
        if len(data) > 0:
            buffer["cs_chart_labels"]= data[0]
        if len(data) > 1:
            buffer["cs_chart_data"]= data[1]
        if len(data) > 2:
            buffer["go_revenue"] = data[2]

        data = sort_data(company.employee_quarter_chart, company.num_emp)
        if len(data) > 0:
            buffer["e_chart_labels"] = data[0]
        if len(data) > 1:
            buffer["e_chart_data"] = data[1]
        if len(data) > 2:
            buffer["go_employee"] = data[2]
        go = {}

        if company.google_industry:
            go["google"] = quote("__".join(company.google_industry.split("/")))

        if company.industry:
            buffer["fInd"] = company.industry
            keyword = buffer["fInd"]
            namelist = [keyword, keyword.replace(" ", "_")]
            namelist = list(set(namelist))
            q_list = map(lambda n: Q(**{"industry__iexact":n}), namelist)
            q_list = reduce(lambda a, b: a | b, q_list)
            buffer["fIndCount"] = Company.objects.filter(q_list).count() - 1
            go["industry"] = str.lower(quote("-".join("__".join(company.industry.split("/")).split(" "))))
            buffer["fGo"] = "/find/" + go["industry"] + "--/"
        elif company.google_industry:
            buffer["fInd"] = company.google_industry
            keyword = buffer["fInd"]
            namelist = [keyword, keyword.replace(" ", "_")]
            namelist = list(set(namelist))
            q_list = map(lambda n: Q(**{"google_industry__iexact":n}), namelist)
            q_list = reduce(lambda a, b: a | b, q_list)
            buffer["fIndCount"] = Company.objects.filter(q_list).count() - 1
            buffer["fGo"] = "/find/?google_industry=" + go["google"]
        else:
            buffer["fInd"] = None
            buffer["fIndCount"] = None
            buffer["fGo"] = None
        if buffer["fIndCount"] == 1:
            buffer["ftag"] = "company"
        else:
            buffer["ftag"] = "companies"

        if company.state:
            try:
                go["state"] = us_state_abbrev[company.state]
            except:
                go["state"] = company.state.capitalize()

        # competitors
        comp = []
        comp_ids = [a["id"] for a in company.competitors.values() if isinstance(a["id"], int)]
        if comp_ids:
            comp = Company.objects.filter(id__in=comp_ids).extra(select={'manual': 'FIELD(id,%s)' % ','.join(map(str, comp_ids))},\
                                                     order_by=['manual']).values("name", "identifier", "domain")

        # strengths and weaknesses
        sng, wek = strengthAndWeaknesses(company)

        # Key Information
        keys = company.keyInfo()

        # last modified time
        lmod = list(company.last_modified.values())
        if len(lmod) > 0:
            lmod = max(lmod)
            buffer["lmod"] = convert_to_localtime(lmod)
        else:
            buffer["lmod"] = "09/05/2020"

        # determine if favourites
        company.fav = False
        try:
            if Favourite.objects.filter(company__id=company.id)[:1]:
                company.fav = True
        except:
            pass

        try:
            country = company.country
            if country == "EU":
                continent = "Europe"
            elif country:
                country_code = pc.country_name_to_country_alpha2(country, cn_name_format="default")
                continent_code = pc.country_alpha2_to_continent_code(country_code)
                continent = continents[continent_code]
                continent = continent.replace(" ", "_")
            else:
                continent = "North America"
        except Exception:
            continent = "N/A"

        def revenue_abbreviation():
            """ Convert annual revenue into abbreviation. EX: 13200000.0 into 13.2M"""

            K = 1000
            K_10 = 10_000
            K_100 = 100_000
            M = 1000_000
            M_10 = 10_000_000
            B = 1000_000_000

            company = Company.objects.get(identifier=id)
            revene = company.annual_revenue

            # No Value
            if revene is None:
                return

            # Less than K alike.
            elif revene < K:
                return revene
            # 1K alike.
            elif revene >= K and revene < K_10:
                revene = str(revene)[:1]
                return revene + ' Thousand Revenue'
            # 34K alike.
            elif revene >= K_10 and revene < K_100:
                revene = str(revene)[:2]
                return revene + ' Thousand Revenue'
            # 340K alike.
            elif revene >= K_100 and revene < M:
                revene = str(revene)[:3]
                return revene + ' Thousand Revenue'
            # 23M alike.
            elif revene >= M and revene < M_10:
                revene = str(revene)[:2]
                return (revene[:1] + '.') + revene[1:] + ' Million Revenue'
            # 230M alike.
            elif revene >= M_10 and revene < B:
                revene = str(revene)[:3]
                return (revene[:2] + '.') + revene[2:] + ' Million Revenue'
            # 2B alike.
            elif revene >= B:
                revene = str(revene)[:2]
                return (revene[:1] + '.') + revene[1:] + ' Billion Revenue'

        connection.close()
        return render(request, 'summary.html', {"company": company, 'revenue_abbreviation': revenue_abbreviation(), "continent": continent, "buffer":buffer, 'dc':dropdown_content,\
                        'rauth': getAuth(request), 'pop': checkPop(request.session, request.user), 'comps': comp, 'sng': sng,\
                        'wek': wek, 'keys': keys, 'go': go})
    except Company.DoesNotExist:
        connection.close()
        return HttpResponseNotFound('<h1>Company does not exist</h1>')

@ratelimit(key='ip', block=True, rate='200/m', method=ratelimit.ALL)
def annualrevenue(request, id):
    try:
        company = Company.objects.get(identifier=id)
        addToVisited(request, company)
        company = company.cleanForFront()
        buffer = dict()
        buffer["g_data"] = []
        for i in range(0,8):
            if(company.__dict__["g"+str(i+1)]):
                temp_dict = dict()
                temp_dict["name"]= g_names[i]
                temp_dict["desc"]= g_descriptions[i]
                buffer["g_data"].append(temp_dict)

        if company.g_true <=6:
            setter = g_colors
        elif company.g_true ==7:
            setter = g_7_col
        else:
            setter = g_8_col
        for i in range(0, int(company.g_true)):
            buffer["g_data"][i]["color"] = setter[i]

        data = sort_data(company.revenue_quarter_chart, company.annual_revenue)
        buffer["cs_chart_labels"]= data[0]
        buffer["cs_chart_data"]= data[1]
        buffer["go_revenue"] = data[2]
        data = sort_data(company.employee_quarter_chart, company.num_emp)
        buffer["e_chart_labels"] = data[0]
        buffer["e_chart_data"] = data[1]
        buffer["go_employee"] = data[2]
        go = {}

        if company.google_industry:
            go["google"] = quote("__".join(company.google_industry.split("/")))

        if company.industry:
            buffer["fInd"] = company.industry
            keyword = buffer["fInd"]
            namelist = [keyword, keyword.replace(" ", "_")]
            namelist = list(set(namelist))
            q_list = map(lambda n: Q(**{"industry__iexact":n}), namelist)
            q_list = reduce(lambda a, b: a | b, q_list)
            buffer["fIndCount"] = Company.objects.filter(q_list).count() - 1
            go["industry"] = str.lower(quote("-".join("__".join(company.industry.split("/")).split(" "))))
            buffer["fGo"] = "/find/" + go["industry"] + "--/"
        elif company.google_industry:
            buffer["fInd"] = company.google_industry
            keyword = buffer["fInd"]
            namelist = [keyword, keyword.replace(" ", "_")]
            namelist = list(set(namelist))
            q_list = map(lambda n: Q(**{"google_industry__iexact":n}), namelist)
            q_list = reduce(lambda a, b: a | b, q_list)
            buffer["fIndCount"] = Company.objects.filter(q_list).count() - 1
            buffer["fGo"] = "/find/?google_industry=" + go["google"]
        else:
            buffer["fInd"] = None
            buffer["fIndCount"] = None
            buffer["fGo"] = None
        if buffer["fIndCount"] == 1:
            buffer["ftag"] = "company"
        else:
            buffer["ftag"] = "companies"

        if company.state:
            go["state"] = us_state_abbrev[company.state]

        # competitors
        comp = [a["id"] for a in company.competitors.values()]
        comp = Company.objects.filter(id__in=comp).extra(select={'manual': 'FIELD(id,%s)' % ','.join(map(str, comp))},\
                                                     order_by=['manual']).values("name", "identifier", "domain")

        # strengths and weaknesses
        sng, wek = strengthAndWeaknesses(company)

        # Key Information
        keys = company.keyInfo()

        # determine if favourites
        company.fav = False
        try:
            Favourite.objects.get(company__id=company.id)
            company.fav = True
        except Favourite.DoesNotExist:
            pass

        country = company.country
        if country == "EU":
            continent = "Europe"
        elif country:
            country_code = pc.country_name_to_country_alpha2(country, cn_name_format="default")
            continent_code = pc.country_alpha2_to_continent_code(country_code)
            continent = continents[continent_code]
            continent = continent.replace(" ", "_")
        else:
            continent = "North America"
        connection.close()
        return render(request, 'annualrevenue.html', {"company": company, "continent": continent, "buffer":buffer, 'dc':dropdown_content,\
                        'rauth': getAuth(request), 'pop': checkPop(request.session, request.user), 'comps': comp, 'sng': sng,\
                        'wek': wek, 'keys': keys, 'go': go})
    except Company.DoesNotExist:
        connection.close()
        return HttpResponseNotFound('<h1>Company does not exist</h1>')


@ratelimit(key='ip', block=True, rate='200/m', method=ratelimit.ALL)
def Gscore(request, id):
    try:
        company = Company.objects.get(identifier=id)
        addToVisited(request, company)
        company = company.cleanForFront()
        buffer = dict()
        buffer["g_data"] = []
        for i in range(0,8):
            if(company.__dict__["g"+str(i+1)]):
                temp_dict = dict()
                temp_dict["name"]= g_names[i]
                temp_dict["desc"]= g_descriptions[i]
                buffer["g_data"].append(temp_dict)

        if company.g_true <=6:
            setter = g_colors
        elif company.g_true ==7:
            setter = g_7_col
        else:
            setter = g_8_col
        for i in range(0, int(company.g_true)):
            buffer["g_data"][i]["color"] = setter[i]

        data = sort_data(company.revenue_quarter_chart, company.annual_revenue)
        buffer["cs_chart_labels"]= data[0]
        buffer["cs_chart_data"]= data[1]
        buffer["go_revenue"] = data[2]
        data = sort_data(company.employee_quarter_chart, company.num_emp)
        buffer["e_chart_labels"] = data[0]
        buffer["e_chart_data"] = data[1]
        buffer["go_employee"] = data[2]
        go = {}

        if company.google_industry:
            go["google"] = quote("__".join(company.google_industry.split("/")))

        if company.industry:
            buffer["fInd"] = company.industry
            keyword = buffer["fInd"]
            namelist = [keyword, keyword.replace(" ", "_")]
            namelist = list(set(namelist))
            q_list = map(lambda n: Q(**{"industry__iexact":n}), namelist)
            q_list = reduce(lambda a, b: a | b, q_list)
            buffer["fIndCount"] = Company.objects.filter(q_list).count() - 1
            go["industry"] = str.lower(quote("-".join("__".join(company.industry.split("/")).split(" "))))
            buffer["fGo"] = "/find/" + go["industry"] + "--/"
        elif company.google_industry:
            buffer["fInd"] = company.google_industry
            keyword = buffer["fInd"]
            namelist = [keyword, keyword.replace(" ", "_")]
            namelist = list(set(namelist))
            q_list = map(lambda n: Q(**{"google_industry__iexact":n}), namelist)
            q_list = reduce(lambda a, b: a | b, q_list)
            buffer["fIndCount"] = Company.objects.filter(q_list).count() - 1
            buffer["fGo"] = "/find/?google_industry=" + go["google"]
        else:
            buffer["fInd"] = None
            buffer["fIndCount"] = None
            buffer["fGo"] = None
        if buffer["fIndCount"] == 1:
            buffer["ftag"] = "company"
        else:
            buffer["ftag"] = "companies"

        if company.state:
            go["state"] = us_state_abbrev[company.state]

        # competitors
        comp = [a["id"] for a in company.competitors.values()]
        comp = Company.objects.filter(id__in=comp).extra(select={'manual': 'FIELD(id,%s)' % ','.join(map(str, comp))},\
                                                     order_by=['manual']).values("name", "identifier", "domain")

        # strengths and weaknesses
        sng, wek = strengthAndWeaknesses(company)

        # Key Information
        keys = company.keyInfo()

        # determine if favourites
        company.fav = False
        try:
            Favourite.objects.get(company__id=company.id)
            company.fav = True
        except Favourite.DoesNotExist:
            pass

        country = company.country
        if country == "EU":
            continent = "Europe"
        elif country:
            country_code = pc.country_name_to_country_alpha2(country, cn_name_format="default")
            continent_code = pc.country_alpha2_to_continent_code(country_code)
            continent = continents[continent_code]
            continent = continent.replace(" ", "_")
        else:
            continent = "North America"
        connection.close()
        return render(request, 'Gscore.html', {"company": company, "continent": continent, "buffer":buffer, 'dc':dropdown_content,\
                        'rauth': getAuth(request), 'pop': checkPop(request.session, request.user), 'comps': comp, 'sng': sng,\
                        'wek': wek, 'keys': keys, 'go': go})
    except Company.DoesNotExist:
        connection.close()
        return HttpResponseNotFound('<h1>Company does not exist</h1>')

@ratelimit(key='ip', block=True, rate='200/m', method=ratelimit.ALL)
def webanalysis(request, id):
    try:
        company = Company.objects.get(identifier=id)
        addToVisited(request, company)
        company = company.cleanForFront()
        buffer = dict()
        buffer["g_data"] = []
        for i in range(0,8):
            if(company.__dict__["g"+str(i+1)]):
                temp_dict = dict()
                temp_dict["name"]= g_names[i]
                temp_dict["desc"]= g_descriptions[i]
                buffer["g_data"].append(temp_dict)

        if company.g_true <=6:
            setter = g_colors
        elif company.g_true ==7:
            setter = g_7_col
        else:
            setter = g_8_col
        for i in range(0, int(company.g_true)):
            buffer["g_data"][i]["color"] = setter[i]

        data = sort_data(company.revenue_quarter_chart, company.annual_revenue)
        buffer["cs_chart_labels"]= data[0]
        buffer["cs_chart_data"]= data[1]
        buffer["go_revenue"] = data[2]
        data = sort_data(company.employee_quarter_chart, company.num_emp)
        buffer["e_chart_labels"] = data[0]
        buffer["e_chart_data"] = data[1]
        buffer["go_employee"] = data[2]
        go = {}

        if company.google_industry:
            go["google"] = quote("__".join(company.google_industry.split("/")))

        if company.industry:
            buffer["fInd"] = company.industry
            keyword = buffer["fInd"]
            namelist = [keyword, keyword.replace(" ", "_")]
            namelist = list(set(namelist))
            q_list = map(lambda n: Q(**{"industry__iexact":n}), namelist)
            q_list = reduce(lambda a, b: a | b, q_list)
            buffer["fIndCount"] = Company.objects.filter(q_list).count() - 1
            go["industry"] = str.lower(quote("-".join("__".join(company.industry.split("/")).split(" "))))
            buffer["fGo"] = "/find/" + go["industry"] + "--/"
        elif company.google_industry:
            buffer["fInd"] = company.google_industry
            keyword = buffer["fInd"]
            namelist = [keyword, keyword.replace(" ", "_")]
            namelist = list(set(namelist))
            q_list = map(lambda n: Q(**{"google_industry__iexact":n}), namelist)
            q_list = reduce(lambda a, b: a | b, q_list)
            buffer["fIndCount"] = Company.objects.filter(q_list).count() - 1
            buffer["fGo"] = "/find/?google_industry=" + go["google"]
        else:
            buffer["fInd"] = None
            buffer["fIndCount"] = None
            buffer["fGo"] = None
        if buffer["fIndCount"] == 1:
            buffer["ftag"] = "company"
        else:
            buffer["ftag"] = "companies"

        if company.state:
            go["state"] = us_state_abbrev[company.state]

        # competitors
        comp = [a["id"] for a in company.competitors.values()]
        comp = Company.objects.filter(id__in=comp).extra(select={'manual': 'FIELD(id,%s)' % ','.join(map(str, comp))},\
                                                     order_by=['manual']).values("name", "identifier", "domain")

        # strengths and weaknesses
        sng, wek = strengthAndWeaknesses(company)

        # Key Information
        keys = company.keyInfo()

        # determine if favourites
        company.fav = False
        try:
            Favourite.objects.get(company__id=company.id)
            company.fav = True
        except Favourite.DoesNotExist:
            pass

        country = company.country
        if country == "EU":
            continent = "Europe"
        elif country:
            country_code = pc.country_name_to_country_alpha2(country, cn_name_format="default")
            continent_code = pc.country_alpha2_to_continent_code(country_code)
            continent = continents[continent_code]
            continent = continent.replace(" ", "_")
        else:
            continent = "North America"
        connection.close()
        return render(request, 'webanalysis.html', {"company": company, "continent": continent, "buffer":buffer, 'dc':dropdown_content,\
                        'rauth': getAuth(request), 'pop': checkPop(request.session, request.user), 'comps': comp, 'sng': sng,\
                        'wek': wek, 'keys': keys, 'go': go})
    except Company.DoesNotExist:
        connection.close()
        return HttpResponseNotFound('<h1>Company does not exist</h1>')

@ratelimit(key='ip', block=True, rate='200/m', method=ratelimit.ALL)
def keyinformation(request, id):
    try:
        company = Company.objects.get(identifier=id)
        addToVisited(request, company)
        company = company.cleanForFront()
        buffer = dict()
        buffer["g_data"] = []
        for i in range(0,8):
            if(company.__dict__["g"+str(i+1)]):
                temp_dict = dict()
                temp_dict["name"]= g_names[i]
                temp_dict["desc"]= g_descriptions[i]
                buffer["g_data"].append(temp_dict)

        if company.g_true <=6:
            setter = g_colors
        elif company.g_true ==7:
            setter = g_7_col
        else:
            setter = g_8_col
        for i in range(0, int(company.g_true)):
            buffer["g_data"][i]["color"] = setter[i]

        data = sort_data(company.revenue_quarter_chart, company.annual_revenue)
        buffer["cs_chart_labels"]= data[0]
        buffer["cs_chart_data"]= data[1]
        buffer["go_revenue"] = data[2]
        data = sort_data(company.employee_quarter_chart, company.num_emp)
        buffer["e_chart_labels"] = data[0]
        buffer["e_chart_data"] = data[1]
        buffer["go_employee"] = data[2]
        go = {}

        if company.google_industry:
            go["google"] = quote("__".join(company.google_industry.split("/")))

        if company.industry:
            buffer["fInd"] = company.industry
            keyword = buffer["fInd"]
            namelist = [keyword, keyword.replace(" ", "_")]
            namelist = list(set(namelist))
            q_list = map(lambda n: Q(**{"industry__iexact":n}), namelist)
            q_list = reduce(lambda a, b: a | b, q_list)
            buffer["fIndCount"] = Company.objects.filter(q_list).count() - 1
            go["industry"] = str.lower(quote("-".join("__".join(company.industry.split("/")).split(" "))))
            buffer["fGo"] = "/find/" + go["industry"] + "--/"
        elif company.google_industry:
            buffer["fInd"] = company.google_industry
            keyword = buffer["fInd"]
            namelist = [keyword, keyword.replace(" ", "_")]
            namelist = list(set(namelist))
            q_list = map(lambda n: Q(**{"google_industry__iexact":n}), namelist)
            q_list = reduce(lambda a, b: a | b, q_list)
            buffer["fIndCount"] = Company.objects.filter(q_list).count() - 1
            buffer["fGo"] = "/find/?google_industry=" + go["google"]
        else:
            buffer["fInd"] = None
            buffer["fIndCount"] = None
            buffer["fGo"] = None
        if buffer["fIndCount"] == 1:
            buffer["ftag"] = "company"
        else:
            buffer["ftag"] = "companies"

        if company.state:
            go["state"] = us_state_abbrev[company.state]

        # competitors
        comp = [a["id"] for a in company.competitors.values()]
        comp = Company.objects.filter(id__in=comp).extra(select={'manual': 'FIELD(id,%s)' % ','.join(map(str, comp))},\
                                                     order_by=['manual']).values("name", "identifier", "domain")

        # strengths and weaknesses
        sng, wek = strengthAndWeaknesses(company)

        # Key Information
        keys = company.keyInfo()

        # determine if favourites
        company.fav = False
        try:
            Favourite.objects.get(company__id=company.id)
            company.fav = True
        except Favourite.DoesNotExist:
            pass

        country = company.country
        if country == "EU":
            continent = "Europe"
        elif country:
            country_code = pc.country_name_to_country_alpha2(country, cn_name_format="default")
            continent_code = pc.country_alpha2_to_continent_code(country_code)
            continent = continents[continent_code]
            continent = continent.replace(" ", "_")
        else:
            continent = "North America"
        connection.close()
        return render(request, 'keyinformation.html', {"company": company, "continent": continent, "buffer":buffer, 'dc':dropdown_content,\
                        'rauth': getAuth(request), 'pop': checkPop(request.session, request.user), 'comps': comp, 'sng': sng,\
                        'wek': wek, 'keys': keys, 'go': go})
    except Company.DoesNotExist:
        connection.close()
        return HttpResponseNotFound('<h1>Company does not exist</h1>')

@ratelimit(key='ip', block=True, rate='200/m', method=ratelimit.ALL)
def employeecount(request, id):
    try:
        company = Company.objects.get(identifier=id)
        addToVisited(request, company)
        company = company.cleanForFront()
        buffer = dict()
        buffer["g_data"] = []
        for i in range(0,8):
            if(company.__dict__["g"+str(i+1)]):
                temp_dict = dict()
                temp_dict["name"]= g_names[i]
                temp_dict["desc"]= g_descriptions[i]
                buffer["g_data"].append(temp_dict)

        if company.g_true <=6:
            setter = g_colors
        elif company.g_true ==7:
            setter = g_7_col
        else:
            setter = g_8_col
        for i in range(0, int(company.g_true)):
            buffer["g_data"][i]["color"] = setter[i]

        data = sort_data(company.revenue_quarter_chart, company.annual_revenue)
        buffer["cs_chart_labels"]= data[0]
        buffer["cs_chart_data"]= data[1]
        buffer["go_revenue"] = data[2]
        data = sort_data(company.employee_quarter_chart, company.num_emp)
        buffer["e_chart_labels"] = data[0]
        buffer["e_chart_data"] = data[1]
        buffer["go_employee"] = data[2]
        go = {}

        if company.google_industry:
            go["google"] = quote("__".join(company.google_industry.split("/")))

        if company.industry:
            buffer["fInd"] = company.industry
            keyword = buffer["fInd"]
            namelist = [keyword, keyword.replace(" ", "_")]
            namelist = list(set(namelist))
            q_list = map(lambda n: Q(**{"industry__iexact":n}), namelist)
            q_list = reduce(lambda a, b: a | b, q_list)
            buffer["fIndCount"] = Company.objects.filter(q_list).count() - 1
            go["industry"] = str.lower(quote("-".join("__".join(company.industry.split("/")).split(" "))))
            buffer["fGo"] = "/find/" + go["industry"] + "--/"
        elif company.google_industry:
            buffer["fInd"] = company.google_industry
            keyword = buffer["fInd"]
            namelist = [keyword, keyword.replace(" ", "_")]
            namelist = list(set(namelist))
            q_list = map(lambda n: Q(**{"google_industry__iexact":n}), namelist)
            q_list = reduce(lambda a, b: a | b, q_list)
            buffer["fIndCount"] = Company.objects.filter(q_list).count() - 1
            buffer["fGo"] = "/find/?google_industry=" + go["google"]
        else:
            buffer["fInd"] = None
            buffer["fIndCount"] = None
            buffer["fGo"] = None
        if buffer["fIndCount"] == 1:
            buffer["ftag"] = "company"
        else:
            buffer["ftag"] = "companies"

        if company.state:
            go["state"] = us_state_abbrev[company.state]

        # competitors
        comp = [a["id"] for a in company.competitors.values()]
        comp = Company.objects.filter(id__in=comp).extra(select={'manual': 'FIELD(id,%s)' % ','.join(map(str, comp))},\
                                                     order_by=['manual']).values("name", "identifier", "domain")

        # strengths and weaknesses
        sng, wek = strengthAndWeaknesses(company)

        # Key Information
        keys = company.keyInfo()

        # determine if favourites
        company.fav = False
        try:
            Favourite.objects.get(company__id=company.id)
            company.fav = True
        except Favourite.DoesNotExist:
            pass

        country = company.country
        if country == "EU":
            continent = "Europe"
        elif country:
            country_code = pc.country_name_to_country_alpha2(country, cn_name_format="default")
            continent_code = pc.country_alpha2_to_continent_code(country_code)
            continent = continents[continent_code]
            continent = continent.replace(" ", "_")
        else:
            continent = "North America"
        connection.close()
        return render(request, 'employeecount.html', {"company": company, "continent": continent, "buffer":buffer, 'dc':dropdown_content,\
                        'rauth': getAuth(request), 'pop': checkPop(request.session, request.user), 'comps': comp, 'sng': sng,\
                        'wek': wek, 'keys': keys, 'go': go})
    except Company.DoesNotExist:
        connection.close()
        return HttpResponseNotFound('<h1>Company does not exist</h1>')

@ratelimit(key='ip', block=True, rate='7/s', method=ratelimit.ALL)
def autocomplete(request):
    if request.is_ajax():
        max_results = 6
        query_limit = 100
        search = request.GET.get('search', None)
        search_params = Q(name__istartswith=search)|Q(domain__istartswith=search)
        # if request.user.is_authenticated:
        #     user = Profile.objects.get(user=request.user)
            # if user.paid == True:
            #     search_params = search_params | Q(description__icontains=search)

        queryset = Company.objects.filter(Q(search_params)).values("name", "domain", "id", "identifier")[:max_results]
        results = []
        count = 0
        for query in queryset:

            ### OLD LOGIC (12-FEB-2022)
            # print(query)
            # company_type = 'name'
            # if query['google_industry'] and search in query['google_industry'].lower():
            #     company_type = 'category'
            #     if count < max_results:
            #         if query['google_industry'] not in results:
            #             results.append(query['google_industry'])
            #     else:
            #         pass

            results.append(query)

        data = {
            'list': results,
        }
        connection.close()
        return JsonResponse(data)
    else:
        connection.close()
        return HttpResponseNotFound()

def ratcliff(s1, s2, sm):
    STRING_MAXLENDIFFER = 0.7
    s1len = len(s1)
    s2len = len(s2)
    if s1len < s2len:
        threshold = float(s1len) / s2len
    else:
        threshold = float(s2len) / s1len
    if threshold < STRING_MAXLENDIFFER:
        return 0.0
    sm.set_seq2(s2.lower())
    return sm.ratio()
    
_translate = dict(B='1', C='2', D='3', F='1', G='2', J='2', K='2', L='4',
                    M='5', N='5', P='1', Q='2', R='6', S='2', T='3', V='1',
                    X='2', Z='2')
_translateget = _translate.get
_re_non_ascii = re.compile(r'^[^a-z]*', re.I)
SOUNDEX_LEN = 5


def soundex(s):
    """Return the soundex code for the given string."""
    # Maximum length of the soundex code.
    s = _re_non_ascii.sub('', s)
    if not s:
        return None
    s = s.upper()
    soundCode = s[0]
    for c in s[1:]:
        cw = _translateget(c, '0')
        if cw != '0' and soundCode[-1] != cw:
            soundCode += cw
    return soundCode[:SOUNDEX_LEN] or None


def _sortKeywords(keyword, kwds):
    sm = SequenceMatcher()
    sm.set_seq1(keyword.lower())
    ratios = [(ratcliff(keyword, k, sm), k) for k in kwds]
    checkContained = False
    if len(keyword) > 4:
        checkContained = True
    for idx, data in enumerate(ratios):
        ratio, key = data
        if key.lower().startswith(keyword.lower()):
            ratios[idx] = (ratio + 0.5, key)
        elif checkContained and keyword.lower() in key.lower():
            ratios[idx] = (ratio + 0.3, key)
    ratios.sort()
    ratios.reverse()
    return [r[1] + str(r[0]) for r in ratios]


def filterSimilarKeywords(keyword, kwdsIterator):
    """Return a sorted list of keywords similar to the one given."""
    seenDict = {}
    kwdSndx = soundex(keyword)
    matches = []
    matchesappend = matches.append
    checkContained = False
    if len(keyword) > 4:
        checkContained = True
    for key in kwdsIterator:
        if key in seenDict:
            continue
        seenDict[key] = None
        if checkContained and keyword in key:
            matchesappend(key)
            continue
        if kwdSndx == soundex(key):
            matchesappend(key)
    return _sortKeywords(keyword, matches)

@ratelimit(key='ip', block=True, rate='7/s', method=ratelimit.ALL)
def industry_autocomplete(request):
    if request.is_ajax():
        max_results = 20

        search = request.GET.get('search', None).lower()
        path = Path(__file__).parent / "static/industries.json"
        f = open(path)
        input_dict = json.load(f)
        data = dict()
        for industry in input_dict:
            data[industry] = get_similarity(industry, search)

        sorted_data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
        sorted_data = dict(filter(lambda elem: elem[1] > 0, sorted_data.items()))
        output_dict = [ x for x in sorted_data ]
    
        # output_dict = _sortKeywords(search, input_dict)
        data = {
            'list': output_dict[0: max_results]
        }
        return JsonResponse(data)
    else:
        return HttpResponseNotFound()

@ratelimit(key='ip', block=True, rate='50/m', method=ratelimit.ALL)
def find(request, area = None):
    print("find")
    if request.user.is_authenticated:
            if request.user.profile.paid==False:
                if request.user.profile.pageview >= 20:
                    return render(request,'premium.html')
                request.user.profile.pageview +=1
                request.user.profile.save()
            else:
                request.user.profile.pageview = 0
                request.user.profile.save()
    else:
        if "page_views" in request.session:
            if request.session["page_views"] > 4:
                connection.close()
                return redirect('/signup/authwall')
            else:
               request.session["page_views"] += 1
        else:
            request.session["page_views"] = 1
    # isolate arguments from URL and extract industry and state from slug
    args = dict(request.GET)
    if area:
        area = area.split("--")
        if area[0]:
            args["industry"] = [area[0]]
        if len(area) > 1:
            if area[1]:
                args["state"] = [area[1]]

    # If no arguments found, fetch the default from cache if it exists
    page_obj = None
    doCache = True
    if len(args) == 0:
        cacheKey = "find_default"
        cacheTimeout = settings.EXP_COLD
    else:
        # if arguments exist, fetch key with respect to URL
        cacheKey = request.get_full_path()
        cacheTimeout = settings.EXP_WARM

    result = cache.get(cacheKey)
    if result:
        print("From Cache - 1")
        page_obj, p, pager = result
        doCache = False

    # clean arguments
    for a in args:
        args[a] = "/".join(unquote(args[a][0]).split("__"))

    # mapping for comparison arguments
    sliderMatching = {
        "arn": "annual_revenue__gte",
        "arx": "annual_revenue__lte",
        "empn": "num_emp__gte",
        "empx": "num_emp__lte",
        "gn": "g_true__gte",
        "gx": "g_true__lte"
    }

    if doCache:
        # define args and kwargs with respect to request arguments
        d = {}
        do = []
        for column in args:
            keyword = args[column]
            if column in ["city", "state", "industry", "google_industry", "arn", "arx", "empn", "empx", "gn", "gx"]:
                if column in ["arn", "arx", "empn", "empx", "gn", "gx"]:
                    revenue = int(float(keyword))
                    d[sliderMatching[column]] = revenue
                else:
                    # in MySQL, this lookup is case preserving but insensitive
                    namelist = [keyword, keyword.replace("-", "_"), keyword.replace("-", " ")]
                    d[column + "__in"] = namelist

        # Provide search arguments if any
        searchAgainst = [
            {"name":"name", "type": "__icontains"},
            {"name":"domain", "type": "__icontains"},
            {"name":"city", "type": "__istartswith"},
            {"name": "google_industry", "type": "__icontains"},
        ]
        if "search" in args:
            keyword = unquote(args["search"])
            q_list = map(lambda n: Q(**{n["name"] + n["type"]:keyword}), searchAgainst)
            q_list = reduce(lambda a, b: a | b, q_list)
            do.append(q_list)

        # filter, order, and extract relevant values and page number to feed to pagiantor
        results = Company.objects.filter(*do, **d)
        results = results.order_by('-g_true').values("id", "name", "identifier", "industry", "google_industry",\
                                                    "domain", "address_2", "address", "city", "state",\
                                                    "postal", "annual_revenue", "num_emp", "g_true")

        page_number = int(request.GET.get('page', 1))
        p = createPageBook(results.count(), 20, page_number)
        page_obj = results[(page_number - 1) * 20: page_number * 20]
        pager = assemblePagination(p)

        for i in page_obj:
            i["num_emp"] = human_format(i["num_emp"])
            i["annual_revenue"] = human_format(i["annual_revenue"])

    # format arguments to be displayed as tags
    for a in args:
        if "-" in args[a]:
            args[a] = " ".join([str.capitalize(b) for b in args[a].split("-")])
        if a in ["arn", "arx", "empn", "empx"]:
            args[a] = human_format(int(float(args[a])))

    # determine selected industry and state to be highlighted in the dropdown
    already = {}
    try:
        if "industry" in args:
            already["industry"] = {
                "show": args["industry"],
                "back": industries[args["industry"]]
            }
    except Exception as e:
        ind = "-".join(args["industry"].split())
        try:
            already["industry"] = {
                "show": ind,
                "back": industries[ind]
            }
        except:
            print(f"Detected an issue with dropdowns: {e}")
    try:
        if "state" in args:
            already["state"] = {
                "show": us_state_abbrev[args["state"]],
                "back": args["state"]
            }
    except Exception as e:
        print(f"Detected an issue with dropdowns: {e}")

    # create headline and title
    indus = None
    staty = None
    if "industry" in args:
        try:
            indus = already["industry"]["show"]
        except:
            indus = args["industry"]
    if "state" in args:
        try:
            staty = already["state"]["show"]
        except:
            staty = args["state"]
    title, heading, meta = createHeadline(indus, args.get("google_industry"), staty, args.get("city"))

    # set cache before returning page
    if doCache:
        cache.set(cacheKey, (page_obj, p, pager), cacheTimeout)

    # determine favourites
    favourites = getFavs(request)
    for i in page_obj:
        i["fav"] = False
        if i["id"] in favourites:
            i["fav"] = True

    # render the page
    connection.close()
    return render(request, 'listings.html', {'page_obj': page_obj, 'args': args, 'state': us_state_abbrev,\
        'industry': industries, 'history': already, 'dc':dropdown_content, 'rauth': getAuth(request),\
        'ckey':cacheKey, 'pager': pager, 'pbj': p, 'title': title, 'heading': heading, 'meta': meta, 'pop': checkPop(request.session, request.user)})

FIND_VALUES = ["id", "name", "identifier", "industry", "google_industry", "domain", "address_2", "address", "city", "state", "postal", "annual_revenue", "num_emp", "g_true", "description"]

@ratelimit(key='ip', block=True, rate='50/m', method=ratelimit.ALL)
def find_test_watson(request, area = None):
    PAGE_SIZE = 10
    # isolate arguments from URL and extract industry and state from slug
    args = dict(request.GET)
    if area:
        area = area.split("--")
        if area[0]:
            args["industry"] = [area[0]]
        if len(area) > 1:
            if area[1]:
                args["state"] = [area[1]]

    # If no arguments found, fetch the default from cache if it exists
    page_obj = None
    doCache = True
    if len(args) == 0:
        cacheKey = "find_default"
        cacheTimeout = settings.EXP_COLD
    else:
        # if arguments exist, fetch key with respect to URL
        cacheKey = request.get_full_path()
        cacheTimeout = settings.EXP_WARM

    result = cache.get(cacheKey)
    if result:
        print("From Cache - 2")
        page_obj, p, pager = result
        doCache = False

    # clean arguments
    for a in args:
        args[a] = "/".join(unquote(args[a][0]).split("__"))

    # mapping for comparison arguments
    sliderMatching = {
        "arn": "annual_revenue__gte",
        "arx": "annual_revenue__lte",
        "empn": "num_emp__gte",
        "empx": "num_emp__lte",
        "gn": "g_true__gte",
        "gx": "g_true__lte"
    }

    if doCache:
        # define args and kwargs with respect to request arguments
        search_data = {}
        q_queries = None
        for column in args:
            keyword = args[column]
            if column in ["arn", "arx", "empn", "empx", "gn", "gx"]:
                revenue = int(float(keyword))
                search_data[sliderMatching[column]] = revenue
            elif column in ["city", "state", "industry", "google_industry"]:
                name_struct = [keyword, keyword.replace("-", "_"), keyword.replace("-", " ")]
                search_data[column + "__in"] = name_struct


        if "search" in args:
            keyword = unquote(args["search"])
            search_keywords = ["name", "domain", "city", "google_industry"]
            q_queries = map(lambda x: Q(**{x: keyword}), search_keywords)
            q_queries = reduce(lambda x, y: x | y, q_queries)

        if "search" in args:
            keyword = unquote(args["search"])
            results = watson.filter(Company.objects.filter(**search_data), keyword)
        else:
            results = Company.objects.filter(**search_data)
        paginated_results = Paginator(results, PAGE_SIZE)
        page_number = int(request.GET.get('page', 1))
        current_page = paginated_results.get_page(page_number)

        page_obj = current_page.object_list.values(*FIND_VALUES)


        p = {
            "count": paginated_results.count,
            "per_page": paginated_results.per_page,
            "number": page_number,
            "total_pages": paginated_results.num_pages,
            "has_previous": current_page.has_previous(),
            "has_next": current_page.has_next(),
            "page_range": paginated_results.page_range
        }
        pager = assemblePagination(p)


        for obj in page_obj:
            obj["num_emp"] = obj["num_emp"]
            obj["annual_revenue"] = obj["annual_revenue"]

    # format arguments to be displayed as tags
    for a in args:
        if "-" in args[a]:
            args[a] = " ".join([str.capitalize(b) for b in args[a].split("-")])
        if a in ["arn", "arx", "empn", "empx"]:
            args[a] = int(float(args[a]))

    # determine selected industry and state to be highlighted in the dropdown
    already = {}
    try:
        if "industry" in args:
            already["industry"] = {
                "show": args["industry"],
                "back": industries[args["industry"]]
            }
    except Exception as e:
        ind = "-".join(args["industry"].split())
        try:
            already["industry"] = {
                "show": ind,
                "back": industries[ind]
            }
        except:
            print(f"Detected an issue with dropdowns: {e}")
    try:
        if "state" in args:
            already["state"] = {
                "show": us_state_abbrev[args["state"]],
                "back": args["state"]
            }
    except Exception as e:
        print(f"Detected an issue with dropdowns: {e}")

    # create headline and title
    indus = None
    staty = None
    if "industry" in args:
        try:
            indus = already["industry"]["show"]
        except:
            indus = args["industry"]
    if "state" in args:
        try:
            staty = already["state"]["show"]
        except:
            staty = args["state"]
    title, heading, meta = createHeadline(indus, args.get("google_industry"), staty, args.get("city"))


    # set cache before returning page
    if doCache:
        cache.set(cacheKey, (page_obj, p, pager), cacheTimeout)

    # determine favourites
    favourites = getFavs(request)

    for i in page_obj:
        i["fav"] = False
        if i["id"] in favourites:
            i["fav"] = True
    connection.close()
    return render(request, 'listings.html', {'page_obj': page_obj, 'args': args, 'state': us_state_abbrev,\
        'industry': industries, 'history': already, 'dc':dropdown_content, 'rauth': getAuth(request),\
        'ckey':cacheKey, 'pager': pager, 'pbj': p, 'title': title, 'heading': heading, 'meta': meta, 'pop': checkPop(request.session, request.user)})

@ratelimit(key='ip', block=True, rate='50/m', method=ratelimit.ALL)
def find_pagination_redesign(request, area = None):
    PAGE_SIZE = 10
    if request.user.is_authenticated:
            if request.user.profile.paid==False:
                if request.user.profile.pageview >= 20:
                    return redirect('/premium')
                request.user.profile.pageview +=1
                request.user.profile.save()
            else:
                request.user.profile.pageview = 0
                request.user.profile.save()
    else:
        if "page_views" in request.session:
            if request.session["page_views"] >= 100:
                connection.close()
                request.session['redirect_to'] = 'find/{}/'.format(area)
                return redirect('/signup/authwall')
            else:
               request.session["page_views"] += 1
        else:
            request.session["page_views"] = 1
    # isolate arguments from URL and extract industry and state from slug
    args = dict(request.GET)
    if area:
        area = area.split("--")
        if area[0]:
            args["industry"] = [area[0]]
        if len(area) > 1:
            if area[1]:
                args["state"] = [area[1]]

    # If no arguments found, fetch the default from cache if it exists
    page_obj = None
    doCache = True
    if len(args) == 0:
        cacheKey = "find_default_pagination"
        cacheTimeout = settings.EXP_COLD
    else:
        # if arguments exist, fetch key with respect to URL
        cacheKey = request.get_full_path()
        cacheTimeout = settings.EXP_WARM

    result = cache.get(cacheKey)
    if result:
        print("From Cache - 3")
        page_obj, p, pager = result
        doCache = False

    # clean arguments
    for a in args:
        args[a] = "/".join(unquote(args[a][0]).split("__"))

    # mapping for comparison arguments
    sliderMatching = {
        "arn": "annual_revenue__gte",
        "arx": "annual_revenue__lte",
        "empn": "num_emp__gte",
        "empx": "num_emp__lte",
        "gn": "g_true__gte",
        "gx": "g_true__lte"
    }

    if doCache:
        # define args and kwargs with respect to request arguments
        search_data = {}
        for column in args:
            keyword = args[column]
            if column in ["arn", "arx", "empn", "empx", "gn", "gx"]:
                revenue = int(float(keyword))
                search_data[sliderMatching[column]] = revenue
            elif column in ["city", "state", "industry", "google_industry"]:
                search_data[column] = keyword.replace("-", " ")

        # Autocomplete search
        if "name" in args:
            # results = Company.objects.filter(Q(Q(name__icontains=args['name']) | Q(domain__icontains=args['name'])), **search_data).order_by("-g_true") # Search with containing word
            results = Company.objects.filter(Q(Q(name__istartswith=args['name']) | Q(domain__istartswith=args['name'])), **search_data).order_by("-g_true") # Starts with word
            print("name!")
        elif "desc" in args:
            if request.user.is_authenticated and request.user.profile.paid == True:
                results = Company.objects.filter(description__icontains=args['desc'], **search_data).order_by("-g_true")
            else:
                context = {}
                context["price_id"] = settings.STRIPE_PRICE
                return render(request,'premium.html',context)

        elif "categories" in args:
            results = Company.objects.filter(google_industry=args['categories'], **search_data).order_by("-g_true")
        elif "search" in args:
            keyword = unquote(args["search"]).strip()
            results = Company.objects.filter(name__icontains=keyword, **search_data).order_by("-g_true")
        else:
            results = Company.objects.filter(**search_data).order_by("-g_true")
        paginated_results = Paginator(results, PAGE_SIZE)
        page_number = int(request.GET.get('page', 1))
        current_page = paginated_results.get_page(page_number)
        page_obj = current_page.object_list.values(*FIND_VALUES)
        total_count = paginated_results.count
        page_number = min(page_number, paginated_results.num_pages)

        if current_page.has_next():
            page_range = range(max(1, page_number-2), min(page_number+6, paginated_results.num_pages + 1))
        else:
            page_range = range(max(1, page_number-2), page_number+1)

        p = {
            "count": total_count,
            "per_page": paginated_results.per_page,
            "number": page_number,
            "total_pages": paginated_results.num_pages,
            "has_previous": current_page.has_previous(),
            "has_next": current_page.has_next(),
            "page_range": page_range
        }

        for obj in page_obj:
            obj["num_emp"] = human_format(obj["num_emp"])
            obj["annual_revenue"] = human_format(obj["annual_revenue"])

        pager = assemblePagination(p)

    # format arguments to be displayed as tags
    for a in args:
        if "-" in args[a]:
            args[a] = " ".join([str.capitalize(b) for b in args[a].split("-")])
        if a in ["arn", "arx", "empn", "empx"]:
            args[a] = human_format(int(float(args[a])))

    # determine selected industry and state to be highlighted in the dropdown
    already = {}
    try:
        if "industry" in args:
            already["industry"] = {
                "show": args["industry"],
                "back": industries[args["industry"]]
            }
    except Exception as e:
        ind = "-".join(args["industry"].split())
        try:
            already["industry"] = {
                "show": ind,
                "back": industries[ind]
            }
        except:
            print(f"Detected an issue with dropdowns: {e}")
    try:
        if "state" in args:
            already["state"] = {
                "show": us_state_abbrev[args["state"]],
                "back": args["state"]
            }
    except Exception as e:
        print(f"Detected an issue with dropdowns: {e}")

    try:
        if "google_industry" in args:
            already["google_industry"] = {
                "show" : args["google_industry"],
            }
    except Exception as e:
        print(f"Detected an issue with dropdowns: {e}")

    # create headline and title
    indus = None
    staty = None
    if "industry" in args:
        try:
            indus = already["industry"]["show"]
        except:
            indus = args["industry"]
    if "state" in args:
        try:
            staty = already["state"]["show"]
        except:
            staty = args["state"]
    title, heading, meta = createHeadline(indus, args.get("google_industry"), staty, args.get("city"))


    # set cache before returning page
    if doCache:
        cache.set(cacheKey, (page_obj, p, pager), cacheTimeout)

    # determine favourites
    favourites = getFavs(request)

    for i in page_obj:
        i["fav"] = False
        if i["id"] in favourites:
            i["fav"] = True

    is_premium = 0
    if request.user.is_authenticated and request.user.profile.paid == True:
        is_premium = 1

    query = {}
    if "name" in args:
        query['key'] = args['name']
    elif "desc" in args:
        if request.user.is_authenticated and request.user.profile.paid == True:
            query['key'] = args['desc']
        else:
            context = {}
            context["price_id"] = settings.STRIPE_PRICE
            return render(request,'premium.html',context)
    elif "categories" in args:
        query['key'] = args['categories']
    elif "search" in args:
        query['key'] = args['search']
    pass
    # mylist = list(page_obj)

    connection.close()

    return render(request, 'new_listings.html', {'page_obj': page_obj, 'args': args, 'state': us_state_abbrev,\
        'industry': industries, 'history': already, 'dc':dropdown_content, 'rauth': getAuth(request),\
        'ckey':cacheKey, 'pager': pager, 'pbj': p, 'title': title, 'heading': heading, 'meta': meta, 'pop': checkPop(request.session, request.user),\
        'is_premium': is_premium, 'query': query })

def get_base_url(request):
  protocol = request.build_absolute_uri().split(request.get_host())[0]
  return F"{protocol}{request.get_host()}"


@csrf_exempt
def hook(request):
    if request.method == "POST":
        if validate_request(request):
            try:
                Tasks(arg=request.body.decode("utf-8")).save()
            except Exception as e:
                print(e, file=sys.stderr)
            connection.close()
            return HttpResponse(status = 200)
        else:
            connection.close()
            return HttpResponse(status = 403)
    connection.close()
    return HttpResponseNotFound()

def acquire(request):
    connection.close()
    return render(request,'acquire.html')

def premium(request):
    request.session['redirect_to'] = 'premium'
    context = {}
    context["price_id"] = settings.STRIPE_PRICE
    connection.close()
    return render(request,'premium.html',context)

def hometest(request):
    connection.close()
    return render(request,'hometest.html')


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        connection.close()
        return JsonResponse(stripe_config)


# @csrf_exempt
# def stripe_config(request):
#     if request.method == 'GET':
#         stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
#         return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    print("CHECKPOINT kona2 create_checkout_session")
    user_email = request.user.email
    price_id = request.GET.get("price_id")
    try:
        print("try")
        checkout_session = stripe.checkout.Session.create(
            client_reference_id=request.user.id if request.user.is_authenticated else None,
            success_url=F'{get_base_url(request)}/'+'success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=F'{get_base_url(request)}/'+'cancelled/',
            payment_method_types=['card'],
            customer_email=request.user.email,
            mode='subscription',
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1
                }
            ]
        )
        print("CHECKPOINT kona2 create_checkout_session end 1")
        connection.close()
        return JsonResponse({'sessionId': checkout_session['id']})
    except Exception as e:
        print(e)
        print("CHECKPOINT kona2 create_checkout_session end 2")
        return JsonResponse({'error': str(e)})

def success(request):
    print("CHECKPOINT kona2 success")
    home_url = request.build_absolute_uri().split("//")[0]+"//"+str(request.get_host())
    connection.close()
    return render(request, 'success.html', context={"home_url":home_url})

def cancel(request):
    connection.close()
    return render(request, 'cancel.html', context={})

def split_name(full_name):
    name = []
    full_name = full_name.split(" ")
    name.append(full_name[0])
    name.append(" ".join(full_name[1:]))
    return tuple(name)

def update_or_create_user_profile_emailaddress(stripe_response):

    # Deconstructing parameter
    email = stripe_response.get('customer_details').get('email')
    # client_stripe_id =  stripe_response.get('client_reference_id', None)
    full_name = stripe_response.get('customer_details').get('name')
    stripe_customer_id = stripe_response.get('customer')

    try:
        # TODO: check if stripe allows to attach metadata to a payment to link
        # profiles that really should be the same one
        # EX: employees getting subscribed by their boss and ending up with 2 different accounts
        user, created = User.objects.update_or_create(email=email, defaults={
            'email' : email,
            'username' : email,
            'first_name' :full_name.split(" ")[0],
            'last_name' : full_name.split(" ")[1],
        })

        user.refresh_from_db()
        Profile.objects.update_or_create(user=user, defaults={
            'first_name' :user.first_name,
            'last_name' : user.last_name,
            'paid' : True,
            'customer_id' : stripe_customer_id,
            'pageview' : 0,
        })

        EmailAddress.objects.update_or_create(user=user, defaults={
            'email' : user.email,
            'verified' : True,
            'primary' : True
        })

        return user

    except Exception as e:
        print(e)



def prep_password_email_text(user):
    password = get_random_string(8)
    user.password = make_password(password)
    user.save()
    body = f"""\n\nWe have taken the liberty to generate a password for you: {password}\n
Login at konaequity.com/login\n
    """
    return body

@csrf_exempt
def webhook_received(request):
    """
    Stripe Notes
    The order with which the webhook events will come in
    1. customer.subscription.created
    2. invoice.created
    3. invoice.paid
    4. charge.created (if there’s a charge)
    """

    user = None

    # endpoint_secret = settings.STRIPE_ENDPOINT_SECRET

    # The endpoint secret is temporarily hardcoded because there were some issues fetching the right value from .env
    endpoint_secret = 'whsec_0TQIAv4LPtrnDKENHh44NQX9nSW1OwCb'

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    event = None
    try:
        print("try kona2 webhook_received")
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        print("try kona2 webhook_received OK")
    except ValueError as e:
        print("Invalid payload:", e)
        # Invalid payload
        connection.close()
        print("CHECKPOINT kona2 create_checkout_session end 1")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print("Invalid signature:", e)
        # Invalid signature
        connection.close()
        print("CHECKPOINT kona2 create_checkout_session end 2")
        return HttpResponse(status=400)
    if event:
        event_type = event["type"]
        print("Event type:", event_type)


        if event_type == 'checkout.session.completed':
            print('🔔 Payment succeeded!')
            session = stripe_response = event['data']['object']

            #Get Required Data
            stripe_customer_id = session.get('customer')
            customer = stripe.Customer.retrieve(session.get("customer"))
            customer_details = session.get("customer_details")
            email_address =   customer_details.get("email")
            user_name = customer_details.get("name")
            client_reference_id = session.get('client_reference_id', None)
            stripe_subscription_id = session.get('subscription', None) or session.get('id')
            subs = stripe.Subscription.retrieve(
                stripe_subscription_id,
            )
            sub_invoice = subs.latest_invoice

            user = update_or_create_user_profile_emailaddress(stripe_response)

            if subs:
                user_inv = stripe.Invoice.retrieve(
                    subs.latest_invoice,
                )
                invoice_host = user_inv.hosted_invoice_url
                if invoice_host:
                    body = F"Thank you for subscribing to Kona Equity Premium. If you have any feedback on how we could improve or any questions, please don’t hesitate to contact us at admin@konaequity.com\n Subscription Invoice\n{invoice_host}\n"

                    # If user doesnt have a password, concatenate this email message with an extra line communicating the user his/her password
                    if not user.password:
                        body = body + prep_password_email_text(user)

                    MessagesService.send_email(user.email, "Kona Equity Premium", body)
        elif event_type == 'customer.subscription.trial_will_end':
            print('Subscription trial will end')
        elif event_type == 'customer.subscription.created':
            print('Subscription created %s', event.get("id", None))
        elif event_type == 'customer.subscription.updated':
            print('Subscription created %s', event.get("id", None))
        elif event_type == 'customer.subscription.deleted':
            # handle subscription cancelled automatically based
            # upon your subscription settings. Or if the user cancels it.
            print('Subscription canceled: %s', event.get("id", None))
        elif event_type == 'charge.succeeded':

            # Isolating customer ID
            stripe_customer_id = event['data']['object'].get('customer')

            # Fetching customer info
            stripe_customer = stripe.Customer.retrieve(stripe_customer_id)

            # Prepping object for update_or_create method
            stripe_response = {
                'customer_details' : {
                    'name' : stripe_customer['name'],
                    'email' : stripe_customer['email'],
                },
                'customer' : stripe_customer_id
            }

            # Update or create
            user = update_or_create_user_profile_emailaddress(stripe_response)

            if not user.password:
                body = prep_password_email_text(user)
                MessagesService.send_email(user.email, "Kona Equity Premium", body)

    connection.close()
    return JsonResponse({'status': 200})

def get_similarity(origin : str, keyword : str):
    origin = origin.lower()
    keyword = keyword.lower()

    origin_array = origin.split() #split string into a list    
    keyword_array = keyword.split()

    sim = 0
    if origin.startswith(keyword): 
        sim = float('inf')
    else:
        for oid, origin in enumerate(origin_array):
            for kid, keyword in enumerate(keyword_array):
                for charid, x in enumerate(keyword):
                    substring = keyword[:charid+1]
                    if substring is not None:
                        index = (len(origin_array) - oid) * (len(keyword_array) - kid)
                        sim += _get_similarity(origin, substring, oid, kid)

    return sim
    
def _get_similarity(origin : str, keyword : str, oid : int, kid : int):
    similarity = 0
    config = { 'same' : 100, 'starts_with_head' : 10, 'starts_with_sub_head' : 2, 'max_word_count': 6, 'contains': 6 }
    weight = 1.2 ** ((6 - oid) * (6 - kid))
    # weight2 = 1.2 ** (6 - kid)
    # weight = weight1 * weight2
    if origin == keyword:
        similarity = config['same'] * weight
    elif origin.startswith(keyword) :
        similarity = config['starts_with_head'] * weight * origin.count(keyword)
    elif origin.endswith(keyword) :
        similarity = config['starts_with_head'] * weight * origin.count(keyword)
    elif keyword in origin:
        similarity = config['contains'] * weight * origin.count(keyword)
    #contains

    return similarity