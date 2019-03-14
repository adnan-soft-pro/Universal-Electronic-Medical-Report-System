from django.core.mail import send_mail
from django.utils import timezone
from django.shortcuts import reverse
from django.db.models import Q
from instructions.models import Instruction, InstructionReminder
from instructions.model_choices import *
from django.template import loader
from accounts.models import User, PracticePreferences, GeneralPracticeUser
from common.functions import get_url_page
from datetime import timedelta

from smtplib import SMTPException
import logging

from django.conf import settings


def instruction_notification_email_job():
    instruction_notification_sars()
    instruction_notification_amra()


def instruction_notification_amra():
    instruction_query_set = Instruction.objects.filter(type='AMRA')
    instruction_query_set = instruction_query_set.filter(~Q(status=INSTRUCTION_STATUS_COMPLETE) & ~Q(status=INSTRUCTION_STATUS_REJECT) & ~Q(status=INSTRUCTION_STATUS_PAID))

    # Get Value for table range 2 days.
    expected_date_2days = timezone.now() - timedelta(days=2)
    to_expected_date_2days = expected_date_2days.replace(hour=23, minute=59, second=59)
    from_expected_date_2days = expected_date_2days.replace(hour=00, minute=00, second=00)
    instruction_query_set_2days = Q(fee_calculation_start_date__range=(from_expected_date_2days, to_expected_date_2days))

    # Get Value for table range 6 days.
    expected_date_6days = timezone.now() - timedelta(days=6)
    to_expected_date_6days = expected_date_6days.replace(hour=23, minute=59, second=59)
    from_expected_date_6days = expected_date_6days.replace(hour=00, minute=00, second=00)
    instruction_query_set_6days = Q(fee_calculation_start_date__range=(from_expected_date_6days, to_expected_date_6days))

    # Get Value for table range 10 days.
    expected_date_10days = timezone.now() - timedelta(days=10)
    to_expected_date_10days = expected_date_10days.replace(hour=23, minute=59, second=59)
    from_expected_date_10days = expected_date_10days.replace(hour=00, minute=00, second=00)
    instruction_query_set_10days = Q(fee_calculation_start_date__range=(from_expected_date_10days, to_expected_date_10days))

    # Get Value for table range 14 days.
    expected_date_14days = timezone.now() - timedelta(days=14)
    to_expected_date_14days = expected_date_14days.replace(hour=23, minute=59, second=59)
    from_expected_date_14days = expected_date_14days.replace(hour=00, minute=00, second=00)
    instruction_query_set_14days = Q(fee_calculation_start_date__range=(from_expected_date_14days, to_expected_date_14days))

    # Get Value for table range 20 days.
    expected_date_20days = timezone.now() - timedelta(days=20)
    to_expected_date_20days = expected_date_20days.replace(hour=23, minute=59, second=59)
    from_expected_date_20days = expected_date_20days.replace(hour=00, minute=00, second=00)
    instruction_query_set_20days = Q(fee_calculation_start_date__range=(from_expected_date_20days, to_expected_date_20days))

    # Get Value for table range 23 days.
    expected_date_23days = timezone.now() - timedelta(days=23)
    to_expected_date_23days = expected_date_23days.replace(hour=23, minute=59, second=59)
    from_expected_date_23days = expected_date_23days.replace(hour=00, minute=00, second=00)
    instruction_query_set_23days = Q(fee_calculation_start_date__range=(from_expected_date_23days, to_expected_date_23days))

    instruction_query_set = instruction_query_set.filter(
        instruction_query_set_2days | instruction_query_set_6days | instruction_query_set_10days | instruction_query_set_14days |
        instruction_query_set_20days | instruction_query_set_23days)

    for instruction in instruction_query_set:
        check_time = instruction.fee_calculation_start_date
        if from_expected_date_23days <= check_time <= to_expected_date_23days:
            auto_reject_amra_after_23days(instruction)
        else:
            send_email_amra(instruction)


def send_email_amra(instruction):
    subject_reject_email = 'AMRA instruction not processed'

    # Send Email for GP.
    gp_email = set()
    instruction_link = settings.EMR_URM + reverse('instructions:view_reject', kwargs={'instruction_id': instruction.id})
    gp_managers = User.objects.filter(
            userprofilebase__generalpracticeuser__organisation=instruction.gp_practice.pk,
            userprofilebase__generalpracticeuser__role=GeneralPracticeUser.PRACTICE_MANAGER
        ).values('email')
    for email in gp_managers:
        gp_email.add(email['email'])

    if not instruction.gp_user == None:
        gp_email.add(instruction.gp_user.user.email)

    try:
        send_mail(
            subject_reject_email,
            'Your instruction has been reject',
            'MediData',
            list(gp_email),
            fail_silently=True,
            html_message=loader.render_to_string('instructions/amra_chasing_email.html', {
                'link': instruction_link
            })
        )
    except SMTPException:
        logging.error('"AMRA" Send mail to GP FAILED')


def auto_reject_amra_after_23days(instruction):
    email_user = 'auto_system@medidata.co'
    auto_reject_user, created = User.objects.get_or_create(
        email=email_user,
        username=email_user,
        first_name='auto-reject'
    )

    instruction.status = INSTRUCTION_STATUS_REJECT
    instruction.rejected_reason = LONG_TIMES
    instruction.rejected_by = auto_reject_user
    instruction.rejected_timestamp = timezone.now()
    instruction.rejected_note = 'Instruction Too long'
    instruction.save()

    instruction_link = settings.MDX_URL + reverse('instructions:view_reject', kwargs={'instruction_id': instruction.id})
    instruction_med_ref = instruction.medi_ref
    subject_reject_email = 'AMRA instruction not processed'

    # Send Email for client.
    client_email = [instruction.client_user.user.email]
    try:
        send_mail(
            subject_reject_email,
            'Your instruction has been reject',
            'MediData',
            client_email,
            fail_silently=True,
            html_message=loader.render_to_string('instructions/amra_reject_email.html', {
                'med_ref': instruction_med_ref,
                'link': instruction_link
            })
        )
    except SMTPException:
        logging.error('"AMRA" Send mail to client FAILED')

    # Send Email for GP.
    gp_email = set()
    instruction_link = settings.EMR_URM + reverse('instructions:view_reject', kwargs={'instruction_id': instruction.id})
    gp_managers = User.objects.filter(
            userprofilebase__generalpracticeuser__organisation=instruction.gp_practice.pk,
            userprofilebase__generalpracticeuser__role=GeneralPracticeUser.PRACTICE_MANAGER
        ).values('email')
    for email in gp_managers:
        gp_email.add(email['email'])

    if not instruction.gp_user == None:
        gp_email.add(instruction.gp_user.user.email)

    try:
        send_mail(
            subject_reject_email,
            'Your instruction has been reject',
            'MediData',
            list(gp_email),
            fail_silently=True,
            html_message=loader.render_to_string('instructions/amra_reject_email.html', {
                'med_ref': instruction_med_ref,
                'link': instruction_link
            })
        )
    except SMTPException:
        logging.error('"AMRA" Send mail to GP FAILED')


def instruction_notification_sars():
    now = timezone.now()
    new_or_pending_instructions = Instruction.objects.filter(
        status__in=(INSTRUCTION_STATUS_NEW, INSTRUCTION_STATUS_PROGRESS),
        type=SARS_TYPE
    )

    date_period_admin = [3, 7, 14]
    date_period_surgery = [7, 14, 21, 30]
    for instruction in new_or_pending_instructions:
        diff_date = now - instruction.created
        if diff_date.days in date_period_admin or diff_date.days in date_period_surgery:
            gp_managers = User.objects.filter(
                userprofilebase__generalpracticeuser__organisation=instruction.gp_practice.pk,
                userprofilebase__generalpracticeuser__role=GeneralPracticeUser.PRACTICE_MANAGER
            ).values('email')
            try:
                if gp_managers and diff_date.days in date_period_admin:
                    send_mail(
                        'Pending Instruction',
                        'You have a pending or not started instruction. Click here {link} to see it.'.format(
                            link=settings.MDX_URL + reverse('instructions:view_pipeline')
                        ),
                        'MediData',
                        [gp['email'] for gp in gp_managers],
                        fail_silently=True,
                        auth_user=settings.EMAIL_HOST_USER,
                        auth_password=settings.EMAIL_HOST_PASSWORD,
                    )
                if instruction.gp_practice and instruction.gp_practice.organisation_email and diff_date.days in date_period_surgery:
                    send_mail(
                        'Pending Instruction',
                        'You have a pending or not started instruction.',
                        'MediData',
                        [instruction.gp_practice.organisation_email],
                        fail_silently=True,
                        auth_user=settings.EMAIL_HOST_USER,
                        auth_password=settings.EMAIL_HOST_PASSWORD,
                    )
                InstructionReminder.objects.create(
                    instruction_id=instruction.id,
                    note="note added to instruction for %s day reminder"%diff_date.days,
                    reminder_day=diff_date.days
                )
            except SMTPException:
                logging.error('Send mail FAILED to send message')


def send_email_to_practice_job():
    unstarted_instructions = Instruction.objects.filter(status=INSTRUCTION_STATUS_NEW)
    for instruction in unstarted_instructions:
        gp_practice = instruction.gp_practice
        practice_preferences = PracticePreferences.objects.get(gp_organisation=gp_practice)
        if practice_preferences.notification == 'DIGEST':
            send_mail(
                'Unstarted Instruction',
                'You have unstarted instructions. Click here {link} to see it.'.format(link=settings.MDX_URL + reverse('instructions:view_pipeline')),
                'MediData',
                [gp_practice.organisation_email],
                fail_silently=True,
                auth_user=settings.EMAIL_HOST_USER,
                auth_password=settings.EMAIL_HOST_PASSWORD,
            )
