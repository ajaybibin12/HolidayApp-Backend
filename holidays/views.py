import requests
from django.conf import settings
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Holiday
from .serializers import HolidaySerializer
from datetime import datetime
from rest_framework.exceptions import ValidationError


class FetchHolidaysView(APIView):
    def get(self, request):
        print("Query Parameters:", request.GET)
        country = request.query_params.get('country')
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        holiday_type = request.query_params.get('type')

        if not year or not year.isdigit() or len(year) != 4 or not (1000 <= int(year) <= 9999):
            raise ValidationError({'error': 'Year must be a 4-digit number between 1000 and 9999'})
        
        if month:
            if not month.isdigit() or not (1 <= int(month) <= 12):
                raise ValidationError({'error': 'Month must be an integer between 1 and 12'})
        
        if not country or not year:
            return Response({'error': 'Country and year are required'}, status=status.HTTP_400_BAD_REQUEST)

        cache_key = f'holidays_{country}_{year}_{month}_{holiday_type}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        # Fetch from Calendarific API
        url = 'https://calendarific.com/api/v2/holidays'
        params = {
            'api_key': settings.CALENDARIFIC_API_KEY,
            'country': country,
            'year': year,
        }
        if month:
            params['month'] = month
        if holiday_type:
            params['type'] = holiday_type

        response = requests.get(url, params=params)
        if response.status_code != 200:
            return Response({'error': 'Failed to fetch data from Calendarific API'}, status=response.status_code)

        holidays = response.json().get('response', {}).get('holidays', [])
        holiday_objects = []

        for holiday in holidays:
            iso_date = holiday.get('date', {}).get('iso', '')
            try:
                formatted_date = datetime.fromisoformat(iso_date).date()
            except ValueError:
                return Response({'error': f'Invalid date format: {iso_date}'}, status=status.HTTP_400_BAD_REQUEST)

            obj, _ = Holiday.objects.update_or_create(
                country=country,
                year=year,
                month=holiday.get('date', {}).get('datetime', {}).get('month', 0),
                name=holiday['name'],
                defaults={
                    'description': holiday.get('description', ''),
                    'date': formatted_date,
                    'type': ', '.join(holiday.get('type', []))
                }
            )
            holiday_objects.append(obj)

        # Serialize and cache the data
        serializer = HolidaySerializer(holiday_objects, many=True)
        cache.set(cache_key, serializer.data, timeout=60 * 60 * 24)
        return Response(serializer.data)



# Endpoint for search the holidays
class SearchHolidaysView(APIView):
    def get(self, request):
        query = request.query_params.get('query')
        if not query:
            return Response({'error': 'Search query is required'}, status=status.HTTP_400_BAD_REQUEST)

        holidays = Holiday.objects.filter(name__icontains=query)
        serializer = HolidaySerializer(holidays, many=True)
        return Response(serializer.data)