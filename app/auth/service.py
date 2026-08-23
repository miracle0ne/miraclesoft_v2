import secrets
import resend

from flask import current_app, url_for


def generate_token():
    return secrets.token_urlsafe(32)


def verification_email(user):

    verification_url = url_for(
        "auth.verify_email",
        token=user.email_verification_token,
        _external=True
    )

    resend.api_key = current_app.config["RESEND_API"]

    resend.Emails.send({
        "from": "MiracleSoft <onboarding@resend.dev>",
        "to": [user.email],
        "subject": "Verify your MiracleSoft account",
        "html": f"""
            <h2>Welcome to MiracleSoft!</h2>

            <p>Thank you for creating an account.</p>

            <p>Please click the link below to verify your email:</p>

            <p>
                <a href="{verification_url}">
                    Verify Email
                </a>
            </p>

            <p>If you did not create this account, please ignore this email.</p>
        """
    })

def reset_password_email(user):

    reset_url = url_for(
        "auth.reset_password",
        token=user.password_reset_token,
        _external=True
    )

    resend.api_key = current_app.config["RESEND_API"]

    resend.Emails.send({
        "from": "MiracleSoft <onboarding@resend.dev>",
        "to": [user.email],
        "subject": "Reset your MiracleSoft password",
        "html": f"""
            <h2>Password Reset</h2>

            <p>Hello {user.name},</p>

            <p>
                We received a request to reset your MiracleSoft password.
            </p>

            <p>
                Click the link below to create a new password:
            </p>

            <p>
                <a href="{reset_url}">
                    Reset Password
                </a>
            </p>

            <p>
                If you did not request a password reset,
                you can safely ignore this email.
            </p>
        """
    })