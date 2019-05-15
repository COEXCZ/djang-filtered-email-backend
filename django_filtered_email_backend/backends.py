# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend as DjangoEmailBackend
from django.core.mail.message import sanitize_address

logger = logging.getLogger("filtered_email_backend")


class FilteredEmailBackend(DjangoEmailBackend):
    """
    If allowed recipients or domains are non-empty set, recipients are validated against them.
    It allowed emails and domains are empty, validation is passed through.
    """

    @staticmethod
    def _filter_is_domain_allowed(recipient, allowed_domains=tuple()):
        if allowed_domains:
            for domain in allowed_domains:
                if recipient.endswith(domain):
                    return True
            return False
        return True

    def _send(self, email_message):
        """A helper method that does the actual sending."""

        if not email_message.recipients():
            return False

        encoding = email_message.encoding or settings.DEFAULT_CHARSET
        from_email = sanitize_address(email_message.from_email, encoding)
        recipients = [sanitize_address(addr, encoding) for addr in email_message.recipients()]

        allowed_recipients = [
            recipient.strip().lower() for recipient in getattr(settings, 'EMAIL_ALLOWED_RECIPIENTS', [])
        ]
        allowed_domains = [
            '@{}'.format(domain.strip().lower()) for domain in getattr(settings, 'EMAIL_ALLOWED_DOMAINS', [])]
        recipients = [recipient.strip().lower() for recipient in recipients]

        if allowed_recipients or allowed_domains:
            filtered_recipients = []

            for domain in allowed_domains:
                for email in recipients:
                    if email.endswith(domain):
                        filtered_recipients.append(email)

            filtered_recipients = list(
                (set(allowed_recipients) & set(recipients))  # clear recipients by allowed recipients
                | set(filtered_recipients)  # union with recipients allowed by domain
            )

            email_message.subject = '[FILTERED] +{allowed_recipients} {subject}'.format(
                allowed_recipients=filtered_recipients,
                subject=email_message.subject
            )

            logger.debug('[FILTERED] +{allowed_recipients} -{excluded_recipients} {subject}'.format(
                allowed_recipients=filtered_recipients,
                excluded_recipients=list(set(recipients).difference(set(filtered_recipients))),
                subject=email_message.subject
            ))

            final_recipients = filtered_recipients
        else:
            final_recipients = recipients

        message = email_message.message()

        try:
            self.connection.sendmail(from_email, final_recipients, message.as_bytes(linesep='\r\n'))
        except Exception as e:
            logger.debug(e, exc_info=True)
            if not self.fail_silently:
                raise
            return False

        return True
