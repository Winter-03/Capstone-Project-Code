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
#This periodic data grab will be coded below to grab a pressure reading every x seconds for 24 hrs:
import time
import random as rand

#ask user if the device needs calibrated
calibration = input("Does the device require calibration(Y/N):")
if len(calibration) == 1 and calibration.upper() == "Y":
    device_calibrate = 85+rand.randint(1,15)
    print("The device has found that the current filter is allowing %s cm^3/s" % device_calibrate)
else:
    devce_calibrate = 85
    print("The device has auto set the nominal air flow rate to %s cm^3/s" % device_calibrate)


sleep_time = input("How often (sec) should the device check to see if the HVAC system is ON for the next 24 hours?:")
if len(sleep_time) == 0:
    print("No time entered, duration defaulted to 5s")
    sleep_time = 5
else:
    sleep_time = int(sleep_time)

repeat_pressure_check = 86400/sleep_time
total_time = 24
print("The HVAC system will be checked every [%s] seconds for a total of [%s] hours" % (sleep_time, total_time))
time_remaining = 86400
initial_collection = 0
arl = []

#the code below creates the loop for the device to check constantly for 24 hrs

higher_watch = 0
while higher_watch < 1:
    watch = 0
    #below is the inner loop to check if the HVAC is on and record data
    while watch <= repeat_pressure_check:
        instantaneous_pressure = rand.randint(1, 100)
        if instantaneous_pressure > 95:
            print("HVAC system has turned [ON] within the last [%s] seconds" % sleep_time)
            system_state = "ON"
            break
        elif watch == 0:
            print("Initializing check...\n-------------------------------------------------------------------------")
            time.sleep(5)
            print("Sampling Started...")
            watch += 1
        else:
            seconds_after_start = str(watch*sleep_time)
            print("The pressure reading taken at ["+seconds_after_start+"s] indicates the HVAC system is [OFF]")
            system_state = "OFF"
            watch += 1
        time.sleep(sleep_time)

    print("Stopping check...\n-------------------------------------------------------------------------")
    time.sleep(5)

    #the for loop below will record data for 30s, average it, and print it

    if system_state == "OFF":
        print("The HVAC system did not turn on in the time designated\nPlease enter new times")
        higher_watch = 1
    else:
        print("Air Filter Life (AFL) will now be determined")
    #the assumption for this section of code is that the flow through a perfect filter is 100 cm^3/s
        flow_rate_collection = []
        print("The device will now spend the next 30s collecting flow data...")
        if initial_collection == 0:
            for i in range(30):
                flow_rate_collection.append(device_calibrate-rand.randint(1, 5))
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
        arl.append(str(result)+"%")

        #printing results for the user

        print("The average flow for the system was found to be [%s]cm^3/s" % result)
        capacity_percent = 100*(result/100)
        per = "%"
        time_remaining = (time_remaining-(watch*sleep_time))/3600
        time_remaining = round(time_remaining, 3)
        print("The HVAC system is running at [%s%s]" % (capacity_percent, per))
        print("-------------------------------------------------------------------------")
        print("The device will now repeat this process with the current settings..."
              "\nSample Time [%s]s\nFor the next [%s] hours" % (sleep_time, time_remaining))
        print("-------------------------------------------------------------------------")
        time_remaining = time_remaining*3600

        #checking to see if the upper loop needs to end

        if time_remaining/3600 < 0.1:
            print("The device has completed 24 hrs of scanning the HVAC system")
            print("Filter life is currently at [%s%s]" % (capacity_percent, per))
            higher_watch = 1
        elif capacity_percent < 5:
            print("The filter life is below 5%")
            print("The device will now stop checking the HVAC system")
            higher_watch = 1
        else:
            continue

#creating a report for the user to view the data

print("A report will be made of the arl %\nLoading Report...")
time.sleep(3)
print(arl)
