import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

admin.site.site_header = 'AmpuShare Admin'
admin.site.index_title = 'Admin'

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/booking/', include('booking.urls')),
                  path('api/social/', include('social.urls')),
                  path('api/user/', include('user.urls')),
                  path('__debug__/', include(debug_toolbar.urls)),
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
