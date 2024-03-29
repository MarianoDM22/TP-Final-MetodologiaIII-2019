from datetime import datetime

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.template import loader
from django.views import generic

from .models import City, Property, ReservationDate, Reservation


def index(request):
    cities = City.objects.all()
    context = {'cities': cities }
    return render(request, 'bookings/index.html', context)


def hotel_search_results(request):
    if request.method == 'GET':
        properties = Property.objects.all()
        context = {'properties': properties}
        return render(request, 'bookings/hotel-search-results.html', context)
    if request.method == 'POST':
        city = request.POST['city']
        pax = request.POST['pax']
        max_price = request.POST['max_price']
        properties = Property.objects.all()

        if not city.__eq__('None'):
            properties = properties.filter(city=city)

        if not pax.__eq__('None'):
            properties = properties.filter(max_pax__gte=pax)

        if max_price is not '':
            properties = properties.filter(daily_cost__lte=max_price)

        context = {'properties': properties}
        return render(request, 'bookings/hotel-search-results.html', context)

def hotel_city_results(request):
    if request.method == 'GET':
        properties = Property.objects.all()
        context = {'properties': properties}
        return render(request, 'bookings/hotel-hotel-list.html', context)
    if request.method == 'POST':
        city = request.POST['city']
        properties = Property.objects.all()

        if not city.__eq__('None'):
            properties = properties.filter(city=city)

        context = {'properties': properties}
        return render(request, 'bookings/hotel-list.html', context)


def hotel_details(request, property_id):
    try:
        requested_property = Property.objects.get(id=property_id)
    except Property.DoesNotExist:
        raise Http404("Not Found")
    return render(request, 'bookings/hotel-details.html', {'property': requested_property})


def check_availability(request):
    if request.method == 'POST':
        datetime_start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d').date()
        datetime_end_date = datetime.strptime(request.POST['end_date'], '%Y-%m-%d').date()
        requested_property = Property.objects.get(id=request.POST['property_id'])
        reservation_dates = ReservationDate.objects.filter(property=requested_property.id)
        for reservation_date in reservation_dates:
            if reservation_date.reservation is not None:
                if datetime_start_date <= reservation_date.date <= datetime_end_date:
                    return render(request, 'bookings/no-availability.html')
        r = Reservation(
            reservation_date=datetime.now().date(),
            property=requested_property,
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'])
        r.save()
        count = 0
        for reservation_date in reservation_dates:
            if datetime_start_date <= reservation_date.date <= datetime_end_date:
                reservation_date.reservation = r
                reservation_date.save()
                count = count + 1
        if count == 0:
            return render(request, 'bookings/no-availability.html')
        r.total_amount = r.property.daily_cost * r.property.reservationdate_set.filter(reservation=r).count()
        r.save()
        return redirect('bookings:successful_booking', r.id)


def successful_booking(request, reservation_id):
    try:
        requested_reservation = Reservation.objects.get(id=reservation_id)
    except Property.DoesNotExist:
        raise Http404("Not Found")
    return render(request, 'bookings/itinerary.html', {'reservation': requested_reservation})
