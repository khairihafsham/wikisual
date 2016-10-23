from channels import Group


def ws_daily_top_charts_add(message):
    Group("daily-top-charts").add(message.reply_channel)


def ws_daily_top_charts_disconnect(message):
    Group("daily-top-charts").discard(message.reply_channel)
