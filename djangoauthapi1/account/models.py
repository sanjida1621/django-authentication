from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


#Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, name, mobile, password=None, password2=None):
        """
        Creates and saves a User with the given email, name, mobile and password.
        """
        if not email: 
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            mobile=mobile,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, mobile, password=None):
        """
        Creates and saves a superuser with the given email, name, mobile and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            mobile=mobile,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
# Custom User Model.
class User(AbstractBaseUser):
        
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=11)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','mobile']

    def validate_bangladeshi_mobile_number(value):
        if not value.startswith('01') or len(value) != 11:
            raise ValidationError(
                _('Invalid Bangladeshi mobile number. Please enter a valid mobile number starting with "01" and with 11 digits.'),
                code='invalid_bangladeshi_mobile_number'
            )
            
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        #   possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin