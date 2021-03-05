from django import template

register = template.Library()


@register.simple_tag
def is_user_can_take_part(competition, user):
    user_did_not_post = not bool(competition.feed_set.filter(user=user).count())
    if user_did_not_post and competition.upload_is_active():
        return {'can_post': True}

    result = {
        'can_post': False,
        'message': 'Upload date expired',
    }

    if not user_did_not_post:
        result['message'] = 'Only one'

    return result

@register.simple_tag
def is_user_can_like(feed, user):
    competition = feed.competition
    if not competition:
        return {'can_like': True}
    if competition.is_active():
        return {'can_like': True}

    result = {
        'can_like': False,
        'message': 'Competition finished',
    }

    return result
