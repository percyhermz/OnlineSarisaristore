from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



class AccountManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, mobile, password=None):
        if not email:
            raise ValueError('Users must have an email')
        if not username:
            raise ValueError('Users must have an username')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last_name')
        if not mobile:
            raise ValueError('Users must have a mobile')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, first_name, last_name, mobile, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user




class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", unique=True, max_length=30)
    mobile = models.CharField(max_length=11, verbose_name="Mobile Number")
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, verbose_name="First Name")
    last_name = models.CharField(max_length=30, verbose_name="Last Name")
    

    date_joined = models.DateTimeField(verbose_name="Date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Last login", auto_now_add=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'mobile']

    objects = AccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perms, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

