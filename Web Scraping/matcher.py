import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('WinHacksKey.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://winhacks-2020-database2.firebaseio.com'
    })

ref = db.reference()
data = ref.get()
ref = db.reference().child("Companies_Emails")

for company in data["Companies"]:
    try:
        for material in data["Companies"][company]["Materials"]:
            for item in data["Supplies Needed"]:
                for supply in data["Supplies Needed"][item]["Materials"]["Keywords"]:
                    if material.lower() == supply.lower():
                        print(str(company)+ " can use "+ str(material) + " to help make "+ str (item))
                        ref.child(company).child("Materials").child(supply.lower()).child(item).set(data["Supplies Needed"][item]["Materials"]["Keywords"][supply])
    except:
        continue

for company in data["Companies"]:
    for category in data["Companies"][company]["Category"]:
        if category.lower() == "information technology solutions" or category.lower() == "information backup":
            ref.child(company).child("Services").child(category.lower()).set("IT Support Services")
        if category.lower() == "security audit" or category.lower() == "security systems and monitoring":
            ref.child(company).child("Services").child(category.lower()).set("Guard - Security services")
