from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DeleteView, DetailView
from django_filters.views import FilterView

from ads.models import Response
from personal.filters import ResponseFilter
from personal.forms import ResponseForm
from personal.tasks import send_message_accept


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'personal/index.html'


class ResponseList(LoginRequiredMixin, FilterView):
    form_class = ResponseForm
    model = Response
    template_name = 'personal/response_list.html'
    context_object_name = 'responses'
    filterset_class = ResponseFilter

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['user'] = self.request.user
        return kwargs


class ResponseDelete(DeleteView):
    model = Response
    template_name = 'personal/response_delete.html'
    success_url = reverse_lazy('responses')


@login_required
def accept(request, pk):
    res = Response.objects.get(id=pk)
    res.accepted()

    send_message_accept.apply_async([res.pk], countdown=5)

    message = 'Вы приняли отзыв '
    return render(request, 'personal/accept.html', {'response': res, 'message': message})


class AccountDetailActivate(DetailView):
    model = User
    template_name = 'activate.html'

    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        activation_code = request.POST.get('activation_code')
        code = user.codes.latest('created_at').code_value
        if activation_code == code:
            user.is_active = True
            user.save()
            return redirect('account')
        else:
            return self.form_invalid(None)

