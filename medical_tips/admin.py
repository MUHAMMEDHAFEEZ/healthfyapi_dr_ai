from django.contrib import admin
from .models import MedicalTip

@admin.register(MedicalTip)
class MedicalTipAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'content')
