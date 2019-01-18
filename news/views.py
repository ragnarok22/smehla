from django.urls import reverse_lazy
from django.views import generic

from accounts import mixins as auth_mixin
from news import forms
from news.models import News, Service


class NewsCreateView(auth_mixin.SuperuserRequiredMixin, generic.CreateView):
    model = News
    form_class = forms.NewsCreateForm

    def get_success_url(self):
        return reverse_lazy('news:detail', kwargs={'pk': self.object.pk})


class NewsDetailView(generic.DetailView):
    model = News


class NewsUpdateView(auth_mixin.SuperuserRequiredMixin, generic.UpdateView):
    model = News
    form_class = forms.NewsCreateForm

    def get_success_url(self):
        return reverse_lazy('news:detail', kwargs={'pk': self.object.pk})


class NewsListView(auth_mixin.NavbarMixin, generic.ListView):
    model = News
    tab_name = 'news'


class NewsDeleteView(auth_mixin.SuperuserRequiredMixin, generic.DeleteView):
    model = News
    success_url = reverse_lazy('news:list')


class ServiceCreate(auth_mixin.AdminRequiredMixin, generic.CreateView):
    model = Service
    success_url = reverse_lazy('news:services')
    fields = '__all__'


class ServiceList(auth_mixin.NavbarMixin, generic.ListView):
    model = Service
    template_name = 'news/services.html'
    tab_name = 'services'


class ServiceUpdate(generic.UpdateView):
    model = Service
    fields = '__all__'
    success_url = reverse_lazy('news:services')


class ServiceDelete(generic.DeleteView):
    model = Service
    success_url = reverse_lazy('news:services')
