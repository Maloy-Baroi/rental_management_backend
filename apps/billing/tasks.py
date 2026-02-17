from celery import shared_task
from django.utils import timezone
from django.db import transaction
from datetime import datetime, timedelta
import logging

from .models import Bill
from apps.contracts.models import RentalContract
from apps.properties.models import UtilityType

logger = logging.getLogger(__name__)


@shared_task(name='apps.billing.tasks.generate_monthly_bills')
def generate_monthly_bills():
    """
    Generate monthly bills for all active rental contracts
    Run on 1st of every month
    """
    today = timezone.now().date()
    billing_month = today.strftime('%Y-%m')
    
    logger.info(f'Generating bills for {billing_month}')
    
    active_contracts = RentalContract.objects.filter(
        status='active',
        contract_from__lte=today,
        contract_to__gte=today
    )
    
    bills_created = 0
    
    for contract in active_contracts:
        try:
            with transaction.atomic():
                # Get rental terms
                rental_terms = contract.unit.rental_terms
                
                # Calculate due date
                due_day = rental_terms.payment_due_day
                due_date = datetime(today.year, today.month, min(due_day, 28)).date()
                
                # Create rent bill
                rent_bill, created = Bill.objects.get_or_create(
                    contract=contract,
                    billing_month=billing_month,
                    utility_type=None,  # Rent
                    defaults={
                        'amount': contract.rent_amount_at_contract,
                        'due_date': due_date,
                        'status': 'pending'
                    }
                )
                
                if created:
                    bills_created += 1
                    logger.info(f'Created rent bill for contract {contract.id}')
                
                # Create utility bills if not included in rent
                for unit_utility in contract.unit.utilities.filter(is_included_in_rent=False):
                    utility_bill, created = Bill.objects.get_or_create(
                        contract=contract,
                        billing_month=billing_month,
                        utility_type=unit_utility.utility_type,
                        defaults={
                            'amount': 0,  # To be updated by landlord
                            'due_date': due_date,
                            'status': 'pending'
                        }
                    )
                    
                    if created:
                        bills_created += 1
                        logger.info(f'Created {unit_utility.utility_type.name} bill for contract {contract.id}')
        
        except Exception as e:
            logger.error(f'Error generating bills for contract {contract.id}: {str(e)}')
    
    logger.info(f'Generated {bills_created} bills for {billing_month}')
    return {'bills_created': bills_created, 'billing_month': billing_month}


@shared_task(name='apps.billing.tasks.check_overdue_bills')
def check_overdue_bills():
    """
    Check for overdue bills and update their status
    Run daily
    """
    today = timezone.now().date()
    
    logger.info('Checking for overdue bills')
    
    overdue_bills = Bill.objects.filter(
        status='pending',
        due_date__lt=today
    )
    
    count = overdue_bills.update(status='overdue')
    
    logger.info(f'Marked {count} bills as overdue')
    return {'overdue_count': count}


@shared_task(name='apps.billing.tasks.send_bill_reminders')
def send_bill_reminders():
    """
    Send reminders for upcoming bills
    Run daily
    """
    today = timezone.now().date()
    reminder_date = today + timedelta(days=3)  # 3 days before due
    
    upcoming_bills = Bill.objects.filter(
        status='pending',
        due_date=reminder_date
    )
    
    # TODO: Implement email/SMS notification
    logger.info(f'Found {upcoming_bills.count()} bills due in 3 days')
    
    return {'reminder_count': upcoming_bills.count()}
