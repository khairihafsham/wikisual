from typing import Union

from django.db.models import Count, F
from django.db import connection
import udatetime as datetime

from wikicollector.models import RecentChange
from wikicollector.utils import dictfetchall


class RecentChangeService(object):

    def get_top_field_by_date(self, field: str,
                                    date: Union[str, None]=None,
                                    top_count: int=10,
                                    return_query=False) -> list:
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

    def get_top_user_by_date_filtered(self,
                                      top_count: int=10,
                                      date: Union[str, None]=None) -> list:
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

    def get_top_countries_by_date(self,
                                  top_count: int=10,
                                  date: Union[str, None]=None) -> list:
        """
        get the top countries from RecentChange table for today
        today is in UTC timezone

        :return: list in format  of [{name: str, total: int}]
        """
        return self.get_top_field_by_date(field='country',
                                          date=date,
                                          top_count=top_count)

    def get_top_titles_by_date_filtered(self,
                                        top_count: int=10,
                                        date: Union[str, None]=None) -> list:
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
                                       top_count: int=3,
                                       date: Union[str, None]=None,
                                       start_hour: int=0,
                                       end_hour: int=23) -> list:
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
