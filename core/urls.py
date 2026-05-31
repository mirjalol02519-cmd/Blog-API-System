from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.core_urls if hasattr(admin.site, 'core_urls') else admin.site.urls),
    path('api/v1/', include('app_blog.urls')), # All API starts here
]

# If DEBUG=True, allow media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
