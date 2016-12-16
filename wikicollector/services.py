from ipaddress import ip_address
from collections import namedtuple

import udatetime as datetime
import geoip2.database
from geoip2.errors import AddressNotFoundError

from django.db.models import Count, F
from django.db import connection
from django.conf import settings

from wikicollector.models import RecentChange
from wikicollector.utils import dictfetchall

GeoData = namedtuple('GeoData', ['city', 'country'])


class GeoService(object):
    """
    just a wrapper class for geoip2 to help load the database and hide the
    internal for getting the geo data from ip address
    """
    def __init__(self, config):
        """
        :config: object preferable the one from django.conf.settings
        """
        self._geo_reader = None
        self.database_path = config.GEOSERVICE.get('DATABASE_PATH')

    @property
    def reader(self):
        """
        if _geo_reader is None, create an instance of geoip2.database.Reader
        and assign to _geo_reader

        :returns: instance of geoip2.database.Reader
        """
        if self._geo_reader is None:
            self._geo_reader = geoip2.database.Reader(self.database_path)

        return self._geo_reader

    def translate_ip(self, ip):
        """
        for a given ip address this method will try to return the corresponding
        country and city.

        internally, it handles AddressNotFoundError from geoip2 and ValueError
        from ipadress.ip_address and will return an empty GeoData when either
        of those two is raised

        :ip: string ip compliant
        :returns: GeoData
        """
        try:
            ip_address(ip)
            result = self.reader.city(ip)
            return GeoData(city=result.city.name, country=result.country.name)
        except (ValueError, AddressNotFoundError) as e:
            return GeoData(city='', country='')


class RecentChangeService(object):
    def __init__(self):
        self._geo_service = None

    @property
    def geo_service(self):
        if self._geo_service is None:
            self._geo_service = GeoService(settings)

        return self._geo_service

    def get_top_field_by_date(self, field,
                                    date=None,
                                    top_count=10,
                                    return_query=False):
        """
        a generic method to get top counts for any particular field from the
        table RecentChange

        :return: list in format  of [{name: str, total: int}]
        """
        if date is None:
            date = datetime.utcnow().date().isoformat()

        exclude = {field: ''}

        query = RecentChange.objects.all() \
            .annotate(name=F(field)) \
            .values('name') \
            .annotate(total=Count(field)) \
            .filter(timestamp__range=('%sT00:00:00Z' % date,
                                      '%sT23:59:59Z' % date)) \
            .exclude(**exclude) \
            .order_by('-total')

        if return_query:
            return query

        return [i for i in query[:top_count]]

    def get_top_user_by_date_filtered(self, top_count=10, date=None):
        """
        get the top users who made changes in RecentChange table for today
        today is in UTC timezone

        :return: list in format  of [{name: str, total: int}]
        """
        query = self.get_top_field_by_date(field='user',
                                           date=date,
                                           top_count=top_count,
                                           return_query=True)
        query = query.filter(bot=False)

        return [i for i in query[:top_count]]

    def get_top_countries_by_date(self, top_count=10, date=None):
        """
        get the top countries from RecentChange table for today
        today is in UTC timezone

        :return: list in format  of [{name: str, total: int}]
        """
        return self.get_top_field_by_date(field='country',
                                          date=date,
                                          top_count=top_count)

    def get_top_titles_by_date_filtered(self, top_count=10, date=None):
        """
        get the top edits in RecentChange table for today
        today is in UTC timezone

        :return: list in format  of [{name: str, total: int}]
        """
        query = self.get_top_field_by_date(field='title',
                                           top_count=top_count,
                                           date=date,
                                           return_query=True)
        query = query.filter(type='edit') \
            .exclude(title__startswith='Wikipedia:') \
            .exclude(title__startswith='User:')

        return [i for i in query[:top_count]]

    def get_top_titles_hourly_filtered(self,
                                       top_count=10,
                                       date=None,
                                       start_hour=0,
                                       end_hour=23):
        """
        query the RecentChange.table
        :returns: [{hour: hour, name: title, total: total}, ..]
        """
        # NOTE
        # seems like a good place to use sqlalchemy, but this is blasphemous
        # but I like composable SQL. Right now, I have to write a new one for
        # each different field
        cursor = connection.cursor()
        sql = """
select t.hour, t2.title as name, t2.total from (
    select generate_series({start_hour}, {end_hour}) as hour
) t
join lateral (
    select title, count(*) total from {table}
    where timestamp between '{date} 00:00:00' and '{date} 23:59:59'
    and extract(hour from timestamp)=t.hour
    and title not like all(array[
        'Category:%',
        'Wikipedia:%',
        'User:%',
        'Special:%'
    ])
    group by title
    order by total desc
    limit {top_count}
) t2 on true
order by hour desc, total desc;
"""
        if date is None:
            date = datetime.utcnow().date().isoformat()

        sql = sql.format(
            top_count=top_count,
            start_hour=start_hour,
            end_hour=end_hour,
            date=date,
            table=RecentChange._meta.db_table
        )

        cursor.execute(sql)

        return dictfetchall(cursor)

    def save_recent_change(self, data):
        """
        receives data as dict. expected data structure to match the one from
        Wikipedia's RecentChange stream API.

        sometimes 'user' is an ip_address, translate it to city and country
        whenever possible

        converts 'timestamp' into Datetime in UTC timezone

        saves all those data into database via RecentChange model

        :data: dict
        """
        geo_data = self.geo_service.translate_ip(data['user'])

        dt = datetime.fromtimestamp(data['timestamp'],
                                    datetime.TZFixedOffset(0))

        params = {
            "title": data['title'],
            "country": geo_data.country,
            "city": geo_data.city,
            "user": data['user'],
            "bot": data['bot'],
            "type": data['type'],
            "timestamp": dt.isoformat()
        }

        rc = RecentChange(**params)
        rc.save()
