from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import permissions, status,  generics
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
# from .models import
from .serializers import *
from . models import Doctor, Specialization

User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = UserSerializer(user, context={"request": None}).data
        token["user"] = user_data
        return token

@api_view(["GET"])
def index(request):
    return Response({"Project": "Medical Appointment API"})

def get_auth_for_user(user, request):
    token = RefreshToken.for_user(user)
    user_data = UserSerializer(user, context={"request": request}).data
    token["user"] = user_data
    return {
        "access": str(token.access_token),
        "refresh": str(token)
    }

class LogInView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"detail": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, email=email, password=password) 
        if not user:
            return Response({"detail": "Incorrect email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        user_data = get_auth_for_user(user, request)
        return Response(user_data, status=status.HTTP_200_OK)

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save() 
            if user:
                tokens = get_auth_for_user(user, request)
                return Response(tokens, status=status.HTTP_201_CREATED)
        return Response({"detail": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

class SpecializationView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        specialization = Specialization.objects.all()
        serializer = SpecializationSerializer(specialization, many=True ,context={"request" : request})
        return Response(serializer.data)

class DoctorsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, doctor_id=None):
        if doctor_id is not None:
            doctor = get_object_or_404(Doctor, id=doctor_id)
            serializer = DoctorSerializer(doctor ,context={"request" : request})
            return Response(serializer.data)
        
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True ,context={"request" : request})
        return Response(serializer.data)

class DoctorSearchView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter ]
    search_fields = ["user__first_name", "user__last_name","name" ,"specialization__specialization"]