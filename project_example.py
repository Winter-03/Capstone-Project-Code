"""
this code is an attempt to emulate what our board will actually be doing in real time
# comments will be left periodically to explain the code found below it
feel free to download this and run it
if you find an issue or think you can add something then:
add an issue:
    https://github.com/MoistH2O/Capstone-Project-Code/issues
try to make a change by yourself:
    https://github.com/MoistH2O/Capstone-Project-Code/pulls
"""


#Unless the board is wired to the HVAC system it will need to grab data periodically
#to see when it needs to start tracking air filter life.
#This periodic data grab will be coded below to grab a pressure reading:
import time
#this library already comes with python
import random as rand
#this library already comes with python
import requests
#python -m pip install requests
from bs4 import BeautifulSoup
#python -m pip install beautifulsoup4
import smtplib
#this library already comes with python, it defines a SMTP client object, used to interact with mail servers
import ssl
#this library already comes with python, it creates a secure connection between the client and the server
from datetime import date
#this library already comes with python


print("This code is used to emulate our project\nIt will take a periodic data samples every day* for 10 days")
print("For testing and time purposes 1 day is 1 minute in this code")
print("-------------------------------------------------------------------------")


#setting up ssl and smtp
port = 465
smtp_server = "smtp.gmail.com"


#ask user if the device needs calibrated
calibration = input("Does the device require calibration(Y/N):")
if len(calibration) == 1 and calibration.upper() == "Y":
    device_calibrate_pres_on = 85+rand.randint(1,15)
    print("The device has found that the current filter is allowing [%s] cm^3/s" % device_calibrate_pres_on)
else:
    device_calibrate_pres_on = 85
    print("The device has auto set the nominal air flow rate to [%s] cm^3/s" % device_calibrate_pres_on)


repeat_pressure_check = input("How many times a day should the device check to see if the HVAC system is ON?:")
if len(repeat_pressure_check) == 0:
    print("No time entered, duration defaulted to [10] times a day")
    repeat_pressure_check = 10
else:
    repeat_pressure_check = int(repeat_pressure_check)
day_duration = 60
sleep_time = round(day_duration/repeat_pressure_check,3)
print("The HVAC system will be checked [%s] times a day or every [%s] seconds for this example code" %
      (repeat_pressure_check, sleep_time))
print("-------------------------------------------------------------------------")
initial_collection = 0
afl_report = []
days_run = 1
battery_life = 100
life_percentage = 100

# #defining the function to find average flow rate
def flow_avg(frc):
    return sum(frc) / len(frc)

#grabbing aqi data for day
def web_grab_aqi(url):
    global aqi
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("div", class_="aqivalue")
    results = str(results)
    aqi_start = results.find(">") + 1
    aqi_end = len(results) - 6
    aqi = results[aqi_start:aqi_end]
    aqi = int(aqi)
web_grab_aqi("https://aqicn.org/city/usa/kansas/peck/")

#the code below creates the loop for the device to check at daily interval periods
#some choices like the chance for the HVAC system to be on a true to real life
while days_run <= 10 and battery_life > 5 and life_percentage > 10:
    watch = 0
    print("Day [%s]" % days_run)
    afl_report.append("Day [%s]" % days_run)
    print("Batter Life Remaining [%s]" % battery_life)
    afl_report.append("Batter Life Remaining [%s]" % battery_life)
    print("Filter Life Remaining [%s]" % life_percentage)
    afl_report.append("Filter Life Remaining [%s]" % life_percentage)
    print("The aqi for today is [%s]" % aqi)
    afl_report.append("AQI [%s]" % aqi)
    #below is the inner loop to check if the HVAC is on and record data
    while watch <= repeat_pressure_check:
        chance_for_HVAC_on = rand.randint(1, 100)
        if watch == 0:
            print("Initializing check for new day...\n-------------------------------------------------------------------------")
            time.sleep(5)
            print("Sampling Started...")
            watch += 1
        elif chance_for_HVAC_on > 60:
            print("HVAC system was found to be ON during test [%s]" % watch)
            system_state = "ON"
            break
        else:
            print("The [%s] pressure test of the day indicates the HVAC system is [OFF]" % watch)
            print("[%s] more pressure test(s) will be preformed today" % (repeat_pressure_check-watch))
            system_state = "OFF"
            watch += 1
        time.sleep(sleep_time)

    print("Stopping check...\n-------------------------------------------------------------------------")
    time.sleep(5)

    #the for loop below will record data for 30s, average it, and print it

    if system_state == "OFF":
        print("The HVAC system did not turn on today\nThis may be due to an insufficient number of samples per day")
        print("The device will continue to run but may not provide results")
    else:
        print("Current Air Filter Life (AFL) will now be determined")
    #the assumption for this section of code is that the flow through a perfect filter is the calibrated amount
        flow_rate_collection = []
        print("The device will now spend the next 15s collecting flow data...")
        if initial_collection == 0:
            for i in range(15):
                flow_rate_collection.append(device_calibrate_pres_on-rand.randint(1, 5))
                time.sleep(1)
        else:
            for i in range(15):
                flow_rate_collection.append(result-rand.randint(1, 10))
                time.sleep(1)
        if rand.randint(1,2) == 1:
            aqi = aqi + rand.randint(1, 20)
        else:
            aqi = aqi - rand.randint(1, 20)
        initial_collection += 1
        print("Flow data collected")

        result = round(flow_avg(flow_rate_collection), 3)
        afl_report.append("Flow Rate [" + str(result)+"]cm^3/s")
        life_percentage = round((result/device_calibrate_pres_on)*100,2)

        #printing results for the user
        print("The average flow for the system was found to be [%s]cm^3/s" % result)
        per = "%"
        day_time_remaining = (day_duration-(watch*sleep_time))
        day_time_remaining = round(day_time_remaining, 3)
        print("The HVAC system is running at [%s%s]" % (life_percentage, per))
        afl_report.append("HVAC running at [%s%s]" % (life_percentage, per))
        print("-------------------------------------------------------------------------")
        afl_report.append("-------------------------------------------------------------------------")
        print("The device will now stop this process for the day")
        print("-------------------------------------------------------------------------")

        #checking to see if the upper loop needs to end

        days_run += 1
        battery_life = battery_life - 0.5*watch
        time.sleep(day_time_remaining)

if days_run == 11:
    print("This code ran for 10 days and has now stopped\nThank you for using it")
elif battery_life <= 5:
    print("The amount of samples per day drained the battery and ended the 10 day test early")
else:
    print("The air filter was clogged before the end of the 10 test days so the the test has ended early")


#creating a report for the user to view the data
print("A report will be made of the 10 day period \nLoading Report...")
time.sleep(3)
for i in afl_report:
    print(i)

#asking the user if an email would like to be sent?
send_email_question = input("\n\n\nWould you like the results emailed to you?: ")
if len(send_email_question) == 1 and send_email_question.upper() == "Y":
    sender_email = input("Enter the device email: ")
    print("Entered Email: [%s]" % sender_email)
    receiver_email = input("Enter the recipients email: ")
    print("Entered Email: [%s]" % receiver_email)
    password = input("Enter the password for [%s]: " % sender_email)
    print("Entered pass: [%s]" % password)
    context = ssl.create_default_context()
    try:
        today = date.today()
        human_day = today.strftime("%m/%d/%y")
        afl_report = str(afl_report)
        message = ("Subject: Test Email from AFL Device [%s]\n\n" % human_day)+afl_report
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
    except:
        print("ERROR: An error occurred while trying to send an email\nto [%s]\nfrom [%s]\npass [%s]"
              % (receiver_email, sender_email, password))
    else:
        print("Email Sent to [%s]" % receiver_email)
else:
    print("Test Results Were not Emailed")

