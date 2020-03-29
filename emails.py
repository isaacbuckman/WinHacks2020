import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('WinHacksKey.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://winhacks-2020-database2.firebaseio.com'
    })

ref = db.reference()
data = ref.get()

def sendEmail(name):
    global data

    companyName = name
    materials = data["Companies_Emails"][companyName]["Materials"]
    materialList = []
    productList = []

    for item in materials:
        materialList.append(item)
        for item2 in data["Companies_Emails"][companyName]["Materials"][item]:
            if item2 not in productList:
                productList.append(item2)
    
    print (productList)
    
    materials = ""
    if len(materialList) == 1:
        materials = str(materialList[0])
    elif len(materialList) == 2:
        materials = str(materialList[0]) + " and " + str(materialList[1])
    else:
        materials = str(materialList[0]) + ", " + str(materialList[1]) + ", and " + str(materialList[2])

    if len(productList) == 1:
        products = str(productList[0])
    elif len(productList) == 2:
        products = str(productList[0]) + " and " + str(productList[1])
    elif len(productList) == 3:
        products = str(productList[0]) + ", " + str(productList[1]) + ", and " + str(productList[2])
    elif len(productList) == 4:
        products = str(productList[0]) + ", " + str(productList[1]) + ", " + str(productList[2]) + ", and " + str(productList[3])


    sender_email = "winhackstesting@gmail.com"
    receiver_email = "winhackstesting@gmail.com"
    password = "HelloJosh1!"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Covid-19 Aid"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    html = """\
    <html>
    <body>
        <p>Dear {0}, <br><br>
        We have noticed that you are capable of using your expertise in <b>{1}</b> 
        to assist with the creation of <b>{2}</b>. Due to the outbreak of COVID-19, we are 
        looking for businesses such as yours to help us produce the goods needed for handling 
        the pandemic. Please fill out the following form to help us determine if you are 
        willing to help out in this national effort, and to what extent. <br>

        <table width="100%" cellspacing="0" cellpadding="0">
  <tr>
      <td>
          <table cellspacing="10" cellpadding="0">
              <tr>
                  <td style="border-radius: 2px;" bgcolor="#ED2939">
                      <a href="https://www.copernica.com" target="_blank" style="padding: 8px 12px; border: 1px solid #ED2939;border-radius: 2px;font-family: Helvetica, Arial, sans-serif;font-size: 14px; color: #ffffff;text-decoration: none;font-weight:bold;display: inline-block;">
                          Navigate to Form             
                      </a>
                  </td>

                  <td style="border-radius: 2px;" bgcolor="#ED2939">
                      <a href="https://www.copernica.com" target="_blank" style="padding: 8px 12px; border: 1px solid #ED2939;border-radius: 2px;font-family: Helvetica, Arial, sans-serif;font-size: 14px; color: #ffffff;text-decoration: none;font-weight:bold;display: inline-block;">
                          I already Submitted!
                      </a>
                  </td>
              </tr>
          </table>
      </td>
  </tr>
</table> 
        </p>
    </body>
    </html>
    """.format(companyName, materials, products)

    # Turn these into plain/html MIMEText objects
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

sendEmail("Advanced Machining Services")