# podcasts/management/commands/startjobs.py

# Standard Library
import logging
import datetime

# Django
from django.conf import settings
from django.core.management.base import BaseCommand

# Third Party
from dateutil import parser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler.jobstores import register_job

from linka.models import TypRevizie
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

def delete_old_job_executions(max_age=604_800):
    """Deletes all apscheduler job execution logs older than `max_age`."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

def sendMail():
    mail_list = ['namova9094@pyrelle.com']  # , 'freyer.viktor@gmail.com']
    now = datetime.datetime.now()
    start = now + datetime.timedelta(days=27)
    end = now + datetime.timedelta(days=28)
    revizie = TypRevizie.objects.all().filter(datum_nadchadzajucej_revizie__gte=start,
                                              datum_nadchadzajucej_revizie__lte=end)

    print("pocet", revizie.count())
    if revizie.count() > 0:
        message = ""
        for revizia in revizie:
            message += f"Názov revízie: \"{revizia.nazov_revizie}\"\n" \
                       f"Typ revízie: \"{revizia.typ_revizie}\"\n" \
                       f"Dátum blížiacej sa revízie: " + revizia.datum_nadchadzajucej_revizie.strftime(
                "%d.%m.%Y") + "\n-------------------------------\n"
        print(message.strip())
        send_mail(
            'Blíži sa dátum revízie!',
            message.strip(),
            'noReplyRevizie@gmail.com',
            mail_list,
            fail_silently=False,
        )
    revizie = TypRevizie.objects.all().filter(datum_nadchadzajucej_revizie__gte=datetime.date.today(),
                                              datum_nadchadzajucej_revizie__lte=datetime.date.today() + datetime.timedelta(
                                                  days=1))

    print("pocet", revizie.count())
    if revizie.count() > 0:
        message = ""
        for revizia in revizie:
            message += f"Názov revízie: \"{revizia.nazov_revizie}\"\n" \
                       f"Typ revízie: \"{revizia.typ_revizie}\"\n" \
                       f"Dátum blížiacej sa revízie: " + revizia.datum_nadchadzajucej_revizie.strftime(
                "%d.%m.%Y") + "\n-------------------------------\n"

        print(message.strip())
        send_mail(
            'Prišiel stanovený dátum revízie!',
            message,
            'noReplyRevizie@gmail.com',
            mail_list,
            fail_silently=False,
        )

class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        sendMail()
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            sendMail,
            trigger="interval",
            days=1,
            id="Posielanie mailu",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Mail odoslaný.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
