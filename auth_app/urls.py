
from django.urls import path
from .views import *

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("register/", AjaxSignUpView.as_view(), name="register"),
    path("update_profile/", update_profile, name="update_profile"),
    path("watchlist/", watchlist, name="watchlist"),
    path("watchtest/", watchtest, name="watchtest"),
    path("supplier/", supplier, name="company_supplier"),
    path("addfav/", addToFavourite, name="addfav"),
    path("remfav/", removeFromFavourite, name="remfav"),

    path('signup/cold-join', signup, name="signup"),
    path('signup/vanity', signup_v, name="signup_vanity"),
    path('signup/authwall', signup_a, name="signup_authwall"),
    path('signup/register_google_user', register_google_user, name="register_google_user"),
    path('login_google_user', login_google_user, name="login_google_user"),
    path('signup/email_verification_request', email_verification_request, name="email_verification_request"),
    path('signup/email_verification_sent', email_verification_sent, name="email_verification_sent"),
    path('signup/email_verification_activate', email_verification_activate, name='email_verification_activate'),
    path('signup/email_verification_finish', email_verification_finish, name='email_verification_finish'),
    path('forgot_password_view', forgot_password_view, name='forgot_password_view'),
    path('forgot_password_request', forgot_password_request, name='forgot_password_request'),
    path('forgot_password_sent', forgot_password_sent, name='forgot_password_sent'),
    path('forgot_password_activate', forgot_password_activate, name='forgot_password_activate'),
    path('reset_password_finish', reset_password_finish, name='reset_password_finish'),

    path('login', login, name="login"),
    path('ugsuper/<str:email>', upgrade_superuser),
]