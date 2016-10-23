from django.db.models import Count, F

from wikicollector.models import RecentChange

import udatetime as datetime


class RecentChangeService(object):

    def get_daily_top_field(self,
                                field: str,
                                top_count: int = 10,
                                return_query=False) -> list:
        """
        a generic method to get top counts for any particular field from the
        table RecentChange

        :return: list in format  of [{field: str, total: int}]
        """
        today = datetime.utcnow().date().isoformat()
        exclude = {field: ''}

        query = RecentChange.objects.all() \
            .annotate(name=F(field)) \
            .values('name') \
            .annotate(total=Count(field)) \
            .filter(timestamp__range=('%sT00:00:00Z' % today,
                                      '%sT23:59:59Z' % today)) \
            .exclude(**exclude) \
            .order_by('-total')

        if return_query:
            return query

        return [i for i in query[:top_count]]

    def get_daily_top_users(self, top_count: int = 10) -> list:
        """
        get the top users who made changes in RecentChange table for today
        today is in UTC timezone

        :return: list in format  of [{user: str, total: int}]
        """
        return self.get_daily_top_field('user', top_count)

    def get_daily_top_countries(self, top_count: int = 10) -> list:
        """
        get the top countries from RecentChange table for today
        today is in UTC timezone

        :return: list in format  of [{country: str, total: int}]
        """
        return self.get_daily_top_field('country', top_count)

    def get_daily_top_titles_filtered(self, top_count: int = 10) -> list:
        """
        get the top edits in RecentChange table for today
        today is in UTC timezone

        :return: list in format  of [{title: str, total: int}]
        """
        query = self.get_daily_top_field('title', top_count, True)
        query = query.filter(type='edit') \
            .exclude(title__startswith='Wikipedia:') \
            .exclude(title__startswith='User:')

        return [i for i in query[:top_count]]
