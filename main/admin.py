from django.contrib import admin

from .models import Car, Document


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('car_model', 'car_number', 'rent_cost_per_day',)


@admin.register(Document)
class RentalDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_full_name', 'company', 
                    'renting_date_from', 'renting_date_to', 'timestamp', 'status')