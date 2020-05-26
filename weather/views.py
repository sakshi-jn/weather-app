from .models import City
from django.shortcuts import render, redirect
import requests
from .forms import CityForm


def index(request):

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=93ab64047e82a28bc16250d0e21fa517'

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            city_count = City.objects.filter(name=new_city).count()

            if city_count == 0:
                r = requests.get(url.format(new_city)).json()

                if r['cod']== 200:
                    form.save()
                else:
                    err_msg= 'Not a valid City!'
            else:
                err_msg = 'City already exist!'

        if err_msg :
            message = err_msg
            message_class = 'is-danger'
        else :
            message = 'City added successfully!'
            message_class = 'is-success'

    #print(err_msg)
    form = CityForm()
    weather_data=[]

    cities = City.objects.all()

    for city in cities:

        city_weather = requests.get(url.format(city)).json()
        weather = {
            'city': city,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon'],
            'long': city_weather['coord']['lon'],
            'lati': city_weather['coord']['lat'],

        }

        weather_data.append(weather)

    context = {
        'weather_data' : weather_data,
        'form': form,
        'message': message,
        'message_class': message_class,
    }

    return render(request, 'index.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()

    return redirect('home')