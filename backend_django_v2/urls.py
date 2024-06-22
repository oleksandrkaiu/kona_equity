from django.urls import path

from backend_django_v2.views import company_view, edit_company, like_company, claim_company, edit_contact

app_name = 'backend_django_v2'
urlpatterns = [
    path('company/<str:id>/', company_view, name='company'),
    path('edit_company/<str:id>', edit_company, name='edit_company'),
    path('like_company/<str:id>', like_company, name='like_company'),
    path('claim_company', claim_company, name='claim_company'),
    path('edit_contact/<str:id>', edit_contact, name='edit_contact'),
]
