from __future__ import unicode_literals

from django import template
from django.conf import settings
from django.utils import timezone

from ads.models import Ad, Impression


register = template.Library()


@register.inclusion_tag('ads/tags/render_ads_zone.html', takes_context=True)
def render_ads_zone(context, zone):
    """
    Returns an advertise for a ``zone``.
    Tag usage:
    {% load ads_tags %}
    {% render_zone 'zone' %}
    """

    # Retrieve random ad for the zone based on weight
    ad = Ad.objects.random_ad(zone)

    if ad is not None:
        request = context['request']
        if request.session.session_key:
            impression, created = Impression.objects.get_or_create(
                ad=ad,
                session_id=request.session.session_key,
                defaults={
                    'impression_date': timezone.now(),
                    'source_ip': request.META.get('REMOTE_ADDR', ''),
                })
    return {
        'ad': ad,
        'zone': settings.ADS_ZONES.get(zone, None)
    }
