from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Appointment
from .serializers import AppointmentSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from datetime import datetime
class AppointmentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        appointment = Appointment.objects.filter(patient=request.user.id).all()
        if not appointment:
            return Response({ "detail" : "No appointment found" },  status=status.HTTP_404_NOT_FOUND)

        serializer = AppointmentSerializer(appointment , many=True , context={"request" : request})
        return Response(serializer.data,  status=status.HTTP_200_OK)
    
    def post(self, request):
        request.data['patient'] = request.user.id
        try:
            # Convert ISO date string to YYYY-MM-DD
            date_str = request.data.get('date')
            request.data['date'] = datetime.fromisoformat(date_str.replace("Z", "+00:00")).date()

            # Convert ISO time string to HH:MM:SS
            time_str = request.data.get('time')
            request.data['time'] = datetime.fromisoformat(time_str.replace("Z", "+00:00")).time()
        except ValueError as e:
            return Response({"error": "Invalid date or time format."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = AppointmentSerializer(data=request.data)
        
        if serializer.is_valid():
            appointment = serializer.save()  
            return Response({
                "message": "Appointment created successfully",
                "appointment": AppointmentSerializer(appointment).data
            }, status=status.HTTP_201_CREATED)
        print(serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
