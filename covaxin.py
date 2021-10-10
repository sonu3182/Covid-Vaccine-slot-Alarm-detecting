import requests
from pygame import mixer 
from datetime import datetime, timedelta
import time


age = int(input("Enter Your Age:-  "))
pincodes = [input('Enter your Pin_Code:-  ')]
print('\n')
num_days = 2

print_flag = 'Y'

print("Starting search for Covid vaccine slots! \n")

actual = datetime.today()
list_format = [actual + timedelta(days=i) for i in range(num_days)]
actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]

while True:
    counter = 0   

    for pincode in pincodes:   
        for given_date in actual_dates:

            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pincode, given_date)
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 

            result = requests.get(URL, headers=header)

            if result.ok:
                response_json = result.json()
                # print(response_json)
                if response_json["centers"]:
                    # if(print_flag.lower() =='y'):
                    for center in response_json["centers"]:
                        for session in center["sessions"]:
                            if (session["min_age_limit"] <= age and session["available_capacity_dose1"] > 0 ) :
                                print('Pincode: ' + pincode)
                                print("Available on: {}".format(given_date))
                                print("\t", center["name"])
                                print("\t", center["block_name"])
                                print("\t Price: ", center["fee_type"])
                                print("\t Availablity : ", session["available_capacity_dose1"])

                                if(session["vaccine"] != ''):
                                    print("\t Vaccine type: ", session["vaccine"])
                                print("\n")
                                counter = counter + 1
            else:
                print("No Response!")

    if counter:
        mixer.init()
        mixer.music.load('sound/dingdong.wav')
        mixer.music.play()
        print("Vaccination slot is available!",datetime.today())
    else:
        if age>=18:
            if age>=45:
                print(f'Slot is not available for 45+ years old people at',datetime.today())
            else:
                print(f'Slot is not available for 18+ years old people at',datetime.today())
        else:
            print('Vacinge is available for only 18+ and 45+ age\n')
            print('Please Enter your correct Age.\n')
            break
    dt = datetime.now() + timedelta(seconds=15)

    while datetime.now() < dt:
        time.sleep(1)
