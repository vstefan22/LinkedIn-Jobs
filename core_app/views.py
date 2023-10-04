from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q
import dateutil.parser, csv
from .models import  LinkedInJob, NumberOfJobs, ApiKeys
from .get_data import get_data

# Create your views here.
def index(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        city = request.POST.get('city').lower()
        country = request.POST.get('country').upper()
        title = request.POST.get('title')

        if title and city and country:
            results = LinkedInJob.objects.filter(Q(posted_date = date) | Q(job_title__contains = title) | Q(job_location__contains = city) | Q(country__contains = country))
        if title and not city and not country:
            results = LinkedInJob.objects.filter(Q(posted_date = date) | Q(job_title__contains = title) | Q(job_location = city) | Q(country = country))
        if not title and city and country:
            results = LinkedInJob.objects.filter(Q(posted_date = date) | Q(job_title = title) | Q(job_location__contains = city) | Q(country__contains = country))
        if not title and not city and country:
            results = LinkedInJob.objects.filter(Q(posted_date = date) | Q(country__contains = country))
        if not title and not city and not country:
            results = LinkedInJob.objects.filter(Q(posted_date = date))
        if not title and city and not country:
            results = LinkedInJob.objects.filter(Q(job_location__contains = city))
        if not date and country:
            results = LinkedInJob.objects.filter(Q(country__contains = country))
        context = {'get_jobs': results}
        return render(request, 'core_app/index.html', context)
    get_jobs =  LinkedInJob.objects.all()
    context = {'get_jobs':get_jobs}
    return render(request, 'core_app/index.html', context)


def charts(request):
    get_data = NumberOfJobs.objects.all()
    context = {'number_of_jobs': get_data}
    return render(request, 'core_app/charts.html', context)


def get_data_view(request):
    if request.method == 'POST':
        name = request.POST.get('name').lower()
        location = request.POST.get('location').lower()
        get_data(name, location)
        get_jobs =  LinkedInJob.objects.all()
        context = {'get_jobs':get_jobs}
        return render(request, 'core_app/index.html', context)
    return render(request, 'core_app/get_data.html')

def create_csv(date, job_url, job_title, company_name, company_url, job_location, posted_date, found_date, headquarter, city, postal_code, industries, phone, date_we_got_data):
    with open(f"{date}.csv", "a") as my_empty_csv:
        # print(empt_list)
        writer = csv.writer(my_empty_csv)
        header = ['Job URL', 'Job Title', 'Company Name', 'Company URL', 'Job Location', 'Posted Date', 'Founded Date', 'Headquarter', 'City', 'Postal Code', 'Industries', 'Phone', 'Date We Got Data']
        data = [job_url, job_title, company_name, company_url, job_location, posted_date, found_date, headquarter, city, postal_code, industries, phone, date_we_got_data]
        writer.writerow(header)
        writer.writerow(data)

def save_table(request):
    if request.method == 'POST':
        date_pass = request.POST.get('date')
        date = dateutil.parser.parse(date_pass).strftime("%Y-%m-%d")
        
        if date == 'all':
            jobs =  LinkedInJob.objects.all()
            for job in jobs:
                create_csv(date_pass, job.job_url, job.job_title, job.company_name, job.company_url, job.job_location, job.posted_date, job.found_date, job.headquarter, job.city, job.postal_code, job.industries, job.phone, job.date_we_got_data, job.number_of_employees)
        else:
            jobs =  LinkedInJob.objects.filter(date_we_got_data = date)
            for job in jobs:
                create_csv(date_pass, job.job_url, job.job_title, job.company_name, job.company_url, job.job_location, job.posted_date, job.found_date, job.headquarter, job.city, job.postal_code, job.industries, job.phone, job.date_we_got_data, job.number_of_employees)
        pass
        
    return render(request, 'core_app/save_table.html')


def change_api(request):
    if request.method == 'POST':
        api_key = request.POST.get('api_key')
        api_type = request.POST.get('api_type').lower()
        
        try:
            ApiKeys.objects.filter(api = api_type).delete()
            ApiKeys.objects.create(api = api_type, api_key = api_key)
        except:   
            messages.error(request,"Invalid input! Only select 2 options (company or jobs)")
    return render(request, 'core_app/change_api_key.html')


def change_email(request, company_name):
    name =  LinkedInJob.objects.filter(company_name = company_name)
    
    if request.method == 'POST':
        nameGot = request.POST.get('name')
        email = request.POST.get('email')
        if name != nameGot:
            name =  LinkedInJob.objects.filter(company_name = nameGot)
        name.update(email = email)

    context = {'name':company_name}
    return render(request, 'core_app/change-email.html', context)