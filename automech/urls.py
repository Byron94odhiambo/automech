from django.contrib import admin
from django.urls import path, include
# If views.py is in the accounts app
from accounts import views
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import landing_page



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', landing_page, name='landing_page'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
