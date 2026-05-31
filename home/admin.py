from django.contrib import admin
from .models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'year', 'price', 'status', 'featured', 'created_at']
    list_filter = ['status', 'featured', 'category', 'brand']
    search_fields = ['brand', 'model', 'year']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = [
        ('Vehicle Info',
         {'fields': ['brand', 'model', 'year', 'category', 'colour', 'fuel', 'transmission', 'mileage']}),
        ('Pricing', {'fields': ['price', 'price_note']}),
        ('Display', {'fields': ['badge', 'featured', 'status']}),
        ('Media', {'fields': ['image_url']}),
        ('WhatsApp', {'fields': ['wa_message']}),
        ('Timestamps', {'fields': ['created_at', 'updated_at']}),
    ]
