from datetime import datetime, timedelta
import random, string
from django.utils import timezone
from math import ceil
import pytz

def convert_to_localtime(utime):
    fmt = '%m/%d/%Y'
    utc = datetime.utcfromtimestamp(int(utime/1000)).replace(tzinfo=pytz.UTC)
    localtz = utc.astimezone(timezone.get_current_timezone())
    return localtz.strftime(fmt)

def generate_random_code(N = 5):
    '''Generates a random string with size N. String may contain upper and lower case alphabets along with digits.
    '''
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))

def human_format(num):
    '''Converts large numbers to human readable form. 3000000 -> 3 M
    '''
    if num is None:
        return "-"
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{} {}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

def sort_data(inp, ann):
    go = True
    try:
        ann = int(ann)
    except:
        return "", ""
    w = []
    for i in inp:
        score = int(i.partition("_")[0]) * 1000
        score += int(i[-1])
        w.append({
            "key": i,
            "score": score
        })
    w = sorted(w, key = lambda x:x["score"])
    w = [a["key"] for a in w]
    chart_data = []
    chart_labels = []
    for i in w:
        if inp[i]:
            chart_data.append(inp[i])
            chart_labels.append(" ".join(i.split("_")).replace("q", "Q"))
    if len(chart_data) == 0:
        go = False
    chart_data = ",".join([str(a) for a in chart_data])
    chart_labels = ",".join(chart_labels)
    return chart_labels, chart_data, go

def returnEpirationDate():
    now = datetime.now()
    return now + timedelta(days=30)

def defaultValues():
    return {}

def defaultCompetitorValues():
    return {
        "c1": {
            "id": None,
            "dist": None
        },
        "c2": {
            "id": None,
            "dist": None
        },
        "c3": {
            "id": None,
            "dist": None
        },
        "c4": {
            "id": None,
            "dist": None
        },
        "c5": {
            "id": None,
            "dist": None
        },
        "c6": {
            "id": None,
            "dist": None
        }
    }

def assemblePagination(page_obj):
    total = page_obj["count"]
    current = page_obj["number"]
    perPage = page_obj["per_page"]

    if total  == 0:
        return "No companies found"
    elif total == 1:
        return "1 company found"
    elif total < perPage:
        return str(total) + " companies found"
    else:
        text = str((current - 1)*perPage + 1) + "-"
        check = current*perPage
        if check < total:
            text += str(check)
        else:
            text += str(total)
        if total == 1:
            return text + " of " + numberWithCommas(total) + " company"
        else:
            return text + " of " + numberWithCommas(total) + " companies"

def numberWithCommas(number):
    return f"{number:,}"

def createPager(page, exists, page_count):
    if not exists:
        return "No companies."
    
    per_page = page["per_page"]
    current = page["number"]

    lower = (current - 1) * per_page + 1
    if page_count < per_page:
        higher = lower + page_count -1
    else:
        higher = current * per_page
    return f"Viewing {lower} - {higher}"
    

def createPageBook(count, per_page, page_num):
    p = {
        "count": count,
        "per_page": per_page,
        "number": page_num
    }
    p["total_pages"] = ceil(p["count"]/p["per_page"])
    if p["number"] < p["total_pages"]:
        page_range = range(max(1, page_num-2), min(page_num+3, count))
    else:
        page_range = range(max(1, page_num-2), page_num)
    p["has_previous"] = p["number"] > 1
    p["has_next"] = p["number"] < p["total_pages"]
    p["page_range"] = page_range

    return p
