from unittest.mock import patch

from django.core.mail import send_mail
from django.test import TestCase, override_settings


def sendmail_mock(self, from_addr, to_addrs, msg, mail_options=[], rcpt_options=[]):
    return to_addrs


@patch('smtplib.SMTP.sendmail', sendmail_mock)
@override_settings(EMAIL_BACKEND='django_filtered_email_backend.FilteredEmailBackend')
class BackendTestCase(TestCase):
    def test_empty(self):
        from django.conf import settings

        send_mail(
            'test_empty',
            'test_empty',
            settings.DEFAULT_FROM_EMAIL,
            ['to@example.com'],
            fail_silently=False,
        )

    @override_settings(EMAIL_ALLOWED_RECIPIENTS=['to@example.com'])
    def test_email_allowed(self):
        from django.conf import settings

        send_mail(
            'test_email_allowed',
            'test_email_allowed',
            settings.DEFAULT_FROM_EMAIL,
            ['to@example.com'],
            fail_silently=False,
        )

    @override_settings(EMAIL_ALLOWED_DOMAINS=['example.com'])
    def test_domain_allowed(self):
        from django.conf import settings

        send_mail(
            'test_domain_allowed',
            'test_domain_allowed',
            settings.DEFAULT_FROM_EMAIL,
            ['to@example.com'],
            fail_silently=False,
        )

    @override_settings(EMAIL_ALLOWED_RECIPIENTS=['to@example.com'])
    def test_email_not_allowed(self):
        from django.conf import settings

        send_mail(
            'test_email_not_allowed',
            'test_email_not_allowed',
            settings.DEFAULT_FROM_EMAIL,
            ['not-to@example.com'],
            fail_silently=False,
        )

    @override_settings(EMAIL_ALLOWED_DOMAINS=['example.com'])
    def test_domain_not_allowed(self):
        from django.conf import settings

        send_mail(
            'test_domain_not_allowed',
            'test_domain_not_allowed',
            settings.DEFAULT_FROM_EMAIL,
            ['to@not-example.com'],
            fail_silently=False,
        )

    @override_settings(EMAIL_ALLOWED_RECIPIENTS=['to@example.com'])
    @override_settings(EMAIL_ALLOWED_DOMAINS=['not-example.com'])
    def test_domain_not_allowed_but_email(self):
        from django.conf import settings

        send_mail(
            'test_domain_not_allowed_but_email',
            'test_domain_not_allowed_but_email',
            settings.DEFAULT_FROM_EMAIL,
            ['to@example.com'],
            fail_silently=False,
        )

    @override_settings(EMAIL_ALLOWED_RECIPIENTS=['not-to@example.com'])
    @override_settings(EMAIL_ALLOWED_DOMAINS=['example.com'])
    def test_email_not_allowed_but_domain(self):
        from django.conf import settings

        send_mail(
            'test_email_not_allowed_but_domain',
            'test_email_not_allowed_but_domain',
            settings.DEFAULT_FROM_EMAIL,
            ['to@example.com'],
            fail_silently=False,
        )