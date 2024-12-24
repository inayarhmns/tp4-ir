from django.urls import path
from search.views import *

app_name = 'search'

urlpatterns = [
   # path('', search, name='search'),
   path('', home, name='home'),
   path('detail/<str:docno>/', detail, name='detail'),
   path('hi', hi, name='hi')

]