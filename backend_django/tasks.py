from background_task import background
from django.core.mail import send_mail, BadHeaderError

EMAIL = "joey@konaequity.com"

@background(schedule=0, queue="email")
def sendEmail(data):
    '''Background task for sending Emails
    '''
    print("Received data: ", data)
    try:
        send_mail(
            subject = data["subject"],
            message = data["message"],
            from_email = EMAIL,
            recipient_list = [EMAIL,],
            auth_user = EMAIL,
            auth_password = 'Maui2020',
            fail_silently = False,
        )
        print("Email sent")
    except BadHeaderError:
        print("Bad Header detected. Deleting message")
