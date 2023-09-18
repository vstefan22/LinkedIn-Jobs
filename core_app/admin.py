from django.contrib import admin
from .models import LinedInJob, NumberOfJobs, ApiKeys

admin.site.register(LinedInJob)
admin.site.register(NumberOfJobs)
admin.site.register(ApiKeys)

# Register your models here.
