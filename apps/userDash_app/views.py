# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.shortcuts import render, redirect
import bcrypt

from models import *

# FORMS

def index(request):
	return render(request, 'userDash_app/index.html')

def registerUserPage(request):
	return render(request, 'userDash_app/registerPage.html')

def loginUserPage(request):
	return render(request, 'userDash_app/loginPage.html')

def dashAdminPage(request):
	if User.objects.get(id=request.session['currentUser']).status == "admin":
		return render(request, 'userDash_app/dashAdminPage.html', { "users": User.objects.all() })
	else:
		return render(request, 'userDash_app/errorPage.html')

def dashUserPage(request):
	if User.objects.get(id=request.session['currentUser']).status == "normal":
		return render(request, 'userDash_app/dashUserPage.html', { "users": User.objects.all() })
	else:
		return redirect('/dashboard/admin')

def newUserPage(request):
	return render(request, 'userDash_app/newUserPage.html')

def editUserPage(request):
	return render(request, 'userDash_app/editUserPage.html', { "user": User.objects.get(id=request.session['currentUser']) })

def userProfilePage(request, id):
	return render(request, 'userDash_app/userProfile.html', { "user": User.objects.get(id=id), "posts": Post.objects.filter(recipient=User.objects.get(id=id)), "comments": Comment.objects.all() })

def editUserfromAdminPage(request, id):
	if User.objects.get(id=request.session['currentUser']).status == "admin":
		return render(request, 'userDash_app/editUserfromAdmin.html', { "user": User.objects.get(id=id) })
	else:
		return render(request, 'userDash_app/errorPage.html')

# USER ACTIONS

def loginUser(request):
	errors = User.objects.login_validator(request.POST, request)
	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags = tag)
		return redirect('/login')
	else:
		# set currentUser value to id of logged in user
		if 'currentUser' not in request.session:
			request.session['currentUser'] = User.objects.get(email=request.POST['email']).id
			print("current user is " + str(request.session['currentUser']))
		# set logged in variable to true
		request.session['loggedIn'] = True
		# check if they are an admin or not
		if User.objects.get(email=request.POST['email']).status == "admin":
			return redirect('/dashboard/admin')
		else:
			return redirect('/dashboard')

def createUser(request):
	errors = User.objects.register_validator(request.POST)
	# Stop if errors exist
	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags = tag)
		return redirect('/register')
	# Allow if no errors
	else:
		hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
		# If first to register, make admin
		if not (User.objects.all()):
			User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hash1, desc="I am the admin", status="admin")
			# create currentUser session variable
			if 'currentUser' not in request.session:
				request.session['currentUser'] = User.objects.last().id
			return redirect('/dashboard/admin')
		# If not first to register, make normal
		else:
			User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hash1, desc="I am a new user", status="normal")
			# If admin creates account, don't change currentUser value
			if 'currentUser' in request.session:
				return redirect('/dashboard/admin')
			# If new user created, change currentUser value to new user
			else:
				if 'currentUser' not in request.session:
					request.session['currentUser'] = User.objects.last().id
				return redirect('/dashboard')

def updateUser(request, id):
	b = User.objects.get(id=id)
	b.email = request.POST['email']
	b.first_name = request.POST['first_name']
	b.last_name = request.POST['last_name']
	b.status = request.POST['status']
	b.desc = request.POST['desc']
	
	b.save()
	return redirect('/users/show/'+id)

def changePassword(request, id):
	b = User.objects.get(id=id)
	errors = User.objects.changePassword_validator(request.POST, id)
	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags = tag)
		return redirect('/users/edit')
	else:
		hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
		b.password = hash1
		b.save()
		return redirect('/users/show/'+id)

def removeUser(request, id):
	User.objects.get(id=id).delete()
	return redirect('/dashboard/admin')

def logout(request):
	request.session.clear()
	return redirect('/')

# POST ACTIONS

def createPost(request, id):
	Post.objects.create(content=request.POST['content'], author=User.objects.get(id=request.session['currentUser']),  recipient=User.objects.get(id=id))
	return redirect('/users/show/'+id)

# COMMENT ACTIONS

def createComment(request, siteid, postid):
	Comment.objects.create(content=request.POST['content'], author=User.objects.get(id=request.session['currentUser']), post=Post.objects.get(id=postid))
	return redirect('/users/show/'+ siteid)