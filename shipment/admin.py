from django.contrib import admin
from shipment.models import Letter

# Register your models here.


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    exclude = ['status']
