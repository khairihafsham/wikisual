from ipaddress import ip_address
import json
import time

from django.core.management.base import BaseCommand

import socketIO_client
import geoip2.database
from geoip2.errors import AddressNotFoundError
from udatetime import fromtimestamp, TZFixedOffset

from wikicollector.models import RecentChange


class Command(BaseCommand):
    help = "Subscribe to Wikipedia's recent change stream"

    def handle(self, *args, **options):
        socketIO = socketIO_client.SocketIO(
            'https://stream.wikimedia.org'
        )
        socketIO.define(WikiNamespace, '/rc')

        socketIO.wait()


class WikiNamespace(socketIO_client.BaseNamespace):
    def initialize(self):
        # FIXME move path out of here, shouldn't be hardcoded
        self.geo_reader = geoip2.database.Reader(
            '/opt/wikisual/geodb/GeoLite2-City.mmdb'
        )

    def on_change(self, change):
        country = city = ''

        try:
            ip_address(change.get('user'))
            result = self.geo_reader.city(change.get('user'))
            city = result.city.name
            country = result.country.name
        except (ValueError, AddressNotFoundError) as e:
            pass

        dt = fromtimestamp(change.get('timestamp', time.time()),
                           TZFixedOffset(0))

        data = {
            "title": change.get('title'),
            "country": country,
            "city": city,
            "user": change.get('user', ''),
            "bot": change.get('bot', False),
            "type": change.get('type', 'Unknown'),
            "timestamp": dt.isoformat()
        }

        rc = RecentChange(**data)
        rc.save()

        print(json.dumps(data))

    def on_connect(self):
        self.emit('subscribe', 'en.wikipedia.org')

    def on_reconnect(self):
        self.emit('subscribe', 'en.wikipedia.org')

    def on_error(self):
        # FIXME
        # need to handle this, there are times when the response/handshake
        # fails
        pass
