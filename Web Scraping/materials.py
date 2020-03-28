import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)

cred = credentials.Certificate('WinHacksKey.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://winhacks-2020-database2.firebaseio.com'
    })

ref = db.reference().child("Companies")
data = ref.get()

materialDict = {}

for company in data:
    materialList = (data[company]["Materials"])
    for material in materialList:
        if material not in materialDict:
            materialDict[material] = 1
        else:
            materialDict[material] += 1

f = open('materials.txt', 'w')
f.write(pp.pformat(materialDict))
