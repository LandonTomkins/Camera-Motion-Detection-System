import time
import smtplib
import csv

#class UserInfoClass():
USER_INFO = []
with open('MotionDetectionContacts.csv', 'r') as contact_file:
    reader = csv.DictReader(contact_file)
    for row in reader:
        USER_INFO.append(row)
        #{"to": "6625521313@cspire1.com", "gmail_user": "rpimotionsystem@gmail.com", "gmail_pass": "rpimotion"}]

SUBJECT = 'Motion Detected!'
TEXT = 'Your Raspberry Pi detected an intruder!'
print(USER_INFO)
print("Sending text")
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
for item in USER_INFO:
    server.login(item["email_un"],item["email_pw"])
    header = 'To: ' + item["recipient"] + '\n' + 'From: ' + item["email_un"]
    header = header + '\n' + 'Subject: ' + SUBJECT + '\n'
    print(header)
    msg = header + '\n' + TEXT + '\n\n'
    server.sendmail(item["email_un"],item["recipient"],msg)

server.quit()
time.sleep(1)
print("Text sent")