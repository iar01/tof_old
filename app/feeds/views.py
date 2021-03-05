from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from core.decorators import ajax_required

from feeds.models import Feed, Photo
from activities.models import Activity, Notification
import hashlib
import json

import time
import datetime

from django.views.decorators.csrf import csrf_exempt
from cloudinary.forms import cl_init_js_callbacks
from .forms import PhotoDirectForm
from django.core.files.storage import default_storage

import cloudinary
import cloudinary.uploader
import cloudinary.api

from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess
from azure.storage.blob import ContentSettings


import facebook

myaccount='tofim'
mykey='5jb1QMcmwb0BYFPeJwfXpw6afn27MXw6MH37BWHSxRYUfWwwaVQK7DzGEN1ygCkxFti20sDGjWUg2pFH3HVHCQ=='


FEEDS_NUM_PAGES = 10


def upload_prompt(request):
    context = dict(direct_form=PhotoDirectForm())

    cl_init_js_callbacks(context['direct_form'], request)
    return render(request, 'upload_prompt.html', context)


@csrf_exempt
def direct_upload_complete(request):
    form = PhotoDirectForm(request.POST)

    if form.is_valid():
        form.save()
        ret = dict(photo_id=form.instance.id)
    else:
        ret = dict(errors=form.errors)
    """
    last_feed = request.POST.get('last_feed')
    user = request.user
    csrf_token = unicode(csrf(request)['csrf_token'])
    feed = Feed()
    feed.user = user
    feed.photo_id = form.instance.id
    post = request.POST['post']
    post = post.strip()
    if len(post) > 0:
          feed.post = post[:255]
          feed.save()
    html = _html_feeds(last_feed, user, csrf_token)
    return HttpResponse(html)
    """
    return HttpResponse(json.dumps(ret), content_type='application/json')


def filter_nones(d):
    return dict((k, v) for k, v in d.iteritems() if v is not None)


def list(request):
    defaults = dict(format="jpg", height=150, width=150)
    defaults["class"] = "thumbnail inline"

    # The different transformations to present
    samples = [
        dict(crop="fill", radius=10),
        dict(crop="scale"),
        dict(crop="fit", format="png"),
        dict(crop="thumb", gravity="face"),
        dict(format="png", angle=20, height=None, width=None, transformation=[
            dict(crop="fill", gravity="north", width=150, height=150, effect="sepia"),
        ]),
    ]
    samples = [filter_nones(dict(defaults, **sample)) for sample in samples]
    return render(request, 'feeds/list.html', dict(photos=Photo.objects.all(), samples=samples))


@login_required
def feeds(request):
    all_feeds = Feed.get_feeds()
    paginator = Paginator(all_feeds, FEEDS_NUM_PAGES)
    feeds = paginator.page(1)
    from_feed = -1
    if feeds:
        from_feed = feeds[0].id
    return render(request, 'feeds/feeds.html', {
        'feeds': feeds,
        'from_feed': from_feed,
        'page': 1,
    })

@login_required
def feed(request, pk):
    feed = get_object_or_404(Feed, pk=pk)
    return render(request, 'feeds/feed.html', {'feed': feed})


@login_required
@ajax_required
def load(request):
    from_feed = request.GET.get('from_feed')
    page = request.GET.get('page')
    feed_source = request.GET.get('feed_source')
    all_feeds = Feed.get_feeds(from_feed)
    if feed_source != 'all':
        all_feeds = all_feeds.filter(user__id=feed_source)
    paginator = Paginator(all_feeds, FEEDS_NUM_PAGES)
    try:
        feeds = paginator.page(page)
    except PageNotAnInteger:
        return HttpResponseBadRequest()
    except EmptyPage:
        feeds = []
    html = u''
    csrf_token = csrf(request)['csrf_token']
    for feed in feeds:
        html = u'{0}{1}'.format(html, render_to_string('feeds/partial_feed.html', {
            'feed': feed,
            'user': request.user,
            'csrf_token': csrf_token
        })
                                )
    return HttpResponse(html)


def _html_feeds(last_feed, user, csrf_token, feed_source='all'):
    feeds = Feed.get_feeds_after(last_feed)
    if feed_source != 'all':
        feeds = feeds.filter(user__id=feed_source)
    html = u''
    for feed in feeds:
        html = u'{0}{1}'.format(html, render_to_string('feeds/partial_feed.html', {
            'feed': feed,
            'user': user,
            'csrf_token': csrf_token
        })
                                )
    return html


@login_required
@ajax_required
def load_new(request):
    last_feed = request.GET.get('last_feed')
    user = request.user
    csrf_token = csrf(request)['csrf_token']
    html = _html_feeds(last_feed, user, csrf_token)
    return HttpResponse(html)


@login_required
@ajax_required
def check(request):
    last_feed = request.GET.get('last_feed')
    feed_source = request.GET.get('feed_source')
    feeds = Feed.get_feeds_after(last_feed)
    if feed_source != 'all':
        feeds = feeds.filter(user__id=feed_source)
    count = feeds.count()
    return HttpResponse(count)


@login_required
@ajax_required
def post(request):
    last_feed = request.POST.get('last_feed')
    user = request.user
    csrf_token = csrf(request)['csrf_token']
    feed = Feed()
    feed.user = user
    post = request.POST['post']
    feed.image_url = request.POST['image']
    post = post.strip()
    if len(post) > 0:
        feed.post = post[:255]
        feed.save()
    html = _html_feeds(last_feed, user, csrf_token)
    return HttpResponse(html)

# token = '1686173174962992|U4k7m1sRpuarWId4YjNlG6mZ3cs'
# @login_required
# @ajax_required
# def post_fb(request, token):
#     graph = facebook.GraphAPI(access_token=token, version='2.2')
#     csrf_token = csrf(request)['csrf_token']
#     post = request.POST['post']
#     feed.image_url = request.POST['image']
#     graph.put_object(parent_object='1730444227192679', connection_name='feed',
#                      message='Hello, world')
#     return None
token = '132903597090064|QISpcDn-MG5K-8lySCgUsoK745k'
@login_required
@ajax_required
def post_fb(request):
    graph = facebook.GraphAPI(access_token="CAAB44AexpRABAI95BYZAN4Ap8jR6ZBZA5EyiftgtmckZAlEL67ZAWDLqL0vbpobQebJn2Edlj3UkHLGkOnX0XynnPJfduENhJlrZBrmOvcoZAUM6hYBmQJZBtjLGG0YzAsZBoouhpb8nJx5WLAJYDtOmvHp9GG7U2GAUJdJkBN3VPUVq8pB2ZAK6ZAYKAvS7OmGlxCXhvOlYP7fBQZDZD")
    
    post = request.POST['post']
    image_url = request.POST['image']
    attachment = {
        'name': post,
        'link': 'http://theonlinefest.com/',
        'caption': 'Check out this image',
        'description': 'description',
        'picture': image_url,
    }
    # graph.put_wall_post(profile_id=1730444227192679, message='Check this out...', attachment=attachment)
    # graph.put_object(parent_object='me', connection_name='feed',
    #             message='sdfgsdfgsdfg')
    return HttpResponse()


@login_required
@ajax_required
def like(request):
    feed_id = request.POST['feed']
    feed = Feed.objects.get(pk=feed_id)
    user = request.user
    like = Activity.objects.filter(activity_type=Activity.LIKE, feed=feed_id, user=user)
    if like:
        user.profile.unotify_liked(feed)
        like.delete()
    else:
        like = Activity(activity_type=Activity.LIKE, feed=feed_id, user=user)
        like.save()
        user.profile.notify_liked(feed)
    return HttpResponse(feed.calculate_likes())


@login_required
@ajax_required
def comment(request):
    if request.method == 'POST':
        feed_id = request.POST['feed']
        feed = Feed.objects.get(pk=feed_id)
        post = request.POST['post']
        post = post.strip()
        if len(post) > 0:
            post = post[:255]
            user = request.user
            feed.comment(user=user, post=post)
            user.profile.notify_commented(feed)
            user.profile.notify_also_commented(feed)
        return render(request, 'feeds/partial_feed_comments.html', {'feed': feed})
    else:
        feed_id = request.GET.get('feed')
        feed = Feed.objects.get(pk=feed_id)
        return render(request, 'feeds/partial_feed_comments.html', {'feed': feed})


@login_required
@ajax_required
def update(request):
    first_feed = request.GET.get('first_feed')
    last_feed = request.GET.get('last_feed')
    feed_source = request.GET.get('feed_source')
    feeds = Feed.get_feeds().filter(id__range=(last_feed, first_feed))
    if feed_source != 'all':
        feeds = feeds.filter(user__id=feed_source)
    dump = {}
    for feed in feeds:
        dump[feed.pk] = {'likes': feed.likes, 'comments': feed.comments}
    data = json.dumps(dump)
    return HttpResponse(data, content_type='application/json')


@login_required
@ajax_required
def track_comments(request):
    feed_id = request.GET.get('feed')
    feed = Feed.objects.get(pk=feed_id)
    return render(request, 'feeds/partial_feed_comments.html', {'feed': feed})


@login_required
@ajax_required
def remove(request):
    try:
        feed_id = request.POST.get('feed')
        feed = Feed.objects.get(pk=feed_id)
        if feed.user == request.user:
            likes = feed.get_likes()
            parent = feed.parent
            for like in likes:
                like.delete()
            feed.delete()
            if parent:
                parent.calculate_comments()
            return HttpResponse()
        else:
            return HttpResponseForbidden()
    except Exception:
        return HttpResponseBadRequest()

def encode(key, string):
    encoded_chars = []
    for i in xrange(string):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = "".join(encoded_chars)
    return base64.urlsafe_b64encode(encoded_string)

@login_required
@ajax_required
def upload_image(request):
    #cld_res = cloudinary.uploader.upload(
    #        request.FILES['files'],
    #)

    ## above cloudinary part is commented out

    #.......................................BLOB image handling....................................................

    try :
        user_name = request.user.username
    except :
        user_name='default'
        pass
    tempfile= request.FILES['files']

    block_blob_service = BlockBlobService(account_name=myaccount, account_key=mykey)
    block_blob_service.create_container('feedimagestest', public_access=PublicAccess.Container)
    block_blob_service.set_container_acl('feedimagestest', public_access=PublicAccess.Container)

    with open('t.png','wb+') as formfile:           ##intermediate file used for uploading contents to blob
        for chunk in tempfile.chunks():
            formfile.write(chunk)

    temp_name = str(request.FILES['files'])
    ext_name = temp_name[(temp_name.rfind('.')):]
    blob_name = (user_name+'_'+time.strftime("%Y-%m-%d-%H:%M")).encode('utf-8')
    blob_name = hashlib.sha1(blob_name).hexdigest()+ext_name
    block_blob_service.create_blob_from_path(
        'feedimagestest',                   ##container
        blob_name,                          ##blob name
        't.png',                            ##temporary file from where the content is picked for uploading
        content_settings=ContentSettings(content_type='image')   ##type of the file to be uploaded
        )

    image_url = 'https://tofimcdn.azureedge.net/feedimagestest/'+ blob_name

    #...................................END of Blob image handling................................................

    data = json.dumps({'src': image_url })        ##url of the image stored on the blob

    #data = json.dumps({'src': cld_res['url'],})  ##cloudinary url that is not required in case of azure data blob

    return HttpResponse(data, content_type='application/json')


@login_required
@ajax_required
def upload_video(request):
    file_obj = request.FILES.get('files')
    filename = '{}_{}'.format(time.time(), file_obj.name)
    with open(default_storage.path('video/' + filename), 'wb+') as destination:
        for chunk in file_obj.chunks():
            destination.write(chunk)
    data = json.dumps({'src': 'video/%s' % filename })
    return HttpResponse(data, content_type='application/json')


@login_required
def feed_edit(request, pk):
    feed = get_object_or_404(Feed, pk=pk)
    print (feed)
    csrf_token = csrf(request)['csrf_token']
    post = request.POST['post']
    post = post.strip()
    if len(post) > 0:
        feed.post = post[:255]
        feed.save()
    return HttpResponseRedirect('/')