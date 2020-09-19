from django.urls import path
from .import views
urlpatterns=[
    path('',views.getweather,name = "homepage"),
    path('delete/<cityname>/',views.delete_city, name='delete_city'),
]