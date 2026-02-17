from celery import shared_task
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


@shared_task(name='apps.accounts.tasks.cleanup_expired_tokens')
def cleanup_expired_tokens():
    """
    Clean up expired JWT tokens from blacklist
    Run daily
    """
    from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
    
    # Delete tokens older than 30 days
    cutoff_date = timezone.now() - timezone.timedelta(days=30)
    
    deleted_count = OutstandingToken.objects.filter(
        expires_at__lt=cutoff_date
    ).delete()[0]
    
    logger.info(f'Cleaned up {deleted_count} expired tokens')
    return {'deleted_count': deleted_count}
