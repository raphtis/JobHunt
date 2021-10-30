from django.db import models
import re
import bcrypt

# Create your models here.
class JobManager(models.Manager):
    def job_validator(self, postData):
        errors = {}
        if len(postData['company_name']) < 2:
            errors ['company_name'] = "Company name should be longer than one character."
        if len(postData['position']) < 2:
            errors['position'] = "Position should be longer than one character."
        if len(postData['status']) < 2:
            errors['status'] = "Status should be longer than one character."
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

class Job(models.Model):
    company_name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, related_name="jobs", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()

