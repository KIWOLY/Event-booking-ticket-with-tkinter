from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('events/', views.EventList.as_view(), name='event_list'),
    path('events/<int:pk>/', views.EventDetail.as_view(), name='event_detail'),
    path('booking/', views.CreateBooking.as_view(), name='create_booking'),
    path('booking/<int:booking_id>/update/', views.UpdateBooking.as_view(), name='update_booking'),
    path('booking/<int:booking_id>/cancel/', views.CancelBooking.as_view(), name='cancel_booking'),
    path('my-bookings/', views.UserBookings.as_view(), name='user_bookings'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
     path('logout/', views.LogoutView.as_view(), name='logout'),

]
