import json
import time

from django.core.management.base import BaseCommand
from channels import Group

from wikicollector.services import RecentChangeService


class Command(BaseCommand):
    help = "Get data from RecentChangeService and push it to the group"

    def handle(self, *args, **options):
        service = RecentChangeService()

        while True:
            data = json.dumps({
                'charts': {
                    'daily-top-countries': service.get_top_countries_by_date(),
                    'daily-top-titles':
                        service.get_top_titles_by_date_filtered()
                }
            })

            self.stdout.write(data)

            Group('daily-top-charts').send({
                "text": data
            })

            time.sleep(5)
