from django.contrib import admin

from adminpanel.models import Booking
from adminpanel.models import SurchargeRates

# Register your models here.
admin.site.register(Booking)
@admin.register(SurchargeRates)
class SurchargeRatesAdmin(admin.ModelAdmin):
    list_display = ('pet_friendly_surcharge', 'smoking_surcharge')