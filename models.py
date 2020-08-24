from django.db import models
import bcrypt
import re

email_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class ApplicantManager(models.Manager):
    def validate(self, post_Data):
        errors = {}
        if len(post_Data['first_name']) < 2:
            errors['first_name'] = "Firstname cannot be less than two characters"
        if len(post_Data['last_name']) < 2:
            errors['last_name'] = "Lastname cannot be less than two characters"
        if not email_re.match(post_Data['email']):
            errors['email'] = "Invalid email address. Enter correct email"
        if len(post_Data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        if post_Data['password'] != post_Data['confirm_password']:
            errors['password'] = "Passwords do not match."
        return errors
    def authenticate(self, email, password):
    	applicants_with_email = self.filter(email=email)
    	if not applicants_with_email:
    		return False
    	applicant = applicants_with_email[0]
    	return bcrypt.checkpw(password.encode('utf-8'), applicant.password.encode('utf-8'))

class Applicant(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = ApplicantManager()

    class Meta:
        db_table = "applicant"
class Profile(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    sex = models.CharField(max_length=10, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    photo = models.FileField(null=True, blank=True, upload_to="media")

    class Meta:
        db_table = "profile"

class Combination(models.Model):
    combination = models.CharField(max_length=50)
    class Meta:
        db_table = "combination"
        
class Application(models.Model):
    applicant   = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    combination = models.ForeignKey(Combination, on_delete=models.CASCADE)
    school_year = models.CharField(max_length=20)
    essay       = models.FileField(upload_to='documents/%Y/%m/%d/')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "applications"