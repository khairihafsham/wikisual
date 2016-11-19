import json

from channels import Group

from wikiweb.services import ChartDataService


def ws_daily_top_charts_add(message):
    Group("daily-top-charts").add(message.reply_channel)


def ws_daily_top_charts_disconnect(message):
    Group("daily-top-charts").discard(message.reply_channel)


def ws_daily_top_charts_message(message):
    # TODO
    # need a command of sort, for example {'command': 'get_data'}
    service = ChartDataService()
    data = json.dumps(service.get_daily_top_chart_data())
    message.reply_channel.send({'text': data})


def ws_hourly_top_charts_add(message):
    Group("hourly-top-charts").add(message.reply_channel)


def ws_hourly_top_charts_disconnect(message):
    Group("hourly-top-charts").discard(message.reply_channel)


def ws_hourly_top_charts_message(message):
    # TODO
    # need a command of sort, for example {'command': 'get_data'}
    service = ChartDataService()
    data = json.dumps(service.get_hourly_top_chart_data())
    message.reply_channel.send({'text': data})
