from django.shortcuts import render, redirect
from httplib2 import Response
from more_itertools import first
from .models import Profile, Favourite, Visited
from django.contrib.auth.models import User
from .forms import UpdateProfileForm
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from allauth.account.views import SignupView, _ajax_response
from backend_django.utils import human_format
from backend_django.ip import getStateFromIp
from django.core.cache import cache
import random
from backend_django.models import Company, Verification
import math
from django.conf import settings
from statistics import harmonic_mean
from fuzzywuzzy import fuzz
from time import time
from allauth.account.models import EmailAddress
from django.utils import timezone
from backend_django.constants import dropdown_content
from backend_django.helpers import getFavs

from module import google
from module import constant as mcs
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import get_template
import smtplib
from email.utils import formataddr
import shortuuid
from datetime import datetime
import time
import logging

logging.basicConfig(filename='/home/konaequity2/konatest/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def dashboard(request):
    if request.user.is_authenticated:
        user = Profile.objects.get(user=request.user)
        auth = user.profile_photo
        user.email = request.user.email
        return render(request, "dashboard.html", {"dc": dropdown_content, "rauth": auth, "user": user})
    else:
        return redirect("/")

def watchlist(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return render(request, "watchlist.html", {"dc": dropdown_content, "rauth": profile.profile_photo, "name": profile.get_full_name()})
    else:
        return redirect("/")

def watchtest(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return render(request, "watchtest.html", {"dc": dropdown_content, "rauth": profile.profile_photo, "name": profile.get_full_name()})
    else:
        return redirect("/")

def addToFavourite(request):
    if request.method == "POST":
        cid = request.POST.get("id")
        if cid:
            cid = int(cid)
            company = Company.objects.filter(id=cid)
            if company.exists():
                csrf_token = get_token(request)
                k = Favourite.objects.filter(user=request.user, company=company[0])
                if k.exists():
                    k = k[0]
                    k.date_added = timezone.now()
                    k.save()
                    return JsonResponse({
                        "status": "success",
                        "company_id": cid,
                        "message": "Already a favourite. Updated timestamp.",
                        "csrf_token":csrf_token
                    })
                b = Favourite.objects.create(user=request.user, company=company[0])
                return JsonResponse({
                    "status": "success",
                    "company_id": cid,
                    "message": str(b),
                    "csrf_token":csrf_token
                })
            else:
                return JsonResponse({
                    "status": "failure",
                    "company_id": cid,
                    "message": "Company does not exist"
                })
    return JsonResponse({
        "status": "failure",
        "message": "Invalid Request"
    })

def removeFromFavourite(request):
    if request.method == "POST":
        cid = request.POST.get("id")
        if cid:
            cid = int(cid)
            company = Company.objects.filter(id=cid)
            if company.exists():
                csrf_token = get_token(request)
                b = Favourite.objects.filter(user=request.user, company=company[0])
                if b.exists():
                    b.delete()
                    return JsonResponse({
                        "status": "success",
                        "company_id": cid,
                        "message": str(b),
                        "csrf_token":csrf_token
                    })
                else:
                    return JsonResponse({
                        "status": "success",
                        "company_id": cid,
                        "message": "Not a favourite",
                        "csrf_token":csrf_token
                    })
            else:
                return JsonResponse({
                    "status": "failure",
                    "company_id": cid,
                    "message": "Company does not exist"
                })
    return JsonResponse({
        "status": "failure",
        "message": "Invalid Request"
    })

def update_profile(request):
    if request.method == "POST":
        form = UpdateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            ip = request.META.get('HTTP_X_REAL_IP')
            ua = request.META.get('HTTP_USER_AGENT')
            res, msg = form.emailVal(ip, ua)
            if res:
                user_profile = Profile.objects.get(user_id=request.user)
                user_profile.first_name = form.cleaned_data["first_name"]
                user_profile.last_name = form.cleaned_data["last_name"]
                user_profile.profile_photo = form.cleaned_data["profile_photo"]
                user_profile.save()
                rauth = str(user_profile.profile_photo)

                # changing email
                old_user = request.user
                old_email = old_user.email
                email = form.cleaned_data["email"]
                if old_email != email and email != "":
                    if User.objects.filter(email = email).exists():
                        return JsonResponse({"errors": ["email_already_exists"]})
                    old_user.email = email
                    old_user.save()

                    # change in allauth
                    e = EmailAddress.objects.get(email = old_email)
                    e.email = email
                    e.save()
                return JsonResponse({"errors": "None", "pp": rauth})
            else:
                return JsonResponse({
                    "errors": {
                        "email": [msg]
                    }
                })
        else:
            return JsonResponse({"errors": form.errors})
    return JsonResponse({
        "errors":{
            "method": "Invalid query"
        }
    })

class AjaxSignUpView(SignupView):
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        print(form)
        if form.is_valid():
            ip = request.META.get('HTTP_X_REAL_IP')
            ip = "127.0.0.1"
            print("Valid", ip)
            ua = request.META.get('HTTP_USER_AGENT')
            ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
            res, msg = form.emailVal(ip, ua)
            if res:
                self.form_valid(form)
                return JsonResponse({"errors": "None"})
            else:
                return JsonResponse({
                    "errors": {
                        "email": [msg]
                    }
                })
            return JsonResponse({"errors": "None"})
        else:
            return JsonResponse({'errors': form.errors})

def supplier(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            perPage = 20
            responseList = []
            command = request.POST.get("command", "saved")
            favourites = getFavs(request)

            if command == "saved":
                f = Favourite.objects.filter(user = request.user).order_by("-date_added").select_related("company")
                paginator = Paginator(f, perPage)
                page_number = request.POST.get('page', 1)
                page_obj = paginator.get_page(page_number)
                for i in page_obj:
                    i = i.company
                    responseList.append(
                        {
                            "id": i.id,
                            "name": i.name,
                            "domain": i.domain,
                            "identifier": i.identifier,
                            "annual_revenue": human_format(i.annual_revenue),
                            "num_emp": human_format(i.num_emp)
                        }
                    )

            if command == "visited":
                f = Visited.objects.filter(user = request.user).order_by("-timestamp").select_related("company")
                paginator = Paginator(f, perPage)
                page_number = request.POST.get('page', 1)
                page_obj = paginator.get_page(page_number)
                for i in page_obj:
                    i = i.company
                    responseList.append(
                        {
                            "id": i.id,
                            "name": i.name,
                            "domain": i.domain,
                            "identifier": i.identifier,
                            "annual_revenue": human_format(i.annual_revenue),
                            "num_emp": human_format(i.num_emp)
                        }
                    )

            elif command == "nearby":
                state, city = getStateFromIp(request)
                page_number = int(request.POST.get('page', 1))
                page_obj = cache.get(f"{state}.{city}")
                if page_obj is None or page_number != 1:
                    cityList = cache.get("city.list")
                    if cityList is None:
                        cityList = (Company.objects.values_list("city", flat=True).distinct())
                        cache.set("city.list", cityList, settings.EXP_ICE)

                    top = [a for a in cityList if fuzz.ratio(city, a) > 85]
                    f = Company.objects.filter(state=state, city__in=top).order_by("-g_true")

                    if not f.exists():
                        f = Company.objects.filter(state=state).order_by("-g_true")
                    paginator = Paginator(f, perPage)
                    page_obj = paginator.get_page(page_number)
                    for i in page_obj:
                        responseList.append(
                            {
                                "id": i.id,
                                "name": i.name,
                                "domain": i.domain,
                                "identifier": i.identifier,
                                "annual_revenue": human_format(i.annual_revenue),
                                "num_emp": human_format(i.num_emp)
                            }
                        )

            if command == "study":
                f = Favourite.objects.filter(user = request.user).order_by("-date_added").select_related("company")[:80]
                comp = {}
                for i in f:
                    i = i.company
                    for k in i.competitors:
                        com = i.competitors[k]
                        if com["id"] in comp:
                            comp[com["id"]].append(com["dist"])
                        else:
                            comp[com["id"]] = [com["dist"]]
                try:
                    del comp[None]
                except KeyError:
                    pass
                comp = [{"id": a, "dist":harmonic_mean(comp[a])} for a in comp]
                comp = sorted(comp, key=lambda x: x["dist"])
                comp = [a["id"] for a in comp]
                comp = [a for a in comp if a not in favourites]
                f = Company.objects.filter(id__in=comp).extra(select={'manual': 'FIELD(id,%s)' % ','.join(map(str, comp))}, order_by=['manual'])

                paginator = Paginator(f, perPage)
                page_number = request.POST.get('page', 1)
                page_obj = paginator.get_page(page_number)
                for i in page_obj:
                    responseList.append(
                        {
                            "id": i.id,
                            "name": i.name,
                            "domain": i.domain,
                            "identifier": i.identifier,
                            "annual_revenue": human_format(i.annual_revenue),
                            "num_emp": human_format(i.num_emp)
                        }
                    )

            for i in responseList:
                i["fav"] = False
                if i["id"] in favourites:
                    i["fav"] = True

            return JsonResponse({
                    "status": "empty" if len(responseList) == 0 else "data",
                    "companies": render(request, "card.html", {"companies": responseList}).content.decode("utf-8"),
                    "pagination": render(request, "pagi.html", {"page_obj": page_obj}).content.decode("utf-8")
                })
        return JsonResponse({
            "error": "Invalid"
        })

def signup(request):
    return render(request, 'signup.html')

def signup_a(request):
    return render(request, 'signup_a.html')

def signup_v(request):
    data = {}
    if 'redirect_to' in request.session:
        id = request.session['redirect_to'].split('/')[1]
        companies = Company.objects.filter(identifier=id)
        if len(companies) > 0:
            data = {'company': companies[0]}
        else:
            return redirect('/')
    else:
        return redirect('/')
    return render(request, 'signup_v.html', data)

def register_google_user(request):
    redirect_to = '/'
    if 'redirect_to' in request.session:
        redirect_to += request.session['redirect_to']
    try:
        if request.user.is_authenticated:
            return redirect(redirect_to)
        if "code" not in request.GET:
            data = {'msg': 'authorization code is not in the request GET'}
            return render(request, 'google_user_error.html', data)
        # ---------- get google identity token with authorization code ---------- #
        id_token = google.getIdentityTokenFromAuthzCode(authz_code=request.GET["code"],
                                                            client_id=settings.GOOGLE_CONSUMER_KEY,
                                                            client_secret=settings.GOOGLE_CONSUMER_SECRET,
                                                            redirect_url=mcs.BASE_URL + "signup/register_google_user")
        if 'res' in id_token:
            if id_token['res'] == None:
                data = {'msg': id_token['msg']}
                return render(request, 'google_user_error.html', data)
        # ---------- process user ---------- #
        user_list = list(User.objects.filter(email=id_token["email"]))
        if len(user_list) == 0:
            user_obj = User()
            user_obj.email = id_token["email"]
            user_obj.username = id_token["email"]
            user_obj.set_password(mcs.THIRDPARTY_IDP_PWD)
            first_name = id_token['name']
            if id_token["given_name"] is not None:
                first_name = id_token['given_name']
            user_obj.first_name = first_name
            user_obj.last_name = id_token["family_name"]
            user_obj.save()
            EmailAddress.objects.create(user=user_obj, email=user_obj.email, verified=True, primary=True)
            Profile.objects.create(user=user_obj, first_name=first_name, last_name=id_token['family_name'])

        user = authenticate(username=id_token["email"], password=mcs.THIRDPARTY_IDP_PWD)
        if user is None:
            return redirect('/login')
        django_login(request, user)
        if 'redirect_to' in request.session:
            del request.session['redirect_to']
        request.session.save()
        return render(request, 'welcome.html', {'email': id_token['email'], 'redirect': redirect_to})
    except Exception as e:
        data = {'msg': str(e)}
        return render(request, 'google_user_error.html', data)

def login_google_user(request):
    redirect_to = '/'
    if 'redirect_to' in request.session:
        redirect_to += request.session['redirect_to']
    try:
        if request.user.is_authenticated:
            return redirect(redirect_to)
        if "code" not in request.GET:
            data = {'msg': 'authorization code is not in the request GET'}
            return render(request, 'google_user_error.html', data)
        # ---------- get google identity token with authorization code ---------- #
        id_token = google.getIdentityTokenFromAuthzCode(authz_code=request.GET["code"],
                                                            client_id=settings.GOOGLE_CONSUMER_KEY,
                                                            client_secret=settings.GOOGLE_CONSUMER_SECRET,
                                                            redirect_url=mcs.BASE_URL + "login_google_user")
        if 'res' in id_token:
            if id_token['res'] == None:
                data = {'msg': id_token['msg']}
                return render(request, 'google_user_error.html', data)
        # ---------- process user ---------- #
        user_list = list(User.objects.filter(email=id_token["email"]))
        if len(user_list) == 0:
            return render(request, 'google_user_error.html', {'msg': 'This user not registered'})
        user = user_list[0]
        user.backend = 'allauth.account.auth_backends.AuthenticationBackend'
        django_login(request, user_list[0])
        if 'redirect_to' in request.session:
            del request.session['redirect_to']
        request.session.save()
        return redirect(redirect_to)
    except Exception as e:
        data = {'msg': str(e)}
        return render(request, 'google_user_error.html', data)

def email_verification_request(request):
    try:
        print(f"POST REQUEST ::  {request.POST}")
        param = request.POST
        email = param['email']
        if "redirect_to" in request.session:
            redirect_to = request.session["redirect_to"]
        else:
            redirect_to = ''
        user_list = list(User.objects.filter(email=email))
        if len(user_list) >= 1:
            return HttpResponse('emailexist')
        token = shortuuid.uuid()
        activation_url = mcs.BASE_URL + "signup/email_verification_activate?verify_token=%s&redirect=%s" % (token, redirect_to)
        logo_url = mcs.BASE_URL + "static/email/logo.png"
        html = render_email({'activation_url': activation_url, 'logo_url': logo_url},
                            "email/email_confirmation_message.html")
        html = MIMEText(html, 'html')
        res = send_mail(to_email=email, subject="Email verification", message=html, from_email=settings.MAILJECT_FROM_EMAIL)
        if res == 'success':
            verification = Verification.objects.create(
                token=token,
                email=email,
                # timestamp added automatically on record creation
            )

            print(verification)
            print(res)

            request.session['verification_id'] = verification.id

        return HttpResponse(res)
    except Exception as e:
        return HttpResponse(str(e))

def email_verification_sent(request):
    try:
        email_sent_at = float(datetime.timestamp(Verification.objects.get(id=request.session.get('verification_id')).created))

        now = datetime.timestamp(datetime.now())

        if now - email_sent_at > mcs.ACTIVATION_LINK_EXPIRE_TIME:
            return render(request, template_name='email_verification_activate_fail.html')
        return render(request, template_name='email_verification_sent.html')
    except:
        return render(request, template_name='email_verification_activate_fail.html')

def email_verification_activate(request):

    try:
        params = request.GET
        token = params['verify_token']

        verification = Verification.objects.filter(token=token).first()

        if not verification:
            return render(request, template_name='email_verification_activate_fail.html')

        now = datetime.timestamp(datetime.now())
        email_sent_at = float(datetime.timestamp(verification.created))

        if now - email_sent_at > mcs.ACTIVATION_LINK_EXPIRE_TIME:
            return render(request, template_name='email_verification_activate_fail.html')

        data = {"email": verification.email, "redirect_to": params['redirect']}
        return render(request, template_name='signup_p2.html', context=data)
    except:
        return render(request, template_name='email_verification_activate_fail.html')


def email_verification_finish(request):
    try:
        param = request.POST
        user_list = list(User.objects.filter(email=param["email"]))
        if len(user_list) >= 1:
            return HttpResponse('emailexist')

        user_obj = User()
        user_obj.email = param["email"]
        user_obj.username = param["email"]
        user_obj.set_password(param["password"])
        user_obj.first_name = param["firstname"]
        user_obj.last_name = param["lastname"]
        user_obj.save()
        EmailAddress.objects.create(user=user_obj, email=user_obj.email, verified=True, primary=True)
        Profile.objects.create(user=user_obj, first_name=param["firstname"], last_name=param["lastname"])
        user = authenticate(username=param["email"], password=param["password"])
        django_login(request, user)
        return HttpResponse('success')
    except Exception as e:
        return HttpResponse('error')

def forgot_password_view(request):
    return render(request, template_name='forgot_password_view.html')

def forgot_password_sent(request):
    try:
        email_sent_at = float(request.session['reset_time'])
        now = datetime.timestamp(datetime.now())
        if now - email_sent_at > mcs.ACTIVATION_LINK_EXPIRE_TIME:
            return render(request, template_name='forgot_password_fail.html')
        return render(request, template_name='forgot_password_sent.html')
    except:
        return render(request, template_name='forgot_password_fail.html')

def forgot_password_activate(request):
    try:
        params = request.GET
        verify_token = params['verify_token']
        if verify_token != request.session['reset_token']:
            return render(request, template_name='forgot_password_fail.html')
        email_sent_at = float(request.session['reset_time'])
        now = datetime.timestamp(datetime.now())
        if now - email_sent_at > mcs.ACTIVATION_LINK_EXPIRE_TIME:
            return render(request, template_name='forgot_password_fail.html')
        data = {"email": request.session['reset_email']}
        return render(request, template_name='reset_password.html', context=data)
    except:
        return render(request, template_name='forgot_password_fail.html')
def reset_password_finish(request):
    try:
        param = request.POST
        email = param['email']
        password = param['password']
        user_obj = User.objects.get(email=email)
        user_obj.set_password(password)
        user_obj.save()
        user = authenticate(username=email, password=password)
        django_login(request, user)
        return HttpResponse('success')
    except:
        return HttpResponse('error')

def forgot_password_request(request):
    param = request.POST
    email = param['email']
    token = shortuuid.uuid()
    forgot_password_url = mcs.BASE_URL + "forgot_password_activate?verify_token=%s" % (token)
    logo_url = mcs.BASE_URL + "static/email/logo.png"
    html = render_email({'forgot_password_url': forgot_password_url, 'logo_url': logo_url},
                        "email/forgot_password_message.html")
    html = MIMEText(html, 'html')
    res = send_mail(to_email=email, subject="Reset password", message=html, from_email=settings.MAILJECT_FROM_EMAIL)
    print(res)
    if res == 'success':
        request.session['reset_email'] = email
        request.session['reset_time'] = datetime.timestamp(datetime.now())
        request.session['reset_token'] = token
    return HttpResponse(res)

def render_email(context, template_path):
    template = get_template(template_path)
    html = template.render(context)
    return html

def check_keys(key_ary, dict_obj):
    for key in key_ary:
        if key not in dict_obj:
            return False
    return True

def login(request):
    try:
        redirect_to = request.GET.get('redirect', None)
        if request.user.is_authenticated:
            if redirect_to is None:
                return redirect('/')
            else:
                try:
                    del request.session['redirect_to']
                except:
                    pass
                return redirect('/{}'.format(redirect_to))
        key_ary = ['email', 'password']
        params = request.POST

        if not check_keys(key_ary, params):
            return render(request, template_name='login.html')

        email = params['email']
        password = params['password']
        user = authenticate(username=email, password=password)
        time.sleep(1)
        print(user)
        if user is None:
            return render(request, template_name='login.html')
        django_login(request, user)
        request.session.save()
        if redirect_to is None:
            return redirect('/')
        else:
            return redirect('/{}'.format(redirect_to))
    except Exception as e:
        print(e)
        return render(request, template_name='login.html')

def send_mail(to_email, subject, message, from_email="", from_name="", to_name=""):
    try:
        msg = MIMEMultipart('alternative')
        msg['subject'] = subject
        msg['from'] = formataddr((from_name, from_email))
        msg['to'] = formataddr((to_name, to_email))
        msg.attach(message)

        server = smtplib.SMTP(settings.MAILJET_SMTP_SERVER, settings.MAILJET_SMTP_PORT)
        server.starttls()
        server.login(settings.MAILJET_USERNAME, settings.MAINJET_PASSWORD)  # username & password

        server.sendmail(msg['from'], [msg['to']], msg.as_string())
        server.quit()
        print('Successfully sent the mail.')
        return 'success'
    except Exception as e:
        return str(e)

def upgrade_superuser(request, email):
    try:
        user = User.objects.get(email=email)
        print(user)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return JsonResponse({"username": user.username, "email": user.email, "firstname": user.first_name, "last_name": user.last_name})
    except:
        return HttpResponse('error')