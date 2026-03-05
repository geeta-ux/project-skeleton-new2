from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None

    name = models.CharField(max_length=150, blank=True)
    
    # New Fields
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Transgender', 'Transgender'),
    )
    AGE_GROUP_CHOICES = (
        ('15-24', '15-24'),
        ('25-34', '25-34'),
        ('35-45', '35-45'),
    )
    EDUCATION_CHOICES = (
        ('Student', 'Student'),
        ('Graduate', 'Graduate'),
        ('Post Graduate', 'Post Graduate'),
    )
    EXPERIENCE_LEVEL_CHOICES = (
        ('Fresher', 'Fresher'),
        ('Experienced', 'Experienced'),
    )

    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, null=True)
    age_group = models.CharField(max_length=20, choices=AGE_GROUP_CHOICES, blank=True, null=True)
    education = models.CharField(max_length=50, choices=EDUCATION_CHOICES, blank=True, null=True)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES, blank=True, null=True)

    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    has_psychometric_access = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()   # <<< IMPORTANT

    class Meta:
        db_table = 'users'
