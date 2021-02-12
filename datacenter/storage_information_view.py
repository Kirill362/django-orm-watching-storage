from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
import django


def get_duration(visitor):
    moscow_time = django.utils.timezone.localtime()
    entered_moscow_time = django.utils.timezone.localtime(visitor.entered_at)
    return moscow_time - entered_moscow_time


def format_duration(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return f'{hours}:{minutes}:{seconds}'


def storage_information_view(request):
    non_closed_visits = []
    visitors = Visit.objects.filter(leaved_at=None)
    for visitor in visitors:
        duration = get_duration(visitor)
        days, seconds = duration.days, duration.seconds
        hours = days * 24 + seconds // 3600
        if hours >= 2:
            is_strange = "Да"
        else:
            is_strange = "Нет"
        visitor_data = {"who_entered": visitor.passcard,
                        "entered_at": django.utils.timezone.localtime(visitor.entered_at),
                        "duration": format_duration(duration),
                        "is_strange": is_strange}
    non_closed_visits.append(visitor_data)

    context = {
        "non_closed_visits": non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
