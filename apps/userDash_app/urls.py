from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
# FORMS
	url(r'^$', views.index),
	url(r'^register$', views.registerUserPage),
	url(r'^login$', views.loginUserPage),
	url(r'^dashboard/admin$', views.dashAdminPage),
	url(r'^dashboard$', views.dashUserPage),
	url(r'^users/new$', views.newUserPage),
	url(r'^users/edit$', views.editUserPage),
	url(r'^users/show/(?P<id>\d+)$', views.userProfilePage),
	url(r'^users/edit/(?P<id>\d+)$', views.editUserfromAdminPage),
# USER ACTIONS
	url(r'^loginUser$', views.loginUser),
	url(r'^create$', views.createUser),
	url(r'^update/(?P<id>\d+)$', views.updateUser),
	url(r'^updatePW/(?P<id>\d+)$', views.changePassword),
	url(r'^remove/(?P<id>\d+)$', views.removeUser),
	url(r'^logout$', views.logout),

# POST ACTIONS
	url(r'^createPost/(?P<id>\d+)$', views.createPost),

# COMMENT ACTIONS
	url(r'^createComment/(?P<siteid>\d+)/(?P<postid>\d+)$', views.createComment),
]