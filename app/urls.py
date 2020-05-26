from django.urls import path
from . import views

urlpatterns = [
    path('/<lat>/<lon>/<city>', views.home, name='this_city'),

]