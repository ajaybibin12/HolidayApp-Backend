from django.urls import path
from .views import FetchHolidaysView,SearchHolidaysView

urlpatterns = [
    path('fetch/', FetchHolidaysView.as_view(), name='fetch_holidays'),
    path('search/', SearchHolidaysView.as_view(), name='search_holidays')
]