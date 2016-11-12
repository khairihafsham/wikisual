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
            hourly = {hour: [] for hour in range(0, 24)}

            for item in service.get_top_titles_hourly_filtered():
                hourly[item['hour']].append(item)

            data = json.dumps({
                'charts': {
                    'hourly-top-titles': hourly
                }
            })

            self.stdout.write(data)

            Group('hourly-top-charts').send({
                "text": data
            })

            time.sleep(30)
