import smtplib
#this library already comes with python, it defines a SMTP client object, used to interact with mail servers
import ssl
#this library aleady comes with python, it creates a secure connection between the client and the server

port = 465
smtp_server = "smtp.gmail.com"
try:
  sender_email = input("Enter the device email: ")
  receiver_email = input("Enter the recipients email: ")
  password = input("Enter the password for [%s]: " % sender_email)

  message = """\
  Subject: Test Email From AFL Device

  This message is a test email from the AFL Device"""

  context = ssl.create_default_context()

  with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
      server.login(sender_email, password)
      server.sendmail(sender_email, receiver_email, message)
except:
    print("ERROR: An error occurred while trying to send an email\nto [%s]\nfrom [%s]\npass [%s]"
          % (receiver_email, sender_email, password))
else:
    print("Email Sent to [%s]" % receiver_email)
