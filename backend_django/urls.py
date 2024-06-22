from django.urls import path, re_path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hook', views.hook),
    re_path(r'^ajax/autocomplete/$', views.autocomplete, name='ajax_autocomplete'),
    re_path(r'^ajax/industry/autocomplete/$', views.industry_autocomplete, name='ajax_industry_autocomplete2'),
    path('find/<str:area>/', views.find_pagination_redesign, name='search'),
    path('find', views.find_pagination_redesign),
    path('find/', views.find_pagination_redesign),
    path('people/', views.find_pagination_people),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('about/', views.about, name="about"),
    path('watch/', views.watch, name="watch"),
    path('new/', views.new, name="new"),
    path('contact/', views.contact, name="contact"),
    path('privacy/', views.privacy, name="privacy"),
    path('premium/', views.premium, name="premium"),
    path('pricing/', views.pricing, name="pricing"),
    path('stripe-config/', views.stripe_config, name="stripe-config"),
    path('create-checkout-session/', views.create_checkout_session, name="create-checkout-session"),
    path('success', views.success, name='success'),
    path('cancelled/', views.cancel, name='cancelled'),
    path('webhook', views.webhook_received, name="webhook"),
]
