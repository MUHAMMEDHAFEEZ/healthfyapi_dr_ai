from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import MedicalTip
from .serializers import MedicalTipSerializer
import random

# Create your views here.

class MedicalTipViewSet(viewsets.ModelViewSet):
    queryset = MedicalTip.objects.filter(is_active=True)
    serializer_class = MedicalTipSerializer

@api_view(['GET'])
def get_daily_tip(request):
    """
    Get a medical tip that changes every 5 minutes.
    If force_new=true is passed as a query parameter, it will return a different tip.
    """
    now = timezone.now()
    five_minutes_ago = now - timedelta(minutes=5)
    force_new = request.query_params.get('force_new', '').lower() == 'true'

    # Get the most recently served tip that's still active
    current_tip = MedicalTip.objects.filter(
        is_active=True,
        last_served__isnull=False
    ).order_by('-last_served').first()

    if current_tip and current_tip.last_served and current_tip.last_served > five_minutes_ago and not force_new:
        # If we have a tip that was served less than 5 minutes ago and no force_new, return it
        serializer = MedicalTipSerializer(current_tip)
        return Response(serializer.data)

    # Get a new random tip, excluding the current one if it exists
    exclude_ids = [current_tip.id] if current_tip else []
    
    # Get all eligible tips
    eligible_tips = MedicalTip.objects.filter(
        is_active=True
    ).exclude(id__in=exclude_ids)

    if not eligible_tips.exists():
        return Response({"message": "No tips available"}, status=404)

    # Get a random tip
    count = eligible_tips.count()
    random_index = random.randint(0, count - 1)
    new_tip = eligible_tips[random_index]

    # Update the last_served time
    new_tip.last_served = now
    new_tip.save()

    serializer = MedicalTipSerializer(new_tip)
    return Response(serializer.data)
