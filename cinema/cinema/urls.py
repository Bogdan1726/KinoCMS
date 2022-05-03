from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar
from django.urls import include
from main import main_language

urlpatterns = [
    path('old_admin/', admin.site.urls),
    path('admin/', include('cms.urls')),
] + i18n_patterns(
    path('i18n/', main_language.set_language, name="set_language"),
    path('', include('main.urls')),
    path('user/', include('user.urls')),

)


if settings.DEBUG:
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
