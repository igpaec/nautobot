from django_unicorn.components import UnicornView

from nautobot.dcim.models import Location


class LocationView(UnicornView):
    locations: Location = None

    def mount(self):
        self.locations = Location.objects.all()
