import datetime

from django.conf import settings
from django.core.management.base import BaseCommand

from tokens.models import Token


class Command(BaseCommand):
    help = 'Deletes all expired tokens. The token expiry time is determined by' \
           'settings.CHATSECURE_PUSH[\'DEFAULT_TOKEN_EXPIRY_TIME_S\']'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run',
            action='store_true',
            dest='dry_run',
            default=False,
            help='Count how many tokens are expired, but do not delete')

    def handle(self, *args, **options):

        now = datetime.datetime.now()
        expiry_timedelta = datetime.timedelta(seconds=settings.CHATSECURE_PUSH['DEFAULT_TOKEN_EXPIRY_TIME_S'])
        earliest_created_date = now - expiry_timedelta  # A token created_date before this is expired

        self.stdout.write(self.style.SUCCESS("Tokens created before %s are expired" % earliest_created_date))

        expired_tokens = Token.objects.filter(date_created__lte=earliest_created_date)

        self.stdout.write(self.style.SUCCESS("%d / %d tokens are expired" % (expired_tokens.count(), Token.objects.all().count())))

        if not options['dry_run']:
            expired_tokens.delete()
