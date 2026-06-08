from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .models import TermsAndConditions

def terms_and_conditions(request):
    # Get the first (or only) Terms and Conditions object from the database
    terms = TermsAndConditions.objects.first()  # You can also use .last() or .get() if needed
    return render(request, 'terms_and_conditions.html', {'terms': terms})


# views.py
from django.shortcuts import render
from .models import AboutUs

def about_us(request):
    about_us_content = AboutUs.objects.first()  # Get the first "About Us" entry
    return render(request, 'about_us.html', {'about_us': about_us_content})

from django.shortcuts import render, redirect
from .models import ContactUs
from django.contrib import messages

def contact_us(request):
    if request.method == 'POST':
        # Retrieve data from the form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')  # Retrieve phone number
        message = request.POST.get('message')

        # Check if all fields are filled
        if name and email and message:
            # Save the data to the database
            ContactUs.objects.create(name=name, email=email, phone=phone, message=message)
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            return redirect('contact')  # Redirect to the contact page after submission
        else:
            messages.error(request, 'All fields are required. Please fill out the form again.')
    
    return render(request, 'contact_us.html')




