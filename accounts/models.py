from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Elektron pochtani kiritishingiz shart!')

        if not username:
            raise ValueError('Username kiritilishi shart!')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password
        )
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)

    address = models.CharField(max_length=200, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    profile_image = models.ImageField(upload_to='users/profile/images/', blank=True, null=True)
    # required

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.username



    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    def profile_image_tur(self):
        if Account.profile_image == None:
            return False
        else:
            return True


class Message(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

