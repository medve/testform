#-*-encoding:utf-8-*-
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import IntegrityError

class PhoneIsAlreadyApproved(IntegrityError):
    pass

class MultiphoneManager(UserManager):
    def get_by_phone(self, phone):
        all_users = self.get_queryset()
        #try to find user with given phone
        #try to find user with given additional phone
        #if nothing found raise DoesNotExist exception
        try:
            user = all_users.get(phone = phone)
        except self.model.DoesNotExist:
            try:
                user = all_users.additionalphones_set().get
                                (
                                  phone=phone, 
                                  approved=True
                            )
        return user

class MultiphoneUser(AbstractUser):
    phone = models.PhoneNumberField(verbose_name='Основной телефон', unique=True)

    objects = MultiphoneManager

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

class AdditionalPhone(models.Model):
    user = models.ForeignKey(MultiphoneUser,verbose_name='Пользователь')
    phone = models.PhoneNumberField(verbose_name='Дополнительный телефон')
    approved = models.BooleanField(default=False,verbose_name='Подтвержден')

    def set_active(self,*args,*kwargs):
        if self.objects.filter(
                 phone = self.phone, 
                 active= True).exists():
            raise PhoneIsAlreadyApproved(
                "This phone is already approved %s"%self.phone)
        self.approved = True
        self.save(*args,*kwargs)

    class Meta:
        verbose_name = "Дополнительный телефон"
        verbose_name_plural = "Дополнительные телефоны"

    def __str__(self):
        return "%s %s"%(user,phone)
    