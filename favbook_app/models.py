from django.db import models

import re
class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name should be at least 2 characters"
        if not postData['first_name'].isalpha():
            errors['first_name_alp'] = "First name should only contain alphabets"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters"
        if not postData['last_name'].isalpha():
            errors['last_name_alp'] = "Last name should only contain alphabets"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if not postData['password'] == postData['confirm_pw']:
            errors['match_pw'] = "Password doesn't match up with confirm password"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters long"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    #book_upload = list of book uploaded by this user
    #favbook = list of book liked by this user

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, related_name="book_upload", on_delete = models.CASCADE)
    fav = models.ManyToManyField(User, related_name="favbook")

