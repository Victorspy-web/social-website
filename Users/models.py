from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("User must have a password")
        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.set_password(password) #change user password
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.save(using=self._db)
        return user_obj
    
    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True
        )
        return user
        
    def create_superuser(self,email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email           = models.EmailField(unique=True, max_length=255)
    # full_name       = models.CharField(max_length=255, blank=True, null=True)
    active          = models.BooleanField(default=True) # can login
    staff           = models.BooleanField(default=False) # staff user nit superuser
    admin           = models.BooleanField(default=False) #superuser
    last_login      = models.DateTimeField(auto_now=True)
    date_created    = models.DateTimeField(auto_now_add=True)
    # confirm       = models.BooleanField(default=False)
    # confirmed_data       = models.DateTimeField(auto_now_add)
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = [] # this field will come up when you run createsuperuser command
    
    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email
    
    def get_short_name(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_active(self):
        return self.active