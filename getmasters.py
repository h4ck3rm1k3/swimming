import requests
import os
import json
import pprint
import time

def get(city,state):
    if city is None : 
        return None
    f = "data2/%s_%s" % (city,state)   
    if not os.path.exists(f):
        url = "http://www.usms.org/placswim/mapsearch.php?action=f2&dist=25&address=&city={city}&state={state}&units=mi".format(city=city,state=state)
        r = requests.get(url)
        o = open (f,"wb")
        t = r.text
        o.write(t.encode("utf8"))
        #d = json.loads(t)
        o.close()
    else:
        t = ""
        o = open (f)
        for l in o.readlines():
            t = t + l
        o.close()
    return t


import glob

data_f = ["Zipcode","ZipCodeType","City","State","LocationType","Lat","Long","Location","Decommisioned","TaxReturnsFiled","EstimatedPopulation","TotalWages"]

allfield=[]
allfield.extend(data_f)
print("^".join(allfield))


seen = {}

def zipc():

    seen = {}

    f = open("free-zipcode-database-Primary.csv")
    for l in f:
        l = l.rstrip()
        (Zipcode,ZipCodeType,City,State,LocationType,Lat,Long,Location,Decommisioned,TaxReturnsFiled,EstimatedPopulation,TotalWages)=l.split(",")

        City = City.replace("\"","")
        State = State.replace("\"","")

        if Zipcode == "\"Zipcode\"": 
            continue
        if State not in seen :
            seen[State]={}
        else:
            if City not in seen[State]:
                seen[State][City]={}
                # first 
                x=get(City,State)
                data = [Zipcode,ZipCodeType,City,State,LocationType,Lat,Long,Location,Decommisioned,TaxReturnsFiled,EstimatedPopulation,TotalWages]
                #print x
                #for f in x :
                #    print x

            else:
                pass


zipc()
