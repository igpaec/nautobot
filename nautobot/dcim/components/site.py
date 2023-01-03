from django_unicorn.components import UnicornView

from nautobot.dcim.models import Site


class SiteView(UnicornView):
    site: Site = None

    def mount(self):
        self.site = Site.objects.all().first()

    def save(self, site_to_save: Site):
        breakpoint()
        site_to_save.save()
