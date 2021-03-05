from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from competitions.models import Category, Competition
from django.core.urlresolvers import reverse
from core.decorators import ajax_required
from django.core.context_processors import csrf
from activities.models import Activity
from django.core.exceptions import MultipleObjectsReturned
from feeds.models import Feed
import operator
import json


@login_required
def categories(request):
    template_context = {
        'categories': Category.objects.all()
    }
    return render(request, 'competitions/categories.html', template_context)


@login_required
def competition(request, pk):
    comp = Competition.objects.get(pk=pk)
    template_context = {
        'competition': comp,
        'csrf_token': csrf(request)['csrf_token'],
    }
    return render(request, 'competitions/competition.html', template_context)

@login_required
def add_entry(request, competition_id):
    Feed.objects.create(
            user=request.user,
            post=request.POST.get('post', '').strip(),
            image_url=request.POST.get('image', ''),
            video_url=request.POST.get('video_url', ''),
            competition_id=competition_id,
    )
    return redirect(reverse('competitions:competition', kwargs={'pk': competition_id}))


@login_required
def results_page(request):
    template_context = {
        'competitions': Competition.objects.all(),
    }
    return render(request, 'competitions/results_page.html', template_context)
