from django.urls import include, re_path, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    # re_path(r"^admin/", admin.site.urls),
    # re_path(r"^admin/", TemplateView.as_view(template_name="index.html")),
    # re_path(r"^admin/", include('authorize.urls')),
    re_path(r"^api/v1/", include('api.urls')),
    path("admin/", admin.site.urls, name="admin"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
