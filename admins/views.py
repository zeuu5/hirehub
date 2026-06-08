from django.shortcuts import render
from .models import Feedback
from django.contrib import messages


# Create your views here.


def save_feedback(request):
    if request.method == 'POST':
        # Get the feedback data from the request
        name = request.POST.get('name')
        email = request.POST.get('email')
        your_feedback = request.POST.get('your_feedback')

        # Check if the required data is provided
        if name and email and your_feedback:
            # Create a new Feedback instance and save it to the database
            Feedback.objects.create(name=name, email=email, your_feedback=your_feedback)
            # Add a success message
            messages.success(request, "Thank you for your feedback!")
        else:
            # Add an error message if any field is missing
            messages.error(request, "All fields are required. Please try again.")
    
    # Render the same page with messages
    return render(request, 'feedback_form.html')
