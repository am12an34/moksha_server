from django.urls import path
from .views import *

urlpatterns = [
    path('/check-auth', CheckAuth.as_view()),
    path('/register', Register.as_view()),
    path('/login', Login.as_view()),
    path('/logout', Logout.as_view()),
    path('/validate-link/account/<slug:otp_hash>', VerifyAccountOtpLink.as_view()),
    path('/verification/<slug:otp_hash>', AccountVerification.as_view()),
    path('/resend-otp/<slug:otp_hash>', ResendOtp.as_view()),
    path('/resend-verification-link', ResendVerificationLink.as_view()),
    path('/validate-link/reset-pass/<slug:forgot_pass_hash>', VerifyResetPassLink.as_view()),
    path('/forgot-password', ForgotPassword.as_view()),
    path('/reset-password/<slug:forgot_pass_hash>', ResetPassword.as_view()),
    path('/change-password', ChangePassword.as_view()),
]
