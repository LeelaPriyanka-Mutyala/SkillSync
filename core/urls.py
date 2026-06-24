from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('listing/<slug:slug>/', views.listing_detail, name='listing_detail'),
    path('create/', views.create_listing, name='create_listing'),
    path('my-requests/', views.my_requests, name='my_requests'),  
    path('accept-request/<int:request_id>/', views.accept_request, name='accept_request'),  
    path('decline-request/<int:request_id>/', views.decline_request, name='decline_request'),  
    path('profile/<str:username>/', views.profile, name='profile'),
     path('register/', views.register, name='register'), 
     path('favorite/<int:listing_id>/', views.toggle_favorite, name='toggle_favorite'),
]