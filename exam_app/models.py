from typing import BinaryIO
from django.db import models
from datetime import datetime
import re

from django.db.models.deletion import CASCADE # the regex model

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        
        # add keys and values to errors dictionary for each invalid field
        FIRST_NAME_REGEX = re.compile(r'^[a-zA-Z ]+$') # fist name check, should be letters
        if not  FIRST_NAME_REGEX.match(postData['f_name']):             
            errors['first_name_format'] = "Invalid name format"
        if len(postData['f_name']) < 2:
            errors['f_name'] = "First name should be at least 2 characters"
        if len(postData['l_name']) < 3:
            errors['l_name'] = "Last name should be at least 3 characters"
        if len(postData['email']) < 6:
            errors['email'] = "Email should be at least 6 characters" 
        if len(postData['pw']) < 8:
            errors['password'] = "Password should be at least 9 characters"
        if postData['pw'] != postData['pw_conf']:
            errors['match'] = "User or password do not match"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['regex'] = "Invalid email format!"

        users_with_email = User.objects.filter(email = postData['email']) 
        if len(users_with_email) >=1:
            errors['users_duplicate'] = "Email address taken already, choose another"
        
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name =  models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class TripManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        today = datetime.now().strftime("%Y-%m-%d")
        start_date = postData['start_date']
        end_date = postData['end_date']
        if start_date < today and postData['start_date']!='':
            errors['past_date'] = "Start date must be in the future"
        if end_date < start_date and postData['start_date'] !='' and postData['end_date']!='':
            errors['wrong_schedule'] = "End date must be after Start date"
        if len(postData['destination']) < 3:
            errors['destination'] = "Destination should be at least 3 characters"
        if len(postData['plan']) < 3:
            errors['plan'] = "plan should be at least 3 characters"   
        if len(postData['start_date'])==0:
            errors['stardate'] = "start date must be provided"
        if len(postData['end_date'])==0:
            errors['enddate'] = "end date must be provided"
        # if date validations
        return errors
        


class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    plan = models.TextField()
    creator = models.ForeignKey(User, related_name="trips", on_delete=CASCADE)
    joined = models.ManyToManyField(User, related_name = "joined_trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TripManager()

    

