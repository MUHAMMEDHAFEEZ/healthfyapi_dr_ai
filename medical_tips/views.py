from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import MedicalTip
from .serializers import MedicalTipSerializer

# Create your views here.

class MedicalTipViewSet(viewsets.ModelViewSet):
    queryset = MedicalTip.objects.filter(is_active=True)
    serializer_class = MedicalTipSerializer

@api_view(['GET'])
def get_daily_tip(request):
    """
    Get a random medical tip for the day
    """
    today = timezone.now().date()
    tip = MedicalTip.objects.filter(
        is_active=True,
        created_at__date=today
    ).first()

    if not tip:
        # If no tip exists for today, get the most recent one
        tip = MedicalTip.objects.filter(is_active=True).first()

    if tip:
        serializer = MedicalTipSerializer(tip)
        return Response(serializer.data)
    return Response({"message": "No tips available"}, status=404)
