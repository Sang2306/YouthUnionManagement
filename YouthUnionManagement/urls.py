import django_js_reverse.views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('home.urls')),
                  path('jsreverse/', django_js_reverse.views.urls_js, name='js_reverse'),
                  path('dang-nhap/', include('youth_union.urls')),
                  path('quan-tri/', include('youth_union_admin.urls'))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
