from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import BooleanField, ExpressionWrapper, Q
from django.db.models.functions import Now


class CustomUser(AbstractUser):
    user_type_data = (
    (1, "AdminHOD"), (2, "Pharmacist"), (3, "Doctor"), (4, "PharmacyClerk"),
    (5, "Patients"))
    user_type = models.CharField(default=1, choices=user_type_data,
                                 max_length=10)


class AdminHOD(models.Model):
    gender_category = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    admin = models.OneToOneField(CustomUser, null=True,
                                 on_delete=models.CASCADE)
    emp_no = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True,
                              choices=gender_category)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    profile_pic = models.ImageField(default="admin.png", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_employed = models.DateTimeField(auto_now_add=True, auto_now=False)
    objects = models.Manager()

    def __str__(self):
        return str(self.admin)


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, null=True)

    def __str__(self):
        return str(self.name)


class ExpiredManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().annotate(
            expired=ExpressionWrapper(Q(valid_to__lt=Now()),
                                      output_field=BooleanField())
        )


class Stock(models.Model):
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE,
                                 blank=True)
    drug_imprint = models.CharField(max_length=6, blank=True, null=True)
    drug_name = models.CharField(max_length=50, blank=True, null=True)
    drug_color = models.CharField(max_length=50, blank=True, null=True)
    drug_shape = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_quantity = models.IntegerField(default='0', blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    manufacture = models.CharField(max_length=50, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    drug_strength = models.CharField(max_length=10, blank=True, null=True)
    valid_from = models.DateTimeField(blank=True, null=True,
                                      default=timezone.now)
    valid_to = models.DateTimeField(blank=False, null=True)
    drug_description = models.TextField(blank=True, max_length=1000, null=True)
    drug_pic = models.ImageField(default="images2.png", null=True, blank=True)
    objects = ExpiredManager()

    def __str__(self):
        return str(self.drug_name)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
