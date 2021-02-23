from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
import django


def passcard_info_view(request, passcode):
    this_passcard_visits = []
    passcard = Passcard.objects.get(passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)
    for visit in visits:
        duration = visit.get_duration()
        visit_card = {
                "entered_at": django.utils.timezone.localtime(visit.entered_at),
                "duration": visit.format_duration(duration),
                "is_strange": visit.check_strange()
            }
        this_passcard_visits.append(visit_card)
    context = {
        "passcard": passcard,
        "this_passcard_visits": this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
