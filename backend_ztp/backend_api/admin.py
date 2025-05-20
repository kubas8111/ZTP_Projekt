from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Count, Q

from .models import Item, Receipt

# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     list_display = (
#         "id",
#         "username",
#         "email",
#         "first_name",
#         "last_name",
#         "is_staff",
#         "is_owner",
#         "is_payer",
#         "owned_items_count",
#         "payer_receipts_count",
#     )
#     search_fields = ("username", "email", "first_name", "last_name")

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         return qs.annotate(
#             owned_items_count=Count("item", distinct=True),
#             payer_receipts_count=Count("receipt", filter=Q(receipt__payer__isnull=False), distinct=True),
#         )

#     def is_owner(self, obj):
#         return obj.item_set.exists()
#     is_owner.boolean = True
#     is_owner.short_description = "Is Owner"

#     def is_payer(self, obj):
#         return obj.receipt_set.exists()
#     is_payer.boolean = True
#     is_payer.short_description = "Is Payer"

#     def owned_items_count(self, obj):
#         return obj.owned_items_count
#     owned_items_count.short_description = "Owned Items"

#     def payer_receipts_count(self, obj):
#         return obj.payer_receipts_count
#     payer_receipts_count.short_description = "Receipts as Payer"

# @admin.register(Person)
# class PersonAdmin(admin.ModelAdmin):
#     list_display = ("id", "name", "payer", "owner")  # Pola widoczne w widoku listy
#     search_fields = ("name",)  # Możliwość wyszukiwania po imieniu
#     list_filter = ("payer", "owner")  # Filtry po polach `payer` i `owner`


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "category", "value", "quantity")  # Widok listy
    search_fields = ("description",)  # Wyszukiwanie po opisie
    list_filter = ("category",)  # Filtracja po kategorii
    filter_horizontal = ("owners",)  # Interfejs do zarządzania relacją ManyToMany


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "payer",
        "payment_date",
        "shop",
        "transaction_type",
    )  # Widok listy
    search_fields = (
        "shop",
        "payer__name",
    )  # Wyszukiwanie po sklepie i imieniu płatnika
    list_filter = (
        "transaction_type",
        "payment_date",
    )  # Filtry po typie transakcji i dacie
    filter_horizontal = ("items",)  # Interfejs do zarządzania relacją ManyToMany
