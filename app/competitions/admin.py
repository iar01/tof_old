from django.contrib import admin
from competitions.models import Competition, Category
from feeds.models import Feed,Photo
import requests
from decimal import getcontext, Decimal
#admin.site.register(Competition)
admin.site.register(Category)
base_url = 'https://graph.facebook.com/v2.5/'
token = 'CAAB44AexpRABAI95BYZAN4Ap8jR6ZBZA5EyiftgtmckZAlEL67ZAWDLqL0vbpobQebJn2Edlj3UkHLGkOnX0XynnPJfduENhJlrZBrm' \
        'OvcoZAUM6hYBmQJZBtjLGG0YzAsZBoouhpb8nJx5WLAJYDtOmvHp9GG7U2GAUJdJkBN3VPUVq8pB2ZAK6ZAYKAvS7OmGlxCXhvOlYP7fBQZDZD'


class Feedadmin(admin.StackedInline):
    model = Feed
    fields = ( 'competition','image_tag','judge_points','user','date','post','parent','likes','comments','share_points','video_url', 'audience_points', 'total_points' )
    readonly_fields = ('competition','image_tag','user','date','post','parent','likes','comments','share_points','video_url', 'audience_points', 'total_points')


def update_status_y(modeladmin, request, queryset):
    getcontext().prec = 4
    for obj in queryset:
        for feed in obj.feed_set.all():
            response = requests.get(base_url + "?id=http://theonlinefest.com/feeds/"+str(feed.id)+"/", params={'access_token': token})
            feed_sharecount= response.json()['share']['share_count']
            feed.share_points = feed_sharecount
            feed.save()
        feed_list = obj.feed_set.all()
        points = [feed.likes*10+feed.share_points*30 for feed in feed_list]
        N =len(points)
        i=0
            #for user_score in points:
            #    S= len([i for i in points if i < user_score]) # no. of shares that are below it when sorted in ascending order
            #    F= len([i for i in points if i == user_score])# frequency of the shares
            #    P = float(((float(S) + float(F/2))/N)*100)
            #    final_score = ((P/100)*35)+5
            #    score.append(final_score)
        j=0
        for feed in feed_list:
            S= len([i for i in points if i < points[j]]) # no. of shares that are below it when sorted in ascending order
            F= len([i for i in points if i == points[j]])# frequency of the shares
            P = Decimal(((Decimal(S) + Decimal(F/2))/N)*100)
            feed.audience_points = Decimal(((P/100)*35)+5)
            feed.total_points = Decimal(feed.audience_points + feed.judge_points)
            feed.save()
            j+=1

    queryset.update(status='y')
update_status_y.short_description = "mark them as calculated"

def update_status_n(modeladmin, request, queryset):
    queryset.update(status='n')
update_status_n.short_description = "mark them as not calculated"

class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['title', 'result_declaration_date','status']
    ordering = ['title']
    actions = [update_status_y,update_status_n]
    inlines = [Feedadmin]

admin.site.register(Competition, CompetitionAdmin)
