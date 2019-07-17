from rest_framework import mixins, viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .mixins import PrefetchQuerysetModelMixin


class PrefetchListAPIView(
    PrefetchQuerysetModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    Concrete view for listing a prefetched queryset.
    """

    pass


class PrefetchRetrieveAPIView(
    PrefetchQuerysetModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    Concrete view for retrieving a prefetched queryset.
    """

    pass
