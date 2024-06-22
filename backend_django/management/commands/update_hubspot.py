from django.core.management.base import BaseCommand
from backend_django.models import Company, Tasks
from time import time, sleep
from backend_django.hubspot import ints, bools, strings, floats, remove_punc
import re
from django_bulk_update.helper import bulk_update
from django.contrib.sitemaps import ping_google
import sys
from django.db import connection

class Command(BaseCommand):
    '''
    This command aggregates and subsequently executes webhooks received by Hubspot
    '''
    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument('--duration', nargs='?', type=int, default=0)
        parser.add_argument('--sleep', nargs='?', type=int, default=5)

    def handle(self, *args, **options):
        duration = options.get("duration", 0)
        sleep_time = options.get("sleep", 10)
        st = time()
        while (duration <= 0) or (time() - st) <= duration:
            try:
                tic = time()
                ids = Tasks.objects.all()[:600].values_list("id", flat=True)
                x = Tasks.objects.filter(pk__in=list(ids))
                print(len(x), flush=True)
                if len(list(x)) == 0:
                    print(f"Nothing found. Going to sleep for {sleep_time} seconds.", flush=True)
                    sleep(sleep_time)
                    connection.close()
                    continue
                y = [a.to_list() for a in x]
                y = [a for k in y for a in k]
                print(f"Updating {len(y)} data points.", flush=True)
                process(y)
                print(x.delete(), flush=True)
                connection.close()

                print("Time for batch: ", time()-tic, flush=True)
            except Exception as e:
                print(e, flush=True)
                sys.exit()
        print(f"Process ended after {time()-st} seconds.", flush=True)

def process(data):
    tictic = tic = time()
    BATCH_SIZE = round(len(data)/100) + 25
    change = []
    properties = ["last_modified"]
    for dat in data:
        sub = dat["subscriptionType"]
        if sub == "company.propertyChange":
            change.append(dat)
    print(time()-tic, " for filtering")
    tic = time()
    ids = [d["objectId"] for d in change]
    ids = list(set(ids))
    objects = Company.objects.in_bulk(ids)
    try:
        # change properties or create companies
        hashmap = {}
        cmap = {}
        for dat in change:
            objectId = dat["objectId"]
            occuredAt = dat["occurredAt"]
            if objectId in hashmap:
                c = hashmap[objectId]
            elif objectId in cmap:
                c = cmap[objectId]
            else:
                try:
                    c = hashmap[objectId] = objects[objectId]
                except:
                    print("Creating a company...")
                    c = cmap[objectId] = Company(id = objectId)
            propertyName = dat["propertyName"]
            value = dat["propertyValue"]
            if propertyName in strings:
                if value:
                    value = str(value).encode('ascii',errors='ignore').decode('ascii')
                else:
                    value = None
                c.setValue(strings[propertyName], value, occuredAt)
                properties.append(strings[propertyName])
            elif propertyName in floats:
                if value:
                    value = float(value)
                else:
                    value = None
                c.setValue(floats[propertyName], value, occuredAt)
                properties.append(floats[propertyName])
            elif propertyName in ints:
                if value:
                    value = int(float(value))
                else:
                    value = None
                c.setValue(ints[propertyName], value, occuredAt)
                properties.append(ints[propertyName])
            elif propertyName in bools:
                if value == "0":
                    value = False
                elif value == "1":
                    value = True
                else:
                    value = None
                c.setValue(bools[propertyName], value, occuredAt)
                properties.append(bools[propertyName])
            elif propertyName == "name":
                c.setValue(propertyName, value, occuredAt)
                c.setValue("identifier", "-".join(str.lower(remove_punc(value)).split() + [str(objectId)]), occuredAt)
                properties += ["name", "identifier"]
            elif propertyName == "is_public":
                if value == "false":
                    value = False
                elif value == "true":
                    value = True
                else:
                    value = None
                c.setValue(propertyName, value, occuredAt)
                properties.append(propertyName)
            elif re.search(r'competitor_[1-6]{1}_', propertyName):
                key = propertyName.split("_")[1]
                old = c.competitors
                if "_id" in propertyName:
                    if value:
                        value = int(float(value))
                    else:
                        value = None
                    old["c" + key]["id"] = value
                elif "_distance" in propertyName:
                    if value:
                        value = float(value)
                    else:
                        value = None
                    old["c" + key]["dist"] = value
                c.competitors = old
                properties.append("competitors")
                c.updateModifiedTime("competitors", occuredAt)
            elif re.search(r'revenue_[0-9]{4}_q[1-4]{1}', propertyName):
                if value:
                    value = float(value)
                else:
                    value = None
                key = propertyName.partition("revenue_")[2]
                old = c.revenue_quarter_chart
                old[key] = value
                c.revenue_quarter_chart = old
                properties.append("revenue_quarter_chart")
                c.updateModifiedTime("revenue_quarter_chart", occuredAt)
            elif re.search(r'employee_count_[0-9]{4}_q[1-4]{1}', propertyName):
                if value:
                    value = float(value)
                else:
                    value = None
                key = propertyName.partition("employee_count_")[2]
                old = c.employee_quarter_chart
                old[key] = value
                c.employee_quarter_chart = old
                properties.append("employee_quarter_chart")
                c.updateModifiedTime("employee_quarter_chart", occuredAt)
        print(time()-tic, " for hashing")

        tic = time()
        properties = list(set(properties))
        properties = [a for a in properties if a != "id"]
        if len(cmap) > 0:
            print("Pinging Google...")
            ping_google(sitemap_url = "/sitemap.xml")
        Company.objects.bulk_create(list(cmap.values()), batch_size=BATCH_SIZE)
        print(time()-tic, " for writing")
        k = list(hashmap.values())
        bulk_update(k, update_fields=properties, batch_size=BATCH_SIZE)
        print(time()-tic, " for updating")
        print("Task completed: ", time()-tictic, flush=True)
    except Exception as e:
        print(f"Exception: {e}", flush = True)
