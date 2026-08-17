from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import NotificationJob
from celery import current_app
from django.utils import timezone
import datetime


#Celery Beat Job
@shared_task
def check_and_dispatch_scheduled_notifications():
    #now = timezone.make_aware(datetime.datetime.now(), datetime.timezone.utc) if timezone.is_naive(datetime.datetime.now()) else timezone.now()
    now = timezone.now()

    #time buffer to make up for processing time
    execution_window = now + datetime.timedelta(seconds=5)

    #check job ID within timeframe with 'status':'PENDING' 
    due_jobs = NotificationJob.objects.filter(status='PENDING', 
                                            scheduled_time__lte=execution_window)
    
    job_count = due_jobs.count()

    if job_count == 0:
        return f"Checked at {now.strftime('%H:%M:%S')}UTC: Zero jobs are due right now"

    for job in due_jobs:
        send_scheduled_email_task(job.id)
    return f"Successfully processed and updated {job_count} notification jobs" 


#Celery Worker's Job
@shared_task
def send_scheduled_email_task(job_id):
    try :
        #pick specific notification from database
        job = NotificationJob.objects.get(id=job_id)

        #process task
        send_mail(
            subject =job.title,
            message=job.message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[job.recipient_email],
            fail_silently=False,
            )
        #save to postgresql
        job.status = 'SUCCESS'
        job.save()
        return f"Successfully sent email for job #{job_id}"

    except NotificationJob.DoesNotExist:
        return f"Job #{job_id} not found."

    except Exception as e:
        if 'job' in locals():
            job.status = 'FAILED'
            job.save()

        raise e


