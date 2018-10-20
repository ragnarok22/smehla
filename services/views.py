from accounts import mixins


class IndexView(mixins.NavbarMixin):
    template_name = 'services/index.html'
    tab_name = 'init'


class ServicesView(mixins.NavbarMixin):
    template_name = 'services/services.html'
    tab_name = 'services'
