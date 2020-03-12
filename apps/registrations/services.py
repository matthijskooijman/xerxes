import re

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import transaction
from django.db.models import Q
from django.db.models.functions import Now
from django.forms import ValidationError
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from apps.events.models import Event

from .models import Registration, RegistrationFieldOption


class RegistrationStatusService:
    @staticmethod
    def finalize_registration(registration):
        """
        Finalizes a registration by setting its status to REGISTERED and doing additional needed bookkeeping.

        Current status must be PREPARATION_COMPLETE, otherwise a ValidationError is raised.

        When there are sufficient slots available for the options selected by this registration, the status is set to
        REGISTERED. If not, status is changed to STATUS_WAITINGLIST.
        """
        if not registration.status.PREPARATION_COMPLETE:
            raise ValidationError(_("Registration not ready for finalization"))

        with transaction.atomic():
            # Lock the event, to prevent multiple registrations from taking up the same slots
            event = Event.objects.with_used_slots().select_for_update().get(pk=registration.event.pk)
            # This selects all options that are associated with the current registration and that have non-null slots.
            # annotated with the number of slots used.
            options_with_slots = RegistrationFieldOption.objects.with_used_slots().filter(
                Q(registrationfieldvalue__registration=registration) & ~Q(slots=None),
            )

            # If the event has slots defined, we can treat it just like any option with slots
            if event.slots is not None:
                options_with_slots = [*options_with_slots, event]

            if any(o.full or o.used_slots >= o.slots for o in options_with_slots):
                registration.status = Registration.statuses.WAITINGLIST
            else:
                registration.status = Registration.statuses.REGISTERED

                # Set full for any options (or the event as a whole) where we used the last slot
                for o in options_with_slots:
                    if o.slots - o.used_slots == 1:
                        o.full = True
                        o.save()

            registration.registered_at = Now()
            registration.save()


class RegistrationNotifyService:
    @staticmethod
    def send_confirmation_email(registration):
        context = {
            'user': registration.user,
            'registration': registration,
        }
        body = render_to_string('registrations/email/registration_confirmation.txt', context)
        subject = render_to_string('registrations/email/registration_confirmation_subject.txt', context).strip()
        # Remove all empty lines, except for the ones that contain just a . (then just remove the .). This allows
        # removing the empty lines produced by template tags that got removed, while keeping the empty lines that were
        # explicitly added in the template.
        body = re.sub("^\n+", "", body)
        body = re.sub("\n\n+", "\n", body)
        body = re.sub("\n\\.\n", "\n\n", body)

        email = EmailMessage(
            body=body, subject=subject, to=[registration.user.email],
            bcc=settings.BCC_EMAIL_TO,
        )
        email.send()
