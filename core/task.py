from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.management import call_command # NEW
from core.celery import app

# from django.contrib.auth.models import User  # Import the User model

logger = get_task_logger(__name__)


@shared_task
def sample_task():
    logger.info("The sample task just ran.")


# NEW
@shared_task
def send_email_report():
    call_command("email_report", )
    
    
    
    
    
    
# @app.task(name="send_notification", bind=True, default_retry_delay=300, max_retries=5)
@shared_task
def send_notification():
    from django.core.mail import send_mail as sm
    from django.contrib.auth.models import User  # Import the User model
    from core.settings import EMAIL_HOST_USER
    # Fetch all users except superuser
    users = User.objects.exclude(is_superuser=True).all()
    user_emails = [user.email for user in users]

    # try sending email
    try:
        res = sm(
            subject="hey",
            html_message="hey aa",
            from_email=EMAIL_HOST_USER,
            recipient_list=user_emails,
            fail_silently=False,
            message=None)
        print(f'Email send to {len(user_emails)} users')
    except Exception:

        # retry when fail
        send_notification.retry()    
    