from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicalTipViewSet, get_daily_tip

router = DefaultRouter()
router.register(r'tips', MedicalTipViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('daily-tip/', get_daily_tip, name='daily-tip'),
] 