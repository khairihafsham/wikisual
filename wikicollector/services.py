from django.db.models import Count, F

from wikicollector.models import RecentChange

import udatetime as datetime


class RecentChangeService(object):

    def get_top_field_by_date(self, field: str,
                                    date: str=datetime.utcnow()
                                                      .date()
                                                      .isoformat(),
                                    top_count: int = 10,
                                    return_query=False) -> list:
        """
        a generic method to get top counts for any particular field from the
        table RecentChange

        :return: list in format  of [{field: str, total: int}]
        """
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
                                      top_count: int = 10,
                                      date: str=datetime
                                        .utcnow()
                                        .date()
                                        .isoformat()) -> list:
        """
        get the top users who made changes in RecentChange table for today
        today is in UTC timezone

        :return: list in format  of [{user: str, total: int}]
        """
        query = self.get_top_field_by_date(field='user',
                                           date=date,
                                           top_count=top_count,
                                           return_query=True)
        query = query.filter(bot=False)

        return [i for i in query[:top_count]]

    def get_top_countries_by_date(self,
                                  top_count: int = 10,
                                  date: str=datetime
                                      .utcnow()
                                      .date()
                                      .isoformat()) -> list:
        """
        get the top countries from RecentChange table for today
        today is in UTC timezone

        :return: list in format  of [{country: str, total: int}]
        """
        return self.get_top_field_by_date(field='country',
                                          date=date,
                                          top_count=top_count)

    def get_top_titles_by_date_filtered(self,
                                        top_count: int = 10,
                                        date: str=datetime
                                            .utcnow()
                                            .date()
                                            .isoformat()) -> list:
        """
        get the top edits in RecentChange table for today
        today is in UTC timezone

        :return: list in format  of [{title: str, total: int}]
        """
        query = self.get_top_field_by_date(field='title',
                                           top_count=top_count,
                                           date=date,
                                           return_query=True)
        query = query.filter(type='edit') \
            .exclude(title__startswith='Wikipedia:') \
            .exclude(title__startswith='User:')

        return [i for i in query[:top_count]]
