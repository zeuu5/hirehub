from django.shortcuts import render,redirect
from . models import Services
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from customers.models import Customer


from django.core.paginator import Paginator
from django.shortcuts import render

from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Services

from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Services
from django.db.models import Avg


def detail_service(request, service_id):
    service = get_object_or_404(Services, id=service_id)
    form = ReviewForm()
    
    # Calculate the average rating
    average_rating = service.reviews.aggregate(Avg('rating'))['rating__avg']
    if average_rating is None:
        average_rating = 0  # Default to 0 if no reviews are present

    return render(request, "service_details.html", {
        "service": service,
        "form": form,
        "average_rating": round(average_rating, 1),  # Round to 1 decimal place
    })






def select_category(request):
    if request.method == "POST":
        category = request.POST.get("title")
        request.session["selected_category"] = category
        return redirect(request.META.get('HTTP_REFERER', '/')) 
    

# views.py
from django.shortcuts import render
from .models import Services
from .forms import ServiceSearchForm

def search_services(request):
    form = ServiceSearchForm(request.GET or None)
    query = request.GET.get('query', '')  # Get the query from the GET request
    results = Services.objects.none()

    if query:
        # If there is a search query, filter the Services model
        results = Services.objects.filter(
            title__icontains=query) | Services.objects.filter(description__icontains=query) | Services.objects.filter(city__icontains=query)

    return render(request, 'search_services.html', {'form': form, 'results': results})







from django.shortcuts import render, get_object_or_404, redirect
from .models import Services, Review


from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required

@login_required
def service_detail(request, service_id):
    service = get_object_or_404(Services, id=service_id)
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.service = service
            review.user = request.user  # Ensure user is logged in
            review.save()

            # Update the service's average rating
            service.update_average_rating()

            return redirect('service_detail', service_id=service.id)

    return render(request, 'service_detail.html', {'service': service, 'form': form})





from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Services, Review
from .forms import ReviewForm

@login_required
def add_review(request, service_id):
    service = get_object_or_404(Services, id=service_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.service = service
            review.user = request.user
            review.save()

            # Update average rating
            service.update_average_rating()

            return JsonResponse({
                "success": True,
                "username": request.user.username,
                "rating": review.rating,
                "comment": review.comment,
                "new_average_rating": service.average_rating  # Send updated average rating
            })
        else:
            return JsonResponse({"success": False, "error": "Invalid form data"}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)




from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Services, Review
from .forms import ReviewForm
import requests

def index(request):
    # Get city from GET request or session
    selected_city = request.GET.get("city", request.session.get("selected_city"))

    # Store selected city in session if provided in the request
    if selected_city:
        request.session["selected_city"] = selected_city

    # Fetch featured services
    featured_services = Services.objects.all()
    
    # Apply city filter to featured services
    if selected_city:
        featured_services = featured_services.filter(city__icontains=selected_city)

    # Slice featured services
    featured_services = featured_services[:4]

    # Fetch latest services (sorted by created_at in descending order)
    latest_services = Services.objects.all().order_by('-created_at')

    # Apply city filter to latest services
    if selected_city:
        latest_services = latest_services.filter(city__icontains=selected_city)

    # Limit latest services to 5 (or as needed)
    latest_services = latest_services[:4]

    return render(request, "index.html", {
        "featured_services": featured_services,
        "latest_services": latest_services,  # Pass latest services to template
        "selected_city": selected_city,  # Pass selected city for UI updates
    })

def list_service(request):
    selected_city = request.session.get("selected_city", "")
    
    page = request.GET.get("page", 1)
    sort_by = request.GET.get("sort", "created_at")
    query = request.GET.get("query", "")

    sorting_options = {
        "price_low": "price",
        "price_high": "-price",
        "newest": "-created_at",
        "oldest": "created_at",
        "priority": "-priority",
    }
    order_by_field = sorting_options.get(sort_by, "-created_at")

    service_list = Services.objects.all()

    if selected_city:
        service_list = service_list.filter(city__icontains=selected_city)

    if query:
        service_list = service_list.filter(title__icontains=query) | service_list.filter(description__icontains=query)

    service_list = service_list.order_by(order_by_field)
    service_paginator = Paginator(service_list, 16)
    service_list = service_paginator.get_page(page)

    latitude = request.session.get("latitude")
    longitude = request.session.get("longitude")

    context = {
        "services": service_list,
        "sort_by": sort_by,
        "query": query,
        "selected_city": selected_city,
        "latitude": latitude,
        "longitude": longitude,
    }
    return render(request, "services.html", context)

@login_required
def add_service(request):
    if request.method == "POST":
        service_name = request.POST.get("service")
        rate = request.POST.get("rate")
        description = request.POST.get("service description")
        image = request.FILES.get("image")
        city = request.POST.get("city")

        if not service_name or not rate or not description or not city:
            messages.error(request, "All fields are required.")
            return render(request, 'add_service.html')

        try:
            rate = float(rate)
        except ValueError:
            messages.error(request, "Invalid rate value.")
            return render(request, 'add_service.html')

        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        latitude, longitude = map(float, data['loc'].split(','))

        service = Services.objects.create(
            title=service_name,
            price=rate,
            description=description,
            image=image,
            customer=request.user,
            city=city,
            latitude=latitude,
            longitude=longitude
        )
        
        request.session["latitude"] = latitude
        request.session["longitude"] = longitude

        messages.success(request, "Service added successfully!")
        return redirect('list_service')

    return render(request, 'add_service.html')

from django.shortcuts import redirect

def select_city(request):
    if request.method == "POST":
        city = request.POST.get("city")
        if city:  # Ensure city is not empty
            request.session["selected_city"] = city
        return redirect(request.META.get("HTTP_REFERER", "/"))
    
    # If method is GET, retrieve the selected city from session
    selected_city = request.session.get("selected_city", "")

    return selected_city  # Modify based on how you want to use it in views
