# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	def register_validator(self, postData):
		errors={}
		if len(postData['first_name']) < 2:
			errors["shortFirst"] = "First name must be more than 2 charactes long."
		if len(postData['last_name']) < 2:
			errors["shortLast"] = "Last name must be more than 2 characters long."
		if not EMAIL_REGEX.match(postData['email']):
			errors["emailformat"] = "Email format must be _____@___.com"
		if (User.objects.filter(email=postData['email'])):
			errors["exists"] = "This email already exists in our database. Please enter a different email or login below."
		if (postData['password'] != postData['confPassword']):
			errors["noMatch"] = "Your password does not match. Please try again."
		return errors
	def login_validator(self, postData, request):
		errors={}
		if not (User.objects.get(email=postData['email'])):
			errors["doesntexists"] = "This email does not exist in our database. Please enter register above."
		elif bcrypt.checkpw(postData['password'].encode(), User.objects.get(email=postData['email']).password.encode()) == False:
			errors['wrongPassword'] = "Incorrect Password. Please try again."
		if ('currentUser' in request.session):
			errors["loggedIn"] = "Someone is already logged in. Please log out before trying to log in."
		return errors

	def changePassword_validator(self, postData, id):
		errors = {}
		if (postData['password'] != postData['confPassword']):
			errors["noMatch"] = "Your password does not match. Please try again."
		if (postData['password']) == User.objects.get(id=id).password:
			errors['samePW'] = "Please enter a new password."
		return errors

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	desc = models.CharField(max_length=1000)
	status = models.CharField(max_length=45)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Post(models.Model):
	content = models.CharField(max_length=1000)
	author = models.ForeignKey(User, related_name="postsMade")
	recipient = models.ForeignKey(User, related_name="postsReceived")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
	content = models.TextField()
	author = models.ForeignKey(User, related_name="comments")
	post = models.ForeignKey(Post, related_name="comments")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)