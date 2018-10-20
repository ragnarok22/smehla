from django.views import generic

from accounts import mixins


class IndexView(mixins.NavbarMixin):
    template_name = 'services/index.html'
    tab_name = 'init'


class ServicesView(generic.TemplateView):
    template_name = 'services/services.html'
