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
    first_mail_intro = (
        "Welcome to Moksha IX – 2025.\n"
        "You're just one step away from joining an unforgettable experience. Let's get your email verified."
    )
    resend_intro = (
        "Here’s your new OTP to complete the verification for Moksha IX – 2025.\n"
        "Use it to continue your journey with us."
    )

    return textwrap.dedent(f'''\  
        Hi {first_name},

        {first_mail_intro if is_new else resend_intro}

        OTP: {otp}  
        Verification Link: {link}

        This OTP will remain valid for the next {valid_time_hours} hour(s). Complete your verification before it expires.

        Need help? Just reply to this email or contact us at {env('EMAIL_HOST_USER')} — we’ll be happy to assist you.

        Warm regards,  
        Moksha IX Tech Team  
        National Institute of Technology, Agartala
    ''')



def get_forgot_password_mail_message(user: User, link: str):
    valid_time_hours = int(env('FORGOT_PASS_VALIDATION_SECONDS')) // 3600

    return textwrap.dedent(f'''\  
        Hello {user.first_name},

        We received a request to reset the password for your Moksha IX – 2025 account linked to this email: {user.email}.  
        If this wasn’t you, feel free to ignore this message — your account is safe.

        To reset your password, simply click the link below or copy it into your browser:

        {link}

        Please note, this link is valid for {valid_time_hours} hour(s). If it expires, you can always request a new one from the website.

        Need help or have questions? Just reply to this email or reach out to us at {env('EMAIL_HOST_USER')}.

        Best regards,  
        Moksha IX Tech Team  
        National Institute of Technology, Agartala
    ''')

