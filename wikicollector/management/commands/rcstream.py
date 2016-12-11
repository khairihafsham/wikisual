from django.core.management.base import BaseCommand

import socketIO_client

from wikicollector.services import RecentChangeService


class Command(BaseCommand):
    help = "Subscribe to Wikipedia's recent change stream"

    def handle(self, *args, **options):
        socketIO = socketIO_client.SocketIO('https://stream.wikimedia.org')
        socketIO.define(WikiNamespace, '/rc')
        socketIO.wait()


class WikiNamespace(socketIO_client.BaseNamespace):
    def initialize(self):
        self.recent_change_service = RecentChangeService()

    def on_change(self, change):
        self.recent_change_service.save_recent_change(change)

    def on_connect(self):
        self.emit('subscribe', 'en.wikipedia.org')

    def on_reconnect(self):
        self.emit('subscribe', 'en.wikipedia.org')

    def on_error(self):
        # FIXME
        # need to handle this, there are times when the response/handshake
        # fails
        pass
