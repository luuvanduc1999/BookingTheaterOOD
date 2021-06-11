"""FirstAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import include
from django.contrib import admin
import django.contrib.auth.urls
from django.urls import path
import system.api_views
import system.views
from system.views import SearchResultsView, ConfirmPageView

urlpatterns = [
    path('', system.views.showHomePage),
    path('infor', system.views.showInfo),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/',system.views.editprofile, name='editprofile'),
    path('order/', system.views.showTicket, name='showTicket'),
    path('order/<idx>', system.views.showTicketID, name='showTicketID'),
    path('booking/', SearchResultsView.as_view(), name='search_results'),
    path('confirm/', ConfirmPageView.as_view(), name='confirm'),
    path('confirm/<str:confirm_code>', system.views.confirm_by_code, name='confirm code'),
    path('booking/<str:movie_id>', system.views.movie_booking, name='movie_booking'),
    path('booking/<str:movie_id>/<str:room_id>', system.views.completeBooking, name='completeBooking'),
]
