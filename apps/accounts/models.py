from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    """Custom user manager"""
    
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('Users must have a phone number')
        
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model using phone as primary identifier"""
    
    phone = PhoneNumberField(
        unique=True,
        db_index=True,
        help_text='User phone number (primary identifier)'
    )
    email = models.EmailField(
        unique=True,
        null=True,
        blank=True,
        db_index=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['phone', 'is_active']),
            models.Index(fields=['email', 'is_active']),
        ]
    
    def __str__(self):
        return str(self.phone)
    
    def soft_delete(self):
        """Soft delete user"""
        self.is_active = False
        self.is_deleted = True
        self.save()


class Household(models.Model):
    """Household/Tenant information"""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='households',
        help_text='User who created this household'
    )
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    nid = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$|^\d{13}$|^\d{17}$',
                message='NID must be 10, 13, or 17 digits'
            )
        ],
        help_text='National ID number'
    )
    contact_phone = PhoneNumberField(help_text='Contact phone number')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'households'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['nid']),
        ]
    
    def __str__(self):
        return f'{self.name} ({self.contact_phone})'
