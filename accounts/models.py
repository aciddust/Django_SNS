import os
import uuid
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

# BASIC_IMG = os.path.join(os.path.dirname(os.path.dirname(__file__)),'media','misc','basic.png')

def image_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join(instance.UPLOAD_PATH, "%s.%s" % (uuid.uuid4(), ext))
    #16자리 고유한 아이디 생성

class UserManager(BaseUserManager):
    # def create_user(self, email, name, date_of_birth, password=None):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        # with open(BASIC_IMG, mode='rb') as basic_img:
        #     binary_img = basic_img.read()

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            # image=binary_img
            # date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_superuser(self, email, name, date_of_birth, password):
    def create_superuser(self, email, name, password):    
        user = self.create_user(
            email,
            name,
            password=password,
            # date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    UPLOAD_PATH = 'user-upload'

    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=64)
    # date_of_birth = models.DateField()
    image = models.ImageField(upload_to=image_upload_to)
    message = models.TextField(verbose_name='상태메시지')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['name', 'date_of_birth']
    REQUIRED_FIELDS = ['name', ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin