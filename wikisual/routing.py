from channels.routing import route
from wikiweb.consumers import (ws_daily_top_charts_add,
                               ws_daily_top_charts_disconnect)

channel_routing = [
    route("websocket.connect",
          ws_daily_top_charts_add,
          path='^/daily-top-charts/?$'),
    route("websocket.disconnect",
          ws_daily_top_charts_disconnect,
          path='^/daily-top-charts/?$')
]
