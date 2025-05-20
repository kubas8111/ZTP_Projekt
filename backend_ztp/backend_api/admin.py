from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Count, Q

from .models import Item, Receipt

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "description", "category", "value", "quantity")  # Widok listy
    search_fields = ("description",)  # Wyszukiwanie po opisie
    list_filter = ("category",)  # Filtracja po kategorii
    # filter_horizontal = ("user",)  # Interfejs do zarządzania relacją ManyToMany


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        # "payer",
        "payment_date",
        "shop",
        "transaction_type",
    )  # Widok listy
    search_fields = (
        "shop",
        # "payer__name",
    )  # Wyszukiwanie po sklepie i imieniu płatnika
    list_filter = (
        "transaction_type",
        "payment_date",
    )  # Filtry po typie transakcji i dacie
    # filter_horizontal = ("items",)  # Interfejs do zarządzania relacją ManyToMany
