from django_filters import FilterSet, ModelChoiceFilter, CharFilter

from ads.models import Response, Ad


class ResponseFilter(FilterSet):
    ad = ModelChoiceFilter(
        queryset=Ad.objects.none(),
        label='Объявление',
        method='filter_ad',
        empty_label='все'
    )

    class Meta:
        model = Response
        fields = ('ad', )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.queryset = Response.objects.filter(ad__author=user)
        self.filters['ad'].queryset = Ad.objects.filter(author=user)

    def filter_ad(self, queryset, name, value):
        return queryset.filter(ad=value)