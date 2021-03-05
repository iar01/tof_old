from django.db import models
from django.conf import settings
from datetime import datetime,timedelta
from django.contrib.auth.models import User
from django.db.models import Max
from feeds.models import Feed
import operator
import requests


class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    def get_open_competitions(self):
        return self.competition_set.filter(start_date__lte=datetime.today().date(),
                                           finish_date__gte=datetime.today().date())

    def get_upcoming_competitions(self):
        return self.competition_set.filter(start_date__gt=datetime.today().date())

    def get_past_competitions(self):
        return self.competition_set.filter(finish_date__lt=datetime.today().date())


class Competition(models.Model):
    TYPES = (
        ('txt', 'Text'),
        ('img', 'Image'),
        ('vid', 'Video'),
    )
    STATUS_CHOICES = (
    ('n', 'not calculated'),
    ('y', 'calculated'),
)
    title = models.CharField(max_length=200)
    theme = models.CharField(max_length=200, null=True, blank=True)
    cash_prize = models.TextField(null=True, blank=True)
    scoring_criteria = models.TextField(null=True, blank=True)
    rulez = models.TextField(null=True, blank=True)
    judge = models.ForeignKey(User, null=True, blank=True)
    judge_about = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=5, choices=TYPES, default='txt')
    category = models.ForeignKey('competitions.Category')
    start_date = models.DateField(default=datetime.now)
    finish_upload_date = models.DateField(default=datetime.now)
    finish_date = models.DateField(default=datetime.now)
    result_declaration_date = models.DateField(default=datetime.now)
    status = models.CharField(max_length=1, default='n', choices=STATUS_CHOICES)

    def __str__(self):
        return self.title

    def upload_is_active(self):
        if self.start_date <= datetime.today().date() and self.finish_upload_date >= datetime.today().date():
            return True
        return False

    def is_active(self):
        if self.start_date <= datetime.today().date() and self.finish_date >= datetime.today().date():
            return True
        return False

    def is_result_declaration_date(self):
        if self.result_declaration_date <= datetime.today().date():
            return True
        return False

    def competition_result(self):
        feed_dict_list = list()
        try:
            for feed in self.feed_set.all():
                feed_dict = dict()
                feed_dict['feed'] = feed
                feed_dict['total_points'] = feed.total_points
                feed_dict['audience_points'] = feed.audience_points
                feed_dict['judges_points'] = feed.judge_points
                feed_dict_list.append(feed_dict)

            sorted_feed_dict_list = sorted(feed_dict_list, key=operator.itemgetter('total_points'))[::-1]
            template_context = {
            'competition': self,
            'winner_feed':sorted_feed_dict_list[0],
            'feed_dict_list':sorted_feed_dict_list[1:],
             }
            return template_context
        except:
            return None

    def get_score(self):
        likes = [feed.likes for feed in self.feed_set.all()]
        try:
            return Feed.objects.filter(likes=max(likes))[0]
        except ValueError:
            return None