import json
from django.http.response import JsonResponse
from backend_django.models import Company, CompanyLike
from backend_django.constants import us_state_abbrev, g_names, g_descriptions, g_colors, g_8_col, g_7_col, continents, dropdown_content, strengthAndWeaknesses
from backend_django.helpers import getAuth, addToVisited, checkPop
from backend_django.utils import sort_data, convert_to_localtime
from urllib.parse import quote
from functools import reduce
from auth_app.models import Favourite
import pycountry_convert as pc
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.db.models import Q
from .helper import get_email_user_data, get_time_now, get_company_info, get_contact_info, get_domain, get_email_domain
from backend_django.tasks import sendEmail
from django.core.mail import BadHeaderError, send_mail

from django.db import connection

def company_view(request, id):
    if request.method == 'POST':
        test_id = request.POST.get('test_id', '')
        to_email = request.POST.get('email', '')
        from_email = "joey@konaequity.com"
        if test_id and to_email:
            try:
                send_mail(
                    subject="Email for Test id",
                    message=f'{test_id} - {to_email}',
                    from_email=from_email,
                    recipient_list=[from_email, ],
                    auth_user=from_email,
                    auth_password='Maui2020',
                    fail_silently=False,
                )
                print('email sent successfully', to_email, test_id)
                connection.close()
                return JsonResponse({"status": "success"})
            except BadHeaderError:
                print('bad header error occurred in sending email')
                connection.close()
                return JsonResponse({"status": "error"})
        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            connection.close()
            return JsonResponse({"status": "error"})
    try:
        if request.user.is_authenticated:
            if request.user.profile.paid==False:
                if request.user.profile.pageview >= 20:
                    return redirect('/premium/')
                request.user.profile.pageview +=1
                request.user.profile.save()
            else:
                request.user.profile.pageview = 0
                request.user.profile.save()
        else:
            if "page_views" in request.session:
                if request.session["page_views"] >= 2:
                    connection.close()
                    request.session['redirect_to'] = 'company/{}'.format(id)
                    print('company/{}'.format(id))
                    return redirect('/signup/vanity')
                    # return HttpResponse("page views>4, sorry")
                else:
                   request.session["page_views"] += 1
            else:
                request.session["page_views"] = 1

        company = Company.objects.get(identifier=id)
        contact_info = get_contact_info(company.id)

        addToVisited(request, company)
        company = company.cleanForFront()
        buffer = dict()
        buffer["g_data"] = []
        for i in range(0, 8):
            if(company.__dict__["g"+str(i+1)]):
                temp_dict = dict()
                temp_dict["name"] = g_names[i]
                temp_dict["desc"] = g_descriptions[i]
                buffer["g_data"].append(temp_dict)

        if company.g_true <= 6:
            setter = g_colors
        elif company.g_true == 7:
            setter = g_7_col
        else:
            setter = g_8_col
        for i in range(0, int(company.g_true)):
            buffer["g_data"][i]["color"] = setter[i]

        data = sort_data(company.revenue_quarter_chart, company.annual_revenue)
        if len(data) > 0:
            buffer["cs_chart_labels"] = data[0]
        if len(data) > 1:
            buffer["cs_chart_data"] = data[1]
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
            q_list = map(lambda n: Q(**{"industry__iexact": n}), namelist)
            q_list = reduce(lambda a, b: a | b, q_list)
            buffer["fIndCount"] = Company.objects.filter(q_list).count() - 1
            go["industry"] = str.lower(
                quote("-".join("__".join(company.industry.split("/")).split(" "))))
            buffer["fGo"] = "/find/" + go["industry"] + "--/"
        elif company.google_industry:
            buffer["fInd"] = company.google_industry
            keyword = buffer["fInd"]
            namelist = [keyword, keyword.replace(" ", "_")]
            namelist = list(set(namelist))
            q_list = map(lambda n: Q(
                **{"google_industry__iexact": n}), namelist)
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
        comp_ids = [a["id"] for a in company.competitors.values()
                    if isinstance(a["id"], int)]
        if comp_ids:
            comp = Company.objects.filter(id__in=comp_ids).extra(select={'manual': 'FIELD(id,%s)' % ','.join(map(str, comp_ids))},
                                                                 order_by=['manual']).values("name", "identifier", "domain", "year_founded")

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
        if request.user.is_authenticated:
            company.fav = Favourite.objects.filter(
                user=request.user, company=company).exists()

        try:
            country = company.country
            if country == "EU":
                continent = "Europe"
            elif country:
                country_code = pc.country_name_to_country_alpha2(
                    country, cn_name_format="default")
                continent_code = pc.country_alpha2_to_continent_code(
                    country_code)
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
            M_100 =100_000_000
            B = 1000_000_000
            B_10 = 10_000_000_000
            B_100 = 100_000_000_000

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
            # 2M alike.
            elif revene >= M and revene < M_10:
                revene = str(revene)[:2]
                return (revene[:1] + '.') + revene[1:] + ' Million Revenue'
            # 23M alike.
            elif revene >= M_10 and revene < M_100:
                revene = str(revene)[:3]
                return (revene[:2] + '.') + revene[2:] + ' Million Revenue'
            # 230M alike.
            elif revene >= M_100 and revene < B:
                revene = str(revene)[:3]
                return revene + ' Million Revenue'
            # 2B alike.
            elif revene >= B and revene < B_10:
                revene = str(revene)[:1]
                return revene + ' Billion Revenue'
            # 20B alike.
            elif revene >= B_10 and revene < B_100:
                revene = str(revene)[:2]
                return revene + ' Billion Revenue'
            #200B alike.
            elif revene >= B_100:
                revene = str(revene)[:3]
                return revene + ' Billion Revenue'


        likes = CompanyLike.objects.filter(company=company, liked=True).count()
        dislikes = CompanyLike.objects.filter(company=company, liked=False).count()

        user_like = None
        if request.user.is_authenticated:
            try:
                user_like = CompanyLike.objects.get(company=company, user=request.user)
            except:
                pass
        connection.close()
        return render(request, 'backend_django_v2/company.html',
                      {"company": company, 'revenue_abbreviation': revenue_abbreviation(), "continent": continent,
                       "buffer": buffer, 'dc': dropdown_content,
                       'rauth': getAuth(request), 'pop': checkPop(request.session, request.user), 'comps': comp,
                       'sng': sng,
                       'wek': wek, 'keys': keys, 'go': go, 'likes': likes, 'dislikes': dislikes, 'user_like': user_like,
                       'contacts': contact_info
                       }
                      )
    except Company.DoesNotExist:
        connection.close()
        return HttpResponseNotFound('<h1>Company does not exist</h1>')


def like_company(request, id):
    if not request.user.is_authenticated:
        connection.close()
        return JsonResponse({"status": "error", "messageç": "You must be logged in to view this page."});

    try:
        user_line = CompanyLike.objects.get(company_id=id, user=request.user)
    except CompanyLike.DoesNotExist:
        user_line = None
    liked = request.POST.get("like_type") == "like"
    if user_line:
        user_line.liked = liked
        user_line.save()
    else:
        CompanyLike.objects.create(company_id=id, user=request.user, liked=liked)
    connection.close()
    return JsonResponse({"status": "success", "message": "You have liked/disliked this company."})


def claim_company(request):
    if not request.user.is_authenticated:
        connection.close()
        return JsonResponse({"status": "error", "message": "You must be logged in to view this page."});
    # Get company ID from request
    try:
        id = request.POST.get("id")
        company = Company.objects.get(id=id)
        company_domain_name = get_domain(company.domain)
        user_email_domain = get_email_domain(request.user.email)

        if company_domain_name != user_email_domain:
            connection.close()
            return JsonResponse({"status": "error", "message": "mismatched domains"});

        user_info = get_email_user_data(request.user)
        # Text email body
        email_body = f"{company.name}'s Claim"
        for val in user_info:
            email_body += f"{val[0]}: {val[1]}\n"

        data = {
            "subject": f'{company.name} Company Claim',
            "message": email_body
        }
        sendEmail(data)
        # HTML email body
        # email_body_html = f"<h1>{company.name}'s Claim</h1>"
        # if user_info:
        #     email_body_html += f"<h3>User Info</h3>"
        # for val in user_info:
        #     email_body_html += f"<p><strong>{val[0]}</strong> {val[1]}</p>"
        # Send email
        # email_to = ["research@konaequity.com", "glaxek@gmail.com"]
        # send_edit_email_thread(
        #     f'{company.name} Company Claim',
        #     email_body,
        #     None,
        #     email_to,
        #     html_message=email_body_html,
        # )
        connection.close()
        return JsonResponse({"status": "success", "message": "You have claimed this company."})
    except Company.DoesNotExist:
        connection.close()
        return JsonResponse({"status": "error", "message": "Company does not exist."});

def edit_company(request, id):
    # Check if user is logged in
    if not request.user.is_authenticated:
        connection.close()
        return JsonResponse({"status": "error", "message": "You must be logged in to view this page."});
    print(request)
    print(request.POST)
    # Get company
    try:
        company = Company.objects.get(id=id)
    except Company.DoesNotExist:
        connection.close()
        return JsonResponse({"status": "error", "message": "Company does not exist."});

    edit_type = request.POST.get("edit_type")
    print(edit_type)
    email_subject = f"{company.name}'s {edit_type} edits"
    user_info = get_email_user_data(request.user)
    company_info = get_company_info(company, edit_type)
    time = get_time_now()

    email_body = f"{company.name}'s {edit_type} Edits\n\n"
    email_body == f"Editor Information:\n\n"
    for val in user_info:
        email_body += f"{val[0]}: {val[1]}\n"
    email_body += f"\n\nCompany Information:\n\n"
    for val in company_info:
        email_body += f"{val[0]}: {val[1]}\n"
    email_body += f"\n\nModified Values:\n\n"
    for val in request.POST:
        if val == "csrfmiddlewaretoken" or val == "edit_type":
            continue
        email_body += f"{val}: {request.POST[val]}\n"
    email_body += f"\n\nTime of Edits:\n\n{time}\n\n"
    email_body += f"\n\nEdit Type:\n\n{edit_type}\n\n"

    data = {
        "subject": email_subject,
        "message": email_body
    }
    sendEmail(data)
    # user_info_html = ""
    # for val in user_info:
    #     user_info_html += f"<p><strong>{val[0]}</strong>: {val[1]}</p>"

    # company_info_html = ""
    # for val in company_info:
    #     company_info_html += f"<p><strong>{val[0]}</strong>: {val[1]}</p>"

    # modified_values = ""
    # for val in request.POST:
    #     if val == "csrfmiddlewaretoken" or val == "edit_type":
    #         continue
    #     modified_values += f"<p>{val}: {request.POST[val]}</p>"

    # email_body_html = f"""
    # <html>
    #     <body>
    #         <h1>{company.name}'s {edit_type} edits</h1>
    #         <h2>Editor Information</h2>
    #         <p>
    #             {user_info_html}
    #         </p>
    #         <h2>Company Information</h2>
    #         <p>
    #             {company_info_html}
    #         </p>
    #         <h2>Modified Values</h2>
    #         <p>
    #             {modified_values}
    #         </p>
    #         <h2>Modified Time</h2>
    #         <p>
    #             {time}
    #         </p>
    #     </body>
    # </html>
    # """
    # email_to = ["research@konaequity.com"]

    # send_edit_email_thread(email_subject, email_body, None, email_to, email_body_html)
    connection.close()
    return JsonResponse({"status": "success", "message": "Company successfully edited."});

def edit_contact(request, id):
    if not request.user.is_authenticated:
        connection.close()
        return JsonResponse({"status": "error", "message": "You must be logged in to view this page."})
    # apiKey = '2f0e2171-0a87-413e-81cb-e0435ab583d5'
    # contactUri = 'https://api.hubapi.com/contacts/v1/contact/vid/' + str(contactId) + '/profile?hapikey=' + apiKey
    # headers = {'Content-Type': 'application/json'}
    # requestBody = json.dumps({
    #       "properties": [
    #         {
    #           "property": "firstname",
    #           "value": firstName
    #         },
    #         {
    #           "property": "lastname",
    #           "value": lastName
    #         },
    #         {
    #           "property": "jobtitle",
    #           "value": jobTitle
    #         }
    #       ]
    # })
    # Get company
    try:
        company = Company.objects.get(id=id)
    except Company.DoesNotExist:
        connection.close()
        return JsonResponse({"status": "error", "message": "Company does not exist."})
    edit_type = request.POST.get("edit_type")
    print(edit_type)
    email_subject = f"{company.name}'s {edit_type} edits"
    user_info = get_email_user_data(request.user)
    contact_info = get_contact_info(id)
    time = get_time_now()

    email_body = f"{company.name}'s {edit_type} Edits\n\n"
    for val in user_info:
        email_body += f"{val[0]}: {val[1]}\n"
    email_body += f"\n\nContact Information:\n\n"
    for val in contact_info:
        for key in val:
            email_body += f"{key}: {val[key]}\n"
    email_body += f"\n\nModified Values:\n\n"

    contacts = request.POST['contacts']
    contacts = json.loads(contacts)
    for contact in contacts:
        for key in contact:
            email_body += f"{key}: {contact[key]}\n"
    email_body += f"\n\nTime of Edits:\n\n{time}\n\n"
    email_body += f"\n\nEdit Type:\n\n{edit_type}\n\n"

    data = {
        "subject": email_subject,
        "message": email_body
    }

    try:
        sendEmail(data)
        connection.close()
        return JsonResponse({"status": "success"})
    except:
        connection.close()
        return JsonResponse({"status": "error"})
