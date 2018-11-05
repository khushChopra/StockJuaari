from django.contrib import admin
from .models import singlestock, profile,feedback
# Register your models here.
admin.site.register(singlestock)
admin.site.register(profile)
admin.site.register(feedback)
