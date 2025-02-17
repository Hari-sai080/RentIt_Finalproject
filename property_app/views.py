from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Property, Booking, Payment, Review
from .forms import PropertyForm 

# ---------------------------
# Property Management Views
# ---------------------------

def add_property(request):
    """View to add a new property."""
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PropertyForm()
    return render(request, 'property_app/add_property.html', {'form': form})

def home(request):
    """View to display the homepage with all properties."""
    properties = Property.objects.all()
    return render(request, 'property_app/home.html', {'properties': properties})

def property_detail(request, pk):
    """View to display details of a single property."""
    property_obj = get_object_or_404(Property, pk=pk)
    return render(request, 'property_app/property_detail.html', {'property': property_obj})

def property_list(request):
    """View to list all properties."""
    properties = Property.objects.all()
    return render(request, 'property_app/property_list.html', {'properties': properties})

def edit_property(request, pk):
    """View to edit an existing property."""
    property_obj = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            form.save()
            return redirect('property_detail', pk=pk)
    else:
        form = PropertyForm(instance=property_obj)
    return render(request, 'property_app/edit_property.html', {'form': form, 'property': property_obj})

@login_required
def delete_property(request, pk):
    """View to delete an existing property."""
    property_obj = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, 'Property deleted successfully!')
        return redirect('property_list')
    return render(request, 'property_app/delete_property.html', {'property': property_obj})

# ---------------------------
# Booking and Payment Views
# ---------------------------

@login_required
def booking_view(request, property_id):
    """View to handle booking for a property."""
    property_obj = get_object_or_404(Property, pk=property_id)
    if request.method == 'POST':
        booking = Booking.objects.create(
            user=request.user,
            property=property_obj,
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            total_amount=property_obj.price  # Adjust logic as needed
        )
        messages.success(request, 'Booking created successfully!')
        return redirect('payment', booking_id=booking.id)
    return render(request, 'property_app/booking.html', {'property': property_obj})

@login_required
def payment_view(request, booking_id):
    """View to process a payment for a booking."""
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        payment = Payment.objects.create(
            user=request.user,
            booking=booking,
            amount=booking.total_amount,
            method=payment_method,
            status='completed',  # Simulation; integrate actual gateway as needed
        )
        messages.success(request, 'Payment successful!')
        return redirect('dashboard')
    return render(request, 'property_app/payment.html', {'booking': booking})

@login_required
def dashboard(request):
    """View to display user dashboard with profile info, bookings, etc."""
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'property_app/dashboard.html', {'bookings': bookings})

def camera_upload(request):
    """View to display a page that uses HTML5 getUserMedia for camera capture."""
    return render(request, 'property_app/camera_upload.html')

@login_required
def add_review(request, pk):
    """View to add a review for a property."""
    property_obj = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if rating and comment:
            Review.objects.create(property=property_obj, user=request.user, rating=rating, comment=comment)
            messages.success(request, "Review added successfully!")
            return redirect('property_detail', pk=pk)
        else:
            messages.error(request, "Please provide both a rating and a comment.")
    return render(request, 'property_app/add_review.html', {'property': property_obj})

# ---------------------------
# Profile and Favorites Views
# ---------------------------

@login_required
def profile(request):
    """View to display the user's profile."""
    return render(request, 'property_app/profile.html', {'user': request.user})

@login_required
def save_property(request, pk):
    """View to save a property to the user's favorites."""
    property_obj = get_object_or_404(Property, pk=pk)
    # Assuming the user has a related Profile object with a saved_properties field.
    request.user.profile.saved_properties.add(property_obj)
    messages.success(request, 'Property saved to favorites!')
    return redirect('property_detail', pk=pk)

@login_required
def remove_saved_property(request, pk):
    """View to remove a property from the user's favorites."""
    property_obj = get_object_or_404(Property, pk=pk)
    request.user.profile.saved_properties.remove(property_obj)
    messages.success(request, 'Property removed from favorites!')
    return redirect('property_detail', pk=pk)

@login_required
def mark_notification_as_read(request, pk):
    """Placeholder view to mark a notification as read."""
    return HttpResponse("Mark notification as read - Not Implemented.")

# ---------------------------
# Messaging and Blog Views (Placeholders)
# ---------------------------

@login_required
def send_message(request, pk):
    """Placeholder view for sending a message regarding a property."""
    return HttpResponse("Send message - Not Implemented.")

def blog_list(request):
    """Placeholder view for listing blog posts."""
    return HttpResponse("Blog list - Not Implemented.")

def blog_detail(request, pk):
    """Placeholder view for a blog post's detail."""
    return HttpResponse("Blog detail - Not Implemented.")

@login_required
def add_blog_post(request):
    """Placeholder view for adding a blog post."""
    return HttpResponse("Add blog post - Not Implemented.")

def terms_of_service(request):
    """Placeholder view for Terms of Service."""
    return HttpResponse("Terms of Service - Not Implemented.")

def privacy_policy(request):
    """Placeholder view for Privacy Policy."""
    return HttpResponse("Privacy Policy - Not Implemented.")

def faqs(request):
    """Placeholder view for FAQs."""
    return HttpResponse("FAQs - Not Implemented.")

def checkout(request):
    """Placeholder view for checkout."""
    return HttpResponse("Checkout - Not Implemented.")

def payment_success(request):
    """Placeholder view for payment success."""
    return HttpResponse("Payment Success - Not Implemented.")

def payment_failed(request):
    """Placeholder view for payment failure."""
    return HttpResponse("Payment Failed - Not Implemented.")
