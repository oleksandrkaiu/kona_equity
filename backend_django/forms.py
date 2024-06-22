from django import forms
from django.conf import settings
from akismet import Akismet
import logging


class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    purpose = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def is_spam(self, ip, ua):
        '''Detects wether a complete message (Email Address, IP, Message content) is spam.
        '''
        akismet_api = Akismet(key=settings.AKISMET_API_KEY, blog_url=settings.AKISMET_BLOG_URL)
        spam = akismet_api.comment_check(
            user_ip=ip,
            user_agent=ua,
            comment_type='contact-form',
            comment_author=self.cleaned_data["name"],
            comment_author_email=self.cleaned_data["email"],
            comment_content=self.cleaned_data["message"],
        )

        # Log all messages (regardless of them being spam or not to a log file)
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler('/home/Konaequity/konaequity/backend_django/logs/spam.log')
        formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        if spam:
            print("Spam message detected.")
            logger.warning(f"Spam message detected: IP: {ip}, User Agent: {ua}, Name: {self.cleaned_data['name']}, Email Address: {self.cleaned_data['email']}, Message: {self.cleaned_data['message']}.")
        else:
            print("Proper message detected.")
            logger.info(f"Proper message detected: IP: {ip}, User Agent: {ua}, Name: {self.cleaned_data['name']}, Email Address: {self.cleaned_data['email']}, Message: {self.cleaned_data['message']}.")

        return spam
