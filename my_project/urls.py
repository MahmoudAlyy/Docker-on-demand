"""my_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from users import views as users_views




urlpatterns = [
    url(r'^$', users_views.home, name='home'),
    url(r'^login/$', auth_views.LoginView.as_view(), {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', users_views.signup, name='signup'),
    url(r'^shell/$', users_views.shell, name='shell'),
    url(r'^browse/$', users_views.browse, name='browse'),
    url(r'^handle/$', users_views.handle, name='handle'),
    url(r'^console/$', users_views.console, name='console'),
    url(r'^console/post/$', users_views.console_post, name='console_post'),


]
