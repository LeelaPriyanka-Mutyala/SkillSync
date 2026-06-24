from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import SkillListing, SwapRequest,Favorite
from .forms import ListingForm, RequestForm, RegistrationForm
def home(request):
    # Get category from URL (e.g., ?category=Tech)
    category = request.GET.get('category')
    
    if category:
        # Filter listings by selected category
        listings = SkillListing.objects.filter(category=category).order_by('-created_at')
    else:
        # Show all listings if no category is selected
        listings = SkillListing.objects.all().order_by('-created_at')
        
    return render(request, 'core/home.html', {'listings': listings})
def listing_detail(request, slug):
    listing = get_object_or_404(SkillListing, slug=slug)
    
    # Prevent users from sending requests to themselves
    can_request = request.user.is_authenticated and request.user != listing.owner
    
    if request.method == 'POST' and can_request:
        form = RequestForm(request.POST)
        if form.is_valid():
            swap_req = form.save(commit=False)
            swap_req.sender = request.user
            swap_req.receiver = listing.owner
            swap_req.listing = listing
            swap_req.save()
            messages.success(request, 'Your swap request has been sent successfully!')
            return redirect('listing_detail', slug=slug)
    else:
        form = RequestForm()

    return render(request, 'core/detail.html', {'listing': listing, 'form': form, 'can_request': can_request})

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            messages.success(request, 'Your skill has been posted!')
            return redirect('home')
    else:
        form = ListingForm()
    return render(request, 'core/create.html', {'form': form})

@login_required
def my_requests(request):
    # Requests received by current user
    received_requests = SwapRequest.objects.filter(receiver=request.user).order_by('-timestamp')
    
    # Requests sent by current user
    sent_requests = SwapRequest.objects.filter(sender=request.user).order_by('-timestamp')
    
    return render(request, 'core/my_requests.html', {
        'received_requests': received_requests,
        'sent_requests': sent_requests
    })

@login_required
def accept_request(request, request_id):
    swap_req = get_object_or_404(SwapRequest, id=request_id, receiver=request.user)
    swap_req.status = 'Accepted'
    swap_req.save()
    messages.success(request, f'You accepted the request from {swap_req.sender.username}!')
    return redirect('my_requests')

@login_required
def decline_request(request, request_id):
    swap_req = get_object_or_404(SwapRequest, id=request_id, receiver=request.user)
    swap_req.status = 'Declined'
    swap_req.save()
    messages.success(request, 'Request declined.')
    return redirect('my_requests')

def profile(request, username):
    user = get_object_or_404(User, username=username)
    listings = SkillListing.objects.filter(owner=user).order_by('-created_at')
    return render(request, 'core/profile.html', {'profile_user': user, 'listings': listings})

# ✅ NEW: Registration View
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after registration
            messages.success(request, f'Welcome {user.username}! Your account has been created successfully.')
            return redirect('home')
    else:
        form = RegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def toggle_favorite(request, listing_id):
    listing = get_object_or_404(SkillListing, id=listing_id)
    
    # Check if already favorited
    fav, created = Favorite.objects.get_or_create(user=request.user, listing=listing)
    
    if not created:
        # If it already exists, delete it (Toggle off)
        fav.delete()
        messages.info(request, 'Removed from your wishlist.')
    else:
        # If it didn't exist, it was just created (Toggle on)
        messages.success(request, 'Added to your wishlist! ❤️')
        
    return redirect('listing_detail', slug=listing.slug)