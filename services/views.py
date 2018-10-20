from accounts import mixins


class IndexView(mixins.NavbarMixin):
    template_name = 'services/index.html'
    tab_name = 'init'


class ServicesView(mixins.NavbarMixin):
    template_name = 'services/services.html'
    tab_name = 'services'


class ServiceToolsView(mixins.LoginRequiredMixin, mixins.NavbarMixin):
    tab_name = 'tools'
    template_name = 'services/tools.html'
