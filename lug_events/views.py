from django.views.generic import ListView
from .models import Event

class EventListView(ListView):
    queryset = Event.objects.all()
    context_object_name = 'events'
    template_name = 'lug_events/event-list.html'

