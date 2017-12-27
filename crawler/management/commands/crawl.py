from django.core.management.base import BaseCommand, CommandError
from crawler.models import *
import json
import datetime

class Command(BaseCommand):
    help = 'Usage example:  python manage.py crawl [max]'

    def add_arguments(self, parser):
        parser.add_argument('max', type=int)

        parser.add_argument(
            '--words_greater',
            dest='words_greater',
            help='Filter titles with number of words greater than',
        )

        parser.add_argument(
            '--words_less',
            dest='words_less',
            help='Filter titles with number of words less than',
        )

        parser.add_argument(
            '--order',
            dest='order',
            help='Order criteria [points, comments]',
        )

    def handle(self, *args, **options):
        """
        Execute crawl
        """
        crawl = Crawl.objects.create()
        if options["max"]:
            crawl.perform_crawl(options["max"])
        else:
            crawl.perform_crawl(30)

        # Filtering
        if options["words_greater"] and options["order"]:
            entries = crawl.filter(words_greater=5, order=options["order"])
        elif options["words_less"] and options["order"]:
            entries = crawl.filter(words_less=5, order=options["order"])
        else:
            entries = crawl.entries.all()
            
        dictionaries = [ entry.as_dict() for entry in entries ]
        output = json.dumps(dictionaries, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))

        self.stdout.write('===================================================')
        self.stdout.write(output)
        self.stdout.write('===================================================')
        self.stdout.write('Completed!')
        crawl.delete()
