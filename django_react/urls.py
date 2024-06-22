"""django_react URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from backend_django.sitemaps import (City_Sitemap, Company_Sitemap,
                                     GIndustry_Sitemap, Industry_Sitemap,
                                     State_Sitemap,
                                     StateCrossGIndusrty_Sitemap,
                                     StateCrossIndustry_Sitemap,
                                     Static_Sitemap)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps import views
from django.urls import include, path
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

admin.autodiscover()
admin.site.enable_nav_sidebar = False

sitemaps = {
    'static': Static_Sitemap(),
    'company': Company_Sitemap(),
    'state': State_Sitemap(),
    'city': City_Sitemap(),
    'industry': Industry_Sitemap(),
    'google_industry': GIndustry_Sitemap(),
    'industry-state': StateCrossIndustry_Sitemap(),
    'google_industry-state': StateCrossGIndusrty_Sitemap()
}

urlpatterns = [
    path('', include('backend_django_v2.urls')),
    path('admin/', admin.site.urls),
    path('admin/clearcache/', include('clearcache.urls')),
    path('', include('backend_django.urls')),
    path('sitemap.xml', views.index, {'sitemaps': sitemaps}),
    path('sitemap-<section>.xml', views.sitemap,
         {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('accounts/', include('allauth.urls')),
    path('', include("auth_app.urls")),
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('pages/', include(wagtail_urls)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += [path(r'silk/', include('silk.urls', namespace='silk'))]
