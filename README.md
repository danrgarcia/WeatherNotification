# WeatherNotification
This script gets your location based on your IP address and then checks the weather for that area every hour. If it is above 75 it sends out a message to make sure and close the windows on your house, but if it is below 75 it sends out a message to make sure the windows on the house are open.

The first time it is ran it will ask for you API key to ipstack.com which is used for determining your public IP address. It will then ask for your darksky.net API key in order to pull weather data. After that it will ask for the 'from' email address in which to send the message using gmail, the password for the gmail smtp account, and then the 'to' address of which to send the message to. It will write this all to a plaintext python file so that if the program is run again it can import that information instead of asking for it again.

Each time the script is run it will it will ask if your windows are currently open and whether you would like to log each weather check to a text file.

I originally created this script because I live in Arizona where the AC is on constantly and I wanted to try and naturally cool the house down during the cooler times of the day. It was a fun project in practicing using API's and parsing JSON data as well as sending SMTP messages.
