import json
import requests
import smtplib
import os
import logging
from datetime import datetime
from time import sleep
from threading import Thread


def send_email(message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(FROM_EMAIL, PASSWORD)
    msg = message
    try:
        server.sendmail(FROM_EMAIL, TO_EMAIL, msg)
    except:
        print('Email failed to send')
    server.quit()


def get_forecast(temp_lat, temp_lon):
    weather_url = f'https://api.darksky.net/forecast/{API_TOKEN_WEATHER}/{temp_lat},{temp_lon}'
    r = requests.get(weather_url)
    j = json.loads(r.text)
    temp_temperature = j['currently']['temperature']
    return temp_temperature


def get_location(temp_ip_address):
    loc_url = f'http://api.ipstack.com/{temp_ip_address}?access_key={API_TOKEN_LOCATION}'
    r = requests.get(loc_url)
    j = json.loads(r.text)
    temp_lat = j['latitude']
    temp_lon = j['longitude']
    return temp_lat, temp_lon


def get_ip_address():
    ip_url = 'http://jsonip.com'
    r = requests.get(ip_url)
    j = json.loads(r.text)
    temp_ip_address = j['ip']
    return temp_ip_address


def main(window_status):
    ip_address = get_ip_address()
    lat, lon = get_location(ip_address)
    temperature = get_forecast(lat, lon)
    if temperature > 75:
        if window_status == 'Open':
            message = f'Make sure windows are closed. Current temperature is {temperature}'
            send_email(message)
            window_status = 'Closed'
    else:
        if window_status == 'Closed':
            message = f'Make sure windows are open. Current temperature is {temperature}'
            send_email(message)
            window_status = 'Open'
    if logging_status == 'Yes':
        logger.info(f"{datetime.now()}: {temperature} - windows are {window_status}")


if os.path.isfile('secrets.py'):
    from secrets import API_TOKEN_WEATHER, API_TOKEN_LOCATION, FROM_EMAIL, PASSWORD, TO_EMAIL
else:
    answer = ''
    API_TOKEN_LOCATION = input('Please enter your API key for https://ipstack.com: ')
    API_TOKEN_WEATHER = input('Please enter your API key for https://darksky.net/dev: ')
    FROM_EMAIL = input("Please enter the 'from' address (gmail): ")
    PASSWORD = input('Please enter the password for this address: ')
    TO_EMAIL = input("Please enter the 'to' address: ")
    f = open("secrets.py", "w+")
    f.write(f'API_TOKEN_LOCATION = "{API_TOKEN_LOCATION}"\n')
    f.write(f'API_TOKEN_WEATHER = "{API_TOKEN_WEATHER}"\n')
    f.write(f'FROM_EMAIL = "{FROM_EMAIL}"\n')
    f.write(f'PASSWORD = "{PASSWORD}"\n')
    f.write(f'TO_EMAIL = "{TO_EMAIL}"\n')
    f.close()

while True:
    answer = input('Are your windows currently open? (y/n): ')
    if answer.upper() == 'Y':
        window_status = 'Open'
        break
    elif answer.upper() == 'N':
        window_status = 'Closed'
        break
while True:
    answer = input('Enable logging of weather checks? (y/n): ')
    if answer.upper() == 'Y':
        logging_status = 'Yes'

        # Set up a logger
        logger = logging.getLogger('weather')
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler('weather_check.log')
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        break
    elif answer.upper() == 'N':
        logging_status = 'No'
        break
os.system('cls')

if __name__ == '__main__':
    Thread(target=main(window_status)).start()
    while True:
        sleep(3600)
        Thread(target=main(window_status)).start()