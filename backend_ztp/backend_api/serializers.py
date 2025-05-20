from django.utils.timezone import now
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (
    Item,
    Receipt,
    RecentShop,
    ItemPrediction,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class PersonExpenseSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    expense_sum = serializers.FloatField()
    receipt_ids = serializers.ListField(child=serializers.IntegerField())
    top_outlier_receipts = serializers.ListField()

class ShopExpenseSerializer(serializers.Serializer):
    shop = serializers.CharField()
    expense_sum = serializers.FloatField()

class ItemSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    receipt = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Item
        fields = [
            "id",
            "save_date",
            "category",
            "value",
            "description",
            "quantity",
            "user",
            "receipt",
        ]
        read_only_fields = ["save_date", "user", "receipt"]



class ReceiptSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    items = ItemSerializer(many=True)

    class Meta:
        model = Receipt
        fields = [
            "id",
            "save_date",
            "payment_date",
            "user",
            "shop",
            "transaction_type",
            "items",
        ]
        read_only_fields = ["save_date", "user"]

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        user = self.context["request"].user
        receipt = Receipt.objects.create(user=user, **validated_data)

        shop_name = validated_data.get("shop", "").strip().lower()
        if shop_name:
            recent_shop, created = RecentShop.objects.get_or_create(
                user=user,
                name=shop_name
            )
            if not created:
                recent_shop.last_used = now()
                recent_shop.save()

        for item_data in items_data:
            item = Item.objects.create(
                user=user,
                receipt=receipt,
                **item_data
            )
            self.update_item_prediction(item, shop_name)

        return receipt

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", [])
        
        # Aktualizuj pola receipt
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Aktualizacja RecentShop na podstawie aktualnego shop
        shop_name = (instance.shop or "").strip().lower()
        user = self.context["request"].user
        if shop_name:
            recent_shop, created = RecentShop.objects.get_or_create(
                user=user,
                name=shop_name
            )
            if not created:
                recent_shop.last_used = now()
                recent_shop.save()

        # Usuń stare itemy i dodaj nowe
        instance.item_set.all().delete()

        for item_data in items_data:
            item = Item.objects.create(
                user=user,
                receipt=instance,
                **item_data
            )
            self.update_item_prediction(item, shop_name)

        return instance

    def update_item_prediction(self, item, shop_name):
        desc = (item.description or "").strip().lower()
        if not desc:
            return

        from .models import ItemPrediction

        prediction, created = ItemPrediction.objects.get_or_create(
            user=item.user,
            item_description=desc
        )
        prediction.frequency += 1
        prediction.save()



class ItemPredictionSerializer(serializers.ModelSerializer):
    item_description = serializers.CharField(source="item.description", read_only=True)
    shop_name = serializers.CharField(source="shop.name", read_only=True)

    class Meta:
        model = ItemPrediction
        fields = [
            "id",
            "item",
            "item_description",
            "shop",
            "shop_name",
            "frequency",
        ]


class UserExpenseSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    expense_sum = serializers.FloatField()

    class Meta:
        fields = ["user", "expense_sum"]


class ShopExpenseSerializer(serializers.Serializer):
    shop = serializers.CharField()
    expense_sum = serializers.FloatField()

    class Meta:
        fields = ["shop", "expense_sum"]


class CategoryPieExpenseSerializer(serializers.Serializer):
    category = serializers.CharField(source="transactions__category")
    expense_sum = serializers.FloatField()
    fill = serializers.CharField()

    class Meta:
        fields = ["category", "expense_sum", "fill"]
