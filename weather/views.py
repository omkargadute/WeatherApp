from django.shortcuts import render,redirect
import requests
from .models import City
from .forms import CityForm

def home(request):
    return render(request,'weather/index.html')

def getweather(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=d89550a8d45ee731978cdf531bc7ab3d'
    
    error = ""
    message = ""
    message_class = ""
    if request.method == "POST":
        form = CityForm(request.POST)

        if form.is_valid():
            cityname = form.cleaned_data['name']
            isPresent = City.objects.filter(name = cityname).count()

            if isPresent == 0:
                data = requests.get(url.format(cityname)).json()

                if data['cod'] == 200:
                    form.save()
                else:
                    error = 'Invalid City Name.'
            else:
                error = "City Already Added."

        if error:
            message = error
            message_class = 'danger'
        else:
            message = 'City added successfully!'
            message_class = 'success'
    form = CityForm()

    cities = City.objects.all()

    weatherData  = []
    for city in cities:
        data = requests.get(url.format(city)).json()
        city_weather = {
            'city': city.name,
            'temperature': data['main']['temp'],
            'description': data["weather"][0]["description"],
            'icon': data["weather"][0]["icon"],
        }
        weatherData.append(city_weather)

    context = {
        'weatherData':weatherData,
        'form':form,
        'message':message,
        'message_class':message_class,
        }
    return render(request,'weather/index.html',context)



def delete_city(request, cityname):
    City.objects.get(name=cityname).delete()
    return redirect('homepage')