from django.db import models

class LinedInJob(models.Model):
    job_url = models.CharField(max_length=200,null = True)
    job_title = models.CharField(max_length=200, null = True)
    company_name = models.CharField(max_length=200, null = True)
    company_url = models.CharField(max_length=200, null = True)
    job_location = models.CharField(max_length=200, null = True)
    posted_date = models.CharField(max_length=200, null = True)
    headquarter = models.CharField(max_length=200, null = True)
    country = models.CharField(max_length=200, null = True)
    city = models.CharField(max_length=200, null = True)
    postal_code = models.CharField(max_length=200, null = True)
    industries = models.CharField(max_length=200, null = True)
    found_date = models.CharField(max_length=200, null = True)
    phone = models.CharField(max_length=200, null = True)
    date_we_got_data = models.DateField(blank=True, null = True)

    def __str__(self):
        return f'{self.job_title} {self.date_we_got_data}'
    
class NumberOfJobs(models.Model):
    number = models.IntegerField()
    date = models.DateField()
    def __str__(self):
        return f'Number of jobs: {self.number} | Date: {self.date}'
    
