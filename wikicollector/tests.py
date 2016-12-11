from datetime import datetime
from unittest.mock import patch, MagicMock

from django.test import TransactionTestCase, TestCase
from django.conf import settings

from geoip2.database import Reader
from geoip2.errors import AddressNotFoundError

from wikicollector.services import RecentChangeService, GeoService, GeoData
from wikicollector import services


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


class GeoServiceTest(TestCase):
    @patch('geoip2.database.Reader', spec=Reader)
    def test_reader_instanceof_geoip_reader(self, MockReader):
        geo = GeoService(settings)
        self.assertIsInstance(geo.reader, Reader)

    @patch('geoip2.database.Reader', spec=Reader)
    @patch('ipaddress.ip_address')
    def test_translate_ip_returns_empty_geodata_on_valueerror(
            self,
            mock_ip_address,
            MockReader):
        mock_ip_address.side_effect = ValueError()
        geo = GeoService(settings)
        geodata = GeoData(city='', country='')
        self.assertEquals(geo.translate_ip('notIP'), geodata)

    @patch('geoip2.database.Reader')
    def test_translate_ip_returns_empty_geodata_on_addressnotfounderror(
            self,
            MockReader):
        MockReader.side_effect = AddressNotFoundError()
        geo = GeoService(settings)
        geodata = GeoData(city='', country='')
        self.assertEquals(geo.translate_ip('127.0.0.1'), geodata)

    def test_translate_ip_returns_complete_geodata(self):
        city = MagicMock()
        city.city.name = 'Kuala Lumpur'
        city.country.name = 'Malaysia'
        reader = MagicMock()
        reader.city = MagicMock(return_value=city)
        MockReader = MagicMock(return_value=reader)

        with patch('geoip2.database.Reader', new=MockReader):
            geo = services.GeoService(settings)
            geodata = GeoData(city='Kuala Lumpur', country='Malaysia')
            result = geo.translate_ip('127.0.0.1')
            self.assertEquals(result, geodata)
