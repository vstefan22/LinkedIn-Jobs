from django.shortcuts import render
from .models import LinedInJob, NumberOfJobs, ApiKeys
from .get_data import get_data
from datetime import datetime
from django.contrib import messages
import pytz
import csv
import requests

# Create your views here.
def index(request):
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

def create_csv(date, job_url, job_title, company_name, company_url, job_location, posted_date, found_date, headquarter, city, postal_code, industries, phone, date_we_got_data):
    print('da')
    with open(f"{date}.csv", "a") as my_empty_csv:
        # print(empt_list)
        writer = csv.writer(my_empty_csv)
        header = ['Job URL', 'Job Title', 'Company Name', 'Company URL', 'Job Location', 'Posted Date', 'Founded Date', 'Headquarter', 'City', 'Postal Code', 'Industries', 'Phone', 'Date We Got Data']
        data = [job_url, job_title, company_name, company_url, job_location, posted_date, found_date, headquarter, city, postal_code, industries, phone, date_we_got_data]
        
        writer.writerow(header)
        writer.writerow(data)
def save_table(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        empt_list = []
        if date == 'all':
            jobs = LinedInJob.objects.all()
            for job in jobs:
                create_csv(date, job.job_url, job.job_title, job.company_name, job.company_url, job.job_location, job.posted_date, job.found_date, job.headquarter, job.city, job.postal_code, job.industries, job.phone, job.date_we_got_data)
        else:
            jobs = LinedInJob.objects.filter(date_we_got_data = date)
            for job in jobs:
                empt_list.append([job.job_url, job.job_title, job.company_name, job.company_url, job.job_location, job.posted_date, job.found_date, job.headquarter, job.city, job.postal_code, job.industries, job.phone, job.date_we_got_data])
                create_csv(date, job.job_url, job.job_title, job.company_name, job.company_url, job.job_location, job.posted_date, job.found_date, job.headquarter, job.city, job.postal_code, job.industries, job.phone, job.date_we_got_data)
        pass
        
    return render(request, 'core_app/save_table.html')


def change_api(request):
    if request.method == 'POST':
        api_key = request.POST.get('api_key')
        api_type = request.POST.get('api_type')
        if api_type == 'company':
            ApiKeys.objects.filter(api_type = 'company').update(api_key = api_key)
        elif api_type == 'jobs':
            ApiKeys.objects.filter(api_type = 'jobs').update(api_key = api_key)
        else:   
            messages.error(request,"Invalid input! Only select 2 options (company or jobs)")
    return render(request, 'core_app/change_api_key.html')


def change_email(request, company_name):
    print(company_name)
    name = LinedInJob.objects.filter(company_name = company_name)
    
    if request.method == 'POST':
        nameGot = request.POST.get('name')
        email = request.POST.get('email')
        print(nameGot, email)
        print('\n')
        print(name)
        if name != nameGot:
            name = LinedInJob.objects.filter(company_name = nameGot)
        print(name)
        name.update(email = email)

    context = {'name':company_name}
    return render(request, 'core_app/change-email.html', context)