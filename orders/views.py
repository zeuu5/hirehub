from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import make_aware, now
from datetime import datetime
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderedItem, Services

def service_delivered(request, booking_id):
    booking = get_object_or_404(Order, id=booking_id, provider=request.user)
    if request.method == "POST" and booking.status == Order.CONFIRMED:
        booking.status = Order.SERVICE_DELIVERED
        booking.save()
        messages.success(request, "Service marked as delivered.")
    return redirect("provider_dashboard")

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Order, id=booking_id)
    if request.user not in [booking.customer, booking.provider]:
        messages.error(request, "Unauthorized action.")
        return redirect("provider_dashboard")

    if booking.status not in [Order.CONFIRMED, Order.PROCESSING]:
        messages.error(request, "Only confirmed or processing bookings can be cancelled.")
        return redirect("provider_dashboard")

    if booking.payment_status and booking.razorpay_payment_id:
        try:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            client.payment.refund(booking.razorpay_payment_id)
            messages.success(request, "Booking cancelled and amount refunded.")
        except Exception as e:
            messages.error(request, f"Refund failed: {str(e)}")

    booking.status = Order.REJECTED
    booking.payment_status = False
    booking.save()
    messages.success(request, "Booking cancelled.")
    return redirect("provider_dashboard")

@login_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Order, id=booking_id, provider=request.user)
    if booking.payment_status and booking.razorpay_payment_id:
        try:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            client.payment.refund(booking.razorpay_payment_id)
            messages.success(request, "Booking rejected and amount refunded.")
        except Exception as e:
            messages.error(request, f"Refund failed: {str(e)}")
    booking.status = Order.REJECTED
    booking.payment_status = False
    booking.save()
    messages.success(request, "Booking rejected.")
    return redirect("provider_dashboard")

@login_required
def accept_booking(request, booking_id):
    booking = get_object_or_404(Order, id=booking_id, provider=request.user)
    booking.status = Order.CONFIRMED
    booking.save()
    messages.success(request, "Booking accepted.")
    return redirect("provider_dashboard")

@login_required
def provider_dashboard(request):
    bookings = Order.objects.filter(provider=request.user)
    return render(request, "provider_dashbord.html", {"bookings": bookings})


@login_required
def show_cart(request):
    cart_order = Order.objects.filter(customer=request.user, status=Order.CART_STAGE).first()
    cart_items = OrderedItem.objects.filter(order=cart_order) if cart_order else []
    return render(request, "cart.html", {"cart_items": cart_items})

@login_required
def remove_item(request, item_id):
    item = get_object_or_404(OrderedItem, id=item_id, order__customer=request.user)
    item.delete()
    return redirect("show_cart")

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from orders.models import Order, OrderedItem
from services.models import Services

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get("razorpay_payment_id")
            razorpay_order_id = request.POST.get("razorpay_order_id")
            signature = request.POST.get("razorpay_signature")

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            client.utility.verify_payment_signature({
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature
            })

            booking = Order.objects.filter(razorpay_payment_id=razorpay_order_id).first()
            if not booking:
                messages.error(request, "Order not found for this payment!")
                return redirect("show_cart")

            booking.payment_status = True
            booking.status = Order.PROCESSING
            booking.save()
            messages.success(request, "Payment successful! Your booking is processing.")
            return redirect("show_cart")
        except razorpay.errors.SignatureVerificationError:
            messages.error(request, "Payment verification failed!")
        except Exception as e:
            messages.error(request, f"Error processing payment: {str(e)}")
    return redirect("show_cart")

@login_required
def checkout_cart(request):
    customer = request.user
    cart_order = Order.objects.filter(customer=customer, status=Order.CART_STAGE).first()
    if not cart_order or not cart_order.added_items.exists():
        messages.error(request, "Your cart is empty or has no items.")
        return redirect("show_cart")

    total_amount = sum(item.service.price for item in cart_order.added_items.all())
    cart_order.paid_amount = total_amount
    cart_order.save()

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment = client.order.create({
        "amount": int(total_amount * 100),
        "currency": "INR",
        "payment_capture": "1"
    })

    cart_order.razorpay_payment_id = payment["id"]
    cart_order.save()
    return render(request, "payment_page.html", {
        "booking": cart_order,
        "razorpay_order_id": payment["id"],
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "total": total_amount
    })





from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderedItem, Services

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderedItem, Services

@login_required
def add_to_cart(request, service_id):
    service = get_object_or_404(Services, id=service_id)
    customer = request.user
    provider = service.customer  

    if provider == customer:
        return redirect("detail_service", service_id=service_id)

    selected_datetime = request.POST.get("selected_datetime")
    if not selected_datetime:
        return redirect("detail_service", service_id=service_id)

    # Find an existing CART_STAGE order for the customer
    cart_order = Order.objects.filter(customer=customer, status=Order.CART_STAGE).first()

    # If no active cart exists, create a new one
    if not cart_order:
        cart_order = Order.objects.create(
            customer=customer,
            provider=provider,
            status=Order.CART_STAGE,
            paid_amount=0
        )

    # Check if service already exists in the cart; if not, add it
    OrderedItem.objects.get_or_create(
        order=cart_order,
        service=service,
        defaults={"service_time": selected_datetime}
    )

    return redirect("show_cart")
