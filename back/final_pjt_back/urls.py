from django.contrib import admin
from django.urls import path, include

urlpatterns = [
     path('admin/', admin.site.urls),
     # accounts
     path('accounts/', include('accounts.urls')),
     # api
     path('apis/', include('apis.urls')),
     # articles
     path('articles/', include('articles.urls')),
     
]
