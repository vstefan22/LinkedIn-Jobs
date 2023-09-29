from django.contrib import admin
from .models import LinkedInJob, NumberOfJobs, ApiKeys

admin.site.register( LinkedInJob)
admin.site.register(NumberOfJobs)
admin.site.register(ApiKeys)

# Register your models here.
