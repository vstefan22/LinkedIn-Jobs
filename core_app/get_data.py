import requests
from datetime import datetime
import pytz
from .models import  LinkedInJob,  NumberOfJobs, ApiKeys
import time


def get_data(name, location):
    LINKED_IN_JOBS_URL = "https://linkedin-jobs-search.p.rapidapi.com/"
    LINKEDIN_COMPANY_INFORMATION_URL = "https://linkedin-profiles-and-company-data.p.rapidapi.com/profile-details"
    company_api = ApiKeys.objects.filter(api = 'company')[0].api_key
    jobs_api = ApiKeys.objects.filter(api = 'jobs')[0].api_key
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
    print('RESPONSE', response)
    jobs = response.json()
    count = 0   
    context = {}
    # print('JOBS', jobs)
    for job in jobs:
        count += 1
        print(count)

        company_name = job['company_name']
        company_url = job['linkedin_company_url_cleaned']
        
        job_url = job['linkedin_job_url_cleaned']
        job_title = job['job_title']
        job_location = job['job_location']
        posted_date = job['posted_date']
        
        linkedin_company_username = company_url.replace('https://www.linkedin.com/company/', '')
        querystring = {"linkedin_url":f"https://www.linkedin.com/company/{linkedin_company_username}/"}

        url = "https://fresh-linkedin-profile-data.p.rapidapi.com/get-company-by-linkedinurl"

        

        headers = {
            "X-RapidAPI-Key": f"{company_api}",
            "X-RapidAPI-Host": "fresh-linkedin-profile-data.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        
        
        print("RESPONSE 2", response)
        if response:
            company_data = response.json()
            if company_data:
                    print(company_data)
                    if company_data['data']:
                        access_company_data = company_data['data']
                        print("\n -- GOT ALL COMPANY DATA -- \n")
                    
                        company_industries = access_company_data['industries'][0]
                        if company_industries == "Staffing and Recruiting":
                            print("\nStaffing and Recruiting\n")
                            pass
                        else:
                            company_headquarter = access_company_data['hq_full_address']
                            email = access_company_data['email']
                            headquarter_country = access_company_data['hq_country']
                            headquarter_city = access_company_data['hq_city']
                            headquarter_postal_code = access_company_data['hq_postalcode']
                            number_of_employees = access_company_data['employee_count']
                            website = access_company_data['website']
                            try:
                                founded_date = access_company_data['year_founded']
                            except:
                                founded_date = "Not Given"

                            phone = access_company_data['phone']
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
                            print(job_location, job_title, posted_date, company_headquarter)
                            LinkedInJob.objects.create(job_url = job_url, website = website, email = email, company_name = company_name, company_url = company_url, job_title = job_title,
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
                            
                # except KeyError:
                #     print("\n-- ERROR -- SLEEP --\n")
                #     time.sleep(5)
                #     try:
                #         if company_data['details']:
                    
                #             company_industries = company_data['details']['industries']
                #             if company_industries == "Staffing and Recruiting":
                #                 pass
                #             else:
                #                 company_headquarter = company_data['details']['locations']['headquarter']['line1']
                #                 headquarter_country = company_data['details']['locations']['headquarter']['country']
                #                 headquarter_city = company_data['details']['locations']['headquarter']['city']
                #                 headquarter_postal_code = company_data['details']['locations']['headquarter']['postal_code']
                                
                #                 try:
                #                     founded_date = company_data['details']['founded']['year']
                #                 except:
                #                     founded_date = "Not Given"

                #                 phone = company_data['details']['phone']
                #                 context[f'Job URL {count}'] = job_url
                #                 context[f'Company Name {count}'] = company_name
                #                 context[f'Company URL {count}'] = company_url
                #                 context[f'Job Title {count}'] = job_title,
                #                 context[f'Job Location {count}'] = job_location,
                #                 context[f'Posted Date {count}'] = posted_date
                #                 context[f'Headquarter {count}'] = company_headquarter
                #                 context[f'Country {count}'] = headquarter_country
                #                 context[f'City {count}'] = headquarter_city
                #                 context[f'Postal Code {count}'] = headquarter_postal_code
                #                 context[f'Industries {count}'] = company_industries
                #                 context[f'Founded Date {count}'] = founded_date
                #                 context[f'Phone {count}'] = phone
                #                 today = datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d')
                #                 LinkedInJob.objects.create(job_url = job_url, company_name = company_name, company_url = company_url, job_title = job_title,
                #                                         job_location = job_location, posted_date = posted_date,
                #                                             headquarter = company_headquarter, city = headquarter_city, 
                #                                             country = headquarter_country, postal_code = headquarter_postal_code,
                #                                             phone = phone, found_date = founded_date, industries = company_industries, date_we_got_data = today, number_of_employees = number_of_employees)
                #                 check = NumberOfJobs.objects.filter(date = today)
                #                 if check:
                #                     number_of_jobs = check[0].number + 1
                #                     check.update(number = number_of_jobs)
                #                 else:
                #                     NumberOfJobs.objects.create(date = today, number = 1)

                        
                #     except:
                #         print("\n -- NO DATA -- \n")
                        

                            


    print('\n')
    print('\n')
    print(count)
    print('\n')
    print(context)
    print('\n')
