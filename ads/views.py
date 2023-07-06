from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from B_Board import settings
from ads.forms import AdsForm, ResForm
from ads.models import Ad, Response
from ads.tasks import send_message_res


class AdsList(ListView):
    model = Ad
    ordering = '-date_create'
    template_name = 'ads/ads.html'
    context_object_name = 'ads'
    paginate_by = 10


class AdDetail(DetailView):
    model = Ad
    template_name = 'ads/ad.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ad = self.get_object().id
        responses = Response.objects.filter(ad=ad)
        context['response'] = responses
        context['MEDIA_URL'] = settings.MEDIA_URL
        return context


class AdCreate(LoginRequiredMixin, CreateView):
    form_class = AdsForm
    model = Ad
    template_name = 'ads/ads_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AdUpdate(LoginRequiredMixin, UpdateView):
    form_class = AdsForm
    model = Ad
    template_name = 'ads/ads_create.html'


class AdDelete(DeleteView):
    model = Ad
    template_name = 'ads/ad_delete.html'
    success_url = reverse_lazy('ads_list')


class ResponseCreate(LoginRequiredMixin, CreateView):
    form_class = ResForm
    nodel = Response
    template_name = 'ads/res_create.html'

    def form_valid(self, form):
        response = form.save(commit=False)
        if self.request.method == 'POST':
            pk = self.request.path.split('/')[-2]
            username = self.request.user
            response.ad = Ad.objects.get(id=pk)
            response.author = User.objects.get(username=username)
        response.save()
        send_message_res.apply_async([response.pk], countdown=5)
        return super().form_valid(form)

    def get_success_url(self):
        url = '/'.join(self.request.path.split('/')[0:-1])
        return url
