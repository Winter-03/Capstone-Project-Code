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
import random as rand

print("This code is used to emulate our project\nIt will take a periodic data samples every day* for 10 days")
print("For testing and time purposes 1 day is 3 minutes in this code")
print("-------------------------------------------------------------------------")

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
day_duration = 180
sleep_time = day_duration/repeat_pressure_check
print("The HVAC system will be checked [%s] times a day or every [%s] seconds for this example code" % (repeat_pressure_check, sleep_time))
print("-------------------------------------------------------------------------")
initial_collection = 0
afl = []
days_run = 1
battery_life = 100
life_percentage = 100
#the code below creates the loop for the device to check at daily interval periods
#some choices like the chance for the HVAC system to be on a true to real life


while days_run != 10 and battery_life > 5 and life_percentage > 10:
    watch = 0
    print("Day [%s]" % days_run)
    print("Batter Life Remaining [%s]" % battery_life)
    print("Filter Life Remaining [%s]" % life_percentage)
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
        print("The device will now spend the next 30s collecting flow data...")
        if initial_collection == 0:
            for i in range(30):
                flow_rate_collection.append(device_calibrate_pres_on-rand.randint(1, 5))
                time.sleep(1)
        else:
            for i in range(30):
                flow_rate_collection.append(result-rand.randint(1, 10))
                time.sleep(1)
        initial_collection += 1
        print("Flow data collected")

        #defining the function to find average flow rate

        def flow_avg(frc):
            return sum(frc)/len(frc)
        result = round(flow_avg(flow_rate_collection), 3)
        afl.append(str(result)+"%")
        life_percentage = round((result/device_calibrate_pres_on)*100,2)
        #printing results for the user

        print("The average flow for the system was found to be [%s]cm^3/s" % result)
        per = "%"
        day_time_remaining = (day_duration-(watch*sleep_time))
        day_time_remaining = round(day_time_remaining, 3)
        print("The HVAC system is running at [%s%s]" % (life_percentage, per))
        print("-------------------------------------------------------------------------")
        print("The device will now stop this process for the day")
        print("-------------------------------------------------------------------------")

        #checking to see if the upper loop needs to end

        days_run += 1
        battery_life = battery_life - 0.5*watch
        time.sleep(day_time_remaining)

if days_run == 5:
    print("This code ran for 5 days and has now stopped\nThank you for using it")
elif battery_life <= 5:
    print("The amount of samples per day drained the battery and ended the 5 day test early")
else:
    print("The air filter was clogged before the end of the 5 test days so the the test has ended early")
#creating a report for the user to view the data

print("A report will be made of the afl %\nLoading Report...")
time.sleep(3)
for i in afl:
    print(i)
