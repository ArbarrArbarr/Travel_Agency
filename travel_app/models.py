from django.db import models
from django.contrib.auth.models import User

class regionModel(models.Model):
    name= models.CharField(max_length=100)
    image= models.ImageField(upload_to="regions",default=None, blank=False)
    
    def __str__(self):
        return self.name
    
class planModel(models.Model):
    title= models.CharField(max_length=100)
    image= models.ImageField(upload_to="plans", default=None, blank=False)
    region= models.ForeignKey(regionModel, on_delete=models.CASCADE, default=None)
    detail= models.TextField()
    price_for_adult_per_day= models.IntegerField(default= 15000)
    price_for_child_per_day= models.IntegerField(default= 10000)
    
    def __str__(self):
        return self.title
    
class userModel(models.Model):
    username= models.CharField(max_length=100)
    email= models.EmailField()
    password= models.CharField(max_length=20)
    phone= models.CharField(max_length=20)
    image= models.ImageField(upload_to="users", default=None, blank=True)
    
    def __str__(self):
        return self.username
    
class bookingModel(models.Model):
    booking_code= models.CharField(max_length=20)
    booking_name= models.CharField(max_length=225)
    booking_email= models.EmailField()
    booking_phone= models.CharField(max_length=20)
    booking_date= models.DateField(default=None)
    duration= models.CharField(max_length=150, null=True)
    booking_plan= models.CharField(max_length=100)
    total_cost= models.BigIntegerField(default=None)
    booking_status= models.BooleanField(default=False)
    plan= models.ForeignKey(planModel, on_delete=models.CASCADE)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    created_time= models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.booking_code
    
class reviewModel(models.Model):
    user= models.ForeignKey(userModel, on_delete=models.CASCADE)
    plan= models.ForeignKey(planModel, on_delete=models.CASCADE)
    review= models.TextField()
    created_time= models.DateTimeField(auto_now_add=True)