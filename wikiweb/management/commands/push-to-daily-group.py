import json
import time

from django.core.management.base import BaseCommand
from channels import Group

from wikiweb.services import ChartDataService


class Command(BaseCommand):
    help = "Get data from RecentChangeService and push it to the group"

    def handle(self, *args, **options):
        service = ChartDataService()

        while True:
            data = json.dumps(service.get_daily_top_chart_data())
            Group('daily-top-charts').send({"text": data})
            time.sleep(30)
