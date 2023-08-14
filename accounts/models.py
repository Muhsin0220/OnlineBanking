from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    username=models.CharField(max_length=15,unique=True)
    first_name=models.CharField(max_length=30)
    password=models.CharField(max_length=100)
    otp=models.CharField(max_length=6,blank=True)
    is_verified=models.BooleanField(default=False)

        
    def __str__(self):
        return self.username

@receiver(post_save,sender=User)
def create_wallet(sender,instance,created,**kwargs):
    if created:
        Wallet.objects.create(user=instance)

class Wallet(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10, decimal_places=2,default=0.00)


class Transaction(models.Model):
    sender=models.ForeignKey(User,related_name='sent_transactions',on_delete=models.CASCADE)
    receiver=models.ForeignKey(User,related_name='received_transactions',on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    date=models.DateTimeField(auto_now_add=True)