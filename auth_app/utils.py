from django.conf import settings
from akismet import Akismet
from .freemails import freeEmails
from email_validator import validate_email, EmailNotValidError


def validateEmailAddress(email, ip, ua):
    akismet_api = Akismet(key=settings.AKISMET_API_KEY, blog_url=settings.AKISMET_BLOG_URL)
    if email.partition("@")[2] in freeEmails:
        return False, "A business email is required."
    try:
        validate_email(email)
    except EmailNotValidError:
        return False, "This is not a valid email address."
    spam = akismet_api.comment_check(
        user_ip=ip,
        user_agent=ua,
        comment_author_email=email
    )
    if spam:
        return False, "This has been identified as spam"
    return True, ""