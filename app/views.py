from django.shortcuts import render
import requests
from datetime import date, timedelta,datetime


# Create your views here.
def home(request, lat,lon,city):
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&appid=93ab64047e82a28bc16250d0e21fa517'

    json_data = requests.get(url.format(lat,lon)).json()

    temp=json_data['current']['temp']

    week_data=[]
    hour_data=[]

    # Iterates through the array of dictionaries named list in json_data

    for item in json_data['hourly']:


        # Time of the weather data received, partitioned into 3 hour blocks
        timestamp= item["dt"]
        d = datetime.fromtimestamp(int(timestamp))
        hour = d.strftime("%I%p").strip('0')

        hourly_weather={
            'hour': hour,
            'temperature': item['temp'],
            'pic': item['weather'][0]['icon']
        }
        hour_data.append( hourly_weather)
        #print( hourly_weather['hour'])
        if (len(hour_data)==24):
            break

    for item in json_data['daily']:
        timestamp = item["dt"]
        d = datetime.fromtimestamp(int(timestamp))
        day = d.strftime("%A")

        weekly_weather={
            'week_day': day,
            'temp_min': item['temp']['min'],
            'temp_max': item['temp']['max'],
            'icon': item['weather'][0]['icon']
        }
        week_data.append(weekly_weather)

    context = {
        'city' : city,
        'week_data' : week_data,
        'hour_data' : hour_data,
        'temp': temp

    }

    return render(request,'home.html', context)