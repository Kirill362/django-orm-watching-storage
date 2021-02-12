from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
import django


def format_duration(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return f'{hours}:{minutes}:{seconds}'


def get_duration(visitor):
    entered_moscow_time = django.utils.timezone.localtime(visitor.entered_at)
    if django.utils.timezone.localtime(visitor.leaved_at) is None:
        moscow_time = django.utils.timezone.localtime()
        return moscow_time - entered_moscow_time
    else:
        leaved_moscow_time = django.utils.timezone.localtime(visitor.leaved_at)
        return leaved_moscow_time - entered_moscow_time


def passcard_info_view(request, passcode):
    this_passcard_visits = []
    passcard = Passcard.objects.get(passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)
    for visit in visits:
        duration = get_duration(visit)
        days, seconds = duration.days, duration.seconds
        hours = days * 24 + seconds // 3600
        if hours >= 2:
            is_strange = "Да"
        else:
            is_strange = "Нет"
        visit_card = {
                "entered_at": django.utils.timezone.localtime(visit.entered_at),
                "duration": format_duration(duration),
                "is_strange": is_strange
            }
        this_passcard_visits.append(visit_card)
    context = {
        "passcard": passcard,
        "this_passcard_visits": this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
