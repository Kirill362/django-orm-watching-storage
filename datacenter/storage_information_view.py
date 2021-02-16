from datacenter.models import Visit
from django.shortcuts import render
import django


def storage_information_view(request):
    non_closed_visits = []
    visitors = Visit.objects.filter(leaved_at=None)
    for visitor in visitors:
        duration = visitor.get_duration()
        visitor_data = {"who_entered": visitor.passcard,
                        "entered_at": django.utils.timezone.localtime(visitor.entered_at),
                        "duration": visitor.format_duration(duration),
                        "is_strange": visitor.check_strange(duration)}
    non_closed_visits.append(visitor_data)

    context = {
        "non_closed_visits": non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
