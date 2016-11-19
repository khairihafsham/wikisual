from unittest.mock import MagicMock

from django.test import TestCase

from wikiweb.services import ChartDataService

from wikicollector.services import RecentChangeService


class ChartDataServiceTestCase(TestCase):

    def test_get_daily_top_chart_data(self):
        rc_service = RecentChangeService()
        service = ChartDataService()
        data = [{'test': 'value'}]
        expected = {
            'charts': {
                'daily-top-countries': data,
                'daily-top-titles': data
            }
        }
        rc_service.get_top_countries_by_date = MagicMock(return_value=data)
        rc_service.get_top_titles_by_date_filtered = \
            MagicMock(return_value=data)
        service.recentchange_service = rc_service

        self.assertEquals(expected, service.get_daily_top_chart_data())

    def test_get_hourly_top_chart_data(self):
        rc_service = RecentChangeService()
        service = ChartDataService()
        data = [{'hour': 1, 'name': 'test'}]
        expected = {
            'charts': {
                'hourly-top-titles': {
                    0: [], 1: data,
                    2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [],
                    10: [], 11: [], 12: [], 13: [], 14: [], 15: [], 16: [],
                    17: [], 18: [], 19: [], 20: [], 21: [], 22: [], 23: [],
                }
            }
        }
        rc_service.get_top_titles_hourly_filtered = \
            MagicMock(return_value=data)
        service.recentchange_service = rc_service

        self.assertEquals(expected, service.get_hourly_top_chart_data())
