from wikicollector.services import RecentChangeService


class ChartDataService(object):
    def __init__(self):
        self.recentchange_service = RecentChangeService()

    def get_daily_top_chart_data(self):
        return {
            'charts': {
                'daily-top-countries':
                    self.recentchange_service.get_top_countries_by_date(),
                'daily-top-titles':
                    self.recentchange_service.get_top_titles_by_date_filtered()
            }
        }

    def get_hourly_top_chart_data(self):
        hourly = {hour: [] for hour in range(0, 24)}

        for item in self.recentchange_service.get_top_titles_hourly_filtered():
            hourly[item['hour']].append(item)

        return {
            'charts': {
                'hourly-top-titles': hourly
            }
        }
