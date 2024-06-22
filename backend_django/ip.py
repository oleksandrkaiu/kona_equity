from .constants import us_state_abbrev
from .models import IP
from user_agents import parse
import requests
import json
from django.conf import settings

def getStateFromIp(request):
    # API Key for Ipstack.com
    access_key = settings.IP_KEY

    ip = request.META.get('HTTP_X_REAL_IP')
    ua = request.META.get('HTTP_USER_AGENT')

    if ip is None:
        return settings.DEFAULT_STATE, ""

    state = settings.DEFAULT_STATE
    c = ""
    find = False
    ua = parse(ua)
    if ua.is_bot:
        return settings.DEFAULT_STATE, ""

    try:
        i = IP.objects.get(ip_addr=ip)
        if i.hasExpired():
            find = True
            i.delete()
        else:
            state = i.state
            c = i.city
    except IP.DoesNotExist:
        find = True

    if find:
        try:
            r = requests.get(f"http://api.ipstack.com/{ip}?access_key={access_key}")
            print("Requesting for state with IP: ", ip, flush=True)
            if r.status_code == 200:
                r = r.json()
                if r.get("success") == False:
                    print(r.get("error", {}).get("info", ""))
                else:
                    c = r.get("city")
                    r = r.get("region_code")
                    if r and c:
                        state = r
                        IP(ip_addr=ip, state=state, city=c).save()
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print("Unexpected issue ", e, flush=True)

    # Return state based on following logic
    if state == settings.DEFAULT_STATE:
        pass
    elif state in settings.BLACKLIST or state not in list(us_state_abbrev.keys()):
        state = settings.DEFAULT_STATE
    return state, c
