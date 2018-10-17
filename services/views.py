from django.views import generic


class IndexView(generic.TemplateView):
    template_name = 'services/index.html'


class ServicesView(generic.TemplateView):
    template_name = 'services/services.html'
