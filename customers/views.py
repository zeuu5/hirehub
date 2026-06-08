
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Customer
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from services.models import Services
from orders.models import Order
import requests
from django.core.paginator import Paginator


def sign_out(request):
    logout(request)
    return redirect('Home')

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer
from services.models import Services


@login_required
def worker_page(request):
    user_services = Services.objects.filter(customer=request.user)  
    page = request.GET.get('page', 1)  
    paginator = Paginator(user_services, 10)  
    paginated_services = paginator.get_page(page)

    return render(request, 'worker_service_list.html', {'services': paginated_services})

@login_required
def service_detail_worker(request, service_id):
    service = get_object_or_404(Services, id=service_id, customer=request.user)
    return render(request, "worker_service_description.html", {"service": service})

@login_required
def delete_service(request, service_id):
    service = get_object_or_404(Services, id=service_id, customer=request.user)
    service.delete()
    messages.success(request, "Service deleted successfully.")
    return redirect("worker_page")
 
# user bookings list
@login_required
def user_page(request):
    orders = Order.objects.filter(customer=request.user)
    return render(request, "user_booking_list.html", {"orders": orders})


from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.utils import IntegrityError
import requests
from .models import Customer  # Ensure Customer model is imported

# def show_user_account(request):
#     context = {}
    
#     if request.method == "POST":
#         if 'register' in request.POST:
#             context['register'] = False
#             try:
#                 username = request.POST.get('username', '').strip()
#                 password = request.POST.get('password', '').strip()
#                 email = request.POST.get('email', '').strip()
#                 address = request.POST.get('address', '').strip()
#                 phone = request.POST.get('phone', '').strip()

#                 # Validate input fields
#                 if not username or not password or not email or not phone:
#                     messages.error(request, "All fields are required.")
#                     return render(request, 'user_account.html', context)

#                 # Check if username already exists
#                 if User.objects.filter(username=username).exists():
#                     messages.error(request, "Username already exists.")
#                     return render(request, 'user_account.html', context)

#                 # Create user account
#                 user = User.objects.create_user(
#                     username=username,
#                     password=password,
#                     email=email
#                 )

#                 # Fetch user's location using ipinfo.io API
#                 try:
#                     response = requests.get('https://ipinfo.io/json', timeout=5)
#                     data = response.json()
#                     if 'loc' in data:
#                         latitude, longitude = data['loc'].split(',')
#                     else:
#                         latitude, longitude = None, None
#                 except requests.RequestException:
#                     latitude, longitude = None, None

#                 # Create customer account
#                 customer = Customer.objects.create(
#                     name=username,
#                     user=user,
#                     phone=phone,
#                     address=address,
#                     latitude=latitude,
#                     longitude=longitude
#                 )

#                 messages.success(request, "Registered Successfully")
#                 # return redirect('Home')

#             except IntegrityError:
#                 messages.error(request, "Username already taken. Try another.")
#             except Exception as e:
#                 messages.error(request, f"An error occurred: {str(e)}")

#         elif 'login' in request.POST:
#             context['register'] = False
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = authenticate(username=username, password=password)
#             if user:
#                 login(request, user)
#                 return redirect('Home')
#             else:
#                 messages.error(request, 'Invalid user credentials')

#     return render(request, 'user_account.html', context)


@login_required
def user_profile(request):
    user = request.user  
    customer, created = Customer.objects.get_or_create(user=user)  # Ensure profile exists
    password_form = PasswordChangeForm(user)  # Initialize password form

    if request.method == "POST":
        if 'update_info' in request.POST:  # Handle profile update
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            address = request.POST.get("address")

            if email:
                user.email = email
                user.save()

            customer.phone = phone if phone is not None else ""
            customer.address = address if address is not None else ""
            customer.save()

            messages.success(request, "Profile updated successfully!")
            return redirect("user_profile")

    # Get the first service ID for the logged-in user
    user_services = Services.objects.filter(customer=request.user)
    service_id = user_services.first().id if user_services.exists() else None

    # **Fix: Get a valid receiver_id (example: first available customer)**
    receiver = Customer.objects.exclude(user=user).first()  # Get another user
    receiver_id = receiver.user.id if receiver else None  

    context = {
        "user": user,
        "customer": customer,
        "password_form": password_form,
        "service_id": service_id,
        "receiver_id": receiver_id,  # Include receiver_id in context
    }
    return render(request, "user_profile.html", context)


from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
import requests
from .models import Customer  # Ensure Customer model is imported

def show_user_account(request):
    context = {}
    
    if request.method == "POST":
        if 'register' in request.POST:
            context['register'] = False
            try:
                username = request.POST.get('username', '').strip()
                password = request.POST.get('password', '').strip()
                email = request.POST.get('email', '').strip()
                address = request.POST.get('address', '').strip()
                phone = request.POST.get('phone', '').strip()

                # Validate input fields
                if not username or not password or not email or not phone:
                    messages.error(request, "All fields are required.")
                    return render(request, 'user_account.html', context)

                # Check if username already exists
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already exists.")
                    return render(request, 'user_account.html', context)

                # Create user account
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email
                )

                # Fetch user's location using ipinfo.io API
                latitude, longitude = None, None
                try:
                    response = requests.get('https://ipinfo.io/json', timeout=5)
                    data = response.json()
                    if 'loc' in data:
                        latitude, longitude = data['loc'].split(',')
                except requests.RequestException:
                    pass

                # Create customer account
                customer = Customer.objects.create(
                    name=username,
                    user=user,
                    phone=phone,
                    address=address,
                    latitude=latitude,
                    longitude=longitude
                )

                messages.success(request, "Registered Successfully")
                # return redirect('Home')

            except IntegrityError:
                messages.error(request, "Username already taken. Try another.")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")

        elif 'login' in request.POST:
            context['register'] = False
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('Home')
            else:
                messages.error(request, 'Invalid user credentials')

    return render(request, 'user_account.html', context)


