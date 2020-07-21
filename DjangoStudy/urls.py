"""DjangoStudy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from Report import views


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('Report.urls')),
    path('', views.hello),
    path('hello', views.hello),
    # path('test', views.test),
    path('tokenTest', views.tokenTest),
    path('passwordTest', views.passwordTest),
    path('login', views.login),
    path('register', views.register),
    path('basic_information', views.basic_information),
    path('browse_statistic', views.browse_statistic),
    path('qa_statistic', views.qa_statistic),
    path('browse_track', views.browse_track),
    path('show_stu_id', views.show_stu_id)

]
