from django.db import models
import re
import bcrypt

# Create your models here.
class JobEntryManager(models.Manager):
    def jobEntry_validator(self, postData):
        errors = {}
        if len(postData['company_name']) < 10:
            errors['company_name'] = "Company name needs to be at least 2 characters."

        if len(postData['position']) < 2:
            errors['position'] = "Position should be 2 or more characters."

        if len(postData['status']) < 2:
            errors['status'] = "Status should be 2 or more characters."

        current_jobEntries = JobEntry.objects.filter(message=postData['position'])
        if len(current_jobEntries) > 0:
            errors['duplicate'] = "That position has already been added."
        return errors



class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be 2 characters or more."

        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be 2 characters or more."

        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['email'])==0:
            errors['email'] = "You must enter an email"
        elif not email_regex.match(postData['email']):
            errors['email'] = "Must be a valid email"

        
        
        current_users = User.objects.filter(email=postData['email'])
        if len(current_users) > 0:
            errors['duplicate'] = "That email is already in use"
        

        if len(postData['password']) < 8:
            errors["password"] = "Password must be 8 characters or more."

        if postData['password'] != postData['confirm_password']:
            errors["match"] = "Passwords do not match."

        return errors

    def login_validator(self, postData):
        errors = {}
        existing_user = User.objects.filter(email=postData['email'])
        if len(postData['email']) == 0:
            errors['email'] = "Email must be entered"

        if len(postData['password']) < 8:
            errors['password'] = "Password must be 8 characters or more"
        elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) != True:
            errors['password'] = "Email and password do not match"
        
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class JobEntry(models.Model): 
    company_name = models.CharField(max_length=255)
    position = models.CharField(max_length=200)
    status = models.TextField()
    created_by = models.ForeignKey(User, related_name="jobEntries", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    object = JobEntryManager()

