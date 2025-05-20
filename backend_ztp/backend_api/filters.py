from django_filters import rest_framework as filters
from .models import Item, Receipt


class ItemFilter(filters.FilterSet):
    user = filters.CharFilter(field_name="user", lookup_expr="exact")

    class Meta:
        model = Item
        fields = ["user"]


class ReceiptFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name="id", lookup_expr="exact")
    user = filters.BaseInFilter(field_name="user", lookup_expr="in")
    shop = filters.CharFilter(field_name="shop", lookup_expr="icontains")
    day = filters.NumberFilter(field_name="payment_date", lookup_expr="day")
    month = filters.NumberFilter(field_name="payment_date", lookup_expr="month")
    year = filters.NumberFilter(field_name="payment_date", lookup_expr="year")
    payment_date = filters.DateFromToRangeFilter(
        field_name="payment_date", lookup_expr="range"
    )
    transaction_type = filters.CharFilter(
        field_name="transaction_type", lookup_expr="exact"
    )
    category = filters.BaseInFilter(field_name="items__category", lookup_expr="in")

    class Meta:
        model = Receipt
        fields = [
            "user",
            "month",
            "year",
            "payment_date",
            "transaction_type",
            "category",
        ]
