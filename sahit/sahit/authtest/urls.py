
#!python
# authtest/urls.py
from django.conf.urls import include, url
from django.contrib import admin
# Add this import
from django.contrib.auth import views
from log.forms import LoginForm
from log.views import homepage,UserFormView, hostelfilter, form_create, hostelfilteradmin, flagchanger, admin_show, start

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('log.urls')),
    url(r'^login/$', views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', views.logout, {'next_page': '/login'}),
    url(r'^homepage/$',homepage),
    url(r'^register/$', UserFormView.as_view(), name='register'),
    url(r'^filter/(?P<hostelname>\w+)/$',hostelfilter),
    url(r'^addcourier',form_create),
    url(r'^adminshow/$',admin_show),
    url(r'^adminshow/(?P<id>\w+)/$',flagchanger),
    url(r'^adminshow/filter/(?P<hostelname>\w+)/$',hostelfilteradmin),
    url(r'^start/$',start),

]
