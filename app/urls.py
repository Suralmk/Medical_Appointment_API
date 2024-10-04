from django.urls import path, include
from .views import *

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
urlpatterns = [
    path('', index, name="index"),
    path('doctors/', DoctorsView.as_view(), name="doctors"),
    path('doctors/<int:doctor_id>/', DoctorsView.as_view(), name="single-doctor"),
    path('doctors/search/', DoctorSearchView.as_view(), name="single-doctor"),
    path('specializations/', SpecializationView.as_view(), name="specializations"),

    #auth
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('login/', LogInView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('reset-password/', index, name="reset-password"),
    path('verify-otp/', index, name="verify-otp"),
    path('create-password/', index, name="create-password"),

    #appointment
    path('appointments/', include("appointment.urls"), name="appointment"),
    path('healthtips/', include("healthtips.urls"), name="healthtips"),
    path('pharmacy/', include("pharmacy.urls"), name="pharmacy"),

]