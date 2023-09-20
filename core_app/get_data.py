import requests
from datetime import datetime
import pytz
from .models import LinedInJob,  NumberOfJobs, ApiKeys
import time


def get_data(name, location):
    LINKED_IN_JOBS_URL = "https://linkedin-jobs-search.p.rapidapi.com/"
    LINKEDIN_COMPANY_INFORMATION_URL = "https://linkedin-profiles-and-company-data.p.rapidapi.com/profile-details"
    company_api = ApiKeys.objects.filter(api = 'company')
    jobs_api = ApiKeys.objects.filter(api = 'jobs')
    payload = {
        "search_terms": f"{name}",
        "location": f"{location}",
        "page": "2"
    }
    headers = {
        "content-type": "application/json",
        'X-RapidAPI-Key': f'{jobs_api}',
        "X-RapidAPI-Host": "linkedin-jobs-search.p.rapidapi.com"
    }

    response = requests.post(LINKED_IN_JOBS_URL, json=payload, headers=headers)

    jobs = response.json()
    count = 0
    context = {}
    for job in jobs:
        count += 1
        

        company_name = job['company_name']
        company_url = job['linkedin_company_url_cleaned']
        
        job_url = job['linkedin_job_url_cleaned']
        job_title = job['job_title']
        job_location = job['job_location']
        posted_date = job['posted_date']
        
        linkedin_company_username = company_url.replace('https://www.linkedin.com/company/', '')
        payload = {
            "profile_id": linkedin_company_username,
            "profile_type": "company",
            "contact_info": True,
            "recommendations": False,
            "related_profiles": False
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": f"{company_api}",
            "X-RapidAPI-Host": "linkedin-profiles-and-company-data.p.rapidapi.com"
        }

        response = requests.post(LINKEDIN_COMPANY_INFORMATION_URL, json=payload, headers=headers)
        if response:
            company_data = response.json()
            if company_data:
                print(company_data)
                try:
                    if company_data['details']:
                    
                        company_industries = company_data['details']['industries']
                        if company_industries == "Staffing and Recruiting":
                            pass
                        else:
                            company_headquarter = company_data['details']['locations']['headquarter']['line1']
                            headquarter_country = company_data['details']['locations']['headquarter']['country']
                            headquarter_city = company_data['details']['locations']['headquarter']['city']
                            headquarter_postal_code = company_data['details']['locations']['headquarter']['postal_code']
                            number_of_employees = company_data['details']['staff']['total']
                            
                            try:
                                founded_date = company_data['details']['founded']['year']
                            except:
                                founded_date = "Not Given"

                            phone = company_data['details']['phone']
                            context[f'Job URL {count}'] = job_url
                            context[f'Company Name {count}'] = company_name
                            context[f'Company URL {count}'] = company_url
                            context[f'Job Title {count}'] = job_title,
                            context[f'Job Location {count}'] = job_location,
                            context[f'Posted Date {count}'] = posted_date
                            context[f'Headquarter {count}'] = company_headquarter
                            context[f'Country {count}'] = headquarter_country
                            context[f'City {count}'] = headquarter_city
                            context[f'Postal Code {count}'] = headquarter_postal_code
                            context[f'Industries {count}'] = company_industries
                            context[f'Founded Date {count}'] = founded_date
                            context[f'Phone {count}'] = phone
                            context[f'Number of employees'] = number_of_employees
                            today = datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d')
                            LinedInJob.objects.create(job_url = job_url, company_name = company_name, company_url = company_url, job_title = job_title,
                                                    job_location = job_location, posted_date = posted_date,
                                                        headquarter = company_headquarter, city = headquarter_city, 
                                                        country = headquarter_country, postal_code = headquarter_postal_code,
                                                        phone = phone, found_date = founded_date, industries = company_industries, date_we_got_data = today, number_of_employees = number_of_employees)
                            check = NumberOfJobs.objects.filter(date = today)
                            if check:
                                number_of_jobs = check[0].number + 1
                                check.update(number = number_of_jobs)
                            else:
                                NumberOfJobs.objects.create(date = today, number = 1)
                            
                except KeyError:
                    time.sleep(1)
                    try:

                        pass
                    except:
                        if company_data['details']:
                    
                            company_industries = company_data['details']['industries']
                            if company_industries == "Staffing and Recruiting":
                                pass
                            else:
                                company_headquarter = company_data['details']['locations']['headquarter']['line1']
                                headquarter_country = company_data['details']['locations']['headquarter']['country']
                                headquarter_city = company_data['details']['locations']['headquarter']['city']
                                headquarter_postal_code = company_data['details']['locations']['headquarter']['postal_code']
                                
                                try:
                                    founded_date = company_data['details']['founded']['year']
                                except:
                                    founded_date = "Not Given"

                                phone = company_data['details']['phone']
                                context[f'Job URL {count}'] = job_url
                                context[f'Company Name {count}'] = company_name
                                context[f'Company URL {count}'] = company_url
                                context[f'Job Title {count}'] = job_title,
                                context[f'Job Location {count}'] = job_location,
                                context[f'Posted Date {count}'] = posted_date
                                context[f'Headquarter {count}'] = company_headquarter
                                context[f'Country {count}'] = headquarter_country
                                context[f'City {count}'] = headquarter_city
                                context[f'Postal Code {count}'] = headquarter_postal_code
                                context[f'Industries {count}'] = company_industries
                                context[f'Founded Date {count}'] = founded_date
                                context[f'Phone {count}'] = phone
                                today = datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d')
                                LinedInJob.objects.create(job_url = job_url, company_name = company_name, company_url = company_url, job_title = job_title,
                                                        job_location = job_location, posted_date = posted_date,
                                                            headquarter = company_headquarter, city = headquarter_city, 
                                                            country = headquarter_country, postal_code = headquarter_postal_code,
                                                            phone = phone, found_date = founded_date, industries = company_industries, date_we_got_data = today, number_of_employees = number_of_employees)
                                check = NumberOfJobs.objects.filter(date = today)
                                if check:
                                    number_of_jobs = check[0].number + 1
                                    check.update(number = number_of_jobs)
                                else:
                                    NumberOfJobs.objects.create(date = today, number = 1)


                            


    print('\n')
    print('\n')
    print(count)
    print('\n')
    print(context)
    print('\n')
