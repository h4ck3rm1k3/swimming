import requests
import os
import json
import pprint
import time

def extract(d):
    box = [None,None,None,None]
    for x in d:
        #print x['latitude'],x['longitude']

        if box[0] is None:
            box[0]= x['latitude'] 
        elif box[0] > x['latitude'] :
            box[0]= x['latitude'] 

        if box[1] is None:
            box[1]= x['latitude'] 
        elif box[1] < x['latitude'] :
            box[1]= x['latitude'] 

        if box[2] is None:
            box[2]= x['longitude'] 
        elif box[2] > x['longitude'] :
            box[2]= x['longitude'] 

        if box[3] is None:
            box[3]= x['longitude'] 
        elif box[3] < x['longitude'] :
            box[3]= x['longitude'] 
    #print box
    return box

def get(x,y):
    if x is None : 
        return None

    f = "data/%s_%s" % (x,y)
    
    if not os.path.exists(f):
        url = "http://swimtoday.org/rest/facilities/%s/%s" % (x,y)
        r = requests.get(url)
        o = open (f,"w")
        t = r.text
        o.write(t)
        d = json.loads(t)
        o.close()
    else:
        o = open (f)
        #d = o.read()
        d = json.load(o)
        #pprint.pprint()
        o.close()
    #return extract(d)
    return d

def merge(a,b):
    if a[0] and b[0]:
        return [
            min(a[0],b[0]),
            max(a[1],b[1]),
            min(a[2],b[2]),
            max(a[3],b[3])
        ]
    elif not a[0] and b[0] :
        return [
            min(b[0],b[0]),
            max(a[1],b[1]),
            min(b[2],b[2]),
            max(a[3],b[3])
        ]
    else :
        return [
            min(a[0],a[0]),
            max(a[1],b[1]),
            min(a[2],a[2]),
            max(a[3],b[3])
        ]

        
def rec(x):
    a = get(x[0],x[2])
    b = get(x[1],x[3])
    c = get(x[0],x[3])
    d = get(x[1],x[2])

    # expand the box
    e= merge(d,merge(c,merge(a,b)))
    rec(e)

import glob

def scan():
    box = [None,None,None,None]
    for x in glob.glob("data/*"):
        print x
        f = open(x)
        d = json.load(f)
        #print d
        e = extract(d)
        box =merge(box,e)

        f.close()
    return box


data_f = ["Zipcode","ZipCodeType","City","State","LocationType","Lat","Long","Location","Decommisioned","TaxReturnsFiled","EstimatedPopulation","TotalWages"]

fields = [
    u'address1',
    u'address2',
    u'city',
    u'facility_id',
    u'facility_name',
    u'latitude' ,
    u'longitude',
    u'mas',
    u'mas_contact',
    u'mas_email',
    u'mas_phone',
    u'mas_program',
    u'usa_state_code']

club_f = [
    u'club_id',
    u'club_name',
    u'contact_business_phone',
    u'contact_email',
    u'contact_name',
    u'nspf',
    u'usas',
    u'usms',
    u'website'
]

allfield=[]
allfield.extend(data_f)
allfield.extend(fields)
allfield.extend(club_f)
print "^".join(allfield)


seen = {}

def zipc():

    f = open("free-zipcode-database-Primary.csv")
    for l in f:
        l = l.rstrip()
        (Zipcode,ZipCodeType,City,State,LocationType,Lat,Long,Location,Decommisioned,TaxReturnsFiled,EstimatedPopulation,TotalWages)=l.split(",")
        if Zipcode == "\"Zipcode\"": 
            continue
        #print Lat,Long
        x=get(Lat,Long)
        #time.sleep(0.1)
        data = [Zipcode,ZipCodeType,City,State,LocationType,Lat,Long,Location,Decommisioned,TaxReturnsFiled,EstimatedPopulation,TotalWages]
        #print x
        for f in x :
            facility=[]

            facility_id = f[u'facility_id']

            if facility_id not in seen :
                seen[facility_id] =1


                #print pprint.pprint(f)
                for b in fields :
                    facility.append(str(f[b]))

                for c in f['clubs']:
                    club = []
                    for b in club_f:
                        club.append(str(c[b]))
                    d =[]
                    d.extend(data)
                    d.extend(facility)
                    d.extend(club)


                    print "^".join(d)
            else:
                # skip
                pass

zipc()
