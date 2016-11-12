from datetime import datetime

from django.test import TransactionTestCase

from wikicollector.services import RecentChangeService


class RecentChangeServiceTestCase(TransactionTestCase):
    fixtures = ['recentchange.json']

    def test_get_top_field_by_date_return_top_3_countries(self):
        service = RecentChangeService()
        expected = [
            {'name': 'United States', 'total': 64},
            {'name': 'United Kingdom', 'total': 25},
            {'name': 'Canada', 'total': 17}
        ]
        result = service.get_top_field_by_date(field='country',
                                               top_count=3,
                                               date='2016-10-24')
        self.assertEquals(expected, result)

    def test_get_top_field_by_date_return_empty_for_today(self):
        service = RecentChangeService()
        date = datetime.utcnow().date().isoformat()

        result = service.get_top_field_by_date(field='country',
                                               top_count=3,
                                               date=date)
        self.assertEquals([], result)

    def test_get_top_countries_by_date(self):
        service = RecentChangeService()
        expected = [
            {'name': 'United States', 'total': 64},
            {'name': 'United Kingdom', 'total': 25},
            {'name': 'Canada', 'total': 17}
        ]
        result = service.get_top_countries_by_date(date='2016-10-24',
                                                   top_count=3)

        self.assertEquals(expected, result)

    def test_get_top_titles_by_date(self):
        service = RecentChangeService()
        expected = [
            {'name': '2018 in film', 'total': 38},
            {'name': 'British Sand Ace Championship', 'total': 36},
            {'name': 'Nine Stones, Winterbourne Abbas', 'total': 33}
        ]
        result = service.get_top_titles_by_date_filtered(date='2016-10-23',
                                                         top_count=3)

        self.assertEquals(expected, result)

        result = service.get_top_titles_by_date_filtered(date='2016-10-24',
                                                         top_count=3)

        self.assertNotEquals(expected, result)

    def test_get_top_user_by_date_filtered(self):
        service = RecentChangeService()
        expected = [
            {'name': 'Serols', 'total': 29},
            {'name': '50.200.57.150', 'total': 24},
            {'name': 'ClueBot NG', 'total': 18}
        ]
        result = service.get_top_user_by_date_filtered(date='2016-10-24',
                                                       top_count=3)

        self.assertEquals(expected, result)

        result = service.get_top_titles_by_date_filtered(date='2016-10-23',
                                                         top_count=3)

        self.assertNotEquals(expected, result)

    def test_get_top_title_hourly_filtered(self):
        service = RecentChangeService()
        expected = [
            {"hour": 16, "name": "USS Hobson (DD-464)", "total": 22},
            {"hour": 16, "name": "Jimmy Perry", "total": 21},
            {"hour": 16, "name": "2018 in film", "total": 19},
            {"hour": 15, "name": "Jessica Drake", "total": 22},
            {"hour": 15, "name": "British Sand Ace Championship", "total": 21},
            {"hour": 15, "name": "List of Catholic saints", "total": 20}
        ]

        result = service.get_top_titles_hourly_filtered(date='2016-10-23',
                                                        top_count=3,
                                                        start_hour=15,
                                                        end_hour=16)

        self.assertEquals(expected, result)
