from django.contrib import admin
from django.urls import path, include
# En myproject/urls.py o al final de settings.py
from django.conf.urls import handler403

handler403 = 'users.views.error_403'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
]
