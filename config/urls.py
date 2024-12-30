from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'config.views.handler404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('salas.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('reservas/', include('reservas.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Permitir servir mídia no modo DEBUG = False (apenas para desenvolvimento local)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)