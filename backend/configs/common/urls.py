from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='static/home.html')),
    url(r'^admin/', include(admin.site.urls)),

    # FRONT-END
    # url(r'^loans/', include('apps.loans.urls.frontend')),

    # API
    url(r'^api/loans/', include('apps.loans.urls.api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

