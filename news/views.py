from django.urls import reverse_lazy
from django.views import generic

from news import forms
from news.models import News


class NewsCreateView(generic.CreateView):
    model = News
    form_class = forms.NewsCreateForm

    def get_success_url(self):
        return reverse_lazy('news:detail', kwargs={'pk': self.object.pk})


class NewsDetailView(generic.DetailView):
    model = News


class NewsUpdateView(generic.UpdateView):
    model = News
    form_class = forms.NewsCreateForm

    def get_success_url(self):
        return reverse_lazy('news:detail', kwargs={'pk': self.object.pk})


class NewsListView(generic.ListView):
    model = News


class NewsDeleteView(generic.DeleteView):
    model = News
    success_url = reverse_lazy('news:list')
