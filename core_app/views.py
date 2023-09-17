from django.shortcuts import render
from .models import LinedInJob, NumberOfJobs
from .get_data import get_data
from datetime import datetime
import pytz

# Create your views here.
def index(request):
    today = datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d')
    
    get_jobs = LinedInJob.objects.all()
    context = {'get_jobs':get_jobs}
    return render(request, 'core_app/index.html', context)

def charts(request):
    get_data = NumberOfJobs.objects.all()
    
    context = {'number_of_jobs': get_data}
    return render(request, 'core_app/charts.html', context)

def get_data_view(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        name = name.lower()
        location = location.lower()
        get_data(name, location)
        get_jobs = LinedInJob.objects.all()
        context = {'get_jobs':get_jobs}
        return render(request, 'core_app/index.html', context)
    return render(request, 'core_app/get_data.html')