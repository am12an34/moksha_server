from users.models import User
import random
import secrets
import string
import textwrap
import environ

env = environ.Env()
environ.Env.read_env()


def generate_profile_tag(length=8):
    uid = ''.join(secrets.choice(string.ascii_lowercase + string.digits)
                  for _ in range(length))
    return 'MOK-' + uid


def generate_hash(length=15):
    random_hash = ''.join(secrets.choice(
        string.ascii_letters + string.digits) for _ in range(length))
    return random_hash


def get_account_verification_link(hash: str):
    client_domain = env('CLIENT_DOMAIN')

    if client_domain[-1] == '/':
        client_domain = client_domain + 'auth/verification/'
    else:
        client_domain = client_domain + '/auth/verification/'

    return client_domain + hash


def get_forgot_password_link(hash: str):
    client_domain = env('CLIENT_DOMAIN')

    if client_domain[-1] == '/':
        client_domain = client_domain + 'auth/reset-password/'
    else:
        client_domain = client_domain + '/auth/reset-password/'

    return client_domain + hash


def generate_otp():
    return random.randint(1000, 9999)


def get_account_verification_mail_message(first_name: str, otp: int, link: str, is_new=True):
    valid_time_hours = int(env('OTP_VALIDATION_SECONDS')) // 3600
    first_mail_intro = 'Welcome to Moksha 2024 Official Website! Verify your email to get started:'
    resend_intro = 'A new OTP has been generated for your account verification:'

    return textwrap.dedent(f'''\
        Hi {first_name},

        {first_mail_intro if is_new else resend_intro}

        OTP: {otp}
        Verification Link: {link}

        Please use this OTP within {valid_time_hours} hour(s) to complete the verification process.

        If you have any questions or require further assistance, please reply to this email or write an email to {env('EMAIL_HOST_USER')}.

        Cheers,
        Moksha 2024 Tech Team,
        NIT Agartala
    ''')


def get_forgot_password_mail_message(user: User, link: str):
    valid_time_hours = int(env('FORGOT_PASS_VALIDATION_SECONDS')) // 3600

    return textwrap.dedent(f'''\
        Dear {user.first_name},

        We have recently received a request to reset the password for your account associated with the email address: {user.email}. If you did not initiate this request, please disregard this email.

        To proceed with resetting your password, please click on the following link or copy and paste it into your web browser:

        {link}

        This link will expire within {valid_time_hours} hour(s). If the link expires, you can initiate a new password reset request through our website.

        If you have any questions or require further assistance, please reply to this email or write an email to {env('EMAIL_HOST_USER')}.

        Cheers,
        Moksha 2024 Tech Team,
        NIT Agartala
    ''')
