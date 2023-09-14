from django.contrib import admin
from travel_app import models

# Register your models here.

admin.site.register(models.regionModel)
admin.site.register(models.planModel)
admin.site.register(models.userModel)
admin.site.register(models.bookingModel)
admin.site.register(models.reviewModel)